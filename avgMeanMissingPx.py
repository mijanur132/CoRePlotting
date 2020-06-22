import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import matplotlib as mpl
import os

sns.set()
sns.set_context("talk")
# sns.set_style("white")
sns.set_style("ticks")
mpl.rc("figure", facecolor="white")

MAX_ROWS = 240
ENABLE_SAVE = True
vidName="combine"
file_path0 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/CoREData_processed2.txt'
file_path1 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/FoVData_processed.txt'
file_path2 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/FoVPData_processed.txt'
file_path3 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/2qlData_processed.txt'
file_path4 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/FoV360Data_processed.txt'
file_path5 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/FoVP360Data_processed.txt'
file_pathx = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/'+vidName+'/'+vidName+'.txt'

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

def prepare_data(file_path):
    print(file_path)
    df_temp = pd.read_csv(file_path,nrows=MAX_ROWS, sep=" |\t", engine='python')
    print(df_temp)
    dl=df_temp.iloc[:,0]
    sr=df_temp.iloc[:,1]
    fr=df_temp.iloc[:,2]
    dlO = np.asanyarray(dl)
    srO = np.asanyarray(sr)
    frO = np.asanyarray(fr)
    print(dl,sr,fr)
    return dlO,srO,frO



def prepare_data_missing_pixel(file_path):
    print(file_path)
    #df_temp = pd.read_csv(file_path, delimiter="\t")
    df_temp = pd.read_csv(file_path, nrows=MAX_ROWS, sep=" |\t", engine='python')
    #print(df_temp)
    m1p=df_temp.iloc[:,3]
    mmp=df_temp.iloc[:,4]
    print("m1p",m1p)
    print ("mmp",mmp)
    return m1p,mmp



