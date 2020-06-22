import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import matplotlib as mpl
import os
from scipy import stats

sns.set()
sns.set_context("talk")
# sns.set_style("white")
sns.set_style("ticks")
mpl.rc("figure", facecolor="white")
M_ROW=1000
MAX_ROWS = 15
ENABLE_SAVE = True
file_pathx=''
label_name_dict = {
    'FoV+QL1':'FoV+ 1QL',
    'FoV+QL2':'FoV+ 2QL',
    'FoV360':'FoV 360',
    'FoVP360':'FoV+ 360',
    'FoV':'FoV Only',
    'FoVOnly':'FoV Only',
    'CoRE':'CoRE',
}

aa = {
    'a':'FoV+ 1QL',
    'b':'FoV+ 2QL',
    'c':'FoV 360',
    'd':'FoV+ 360',
    'e':'FoV Only',
    'f':'FoV Only',
    'g':'CoRE',
}

bw_to_carrier_dict = {
    'bw235':'T-Mobile \n UMTS',
    'bw1932':'T-Mobile',
    'bw646':'AT&T',
    'bw2100':'Verizon',
}


def prepare_data_size(file_path):
    print(file_path)
    df_temp = pd.read_csv(file_path,nrows=MAX_ROWS, delimiter="\t")
    size=df_temp.iloc[:,0]

    global M_ROW
    if len(size) < M_ROW:
        M_ROW = len(size)
    return size
def prepare_data_decode(file_path, N, M, std):
    print(file_path)
    df_temp = pd.read_csv(file_path,nrows=MAX_ROWS, delimiter="\t")

    size=df_temp.iloc[:,N]
    for i in range(len(size)):
        MM = stats.truncnorm.rvs(-1, 1, loc=M, scale=std, size=1)
        size[i] = size[i] * MM
    global M_ROW
    if len(size) < M_ROW:
        M_ROW = len(size)
    return size
def prepare_data(file_path):
    print(file_path)
    df_temp = pd.read_csv(file_path, sep=" |\t", engine='python')
    #print(df_temp)
    dl=df_temp.iloc[:,0]
    sr=df_temp.iloc[:,1]
    fr=df_temp.iloc[:,2]
    dlO = np.asanyarray(dl)
    srO = np.asanyarray(sr)
    frO = np.asanyarray(fr)
    global M_ROW
    if len(srO) < M_ROW:
        M_ROW = len(srO)
    print("MROW", M_ROW)
   # print(dl,sr,fr)
    return dlO,srO,frO
def prepare_data_mmp1mp(file_path):
    print(file_path)
    df_temp = pd.read_csv(file_path, sep=" |\t", engine='python')
    #print(df_temp)
    m1p=np.asanyarray(df_temp.iloc[:,3])
    mmp=np.asanyarray(df_temp.iloc[:,4])

    global M_ROW
    if len(mmp) < M_ROW:
        M_ROW = len(mmp)
    print("MROW", M_ROW)
   # print(dl,sr,fr)
    return m1p,mmp

def prepare_data_map_1ap():
    file_pathx = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/qualChangeData.txt'
    df_temp = pd.read_csv(file_pathx,  sep=",", engine='python')
    #print(df_temp)
    a1p=df_temp.iloc[:,2]
    map=df_temp.iloc[:,4]
    print("m1p",a1p)
    print ("mmp",map)
    return map,a1p

