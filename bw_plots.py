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
sns.set_style("white")
mpl.rc("figure", facecolor="white")
PLT_AVG = True



folder_path = './bw_data/'

COL_NAME_MS = 'data_arrvial_time_MS'
COL_NAME_S = 'data_arrvial_time_S'
MAX_ROWS = 10000000000000
ENABLE_SAVE = True

TIME_S = 60

def plot_data():

    for subdir,dirs, files in os.walk(folder_path):
        for file in files:
            file_path =  subdir + os.sep + file

            if '.txt' not in file:
                continue

            if os.path.getsize(file_path) == 0:
                continue


            df_temp = pd.read_csv(file_path,header=None,nrows=MAX_ROWS)

            #print (file_path)
            # print (df_temp.head(10))

            df_temp.columns = [COL_NAME_MS]

            df_120 = df_temp[df_temp[COL_NAME_MS] < 60000]


            if 'Verizon' not in file:
                max_val_b = df_120[COL_NAME_MS].max() + 1
            else:
                #The trace for verizon is only for 100 seconds, there is a single entry for 101 second whitch should be ingnored
                max_val_b = df_120[COL_NAME_MS].max()

            max_val_b = max_val_b/1000

            print ("Length:",len(df_120.index))
            print ("Avg Value(1000):",(len(df_120.index) * 1.4)/max_val_b)
            print ("Avg Value(1024):",(len(df_120.index) * (1400/1024))/max_val_b)


            df_temp[COL_NAME_S] = df_temp[COL_NAME_MS]/1000

            df_temp[COL_NAME_S] = df_temp[COL_NAME_S].astype('int64')


            df = df_temp.groupby(COL_NAME_S).size().reset_index(name='TOTAL_DATA')


            df =  df[df[COL_NAME_S] < 60]

            df['TOTAL_DATA_1024'] =  df['TOTAL_DATA'] * (1400/1024)

            df['TOTAL_DATA_1000'] =  df['TOTAL_DATA'] * (1400/1000)

            # print (file,"Length:",len(df.index),"Mean: (1024)",df['TOTAL_DATA_1024'].sum()/120)
            # print (file,"Length:",len(df.index),"Mean: (1000)",df['TOTAL_DATA_1000'].sum()/120)

            if 'Verizon' not in file:
                max_val = df[COL_NAME_S].max() + 1
                max_val = TIME_S
            else:
                #The trace for verizon is only for 100 seconds, there is a single entry for 101 second whitch should be ingnored
                max_val = TIME_S

            print (file,"Sum:",df['TOTAL_DATA_1024'].sum(),"Max Val:",max_val,"Avg BW: (1024) - ",round(df['TOTAL_DATA_1024'].sum()/(TIME_S)))
            # print (file,"Sum:",df['TOTAL_DATA_1024'].sum(),"Max Val:",max_val-1,"Avg BW: (1024) - ",round(df['TOTAL_DATA_1024'].sum()/(max_val-1)))
            #print (file,"Avg BW: (1000)",df['TOTAL_DATA_1000'].sum()/120)


            csv_save_name = file_path.replace(".txt",'plot_data.csv')
            df.to_csv(csv_save_name,index=False)

            # print (df)

            ax = sns.lineplot(x=df[COL_NAME_S], y=df['TOTAL_DATA_1024'])
            # ax = sns.lineplot(x=df[COL_NAME_S], y=df['TOTAL_DATA_1000'])

            title = "Bandwidth: " + file.split('.')[0]
            #plt.title(title)
            if PLT_AVG == True:
                y_med = round(df['TOTAL_DATA_1024'].sum()/(TIME_S))
                print(y_med)
                x = plt.gca().axes.get_xlim()
                plt.plot(x, len(x) * [y_med], sns.xkcd_rgb['pale red'],linestyle='--',label='Avg. bandwidth')
                plt.legend()
            # plt.axvline(x=0,y=np.median(df['TOTAL_DATA_1024']), color='b', linestyle='--')
            plt.xlabel("Time (s)")
            plt.ylabel("Data transferred (KB)")
            #plt.ylim(0,3500)
            plt_name = file_path.replace('.down', '_down')
            if PLT_AVG == True:
                plt_name = plt_name.replace('.txt','BW_AVG.pdf')
            else:
                plt_name = plt_name.replace('.txt','BW_.pdf')
            #print (plt_name)

            if ENABLE_SAVE == True:
                plt.savefig(plt_name,bbox_inches='tight')

            plt.show()


def main(argv):

    pd.options.display.max_colwidth = 300
    pd.options.display.float_format = '{:.2f}'.format
    plot_data()


if __name__ == '__main__':
    main(sys.argv[1:])


