from __future__ import division

import sys, time, getopt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools
import matplotlib
# matplotlib.use('Agg')
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
rcParams["figure.figsize"] = (8,9) # for 6 sets - Figure 8 
#rcParams["figure.figsize"] = (5,9) # for 3 sets - Figure 6-7
#rcParams["figure.figsize"] = (5,9) # for 2 sets - Figure 9-11

def plot_datasets(dataset, view, utilization):
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
        conv_ori.append(inputs[0])
        conv_carry.append(inputs[1])
        conv_inflation.append(inputs[2])
        ori.append(inputs[3])
        carry.append(inputs[4])
        inflation.append(inputs[5])
    
    # Figure 6-7
    #bxinput.append(conv_ori)
    #bxinput_2.append(conv_carry)
    #bxinput_2.append(conv_inflation)

    # Figure 8
    bxinput.append(conv_ori)
    bxinput.append(ori)
    
    bxinput_2.append(conv_carry)
    bxinput_2.append(conv_inflation)
    bxinput_2.append(carry)
    bxinput_2.append(inflation)
    
    #bxinput.append(ori)
    #bxinput.append(carry)
    #bxinput.append(inflation)

    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('o', 'v','*','D','x','+'))
    colors = itertools.cycle(('c','r','b','g','r','y','y','b'))
    names = []
    fig = plt.figure()    
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.1, 2]) 
    #ax = fig.add_subplot(111)
    ax = plt.subplot(gs[0])
    ax.set_facecolor('0.9')
    #fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)
    fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)
    ax.set_yscale("log")
    ax.set_ylabel('WCDFP (log-scale)',size=20)
    ax.tick_params(axis='both', which='major',labelsize=12)
    ax.vlines(0.5, 0, 1, linestyles='dotted', transform=ax.transAxes)

    # Figure 6 
    # U80
    #ax.set_ylim([10**-8, 10**0.5])
    # U60
    #ax.set_ylim([10**-18, 10**1])
    #ax.set_yticks([10**-18, 10**-15, 10**-12, 10**-9, 10**-6, 10**-3, 10**0]) # for Conv sets U60/80

    # Figure 7
    # U80
    #ax.set_ylim([10**-18, 10**1])
    # U60
    #ax.set_ylim([10**-63, 10**4])
    #ax.set_yticks([10**-60, 10**-48, 10**-36, 10**-24, 10**-12, 10**0]) # for Conv sets U60/80
   
    # Figure 8
    ax.set_ylim([10**-84, 10**5])

    # Figure 10
    #ax.set_ylim([10**-30, 10**5])
    #ax.set_yticks([10**-30, 10**-20, 10**-10, 10**0]) # for CB sets U45
    # Figure 11
    #ax.set_ylim([10**-300, 10**5]) # for CB sets
    #ax.set_yticks([10**-300, 10**-200, 10**-100, 10**0]) # for CB sets task 25/15

       
    #labels = ['Conv-CarryIn','Conv-Inflation', 'CB-CarryIn', 'CB-Inflation'] # 4 sets
    #labels = ['Conv-Refuted','Conv-CarryIn','Conv-Inflation'] # 3 sets
    #labels = ['Conv-Refuted'+r'$\times$'] # 1 set
    labels = ['Conv-Refuted'+r'$\times$', 'CB-Refuted'+r'$\times$'] # 2 set
    #labels = ['CB-Refuted','CB-CarryIn','CB-Inflation'] # 3 sets
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
    # Figure 8
    ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6, 0.6)) # 2 sets
    #ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6, 0.6, 0.6, 0.6, 0.6, 0.6)) # 6 sets
    #ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6, 0.6, 0.6)) # 3 sets
    
    # Figure 6-7
    #ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6))

    # Figure 5-7 -- second group
    ax = plt.subplot(gs[1])
    fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)
    
    # Figure 5 U80
    #ax.set_ylim([10**-8, 10**0.5])
    # Figure 5 U60
    #ax.set_ylim([10**-18, 10**1])

    # Figure 6
    # U80
    #ax.set_ylim([10**-18, 10**1])
    # U60
    #ax.set_ylim([10**-63, 10**4])
    #ax.set_yticks([10**-60, 10**-48, 10**-36, 10**-24, 10**-12, 10**0]) # for Conv sets U60/80
    
    # Figure 8
    ax.set_ylim([10**-84, 10**5])
    #ax.set_yticks([10**-100, 10**-75, 10**-50, 10**-25, 10**0]) 
    labels = ['Conv-CarryIn','Conv-Inflation', 'CB-CarryIn', 'CB-Inflation'] # 4 sets
    ax.vlines(0.5, 0, 1, linestyles='dotted', transform=ax.transAxes)

    ax.set_yscale("log")
    ax.tick_params(axis='both', which='major',labelsize=12)
    #labels = ['Conv-CarryIn','Conv-Inflation'] # 2 sets
    #for tick in ax.xaxis.get_major_ticks():
        #tick.label.set_fontsize(14)

    ax.yaxis.set_ticklabels([])
    #ax.boxplot(bxinput_2, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6))
    # Figure 8
    ax.boxplot(bxinput_2, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops, widths=(0.6, 0.6, 0.6, 0.6))
    ax.grid()

    #plt.legend(handles=[av, box, whisk], fontsize=12, frameon=True, loc=3)
    #plt.clf()
    #plt.show()
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
            plot = plot_datasets(dataset, view, utilization)
            save_pdf = PdfPages('./'+ ident + '_' + str(num_tasks) + '_' + str(num_sets)+  '_' +str(utilization)+ '_'+str(fault_rate)+'.pdf')
            # save_pdf = PdfPages(ident  + '_' + str(view) + '.pdf')
            save_pdf.savefig(plot, bbox_inches='tight', pad_inches=0.0)
            save_pdf.close()

        except Exception as e:
            print (e)
            continue
    else:
        print ('Must specify identifier')
        return
        
if __name__=="__main__":
    main()
