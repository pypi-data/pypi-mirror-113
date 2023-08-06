import os
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
from ..util import get_readable, get_pair_data, remove_outliers_from_both, remove_any_nan, get_system_data, is_num_clean

def save_plt(plt, file_path, file_name):
    full_path = file_path + file_name
    print("Saving: '" + full_path)
    try:
        plt.savefig(full_path)
    except:
        os.mkdir(file_path)
        plt.savefig(full_path)

def plot_pair_ratio(pair_data, plotLabel, **kwargs):
    """
    Creates a graph comparing the ratio of a specified data in pairs
    of planets to the first planet in the pair.

    Arguments:
        'use_log10': Base values in log10 (recommended for large data)
        'max_deviations': Removes outliers which deviate from the mean
                            by the standard deviation * this value.
        'file_path': File path to save graphs to.
        'file_name': Custom name for the file.
    """

    plt.clf()

    # setup arguments
    defaultKwargs = {
        'use_log10': True,
        'max_deviations': None,
        'file_path': "./graphs/",
        'file_name': f"Graph_of_{plotLabel}_Pair_Ratios.png",
    }
    kwargs = { **defaultKwargs, **kwargs }
    max_deviations = kwargs.get('max_deviations') or None

    # define axes
    extracted, _ = get_pair_data(pair_data, plotLabel)
    # this could be optimized and turned into one for loop but i like the
    # clean syntax of this solution
    x = [vals[0]/vals[1] for vals in extracted]
    y = [vals[0] for vals in extracted]

    # remove outliers
    if max_deviations:
        remove_outliers_from_both(x, y, max_deviations)

    # create the plot
    plt.scatter(x, y, color="red")

    if kwargs.get('use_log10'):
        axes = plt.gca()
        axes.set_yscale('log')
        axes.set_xscale('log')

    title = get_readable(plotLabel)
    if max_deviations:
        title = title + " (|x-x̄| < " + str(max_deviations) + "σ)"
    plt.title(title)
    plt.xlabel("Ratio of A/B")
    plt.ylabel("A of Pair")
    save_plt(plt, kwargs.get("file_path"), kwargs.get("file_name"))

def plot_dual(data, x_label, y_label, **kwargs):
    """
    Plot chart with two different categories as x and y
    """

    plt.clf()

    # setup arguments
    defaultKwargs = {
        'use_log10': True,
        'file_path': "./graphs/",
        'file_name': f"Graph_of_{x_label}_and_{y_label}.png",
    }
    kwargs = { **defaultKwargs, **kwargs }

    # get axes for
    x, y = remove_any_nan(data, x_label, y_label)

    plt.scatter(x, y, color="red")

    if kwargs.get('use_log10'):
        axes = plt.gca()
        axes.set_yscale('log')
        axes.set_xscale('log')

    x_readable = get_readable(x_label)
    y_readable = get_readable(y_label)
    plt.title(x_readable+" and "+y_readable)
    plt.xlabel(x_readable)
    plt.ylabel(y_readable)
    save_plt(plt, kwargs.get("file_path"), kwargs.get("file_name"))

def plot_system_average(data, main_label, avg_label, **kwargs):
    """
        Compare average of system planets to a value of the first planet in the system.
    """

    plt.clf()

    defaultKwargs = {
        'use_log10_main': False,
        'use_log10_avg': True,
        'file_path': "./graphs/",
        'file_name': f"Graph_of_avg_{main_label}_and_{avg_label}.png",
    }
    kwargs = { **defaultKwargs, **kwargs }


    sys_data = get_system_data(data)
    avgs = {}
    for host, pls in sys_data.items():
        avg = 0
        for pl in pls:
            avg += pl[avg_label]
        avg/=len(pls)
        avgs[host] = avg
    
    x = [sys[0][main_label] for _, sys in sys_data.items()]
    y = avgs.values()
    
    plt.scatter(x, y, color="red")

    axes = plt.gca()
    if kwargs.get('use_log10_main'):
        axes.set_xscale('log')
    if kwargs.get('use_log10_avg'):
        axes.set_yscale('log')
    x_readable = get_readable(main_label)
    y_readable = "Avg of " + get_readable(avg_label)
    plt.title(x_readable+" and "+y_readable)
    plt.xlabel(x_readable)
    plt.ylabel(y_readable)
    save_plt(plt, kwargs.get("file_path"), kwargs.get("file_name"))