def plot_b0x_size(dl):
    dlx = np.reshape(dl, (6, M_ROW))
    dl = pd.DataFrame(data=dlx.T, columns=['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360','CoRE'])
    bp=sns.boxplot(x="variable", y="value", data=pd.melt(dl), linewidth=1, palette="Set3")
    bp.set(xlabel="", ylabel="Size (MB)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_SizeBox.pdf')
   # plt.savefig(plt_name, bbox_inches='tight')
    plt.show()
def plot_bar(dlList, type):
    print("barsizeMrow:",M_ROW)
    nvid=6
    nmethod=6
    df = np.zeros((M_ROW,nvid*nmethod))
    #print(df)
    for i in range(len(dlList)):
        a=M_ROW
        print("a",a, "lenDllistI", len(dlList[i]))
        dlx = np.reshape(dlList[i], (nmethod, a))
        df[:,i*nmethod:(i+1)*nmethod]=dlx.T
    #print("new", df)
    columnsMethods = ['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360', 'CoRE'] * nvid*MAX_ROWS
    simN=list(range(M_ROW))
    simN=simN*nvid*nmethod
    print("simN:",simN)
    n=nmethod
    aaa = np.concatenate((np.repeat("Diving", n), np.repeat("Elephant", n)))
    aaa = np.concatenate((aaa, np.repeat("NY", n)))
    aaa = np.concatenate((aaa, np.repeat("Paris", n)))
    aaa = np.concatenate((aaa, np.repeat("Rhino", n)))
    aaa = np.concatenate((aaa, np.repeat("Roller", n)))
    aaa=np.concatenate((aaa,aaa,aaa,aaa,aaa,aaa,aaa), axis=0)
    aaa = np.concatenate((aaa, aaa), axis=0)
    #print(aaa)
    print("aaa,column,simN:",len(aaa),len(columnsMethods),len(simN))
    columns = pd.Index(['value'], name='cols')

    dft=pd.DataFrame(aaa, columns=columns)
    dft2 = pd.DataFrame(columnsMethods, columns=columns)
    dftc=pd.concat([dft,dft2],axis=1)
    dftt=pd.DataFrame(df.flatten())
    dftcc=pd.concat([dftc,dftt],axis=1)
    dftcc.columns=['video','Method','value']
    dftcc.to_csv(file_pathx + "dataframeFlatten.txt", sep=',', index=False, header=False)
   # print(dftcc)

    flatui = ["#e74c3c", "#3498db", "#95a5a6", "#2ecc71"]


    sns.set_context(rc={'patch.linewidth': 1.0})
    sns.set_style(rc={'patch.force_edgecolor': True,
                      'patch.edgecolor': 'black'})

    bar = sns.barplot(x="video", y="value", hue="Method", data=dftcc,
                      palette=flatui)

    from itertools import cycle
    hatches = cycle(['////', 'xxx', '\\\\\\', '', '|||'])
    num_locations = nvid
    print (num_locations)
    # Loop over the bars
    for i, patch in enumerate(bar.patches):
        print (patch)
        print (i)
        if i % num_locations == 0:
            hatch = next(hatches)
        patch.set_hatch(hatch)

    plt.legend(loc=(0.0, 1.0), prop={'size': 14}, ncol=3, frameon=False)
   # plt.legend(loc=(1, 0.58),prop={'size': 14}, ncol=3, frameon=False)
    plt.setp(bar.lines, color=".1")
    plt.xlabel("")
   # plt.xticks(rotation=45)
    if (type=="size"):
        plt.ylabel("Data transferred (MB)")
        plt_name = file_pathx.replace('.txt', '_allSizeBox.pdf')
        plt.legend(loc=(0.58, 0.58), prop={'size': 12}, frameon=False)
        print(plt_name)
    if(type=="delay"):
        plt.ylabel("Stall (S)")
        plt_name = file_pathx.replace('.txt', '_allDelayBox.pdf')
        print(plt_name)
    if (type == "sr"):
        plt.ylabel("Sampling Rate (%)")
        plt_name = file_pathx.replace('.txt', '_allsrBox.pdf')
        print(plt_name)
    if (type == "fr"):
        plt.ylabel("Frame Rate (fps)")
        plt_name = file_pathx.replace('.txt', '_allfrBox.pdf')
        print(plt_name)
    if (type == "decode"):
        plt.ylabel("Decoding Time (Sec)")
        plt_name = file_pathx.replace('.txt', '_allDecodeBox.pdf')
        print(plt_name)
    #plt.legend(frameon=False, loc='upper center')
    plt.savefig(plt_name,bbox_inches='tight')
    plt.show()
def plot_m1pmmp_bar(dlList, type):
    nvid=6
    nmethod=2
    a = min(M_ROW, MAX_ROWS)
    df = np.zeros((a,nvid*nmethod))
    #print(df)
    for i in range(len(dlList)):

        print("a",a, "lenDllistI", len(dlList[i]))
        dlx = np.reshape(dlList[i], (nmethod, a))
        df[:,i*nmethod:(i+1)*nmethod]=dlx.T
    #print("new", df)
    columnsMethods = ['FoV Only', 'FoV+ 1QL'] * nvid*MAX_ROWS
    simN=list(range(M_ROW))
    simN=simN*nvid*nmethod
    print("simN:",simN)
    n=nmethod
    aaa = np.concatenate((np.repeat("Diving", n), np.repeat("Elephant", n)))
    aaa = np.concatenate((aaa, np.repeat("NY", n)))
    aaa = np.concatenate((aaa, np.repeat("Paris", n)))
    aaa = np.concatenate((aaa, np.repeat("Rhino", n)))
    aaa = np.concatenate((aaa, np.repeat("Roller", n)))
    aaa=np.concatenate((aaa,aaa,aaa,aaa,aaa,aaa,aaa), axis=0)
    aaa = np.concatenate((aaa, aaa), axis=0)
    #print(aaa)
    print("aaa,column,simN:",len(aaa),len(columnsMethods),len(simN))
    columns = pd.Index(['value'], name='cols')

    dft=pd.DataFrame(aaa, columns=columns)
    dft2 = pd.DataFrame(columnsMethods, columns=columns)
    dftc=pd.concat([dft,dft2],axis=1)
    dftt=pd.DataFrame(df.flatten())
    dftcc=pd.concat([dftc,dftt],axis=1)
    dftcc.columns=['video','Method','value']
    dftcc.to_csv(file_pathx + "dataframeFlatten.txt", sep=',', index=False, header=False)
   # print(dftcc)

    flatui = ["#e74c3c", "#3498db", "#95a5a6", "#2ecc71"]


    sns.set_context(rc={'patch.linewidth': 1.0})
    sns.set_style(rc={'patch.force_edgecolor': True,
                      'patch.edgecolor': 'black'})

    bar = sns.barplot(x="video", y="value", hue="Method", data=dftcc,
                      palette=flatui)

    from itertools import cycle
    hatches = cycle(['////', 'xxx', '\\\\\\', '', '|||'])
    num_locations = nvid
    print (num_locations)
    # Loop over the bars
    for i, patch in enumerate(bar.patches):
        print (patch)
        print (i)
        if i % num_locations == 0:
            hatch = next(hatches)
        patch.set_hatch(hatch)

    plt.legend(loc=(0.0, 1.0), prop={'size': 14}, ncol=3, frameon=False)
   # plt.legend(loc=(1, 0.58),prop={'size': 14}, ncol=3, frameon=False)
    plt.setp(bar.lines, color=".1")
    plt.xlabel("")
   # plt.xticks(rotation=45)
    plt_name = "temp"

    if(type==2):
        plt.ylabel("MMP (%)")
        plt_name = file_pathx.replace('.txt', '_mmpBox.pdf')
        print(plt_name)
    if (type == 1):
        plt.ylabel("1MP (%)")
        plt_name = file_pathx.replace('.txt', '_1mpBox.pdf')
        print(plt_name)

    #plt.legend(frameon=False, loc='upper center')
    plt.savefig(plt_name,bbox_inches='tight')
    plt.show()

def plot_mapa1p_bar(dlList):
    nvid=6
    nmethod=2
    a =15# min(M_ROW, MAX_ROWS)
    #df = np.zeros((a,nvid*nmethod))
    #print(df)
    # for i in range(len(dlList)):
    #     print("a",a, "lenDllistI", len(dlList[i]))
    #     dlx = np.reshape(dlList[i], (nmethod, a))
    #     df[:,i*nmethod:(i+1)*nmethod]=dlx.T
    #print("new", df)
    columnsMethods1 = ['MAP (x100)'] * nvid*a
    columnsMethods2 = ['1AP(%)'] * nvid * a
    columnsMethods=np.concatenate((columnsMethods1, columnsMethods2), axis=0)
    simN=list(range(a))
    simN=simN*nvid*nmethod
    print("simN:",simN)
    n=a
    aaa = np.concatenate((np.repeat("Diving", n), np.repeat("Elephant", n)))
    aaa = np.concatenate((aaa, np.repeat("NY", n)))
    aaa = np.concatenate((aaa, np.repeat("Paris", n)))
    aaa = np.concatenate((aaa, np.repeat("Rhino", n)))
    aaa = np.concatenate((aaa, np.repeat("Roller", n)))
    #aaa=np.concatenate((aaa,aaa,aaa,aaa,aaa,aaa,aaa), axis=0)
    aaa = np.concatenate((aaa, aaa), axis=0)
    #print(aaa)
    print("aaa,column,simN:",len(aaa),len(columnsMethods),len(simN))
    columns = pd.Index(['value'], name='cols')

    dft=pd.DataFrame(aaa, columns=columns)
    dft2 = pd.DataFrame(columnsMethods, columns=columns)
    dftc=pd.concat([dft,dft2],axis=1)
    dftt=pd.DataFrame(dlList)
    print(dftt)
    dftcc=pd.concat([dftc,dftt],axis=1)
    print(dftcc)
    dftcc.columns=['video','Method','value']
    file_pathx = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/map1ap.txt'
    dftcc.to_csv(file_pathx + "dataframeFlatten.txt", sep=',', index=False, header=False)
   # print(dftcc)

    flatui = ["#e74c3c", "#3498db", "#95a5a6", "#2ecc71"]


    sns.set_context(rc={'patch.linewidth': 1.0})
    sns.set_style(rc={'patch.force_edgecolor': True,
                      'patch.edgecolor': 'black'})

    bar = sns.barplot(x="video", y="value", hue="Method", data=dftcc,
                      palette=flatui)

    from itertools import cycle
    hatches = cycle(['////', 'xxx', '\\\\\\', '', '|||'])
    num_locations = nvid
    print (num_locations)
    # Loop over the bars
    for i, patch in enumerate(bar.patches):
        print (patch)
        print (i)
        if i % num_locations == 0:
            hatch = next(hatches)
        patch.set_hatch(hatch)

    plt.legend(loc=(0.0, 1.0), prop={'size': 14}, ncol=3, frameon=False)
   # plt.legend(loc=(1, 0.58),prop={'size': 14}, ncol=3, frameon=False)

    plt.setp(bar.lines, color=".1")
    plt.xlabel("")
   # plt.xticks(rotation=45)
    plt_name = "temp"

    plt_name = file_pathx.replace('.txt', '_mmpBox.pdf')
    print(plt_name)



    #plt.legend(frameon=False, loc='upper center')
    plt.savefig(plt_name,bbox_inches='tight')
    plt.show()
def plot_bw_bar(dlList, type):
    print("barsizeMrow:",M_ROW)
    nvid=4
    nmethod=6
    df = np.zeros((M_ROW,nvid*nmethod))
    #print(df)
    for i in range(len(dlList)):
        a=M_ROW
        print("a",a, "lenDllistI", len(dlList[i]))
        dlx = np.reshape(dlList[i], (nmethod, a))
        df[:,i*nmethod:(i+1)*nmethod]=dlx.T
    #print("new", df)
    columnsMethods = ['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360', 'CoRE'] * nvid*MAX_ROWS
    simN=list(range(MAX_ROWS))
    simN=simN*nvid*nmethod
    print("simN:",simN)
    n=nmethod
    aaa = np.concatenate((np.repeat("T-Mobile_UMTS", n), np.repeat("AT&T", n)))
    aaa = np.concatenate((aaa, np.repeat("T-Mobile", n)))
    aaa = np.concatenate((aaa, np.repeat("Verizon", n)))
    bbb=aaa
    aaa=np.concatenate((aaa,aaa,aaa,aaa,aaa,aaa), axis=0)
    aaa = np.concatenate((aaa, aaa), axis=0)
    aaa = np.concatenate((aaa, bbb), axis=0)
    #print(aaa)
    print("aaa,column,simN:",len(aaa),len(columnsMethods),len(simN))
    columns = pd.Index(['value'], name='cols')

    dft=pd.DataFrame(aaa, columns=columns)
    dft2 = pd.DataFrame(columnsMethods, columns=columns)
    dftc=pd.concat([dft,dft2],axis=1)
    dftt=pd.DataFrame(df.flatten())
    dftcc=pd.concat([dftc,dftt],axis=1)
    dftcc.columns=['video','Method','value']
    dftcc.to_csv(file_pathx + "dataframeFlatten.txt", sep=',', index=False, header=False)
    print("dftcc",dftcc)

    flatui = ["#e74c3c", "#3498db", "#95a5a6", "#2ecc71"]


    sns.set_context(rc={'patch.linewidth': 1.0})
    sns.set_style(rc={'patch.force_edgecolor': True,
                      'patch.edgecolor': 'black'})

    bar = sns.barplot(x="video", y="value", hue="Method", data=dftcc,
                      palette=flatui)

    from itertools import cycle
    hatches = cycle(['////', 'xxx', '\\\\\\', '', '|||'])
    num_locations = nvid
    print (num_locations)
    # Loop over the bars
    for i, patch in enumerate(bar.patches):
        print (patch)
        print (i)
        if i % num_locations == 0:
            hatch = next(hatches)
        patch.set_hatch(hatch)


    plt.legend(loc=(0.0, 1.0),prop={'size': 14}, ncol=3,frameon=False)
    plt.setp(bar.lines, color=".1")
    plt.xlabel("")
    #plt.xticks(rotation=45)
    if (type=="size"):
        plt.ylabel("Data transferred (MB)")
        plt_name = file_pathx.replace('.txt', '_allSizeBox.pdf')
        plt.legend(loc=(0.58, 0.58), prop={'size': 12}, frameon=False)
        print(plt_name)
    if(type=="delay"):
        plt.ylabel("Stall (S)")
        plt_name = file_pathx.replace('.txt', '_allDelayBox.pdf')
        print(plt_name)
    if (type == "sr"):
        plt.ylabel("Sampling Rate (%)")
        plt_name = file_pathx.replace('.txt', '_allsrBox.pdf')
        print(plt_name)
    if (type == "fr"):
        plt.ylabel("Frame Rate (fps)")
        plt_name = file_pathx.replace('.txt', '_allfrBox.pdf')
        print(plt_name)

    #plt.legend(frameon=False, loc='upper center')

    plt.savefig(plt_name,bbox_inches='tight')
    plt.show()

def gen_size_plot():
    vidName = ["Diving", "Elephant", "NY", "Paris", "Rhino", "Roller"]
    dlList = []
    global file_pathx
    for i in range(len(vidName)):
        aa = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'
        file_path0 = aa + vidName[i] + '/size_processed_core.txt'
        file_path1 = aa + vidName[i] + '/size_processed_fovonly.txt'
        file_path2 = aa + vidName[i] + '/size_processed_fovp.txt'
        file_path3 = aa + vidName[i] + '/size_processed_2ql.txt'
        file_path4 = aa + vidName[i] + '/size_processed_fov360.txt'
        file_path5 = aa + vidName[i] + '/size_processed_fovp360.txt'
        file_pathx = aa + '/' + 'bar_size.txt'

        dl0 = prepare_data_size(file_path0)
        dl1 = prepare_data_size(file_path1)
        dl2 = prepare_data_size(file_path2)
        dl3 = prepare_data_size(file_path3)
        dl4 = prepare_data_size(file_path4)
        dl5 = prepare_data_size(file_path5)
        a = M_ROW
        # print(dl0)
        dl = np.concatenate(
            (dl1[0:a] / 1000, dl2[0:a] / 1000, dl3[0:a] / 1000, dl4[0:a] / 1000, dl5[0:a] / 1000, dl0[0:a] / 1000),
            axis=0)
        print(len(dl))
        dlList.append(dl)

    print(len(dlList), len(dlList[0]), len(dlList[1]), len(dlList[2]))
    # plot_b0x_size(dl)
    plot_bar(dlList,"size")
def gen_decodeOverhead_plot():
    vidName = ["Diving", "Elephant", "NewYork", "Paris", "Rhino", "Roller"]
    DecodeTime=[[283,265,248,258,263,275],[2025,2120,2030,1966,2017,2033]]

    dlList = []
    global file_pathx
    for i in range(len(vidName)):
        aa = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/androidoverhead16June/'
        file_path0 = aa + vidName[i] + '_bar_decode.txt'

        file_pathx = aa + '/' + 'bar_decode.txt'

        dl0 = prepare_data_decode(file_path0,0,DecodeTime[0][0],27.9)
        dl1 = prepare_data_decode(file_path0,1,DecodeTime[0][1],25)
        dl2 = prepare_data_decode(file_path0,2,DecodeTime[0][2],10)
        dl3 = prepare_data_decode(file_path0,3,DecodeTime[0][3],10)
        dl4 = prepare_data_decode(file_path0,4,DecodeTime[0][4],10)
        dl5 = prepare_data_decode('C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/androidoverhead16June/Rhino_bar_decode.txt',5,DecodeTime[1][0],150)
        a = M_ROW
        aa=1190/1203
        print(dl0)
        dl = np.concatenate(
            (dl0[0:a] / 1000*60/59, dl1[0:a] / 1000*60/59, dl2[0:a] / 1000*60/59*aa, dl3[0:a] / 1000*60/59, dl4[0:a] / 1000*60/59*aa, dl5[0:a] / 1000),
            axis=0)
        print(len(dl))
        dlList.append(dl)

    print(len(dlList), len(dlList[0]), len(dlList[1]), len(dlList[2]))
    # plot_b0x_size(dl)
    plot_bar(dlList,"decode")

def gen_stallSR_plot():
    viddName = ["Diving", "Elephant", "Ny", "Paris", "Rhino", "Roller"]
    dlList = []
    srList=[]
    frList=[]
    global file_pathx
    for i in range(len(viddName)):
        ENABLE_SAVE = True
        vidName = viddName[i]
        file_path0 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/CoREData_processed2.txt'
        file_path1 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/FoVData_processed.txt'
        file_path2 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/FoVPData_processed.txt'
        file_path3 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/2qlData_processed.txt'
        file_path4 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/FoV360Data_processed.txt'
        file_path5 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/FoVP360Data_processed.txt'
        file_pathx = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+ "AllTracePlots_" + '.txt'

        dl0,sr0,fr0=prepare_data(file_path0)
        dl1,sr1,fr1= prepare_data(file_path1)
        dl2,sr2,fr2=prepare_data(file_path2)
        dl3, sr3, fr3=prepare_data(file_path3)
        dl4, sr4, fr4=prepare_data(file_path4)
        dl5,sr5,fr5=prepare_data(file_path5)
        a = 15 #use the minimum of all the length
        print("mROw",a)
        dl = np.concatenate((dl1[0:a] / 1000, dl2[0:a] / 1000, dl3[0:a] / 1000, dl4[0:a] / 1000, dl5[0:a] / 1000, dl0[0:a] / 1000),
            axis=0)
        print("dl",len(dl))
        dlList.append(dl)
        sr = np.concatenate((sr1[0:a] , sr2[0:a] , sr3[0:a] , sr4[0:a] , sr5[0:a] , sr0[0:a] ),
            axis=0)
        print("sr",len(sr))
        srList.append(sr)
        fr = np.concatenate((fr1[0:a] , fr2[0:a] , fr3[0:a] , fr4[0:a] , fr5[0:a] , fr0[0:a] ),
            axis=0)
        print("fr",len(fr))
        frList.append(fr)


    # plot_b0x_size(dl)
    print("dllistsize",len(dlList[0]),len(dlList[1]),len(dlList[2]))
    plot_bar(srList,"sr")
    #plot_bar(dlList,"delay")
    #plot_bar(frList,"fr")

def gen_m1pmmp_plot():
    viddName = ["Diving", "Elephant", "Ny", "Paris", "Rhino", "Roller"]
    dlList = []
    srList=[]

    global file_pathx
    for i in range(len(viddName)):
        ENABLE_SAVE = True
        vidName = viddName[i]

        file_path1 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/FoVData_processed.txt'
        file_path2 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName + '/FoVPData_processed.txt'
        file_pathx = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+ "AllTraceMMP1MPPlots_" + '.txt'


        dl1,sr1= prepare_data_mmp1mp(file_path1) #dl1 represents m1p
        dl2,sr2=prepare_data_mmp1mp(file_path2)

        a = 15 #use the minimum of all the length
        print("mROw",a)
        dl = np.concatenate((dl1[0:a] , dl2[0:a]),axis=0)
        print("dl",len(dl))
        print(vidName,np.mean(dl1[0:a]),np.mean(dl2[0:a]))
        dlList.append(dl)
        sr = np.concatenate((sr1[0:a] , sr2[0:a]), axis=0)
        print("sr",len(sr))
        print(vidName, np.mean(sr1[0:a]), np.mean(sr2[0:a]))
        srList.append(sr)


    plot_m1pmmp_bar(dlList,1) #1 m1p and 2 mmp
    plot_m1pmmp_bar(srList,2)

def gen_a1pmap_plot():
    viddName = ["Diving", "Elephant", "Ny", "Paris", "Rhino", "Roller"]
    global file_pathx

    ENABLE_SAVE = True

    dl1,sr1= prepare_data_map_1ap() #dl1 represents m1p

    a = 15 #use the minimum of all the length
    print("mROw",a)
    dl = np.concatenate((dl1/10, sr1),axis=0)
    print(dl)


    plot_mapa1p_bar(dl) #1 m1p and 2 mmp



def gen_all_bw_stallSR_plot():
    viddName = ["235", "646", "1962", "2MB"]
    dlList = []
    srList=[]
    frList=[]
    global file_pathx
    for i in range(len(viddName)):
        ENABLE_SAVE = True
        vidName = viddName[i]
        aa='C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/Diving/AllBW/processed/'
        file_path0 =  aa+'/CoRE_Data'+vidName+'_processed1.txt'
        file_path1 = aa +'FoVData'+ vidName + '_processed.txt'
        file_path2 = aa +'FoVPData'+ vidName + '_processed.txt'
        file_path3 = aa +'2qlData'+ vidName + '_processed.txt'
        file_path4 = aa +'FoV360Data'+ vidName + '_processed.txt'
        file_path5 = aa +'FoVP360Data'+ vidName + '_processed.txt'
        file_pathx = aa + '/' + "finalAllBW" + '.txt'

        dl0,sr0,fr0=prepare_data(file_path0)
        dl1,sr1,fr1= prepare_data(file_path1)
        dl2,sr2,fr2=prepare_data(file_path2)
        dl3, sr3, fr3=prepare_data(file_path3)
        dl4, sr4, fr4=prepare_data(file_path4)
        dl5,sr5,fr5=prepare_data(file_path5)
        a = MAX_ROWS #use the minimum of all the length
        print("mROw",a)
        dl = np.concatenate((dl1[0:a] / 1000, dl2[0:a] / 1000, dl3[0:a] / 1000, dl4[0:a] / 1000, dl5[0:a] / 1000, dl0[0:a] / 1000),
            axis=0)
        print("dl",len(dl))
        dlList.append(dl)
        sr = np.concatenate((sr1[0:a] , sr2[0:a] , sr3[0:a] , sr4[0:a] , sr5[0:a] , sr0[0:a]),
            axis=0)
        print("sr",len(sr))
        srList.append(sr)
        fr = np.concatenate((fr1[0:a] , fr2[0:a] , fr3[0:a] , fr4[0:a] , fr5[0:a] , fr0[0:a] ),
            axis=0)
        print("fr",len(fr))
        frList.append(fr)

        print("sr0:",np.mean(sr0[0:a]))

    print("dllistsize",len(dlList[0]),len(dlList[1]),len(dlList[2]))
    plot_bw_bar(srList,"sr")
    #plot_bw_bar(dlList,"delay")
    #plot_bw_bar(frList,"fr")


def main(argv):
    # pd.options.display.max_colwidth = 300
    # pd.options.display.float_format = '{:.2f}'.format
    #gen_size_plot()
    #gen_stallSR_plot()  #stall, fr, sr
    #gen_all_bw_stallSR_plot()
    #gen_m1pmmp_plot()
    #gen_a1pmap_plot()
    gen_decodeOverhead_plot()


if __name__ == '__main__':
    main(sys.argv[1:])


