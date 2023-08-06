# readable names for data labels
_READABLE_LABELS = {'pl_name': 'Planet Name',
    'hostname': 'Host Name',
    'default_flag': 'Default Parameter Set',
    'sy_snum': 'Number of Stars',
    'sy_pnum': 'Number of Planets',
    'discoverymethod': 'Discovery Method',
    'disc_year': 'Discovery Year',
    'disc_facility': 'Discovery Facility',
    'soltype': 'Solution Type',
    'pl_controv_flag': 'Controversial Flag',
    'pl_refname': 'Planetary Parameter Reference',
    'pl_orbper': 'Orbital Period [days]',
    'pl_orbsmax': 'Orbit Semi-Major Axis [au]',
    'pl_rade': 'Planet Radius [Earth Radius]',
    'pl_radj': 'Planet Radius [Jupiter Radius]',
    'pl_masse': 'Planet Mass [Earth Mass]',
    'pl_massj': 'Planet Mass [Jupiter Mass]',
    'pl_bmasse': 'Planet Mass or Mass*sin(i) [Earth Mass]',
    'pl_bmassj': 'Planet Mass or Mass*sin(i) [Jupiter Mass]',
    'pl_dens': 'Planet Density [g/cm**3]',
    'pl_orbeccen': 'Eccentricity',
    'pl_insol': 'Insolation Flux [Earth Flux]',
    'pl_eqt': 'Equilibrium Temperature [K]',
    'ttv_flag': 'Data show Transit Timing Variations',
    'st_refname': 'Stellar Parameter Reference',
    'st_spectype': 'Spectral Type',
    'st_teff': 'Stellar Effective Temperature [K]',
    'st_rad': 'Stellar Radius [Solar Radius]',
    'st_mass': 'Stellar Mass [Solar mass]',
    'st_met': 'Stellar Metallicity [dex]',
    'st_metratio': 'Stellar Metallicity Ratio',
    'st_logg': 'Stellar Surface Gravity [log10(cm/s**2)]',
    'sy_refname': 'System Parameter Reference',
    'rastr': 'RA [sexagesimal]',
    'ra': 'RA [deg]',
    'decstr': 'Dec [sexagesimal]',
    'dec': 'Dec [deg]',
    'sy_dist': 'Distance [pc]',
    'sy_vmag': 'V (Johnson) Magnitude',
    'sy_kmag': 'Ks (2MASS) Magnitude',
    'sy_gaiamag': 'Gaia Magnitude',
    'rowupdate': 'Date of Last Update',
    'pl_pubdate': 'Planetary Parameter Reference Publication Date',
    'releasedate': 'Release Date'}

def get_label_list():
    list = []
    for label, _ in _READABLE_LABELS.items():
            list.append(label)
    return list

def get_readable(label):
    return _READABLE_LABELS[label]