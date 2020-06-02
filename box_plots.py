import pandas as pd
import sys

import seaborn as sns
import matplotlib as mpl
from collections import  defaultdict
import matplotlib.pyplot as plt
from pathlib import Path
import os.path
import numpy as np

MAX_ROWS = 20000
ENABLE_SAVE = True
ENABLE_COMPARISON_PLT = False


from sys import platform
if platform == "darwin":
    folder_path = '/Users/amitsheoran/PycharmProjects/Core_Plots/New_Data/Boxplot_data/'
    core_folder_path = '/Users/amitsheoran/PycharmProjects/Core_Plots/New_Data/Boxplot_data/CoRE/'
elif platform == "win32":
    core_folder_path = '.\\New_Data\\Boxplot_data\\CoRE\\'
    folder_path = '.\\New_Data\\Boxplot_data\\'

metrics = ['Delay','Qual','TotalData']
bandwidth = ['646']
setup = ['FoV360','FoVPlus360']
#exp_setup = ['tile','CoRE']
exp_setup = ['tile']
#vid_names = ['roller','diving','rhino']
vid_names = ['diving']
movement = ['D']

core_param = ['fetch_1s','fetch_2s','fetch_3s','fetch_4s']

# col_name_dict = defaultdict(list, (('tile', ['blankP','frameR', 'srAvg','srMin'])))

col_name_dict = defaultdict(list, (('Delay', ['FileName', 'Delay']), ('Qual', ['FileName','avgQualBorder', 'avgQualPopescu']),
                       ('TotalData', ['FileName','blank%','totalChunk2req']),
                       ('tile', ['FileName','blankP','frameR', 'srAvg','srMin']),
                        ('tileP', ['FileName','blankP','frameR', 'srAvg','srMin']),
                       ('CoRE', ['FileName','srAAvgRealTime','srMinRealTime', 'frRealTime']),
                       ('CoRE_old', ['FileName','avgSR','minSR','maxSR','MinFR','avgFR','totalDelay'])))


label_name_dict = {
    'frameR':'Frame_Rate',
    'frRealTime':'Frame_Rate_FoV+[CoRE]',

    'blankP':'BlankP',

    'srAvg':'Average_Sampling_Rate',
    'srAAvgRealTime':'Average_Sampling_Rate_FoV+[CoRE]',

    'srMin':'Minimum_Sampling_Rate',
    'srMinRealTime':'_Minimum_Sampling_Rate_FoV+[CoRE]'
}


def names_to_label(str):
    if str in label_name_dict:
        return label_name_dict[str]
    else:
        return (str)

def get_col_names(metric):
    if metric in col_name_dict:
        return col_name_dict[metric]

    return None


def clean_df(df,metric):
    col_names = get_col_names(metric)

    if col_names == None:
        exit(-1)

    print("DF_cols:")
    print(list(df.columns))
    df.columns = col_names

    def clean_header(val):
        new_val = val.split(':')[1]
        return float(new_val)

    def get_vid_name(file_name):
        new_name = file_name.split('/')[-1]
        new_name = new_name.split('.')[0]
        return new_name

    for item in  col_names[1:]:
        df[item] = df[item].apply(clean_header)

    new_col_names = []
    for item in col_names:
        new_col_names.append(names_to_label(item))


    df.columns = new_col_names

    df['vid_name'] = df['FileName'].apply(get_vid_name)

    df = df.drop(['FileName'], axis=1)
    print (df.head())

    return df


