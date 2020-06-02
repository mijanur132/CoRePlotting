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
M_ROW=1000
MAX_ROWS = 500
ENABLE_SAVE = True
vidName=""
file_path0 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/size_processed_core.txt'
file_path1 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/size_processed_fovonly.txt'
file_path2 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/size_processed_fovp.txt'
file_path3 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/size_processed_2ql.txt'
file_path4 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/size_processed_fov360.txt'
file_path5 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/size_processed_fovp360.txt'
file_pathx = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/combine'+vidName+'/'+'size.txt'

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
    df_temp = pd.read_csv(file_path, delimiter="\t")
    size=df_temp.iloc[:,0]
    global M_ROW
    if len(size) < M_ROW:
        M_ROW = len(size)
    return size

def sumAnB(fileA,fileB, name,pathsave):
    df_tempA = pd.read_csv(fileA, delimiter="\t").to_numpy()
    df_tempB= pd.read_csv(fileB,  delimiter="\t").to_numpy()
    df_tempC = pd.read_csv(pathsave+"size_processed_fovonly.txt", delimiter="\t").to_numpy()
    print(len(df_tempA),len(df_tempB), len(df_tempB))
    temp3=np.zeros(len(df_tempA))
    for a in range(len(df_tempB)):
        print(a, df_tempB[a], df_tempA[a], df_tempC[a])
        aa=int(df_tempB[a])-int(df_tempA[a]) + int(df_tempC[a])
        temp3[a]=aa
        print(aa,temp3[a])
    np.savetxt(pathsave+"size_processed_2ql"+".txt",temp3, fmt="%i")


def plot_b0x_size(dl):
    dlx = np.reshape(dl, (6, M_ROW))
    dl = pd.DataFrame(data=dlx.T, columns=['FoV Only', 'FoV+ 1QL', 'FoV+ 2QL', 'FoV 360', 'FoV+ 360','CoRE'])
    bp=sns.boxplot(x="variable", y="value", data=pd.melt(dl), linewidth=1, palette="Set3")
    bp.set(xlabel="", ylabel="Size (MB)")
    plt.xticks(rotation=45)
    plt_name = file_pathx.replace('.txt', '_SizeBox.pdf')
    plt.savefig(plt_name, bbox_inches='tight')
    plt.show()




def main(argv):
    file_path3x = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/' + vidName+"/"
    # sumAnB(file_path3x+"temp1_2ql.txt",file_path3x+"temp2_2ql.txt", "_2ql", file_path3x)
    # sumAnB(file_path3x + "temp1_fovp360.txt", file_path3x + "temp2_fovp360.txt", "_fovp360",file_path3x)
    # sumAnB(file_path3x + "size_processed_fov360.txt", file_path3x + "size_processed_fovp360.txt", "_fov360",file_path3x)

    pd.options.display.max_colwidth = 300
    pd.options.display.float_format = '{:.2f}'.format
    dl0=prepare_data_size(file_path0)
    dl1= prepare_data_size(file_path1)
    dl2=prepare_data_size(file_path2)
    dl3=prepare_data_size(file_path3)
    dl4=prepare_data_size(file_path4)
    dl5=prepare_data_size(file_path5)
    a=M_ROW
    print(dl0)
    dl= np.concatenate ((dl1[0:a]/1000, dl2[0:a]/1000, dl3[0:a]/1000, dl4[0:a]/1000, dl5[0:a]/1000,dl0[0:a]/1000),axis=0)

    plot_b0x_size(dl)





if __name__ == '__main__':
    main(sys.argv[1:])


