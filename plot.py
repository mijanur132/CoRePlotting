import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import matplotlib as mpl

sns.set()
sns.set_context("talk")
sns.set_style("white")
mpl.rc("figure", facecolor="white")

MAX_ROWS = 20000

folder_path = '/Users/amitsheoran/Dropbox/Poster-ICNP/plot_data/'

fig_1c = folder_path + 'Sampling-Rate.csv'
fig_3 = folder_path + 'Sampling-Rate.csv'
fig_2 = folder_path + 'Tiling.csv'

LABEL_FONT_SIZE = 20
LEGENT_FONT_SIZE = 20
TICK_FONT_SIZE = 18

def plot_1c():

    df_1c = pd.read_csv(fig_1c, sep=',', nrows=MAX_ROWS)
    df_1c.columns = ['Pixel','Sampling_Rate','Pixel_Separation']

    x_axis = df_1c['Pixel'].tolist()

    sampling_rate = df_1c['Sampling_Rate'].tolist()
    pixel_seperation = df_1c['Pixel_Separation'].tolist()

    fig, ax1 = plt.subplots(figsize=(8, 4))

    ax2 = ax1.twinx()
    ax1.plot(x_axis, sampling_rate, 'g-',label='Sampling Rate')
    ax2.plot(x_axis, pixel_seperation, 'r--',label='Sampling Step')


    ax1.set_xlabel('Pixel Number',fontsize=LABEL_FONT_SIZE)
    ax1.set_ylabel('Sampling Rate [$pix^{-1}$]',fontsize=LABEL_FONT_SIZE,color='g')
    ax2.set_ylabel('Sampling Step [$pix$]',fontsize=LABEL_FONT_SIZE,color='r')

    fig.legend(loc='center',frameon = True,fontsize=LEGENT_FONT_SIZE,bbox_to_anchor=(0., .5, 1., .5))
    ax1.xaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax1.yaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax1.tick_params(axis='y', colors='g')
    ax2.yaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax2.tick_params(axis='y', colors='r')

    import matplotlib.ticker as ticker
    tick_spacing =1

    ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # plt.xlim(-100, 989)

    # plt.tight_layout()
    save_name = fig_1c.replace(".csv",".pdf")
    plt.savefig(save_name,)

    plt.show()



def plot_3():

    df_1c = pd.read_csv(fig_1c, sep=',', nrows=MAX_ROWS)
    df_1c.columns = ['Pixel','Sampling_Step','Uncompressed']

    x_axis = df_1c['Pixel'].tolist()

    sampling_rate = df_1c['Sampling_Step'].tolist()
    pixel_seperation = df_1c['Uncompressed'].tolist()

    fig, ax1 = plt.subplots(figsize=(8, 4))

    ax2 = ax1.twinx()
    ax2.plot(x_axis, sampling_rate, 'g-',label='Sampling Step')
    ax1.plot(x_axis, pixel_seperation, 'r--',label='Uncompressed Coordinate')


    ax1.set_xlabel('CoRE Coordinate [pix]',fontsize=LABEL_FONT_SIZE)
    ax2.set_ylabel('Sampling Step [pix]',fontsize=LABEL_FONT_SIZE,color='g')
    ax1.set_ylabel('Uncompressed \nCoordinate [pix]',fontsize=LABEL_FONT_SIZE,color='r')


    fig.legend(loc='center',frameon = False,fontsize=LEGENT_FONT_SIZE,bbox_to_anchor=(-0.05, .55, 1.1, .5))
    ax1.xaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax1.yaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax2.tick_params(axis='y', colors='g')
    ax2.yaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax1.tick_params(axis='y', colors='r')



    import matplotlib.ticker as ticker
    tick_spacing =1

    # ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax2.set_ylim([0,15])
    # plt.xlim(-100, 989)

    plt.tight_layout()
    save_name = fig_1c.replace(".csv",".pdf")
    plt.savefig(save_name)

    plt.show()




def get_hatch_style(t_label):

    print ("------------------------------------------------------------",t_label)

    if "1" in t_label:
        line_style = ''
        t_color = "#ff7f0e"
        t_color = "blue"

    if "4" in t_label:
        line_style = ''
        t_color = "red"

    if "CaRE" in t_label:
        line_style = ''
        t_color = "green"

    return (t_color,line_style)

def plot_2():

    df_2 = pd.read_csv(fig_2, sep=',', nrows=MAX_ROWS)
    df_2.columns = ['Label','1_Chunk','4_Chunk','CaRE']

    # Converting to % Scale
    percentage_list= ['1_Chunk','4_Chunk','CaRE']

    for item in percentage_list:
        df_2[item] = df_2[item].apply(lambda x: x/100)


    bar_1_chunk = df_2['4_Chunk'].tolist()
    bar_4_chunk = df_2['1_Chunk'].tolist()
    bar_CaRE = df_2['CaRE'].tolist()

    x_labels = df_2['Label'].tolist()

    barWidth = 0.25

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

    p1 = np.arange(len(bar_1_chunk))
    p2 = [x + barWidth for x in p1]
    p3 = [x + barWidth for x in p2]

    # Make the plot
    t_color,hatch_style= get_hatch_style('4_Chunk')
    plt.bar(p1, bar_1_chunk, width=barWidth, edgecolor=['black'] * len(p2), label='Tiling 4s',
    color=t_color,hatch=hatch_style,linewidth=1)

    t_color, hatch_style = get_hatch_style('1_Chunk')
    plt.bar(p2, bar_4_chunk, width=barWidth, edgecolor=['black'] * len(p2), label='Tiling 1s',
    color=t_color, hatch=hatch_style,linewidth=1)

    t_color, hatch_style = get_hatch_style('CaRE')
    plt.bar(p3, bar_CaRE, width=barWidth, edgecolor=['black'] * len(p2), label='CoRE',
    color=t_color, hatch=hatch_style,linewidth=1)

    plt.xticks([r + barWidth for r in range(len(bar_1_chunk))], x_labels)

    #fig.legend(loc='upper right',frameon = True,fontsize=18,bbox_to_anchor=(.95, .95))
    fig.legend(loc='upper right',frameon = False,fontsize=LEGENT_FONT_SIZE,bbox_to_anchor=(.95, .92))
    ax.xaxis.set_tick_params(labelsize=TICK_FONT_SIZE)
    ax.yaxis.set_tick_params(labelsize=TICK_FONT_SIZE)

    plt.ylabel('% of 360 video transferred',fontsize=LABEL_FONT_SIZE)
    plt.xlabel('Transfer mechanism',fontsize=LABEL_FONT_SIZE)
    plt.tight_layout()

    save_name = fig_2.replace(".csv",".pdf")
    plt.savefig(save_name)
    plt.show()

def plot_data():
    #plot_1c()
    plot_2()
    #plot_3()


def main(argv):

    pd.options.display.max_colwidth = 300
    pd.options.display.float_format = '{:.2f}'.format
    plot_data()


if __name__ == '__main__':
    main(sys.argv[1:])