def plot_metric(vid_name,static,bw):

    print ("Input Params:",vid_name,static,bw)

    fov  = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFov360_' + static + '_' + bw + '.txt'
    fov_plus  = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFovP360_' + static + '_' + bw + '.txt'

    print (fov_plus)
    if os.path.exists(fov_plus) != True or os.path.exists(fov) != True:
        print("File Not found, returning",fov_plus,fov)
        return

    print (fov)

    df_fov = pd.read_csv(fov, sep=',', nrows=MAX_ROWS)
    df_fov_plus = pd.read_csv(fov_plus, sep=',', nrows=MAX_ROWS)


    df_fov = clean_df(df_fov,'tile')
    print("dfFovPlus: ");
    df_fov_plus = clean_df(df_fov_plus,'tileP')


    print("df_fov:",list(df_fov.columns),len(df_fov.index))
    print("df_fov_plus",list(df_fov_plus.columns),len(df_fov_plus.index))

    # print (df_fov['Delay'])

    # df_fov['Delay'].plot('bar')

    plot_features = list(df_fov_plus.columns)

    plot_features.remove('vid_name')

    print(plot_features)


    index_val =  list(df_fov_plus.index.values)

    df_fov_plus['Time'] = index_val

    df_fov_plus = df_fov_plus[df_fov_plus['Time'] < 1000]

    df_fov_plus =  df_fov_plus.drop(['vid_name'],axis=1)

    print (df_fov_plus)


    index_val =  list(df_fov.index.values)

    df_fov['Time'] = index_val

    df_fov = df_fov[df_fov['Time'] < 1000]

    df_fov =  df_fov.drop(['vid_name'],axis=1)

    print (df_fov)

    plot_features_fov = list(df_fov.columns)

    print(plot_features_fov)





    for feature in plot_features_fov:

        if feature == 'Time':
            continue

        print ("Feature",feature)

        ax= sns.lineplot(x=df_fov['Time'],y=df_fov[feature])
        ax = sns.lineplot(x=df_fov['Time'], y=df_fov_plus[feature])
        title =  str(feature) + ' [FOV] ' +  str(vid_name)
        plt.title(title)
        plt.xlabel("")
        plt_name = fov.replace('.txt','_PLT_')
        plt_name =  plt_name + "%s"%(feature) + '.pdf'
        if ENABLE_SAVE:
            plt.savefig(plt_name,bbox_inches='tight')
        plt.show()

    # for feature in plot_features:
    #     if feature == 'Time':
    #         continue
    #     ax= sns.lineplot(x=df_fov_plus['Time'],y=df_fov_plus[feature])
    #     title =  str(feature) + ' [FOV_PLUS] ' +  str(vid_name)
    #     plt.title(title)
    #     plt.xlabel("")
    #     plt_name = fov_plus.replace('.txt','_PLT_')
    #     plt_name =  plt_name + "%s"%(feature) + '.pdf'
    #     if ENABLE_SAVE:
    #         plt.savefig(plt_name,bbox_inches='tight')
    #     plt.show()



def plot_metric_core_new(vid_name,static,bw):

    print ("Input Params:",vid_name,static,bw)

    # fov  = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFov_' + static + '_' + bw + '.txt'
    fov_plus  = core_folder_path  + 'Core_FR_SR_' + vid_name + '_' + static + '_' + bw + '.txt'

    print (fov_plus)
    if os.path.exists(fov_plus) != True:
        print("File Not found, returning",fov_plus)
        return

    print (fov_plus)

    # df_fov = pd.read_csv(fov, sep=',', nrows=MAX_ROWS)
    df_Core = pd.read_csv(fov_plus, sep=',', nrows=MAX_ROWS)


    # df_fov = clean_df(df_fov,metric)
    df_Core = clean_df(df_Core,'CoRE')


    # print("df_fov:",list(df_fov.columns),len(df_fov.index))
    print("df_Core",list(df_Core.columns),len(df_Core.index))

    # print (df_fov['Delay'])

    # df_fov['Delay'].plot('bar')

    plot_features = list(df_Core.columns)

    plot_features.remove('vid_name')

    print(plot_features)



    save = folder_path  + 'test_Core.csv'

    df_Core.to_csv(save,index=False)

    index_val =  list(df_Core.index.values)

    df_Core['Time'] = index_val

    df_Core = df_Core[df_Core['Time'] < 2000]



    df_Core =  df_Core.drop(['vid_name'],axis=1)

    print (df_Core)

    for feature in plot_features:
        ax= sns.lineplot(x=df_Core['Time'],y=df_Core[feature])

        title =  str(feature) + ' [CoRE] ' +  str(vid_name)
        plt.title(title)
        plt.xlabel("")
        plt_name = fov_plus.replace('.txt','_PLT_')
        plt_name =  plt_name + "%s"%(feature) + '.pdf'
        if ENABLE_SAVE:
            plt.savefig(plt_name,bbox_inches='tight')
        plt.show()



def get_y_label(str):
    if 'Average' in str:
        return "Average Sampling Rate"
    if 'Minimum' in str:
        return "Minimum Sampling Rate"
    if 'Frame' in str:
        return 'Frame Rate'
    if 'Stall' in str:
        return 'Stall'

    return str

