from __future__ import division

import sys, time, getopt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools
import matplotlib
plt.switch_backend('Agg')
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
from os import listdir
from os.path import isfile, join
import mpmath as mp

mp.dps = 15

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = True
rcParams["figure.figsize"] = (5,9) # for 2 sets - Figure 9-11

def plot_datasets(dataset, utilization):
    # format the input as the result
    bxinput = []
    bxinput_2 = []
    conv_ori = []
    conv_carry = []
    conv_inflation = []
    ori = []
    carry = []
    inflation = []
    for inputs in dataset:
        #conv_ori.append(inputs[0])
        #conv_carry.append(inputs[1])
        #conv_inflation.append(inputs[2])
        #ori.append(inputs[3])
        carry.append(inputs[4])
        inflation.append(inputs[5])
    
    # Figure 9
    #bxinput.append(ori)
    bxinput.append(carry)
    bxinput.append(inflation)

    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('o', 'v','*','D','x','+'))
    colors = itertools.cycle(('c','r','b','g','r','y','y','b'))
    names = []
    fig = plt.figure()    
    ax = fig.add_subplot(111)    
    fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)
    ax.set_yscale("log")
    ax.set_ylabel('WCDFP (log-scale)',size=20)
    ax.tick_params(axis='both', which='major',labelsize=12)

    # Figure 9 and 10
    ax.set_ylim([10**-30, 10**5])
    ax.set_yticks([10**-30, 10**-20, 10**-10, 10**0]) # for CB sets U45

    labels = ['CB-CarryIn','CB-Inflation']
    #the blue box
    boxprops = dict(linewidth=2, color='blue')
    #the median line
    medianprops = dict(linewidth=2.5, color='orange')
    whiskerprops = dict(linewidth=2.5, color='black')
    capprops = dict(linewidth=2.5)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(18)
    
    ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6, 0.6)) # 2 sets
    ax.grid()

    return fig

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:n:u:s:f:h:l", ["ident=", "num_tasks=","utilization=", "num_sets=", "fault_rate=", "hard_task_factor=", "limited"])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)

    num_tasks, num_sets, fault_rate, hard_task_factor = 0, 0, 0, 0
    ident = None
    limited = False
    utilization = 45
    for opt, arg in opts:
        if opt in ('-i', '--ident'):
            ident = str(arg)
        if opt in ('-n', '--num_tasks'):
            num_tasks = int(arg)
        if opt in ('-u', '--utilization'):
            utilization = int(arg)
        if opt in ('-s', '--num_sets'):
            num_sets = int(arg)
        if opt in ('-f', '--fault_rate'):
            fault_rate = min(1.0, float(arg))
        if opt in ('-h', '--hard_task_factor'):
            hard_task_factor = float(arg)
        if opt in ('-l', '--limited'):
            limited = True

    datasets = []
    dataset = []

    if ident is not None:
        filename = 'tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + 's_' + str(num_sets) + 'f_'+ str(fault_rate) + 'h_'+ str(hard_task_factor) + str('l' if limited else '')
        filename_ori = 'mp_res_ori_' + filename
        filename_carry = 'mp_res_carry_' + filename
        filename_inflation = 'mp_res_inflation_' + filename        
        filename_conv_ori = 'mp_res_conv_ori_' + filename
        filename_conv_carry = 'mp_res_conv_carry_' + filename
        filename_conv_inflation = 'mp_res_conv_inflation_' + filename

        try:
            results_conv_ori = np.load('../results/' + filename_conv_ori + '.npy', allow_pickle=True)
            results_conv_carry = np.load('../results/' + filename_conv_carry + '.npy', allow_pickle=True)
            results_conv_inflation = np.load('../results/' + filename_conv_inflation + '.npy', allow_pickle=True)
            
            results_ori = np.load('../results/' + filename_ori + '.npy', allow_pickle=True)
            results_carry = np.load('../results/' + filename_carry + '.npy', allow_pickle=True)
            results_inflation = np.load('../results/' + filename_inflation + '.npy', allow_pickle=True)
            
            for res_ori, res_carry, res_inflation, res_conv_ori, res_conv_carry, res_conv_inflation in zip(results_ori, results_carry, results_inflation, results_conv_ori, results_conv_carry, results_conv_inflation):            
                dataset.append([res_conv_ori, res_conv_carry, res_conv_inflation, res_ori['ErrProb'], res_carry['ErrProb'], res_inflation['ErrProb']])
            plot = plot_datasets(dataset, utilization)
            save_pdf = PdfPages('./outputs/Fig10_'+ str(num_tasks) +'tasks.pdf')
            save_pdf.savefig(plot, bbox_inches='tight', pad_inches=0.0)
            save_pdf.close()

        except Exception as e:
            print (e)            
    else:
        print ('Must specify identifier')
        return
        
if __name__=="__main__":
    main()
