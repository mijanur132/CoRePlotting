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

MAX_ROWS = 100
ENABLE_SAVE = True


file_path1 = 'C:/Users/pmija/OneDrive - purdue.edu/lab129/EdgeVR/Code/Video/source/mobisys/allTrace/fov 360/tile_delay.txt'


label_name_dict = {
    'FoV+QL1':'FoV+ 1QL',
    'FoV+QL2':'FoV+ 2QL',
    'FoV360':'FoV 360',
    'FoVP360':'FoV+ 360',
    'FoV':'FoV Only',
    'FoVOnly':'FoV Only',
    'CoRE':'CoRE',
}

bw_to_carrier_dict = {
    'bw235':'T-Mobile \n UMTS',
    'bw1932':'T-Mobile',
    'bw646':'AT&T',
    'bw2100':'Verizon',
}

def prepare_data(data_path):
    df_temp = pd.read_csv(file_path,nrows=MAX_ROWS)
    print (file_path)
    print (df_temp.head(10))

def plot_data(plt_col):

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


def main(argv):

    pd.options.display.max_colwidth = 300
    pd.options.display.float_format = '{:.2f}'.format
    prepare_data(file_path1)
   # plot_data('Avg Frame Rate')
    #plot_data('Stall')


if __name__ == '__main__':
    main(sys.argv[1:])