def plot_comparision_plots(vid_name,static,bw):

    print ("Input Params:",vid_name,static,bw)

    fov_plus  = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFovP_' + static + '_' + bw + '.txt'
    core_file = core_folder_path  + 'Core_FR_SR_' + vid_name + '_' + static + '_' + bw + '.txt'


    print (fov_plus)
    print (core_file)
    if os.path.exists(fov_plus) != True or os.path.exists(core_file) != True:
        print("File Not found, returning",fov_plus,core_file)
        return

    # print (fov_plus)

    df_fov_plus = pd.read_csv(fov_plus, sep=',', nrows=MAX_ROWS)
    df_Core = pd.read_csv(core_file, sep=',', nrows=MAX_ROWS)

    df_Core = clean_df(df_Core,'CoRE')
    df_fov_plus = clean_df(df_fov_plus,'tile')

    print(df_fov_plus.head())

    plot_features = list(df_Core.columns)

    plot_features.remove('vid_name')

    print(plot_features)

    index_val =  list(df_Core.index.values)
    df_Core['Time'] = index_val
    df_Core['U_Time'] =  df_Core['Time'] * (33/1000)
    df_Core = df_Core[df_Core['Time'] <= 2000]

    index_val =  list(df_fov_plus.index.values)
    df_fov_plus['Time'] = index_val
    df_fov_plus['U_Time'] =  df_fov_plus['Time'] * (33/1000)
    df_fov_plus = df_fov_plus[df_fov_plus['Time'] <= 2000]


    df_Core = df_Core.drop(['vid_name'],axis=1)
    #df_fov_plus = df_fov_plus.drop(['vid_name','FrameRate_Stall_FoV+'],axis=1)
    df_fov_plus = df_fov_plus.drop(['vid_name'],axis=1)

    df_merged =  pd.merge(df_fov_plus,df_Core,on='U_Time',how='inner')

    df_merged.set_index('U_Time')
    print (df_merged.head())
    print (df_merged.columns)

    def calc_Stall_for_CoRE(x):
        if x == 0:
            return 1
        return 0

    def calc_Stall_for_Tile(x):
        if x == 0:
            return 1
        return 0


    df_merged['Stall_FoV+[CoRE]'] = df_merged['Frame_Rate_FoV+[CoRE]'].apply(calc_Stall_for_CoRE)
    df_merged['Stall_FoV+[Tile]'] = df_merged['Frame_Rate_FoV+[Tile]'].apply(calc_Stall_for_Tile)

    print (df_merged.head())

    #Add the stall paramter to plot
    plot_features.append('Stall_FoV+[CoRE]')

    for feature in plot_features:

        fov_feature = feature.replace('CoRE','Tile')

        df_temp = df_merged[[feature,fov_feature,'U_Time']]
        df_temp = df_temp.set_index('U_Time')


        print ("========",df_temp.columns)
        # df_temp = df_temp.drop(['U_Time'], axis=1)

        title_feature = feature.split('[')[0]
        df_temp.columns = ['CoRE','FoV+ 1QL']

        print(df_temp.head())

        ax = sns.lineplot(data=df_temp)
        # title = 'Comparison of ' + str(title_feature) + '(' + str(vid_name) + ') ' + str(static)
        # plt.title(title)
        plt.xlabel("User Real Time (s)")
        plt.ylabel(get_y_label(feature))

        if 'Stall' in feature:
            plt.yticks(np.arange(2), ('No', 'Yes'))
        # plt.xlim(0,60)
        # Core_FR_SR_diving_F_646_CMP_diving_Average_Sampling_Rate_FoV +.pdf

        plt_name = core_file.replace('.txt', '_CMP_')
        plt_name = plt_name + "%s_%s" % (vid_name,title_feature) + '.pdf'

        print(plt_name)
        # print("Core_FR_SR_diving_F_646_CMP_diving_Average_Sampling_Rate_FoV +.pdf")

        if ENABLE_SAVE == True:
            plt.savefig(plt_name,bbox_inches='tight')
        plt.show()


        # ax = sns.boxplot(x=df_temp['merged_vid'], y=df_temp[feature])
        # title = '[Comparison] ' + exp_setup + '_' + metric + '_' + bw + ' (' + vid + ')'
        # plt.title(title)
        # plt.xlabel("")
        # plt_name = fov.replace('.txt', '_CMP_')
        # plt_name = plt_name + "%s_%s" % (vid,feature) + '.pdf'
        # if ENABLE_SAVE == True:
        #     plt.savefig(plt_name,bbox_inches='tight')
        # plt.show()

