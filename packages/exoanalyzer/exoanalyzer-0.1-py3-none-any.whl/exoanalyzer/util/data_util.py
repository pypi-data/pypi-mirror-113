import math
import numpy as np

def get_system_planets(data, do_sort = True):
    """Returns a dictionary where key = hostname and value = list of planets from data which is a list of planet data"""
    hosts = {}
    for planet_id in range(len(data)):
        planet = data[planet_id]
        hostname = planet['hostname']
        if not hostname in hosts:
            hosts[hostname] = []
        hosts[hostname].append(planet_id)
    if do_sort:
        for hostname, planets in hosts.items():
            all_planets_valid = True
            for i in planets:
                if math.isnan(data[i]['pl_orbsmax']):
                    all_planets_valid = False
                    break
            
            if all_planets_valid:
                hosts[hostname] = sorted(planets, key=lambda i: data[i]['pl_orbsmax'] or 0)
            else:
                hosts[hostname] = planets
            all_planets_valid = True
    return hosts

def get_system_data(data):
    sys_planets = get_system_planets(data)

    for name, list in sys_planets.items():
        sys_planets[name] = [data[id] for id in list]

    return sys_planets

def get_system_pairs(data, do_sort = True):
    """
        Get pairs of planets.

        Args:
            'do_sort': Should the planets be sorted by distance from host star
    """
    system_planets = get_system_planets(data, do_sort)
    pairs = []
    for planets in system_planets.values():
        if len(planets) > 1:
            for i in range(len(planets)):
                if (i+1)%2==0:
                    pairs.append((data[planets[i-1]], data[planets[i]]))
    return pairs

def is_num_clean(n):
    return not (math.isinf(n) or math.isnan(n))

def get_pair_data(pairs, label, clean=True, **kwargs):
    modifier = kwargs.get("modifier")
    pair_data = []
    pair_ids = []

    for i in range(len(pairs)):
        pair = pairs[i]
        valA, valB = pair[0].get(label), pair[1].get(label)
        if valA and valB:
            if modifier:
                valA, valB = modifier(valA), modifier(valB)
            if clean:
                if is_num_clean(valA) and is_num_clean(valB): #valA != 0 and valB != 0
                    pair_data.append([valA, valB])
                    pair_ids.append(i)
                #else:
                #should it append something here to keep indices consistent?
            else:
                pair_data.append([valA, valB])
                pair_ids.append(i)
        #else:
        #should it append here too to keep indices consistent?
    return pair_data, pair_ids

def get_is_outlier(array, max_deviations = 2):
    mean = np.mean(array)
    std = np.std(array)
    # dist_from_mean = abs(array - mean)
    is_outlier = lambda x: abs(x-mean) > max_deviations * std
    return is_outlier

def remove_outliers_from_both(a, b, md):
    is_outlier = get_is_outlier(a, md)
    removes = 0
    for i in range(len(a)):
        i = i-removes
        if is_outlier(a[i]):
            removes += 1
            a.pop(i)
            b.pop(i)

# def get_datas(data, label, removeInvalid = True):
#     datas = []
#     for pl in data:
#         if removeInvalid:
#             val = pl[label]
#             if is_num_clean(val):
#                 datas.append(val)
#         else:
#             datas.append(pl[label])
#     return datas

def remove_any_nan(data, labelA, labelB):
    listA = []
    listB = []

    for pl in data:
        valA = pl[labelA]
        valB = pl[labelB]
        if is_num_clean(valA) and is_num_clean(valB):
            listA.append(valA)
            listB.append(valB)

    return listA, listB

def remove_nan_lists(listA, listB):
    removed = 0
    for i in range(len(listA)):
        i -= removed
        valA = listA[i]
        valB = listB[i]
        if not is_num_clean(valA) or not is_num_clean(valB):
            removed += 1
            listA.pop(i)
            listB.pop(i)
