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




#file_path = './data/data_transferred.csv'
file_path = './New_Data/data/data_transferred4vid.csv'

COL_NAME_MS = 'data_arrvial_time_MS'
COL_NAME_S = 'data_arrvial_time_S'
MAX_ROWS = 10000
ENABLE_SAVE = True


label_name_dict = {
    'FoV+QL1':'FoV+ 1QL',
    'FoV+QL2':'FoV+ 2QL',
    'FoV360':'FoV 360',
    'FoVP360':'FoV+ 360',
    'FoV':'FoV Only',
    'CoRE':'CoRE'
}


def plot_data():

    df_temp = pd.read_csv(file_path,nrows=MAX_ROWS)

    print (file_path)
    print (df_temp.head(10))


    df_temp['Encoding_label'] =  df_temp['Encoding'].map(label_name_dict)
    df_temp['Data(MB)'] = df_temp['Data(KB)']/1024

    print (df_temp)

    # flatui = ['darkred', 'blue',"dimgrey",'darkgreen']
    flatui = ["#e74c3c","#3498db", "#95a5a6","#2ecc71"]
    # sns.palplot(sns.color_palette(flatui))
    # plt.show()

    sns.set_context(rc={'patch.linewidth': 1.0})
    sns.set_style(rc={'patch.force_edgecolor': True,
                      'patch.edgecolor': 'black'})

    bar = sns.barplot(x=df_temp['vid_name'], y=df_temp['Data(MB)'],hue=df_temp['Encoding_label'],
                      palette=flatui)




    from itertools import cycle

    hatches = cycle(['////', 'xxx', '\\\\\\', '','|||'])

    num_locations = len(df_temp.vid_name.unique())

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


    plt.legend(frameon=False)
    plt.setp(bar.lines, color=".1")

    # title = "Bandwidth: " + file_path.split('.')[0]
    # plt.title(title)
    plt.xlabel("")
    plt.ylabel("Data transferred (MB)")
    plt.legend(frameon=False, loc='upper center')
    plt_name = file_path.replace('.csv', '_PLT.pdf')

    if ENABLE_SAVE == True:
        plt.savefig(plt_name,bbox_inches='tight')

    plt.show()


def main(argv):

    pd.options.display.max_colwidth = 300
    pd.options.display.float_format = '{:.2f}'.format
    plot_data()


if __name__ == '__main__':
    main(sys.argv[1:])