def plot_comparision_tiles_360StallOnly(vid_name,static,bw):

    print ("Input Params:",vid_name,static,bw)

    fov360  = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFov360_' + static + '_' + bw + '.txt'
    fovP360 = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFovP360_' + static + '_' + bw + '.txt'

    if os.path.exists(fov360) != True or os.path.exists(fovP360) != True:
        print("File Not found, returning",fov360,fovP360)
        return

    df_fov_plus = pd.read_csv(fovP360, sep=',', nrows=MAX_ROWS)
    df_fov = pd.read_csv(fov360, sep=',', nrows=MAX_ROWS)

    df_fov = clean_df(df_fov,'tile')
    df_fov_plus = clean_df(df_fov_plus,'tile')

    print("head: ")
    print(df_fov_plus.head())
    plot_features = list(df_fov.columns)
    plot_features.remove('vid_name')
    plot_features.remove('BlankP')
    print("plt_ftrs: ")
    print(plot_features)

    index_val =  list(df_fov.index.values)
    df_fov['Time'] = index_val
    df_fov['U_Time'] =  df_fov['Time'] * (33/1000)
    df_fov = df_fov[df_fov['Time'] <= 2000]

    index_val =  list(df_fov_plus.index.values)
    df_fov_plus['Time'] = index_val
    df_fov_plus['U_Time'] =  df_fov_plus['Time'] * (33/1000)
    df_fov_plus = df_fov_plus[df_fov_plus['Time'] <= 2000]


    df_fov = df_fov.drop(['vid_name'],axis=1)
    df_fov_plus = df_fov_plus.drop(['vid_name'],axis=1)

    df_merged =  pd.merge(df_fov,df_fov_plus,on='U_Time',how='inner')

    df_merged.set_index('U_Time')
    print ("mergedHeadCols")
    print(df_merged.head())
    print ("mergedCols")
    print (df_merged.columns)

    def calc_Stall_for_CoRE(x):
        if x == 0:
            return 1
        return 0

    def calc_Stall_for_Tile(x):
        if x == 1000:
            return 1
        return 0


    #df_merged['Stall_FoV+[tileP]'] = df_merged['Frame_Rate_FoV+[tileP]'].apply(calc_Stall_for_CoRE)
    df_merged['Stall_x'] = df_merged['BlankP_x'].apply(calc_Stall_for_Tile)
    df_merged['Stall_y'] = df_merged['BlankP_y'].apply(calc_Stall_for_Tile)
    print(df_merged['Stall_x'])
    print(df_merged['Stall_y'])
    print("dfMerged: ")
    print (df_merged.head())
    #Add the stall paramter to plot
   # plot_features.append('Stall')
    print(plot_features)
    for feature in plot_features:
        print("feature: ")
        print(feature)


        fov_feature = feature+'_y'
        feature = feature + '_x'
        print(fov_feature)
        print(feature)
        print(df_merged)
        df_temp = df_merged[['Frame_Rate_x','_y','U_Time']]
        print("df_temp: ")
        print(df_temp)
        df_temp = df_temp.set_index('U_Time')
        print ("========",df_temp.columns)
        # df_temp = df_temp.drop(['U_Time'], axis=1)

        title_feature = feature.split('[')[0]
        df_temp.columns = ['FoV 360','FoV+ 360']

        print(df_temp.head())

        ax = sns.lineplot(data=df_temp)
        # title = 'Comparison of ' + str(title_feature) + '(' + str(vid_name) + ') ' + str(static)
        # plt.title(title)
        plt.xlabel("User Real Time (s)")
        #plt.ylabel(get_y_label(feature))
        plt.ylabel('Stall')
        #
        if feature in feature:
             plt.yticks(np.arange(2), ('No', 'Yes'))
        # # plt.xlim(0,60)
        # # Core_FR_SR_diving_F_646_CMP_diving_Average_Sampling_Rate_FoV +.pdf
        #
        print(df_fov)
        #plt_name = df_fov.replace('.txt', '_CMP_')

        #plt_name = feature+".pdf"
        plt_name = "Stall" + ".pdf"


        #plt_name = plt_name + "%s_%s" % (vid_name,title_feature) + '.pdf'
        #
        print(plt_name)
        # # print("Core_FR_SR_diving_F_646_CMP_diving_Average_Sampling_Rate_FoV +.pdf")
        #
        if ENABLE_SAVE == True:
             plt.savefig(plt_name,bbox_inches='tight')
        plt.show()