def plot_b0x_missing_pixels(m1p, mmp):
    a=int(len(m1p)/2)
    dlx = np.reshape(m1p, (2, a))
    srx = np.reshape(mmp, (2, a))
    dl = pd.DataFrame(data=dlx.T, columns=['FoV Only', 'FoV+ 2QL'])
    ds = pd.DataFrame(data=srx.T, columns=['FoV Only', 'FoV+ 2QL'])
    bp=sns.boxplot(x="variable", y="value", data=pd.melt(dl), linewidth=1, palette="Set3")
    bp.set(xlabel="", ylabel="1MP (%)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_1MP.pdf')
    plt.savefig(plt_name, bbox_inches='tight')
    plt.show()

    bp2=sns.boxplot(x="variable", y="value", data=pd.melt(ds), linewidth=1)
    bp2.set(xlabel="", ylabel="MMP (%)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_MMP.pdf')
    plt.savefig(plt_name, bbox_inches='tight')
    plt.show()

def plot_data(plt_col, delayMat, srMat, frMat):

    df_temp = pd.read_csv(file_path,nrows=MAX_ROWS)

    print (file_path)
    print (df_temp.head(10))



    df_temp['Encoding_label'] =  df_temp['Encoding'].map(label_name_dict)
    df_temp['bandwidth'] =  df_temp['bandwidth'].map(bw_to_carrier_dict)
    # df_temp['Data(MB)'] = df_temp['Data(KB)']/1024

    print (df_temp)

    # flatui = ['darkred', 'blue',"dimgrey",'darkgreen']
    flatui = ["#e74c3c","#3498db", "#95a5a6","#2ecc71"]

    # flatui = ['darkred','dimgrey','darkgreen']
    flatui = ["#95a5a6","#e74c3c","#2ecc71"]
    # sns.palplot(sns.color_palette(flatui))
    # plt.show()

    sns.set_context(rc={'patch.linewidth': 1.0})

    #df_temp['vid_name'] = df_temp['vid_name'].apply(lambda x: x.replace('F',''))

    sns.set_style(rc={'patch.force_edgecolor': True,
                      'patch.edgecolor': 'black'})

    df_temp['PLT_X'] = df_temp['bandwidth']
    if plt_col == 'Stall':

        bar = sns.barplot(x=df_temp['PLT_X'], y=df_temp['Stall'],hue=df_temp['Encoding_label'],
                          palette=flatui)
    else:
        bar = sns.barplot(x=df_temp['PLT_X'], y=df_temp['Avg Frame Rate'],hue=df_temp['Encoding_label'],
                          palette=flatui)



    from itertools import cycle
    hatches = cycle(['////', '\\\\\\', '_','|','+'])

    num_locations = len(df_temp.PLT_X.unique())

    print (num_locations)


    # Loop over the bars
    for i, patch in enumerate(bar.patches):
        print (patch)
        # print (i,hatches[(i+1)%len(hatches)])
        # # Set a different hatch for each bar
        # patch.set_hatch(hatches[(i+1)%len(hatches)])
        print (i)
        if i % num_locations == 0:
            hatch = next(hatches)
        patch.set_hatch(hatch)


    # title = "Bandwidth: " + file_path.split('.')[0]
    # plt.title(title)
    plt.xlabel("")

    plt.legend(frameon=False, prop={'size':12})
    plt.setp(bar.lines, color=".1")

    if plt_col == 'Stall':
        plt.ylabel("Stall (s)")
        plt_name = file_path.replace('.csv', '_STALL.pdf')
    else:
        plt.ylabel("Avg Frame Rate")
        plt_name = file_path.replace('.csv', '_AFR.pdf')

    if ENABLE_SAVE == True:
        plt.savefig(plt_name,bbox_inches='tight')

    plt.show()

def plot_b0x(dl, sr, fr):
    a=MAX_ROWS-1
    dlx = np.reshape(dl, (6, a))
    srx = np.reshape(sr, (6, a))
    frx = np.reshape(fr, (6, a))
    dl = pd.DataFrame(data=dlx.T, columns=['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360','CoRE'])
    ds = pd.DataFrame(data=srx.T, columns=['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360','CoRE'])
    df = pd.DataFrame(data=frx.T, columns=['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360','CoRE'])
    bp=sns.boxplot(x="variable", y="value", data=pd.melt(dl), linewidth=1, palette="Set3")
    bp.set(xlabel="", ylabel="Stall (s)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_StallBox.pdf')
    plt.savefig(plt_name, bbox_inches='tight')
    plt.show()
    bp2=sns.boxplot(x="variable", y="value", data=pd.melt(ds), linewidth=1)
    bp2.set(xlabel="", ylabel="Sampling Rate (%)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_SRBox.pdf')
    plt.savefig(plt_name, bbox_inches='tight')
    plt.show()
    bp3=sns.boxplot(x="variable", y="value", data=pd.melt(df), linewidth=1)
    bp3.set(xlabel="", ylabel="Frame Rate (fps)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_FRBox.pdf')
    plt.savefig(plt_name, bbox_inches='tight')
    plt.show()



def main(argv):
    pd.options.display.max_colwidth = 300
    pd.options.display.float_format = '{:.2f}'.format
    # dl0,sr0,fr0=prepare_data(file_path0)
    # dl1,sr1,fr1= prepare_data(file_path1)
    # dl2,sr2,fr2=prepare_data(file_path2)
    # dl3, sr3, fr3=prepare_data(file_path3)
    # dl4, sr4, fr4=prepare_data(file_path4)
    # dl5,sr5,fr5=prepare_data(file_path5)
    # a=MAX_ROWS
    # print(sr0)
    # print(fr0)
    # print(dl0)
    # dl= np.concatenate ((dl1[0:a]/1000, dl2[0:a]/1000, dl3[0:a]/1000, dl4[0:a]/1000, dl5[0:a]/1000,dl0[0:a]/1000),axis=0)
    # sr =np.concatenate((sr1[0:a], sr2[0:a], sr3[0:a], sr4[0:a], sr5[0:a],sr0[0:a]), axis=0)
    # fr = np.concatenate((fr1[0:a], fr2[0:a], fr3[0:a], fr4[0:a], fr5[0:a],fr0[0:a]), axis=0)
    #
    # plot_b0x(dl,sr,fr)
    #
    # dl0,sr0=prepare_data_missing_pixel(file_path1)
    # dl1,sr1= prepare_data_missing_pixel(file_path2)
    # a=MAX_ROWS
    # print("sr0",sr0)
    # print("dl0",dl0)
    # dl= np.concatenate ((dl0[0:a], dl1[0:a]),axis=0)
    # sr =np.concatenate((sr0[0:a], sr1[0:a]),axis=0)
    # plot_b0x_missing_pixels(dl,sr)


    dl0,sr0=prepare_data_map_1ap()

    a=MAX_ROWS
    print("sr0",sr0)
    print("dl0",dl0)
    dl= np.concatenate ((dl0[0:a], dl1[0:a]),axis=0)
    sr =np.concatenate((sr0[0:a], sr1[0:a]),axis=0)
    plot_b0x_missing_pixels(dl,sr)
   # plot_data('Avg Frame Rate')
    #plot_data('Stall')


if __name__ == '__main__':
    main(sys.argv[1:])