def plot_ratio_to_greatest(data, label, **kwargs):
    """
        Plots ratio 
    """
    defaultKwargs = {
        'use_log10': True,
        'file_path': "./graphs/",
        'file_name': f"Graph_of_greatest_{label}.png",
    }
    kwargs = { **defaultKwargs, **kwargs }

    x = []
    y = []

    sys_data = get_system_data(data)
    for host, pls in sys_data.items():
        if len(pls) < 2:
            continue
        total = 0
        greatest = -1e15
        for pl in pls:
            val = pl[label]
            total += val
            greatest = max(greatest, val)
        ratio = greatest/total
        x.append(ratio*100)
        y.append(greatest)
    
    # remove_nan_lists(x, y)
    
    plt.scatter(x, y, color="red")

    if kwargs.get('use_log10'):
        axes = plt.gca()
        axes.set_yscale('log')
    x_readable = "% of greatest to total"
    y_readable = "Greatest " + get_readable(label)
    plt.title(x_readable+" and "+y_readable)
    plt.xlabel(x_readable)
    plt.ylabel(y_readable)
    save_plt(plt, kwargs.get("file_path"), kwargs.get("file_name"))

def plot_pair_comparison(pair_data, label, categories, **kwargs):
    """
    Creates a graph which categorizes pairs into specified categories.

    Arguments:
        'file_path': File path to save graphs to.
        'file_name': Custom name for the file.
    """

    plt.clf()

    # setup arguments
    defaultKwargs = {
        'file_path': "./graphs/",
        'file_name': f"Graph_of_{label}_Pair_Bar_Comparison.png",
    }
    kwargs = { **defaultKwargs, **kwargs }

    # define axes
    extracted, pair_ids = get_pair_data(pair_data, label)

    positions = [*range(0, len(categories)+1)]
    values = {}
    for pair in extracted:
        memberOf = None
        for name, category in categories.items():
            isMember = category(*pair)
            if isMember:
                memberOf = name
                break
        if memberOf:
            if not values.get(memberOf):
                values[memberOf] = 0
            values[memberOf] += 1
        else:
            print("Other:", pair_data[pair_ids[extracted.index(pair)]][0]["pl_name"], pair_data[pair_ids[extracted.index(pair)]][1]["pl_name"])
            if not values.get("Other"):
                values["Other"] = 0
            values["Other"] += 1
    
    value_list = []
    category_names = list(categories.keys())
    if values.get("Other"):
        category_names.append("Other")
    for name in category_names:
        value_list.append(values[name])

    print(positions, value_list)

    # create the plot
    bar = plt.bar(positions, value_list, color="red", width=0.75)
    
    ax = plt.gca()
    labels = [""]
    for bar_label in category_names:
        labels.append("")
        labels.append(bar_label)
    ax.set_xticklabels(labels)
    total = len(extracted)
    labels = []
    for val in value_list:
        labels.append(str(round(val/total * 1000)/10) + "%")
    ax.bar_label(bar, labels=labels)

    plt.title(get_readable(label))
    # plt.xlabel("Category")
    plt.ylabel("# of Planets")
    save_plt(plt, kwargs.get("file_path"), kwargs.get("file_name"))

def plot_pl_categories(data, label, categories, **kwargs):
    """
    Creates a graph which categorizes planets into specified categories.

    Arguments:
        'file_path': File path to save graphs to.
        'file_name': Custom name for the file.
    """

    plt.clf()

    # setup arguments
    defaultKwargs = {
        'file_path': "./graphs/",
        'file_name': f"Bar_Categories_of_{label}.png",
    }
    kwargs = { **defaultKwargs, **kwargs }

    # define axes

    positions = [*range(0, len(categories)+1)]
    values = {}
    for pl in data:
        val = pl[label]
        # if not is_num_clean(val):
        #     continue
        memberOf = None
        for name, category in categories.items():
            isMember = category(val)
            if isMember:
                memberOf = name
                break
        if memberOf:
            if not values.get(memberOf):
                values[memberOf] = 0
            values[memberOf] += 1
        else:
            print("Other:", pl["pl_name"])
            if not values.get("Other"):
                values["Other"] = 0
            values["Other"] += 1
    
    value_list = []
    category_names = list(categories.keys())
    if values.get("Other"):
        category_names.append("Other")
    for name in category_names:
        value_list.append(values[name])

    print(positions, value_list)

    # create the plot
    bar = plt.bar(positions, value_list, color="red", width=0.75)
    
    ax = plt.gca()
    labels = [""]
    for bar_label in category_names:
        labels.append("")
        labels.append(bar_label)
    ax.set_xticklabels(labels)
    total = len(data)
    labels = []
    for val in value_list:
        labels.append(str(round(val/total * 1000)/10) + "%")
    ax.bar_label(bar, labels=labels)

    plt.title(get_readable(label))
    # plt.xlabel("Category")
    plt.ylabel("# of Planets")
    save_plt(plt, kwargs.get("file_path"), kwargs.get("file_name"))