def plot_comparision_tiles_360allexceptStall(vid_name,static,bw):

    print ("Input Params:",vid_name,static,bw)

    fov360  = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFov360_' + static + '_' + bw + '.txt'
    fovP360 = folder_path  + 'tile_' + vid_name + '_BP_FR_SRavg_SRminFovP360_' + static + '_' + bw + '.txt'

    if os.path.exists(fov360) != True or os.path.exists(fovP360) != True:
        print("File Not found, returning",fov360,fovP360)
        return

    df_fov_plus = pd.read_csv(fovP360, sep=',', nrows=MAX_ROWS)
    df_fov = pd.read_csv(fov360, sep=',', nrows=MAX_ROWS)

    df_fov = clean_df(df_fov,'tile')
    df_fov_plus = clean_df(df_fov_plus,'tile')

    print("head: ")
    print(df_fov_plus.head())
    plot_features = list(df_fov.columns)
    plot_features.remove('vid_name')
    plot_features.remove('BlankP')
    print("plt_ftrs: ")
    print(plot_features)

    index_val =  list(df_fov.index.values)
    df_fov['Time'] = index_val
    df_fov['U_Time'] =  df_fov['Time'] * (33/1000)
    df_fov = df_fov[df_fov['Time'] <= 2000]

    index_val =  list(df_fov_plus.index.values)
    df_fov_plus['Time'] = index_val
    df_fov_plus['U_Time'] =  df_fov_plus['Time'] * (33/1000)
    df_fov_plus = df_fov_plus[df_fov_plus['Time'] <= 2000]


    df_fov = df_fov.drop(['vid_name'],axis=1)
    df_fov_plus = df_fov_plus.drop(['vid_name'],axis=1)

    df_merged =  pd.merge(df_fov,df_fov_plus,on='U_Time',how='inner')

    df_merged.set_index('U_Time')
    print ("mergedHeadCols")
    print(df_merged.head())
    print ("mergedCols")
    print (df_merged.columns)


    #df_merged['Stall_FoV+[tileP]'] = df_merged['Frame_Rate_FoV+[tileP]'].apply(calc_Stall_for_CoRE)


    print("dfMerged: ")
    print (df_merged.head())
    #Add the stall paramter to plot
   # plot_features.append('Stall')
    print(plot_features)
    for feature in plot_features:
        print("feature: ")
        print(feature)
        fov_feature = feature+'_y'
        feature = feature + '_x'
        print(fov_feature)
        print(feature)
        print(df_merged)
       # df_temp = df_merged[['Frame_Rate_x','Frame_Rate_y','U_Time']]
        df_temp = df_merged[[feature, fov_feature, 'U_Time']]
        print("df_temp: ")
        print(df_temp)
        df_temp = df_temp.set_index('U_Time')
        print ("========",df_temp.columns)
        # df_temp = df_temp.drop(['U_Time'], axis=1)

        title_feature = feature.split('[')[0]
        df_temp.columns = ['FoV 360','FoV+ 360']

        print(df_temp.head())

        ax = sns.lineplot(data=df_temp)
        # title = 'Comparison of ' + str(title_feature) + '(' + str(vid_name) + ') ' + str(static)
        # plt.title(title)
        plt.xlabel("User Real Time (s)")
        plt.ylabel(get_y_label(feature))
       # plt.ylabel('Stall')
        #

        # # plt.xlim(0,60)
        # # Core_FR_SR_diving_F_646_CMP_diving_Average_Sampling_Rate_FoV +.pdf
        #
        print(df_fov)
        plt_name = df_fov.replace('.txt', '_CMP_')
        #plt_name = plt_name + "%s_%s" % (vid_name, title_feature) + '.pdf'
        plt_name = feature+".pdf"
        #plt_name = "Stall" + ".pdf"


        #plt_name = plt_name + "%s_%s" % (vid_name,title_feature) + '.pdf'
        #
        print(plt_name)
        # # print("Core_FR_SR_diving_F_646_CMP_diving_Average_Sampling_Rate_FoV +.pdf")
        #
        if ENABLE_SAVE == True:
             plt.savefig(plt_name,bbox_inches='tight')
        plt.show()


def main(argv):

    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', 300)

    pd.options.display.float_format = '{:.2f}'.format
    pd.options.mode.chained_assignment = None


    pd.options.display.max_colwidth = 300

    pd.options.display.float_format = '{:.2f}'.format

    sns.set()
    sns.set_context("talk")
    sns.set_style("white")
    #sns.palplot(sns.color_palette("hls", 8))
    # mpl.rc("figure", facecolor="white")




    #
    # for vid in vid_names:
    #     for s in movement:
    #         for b in bandwidth:
    #             plot_metric(vid,s,b)
    #             # exit(0)


    # for vid in vid_names:
    #     for s in movement:
    #         for b in bandwidth:
    #             plot_metric_core_new(vid,s,b)


    for vid in vid_names:
        for s in movement:
            for b in bandwidth:
                plot_comparision_plots360all(vid,s,b)




if __name__ == '__main__':
    main(sys.argv[1:])
