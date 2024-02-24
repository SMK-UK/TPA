import data_functions as dat
import filter_functions as fil
import fitting_functions as fit
from math_functions import normalise, OD_calc
from plotting_functions import plot_scope
from scipy.integrate import simpson

import os

directory = r"C:\Users\keena\Downloads\TPA"
folder = "2301_lock_HP"

dir = os.path.join(directory, folder)

exts = ('avg.csv')
excs = ['.png']
refs_995 = ['995_solo']
refs_1550 = ['1550_solo']
refs = refs_995 + refs_1550
# polarisation for maximum and minimum absorption of both 1550 and 995 pulses
pol_1550 = ['230', '280']
pol_995 = ['40', '85']

# interogate directory to extract folder and file names
folder_list, file_list = dat.dir_interogate(path=dir, extensions=exts, exceptions=excs)
# create dictionary for indexing folders and files
fol_i = dat.make_index_dict(folder_list)
fil_i = [dat.make_index_dict(file_sub_list) for file_sub_list in file_list]
# assemble reference paths
ref_995_path = dat.search_paths(folder_list, file_list, include=refs_995)
ref_1550_path = dat.search_paths(folder_list, file_list, include=refs_1550)
ref_995_path_list = [os.path.join(dir, x) for x in ref_995_path]
ref_1550_path_list = [os.path.join(dir, x) for x in ref_1550_path]
# find polarisation numbers from reference file names
pols_995 = [dat.find_numbers(os.path.split(path)[1], '\d+') for path in ref_995_path]
pols_1550 = [dat.find_numbers(os.path.split(path)[1], '\d+') for path in ref_1550_path]
# extract excel data from the folders
data_path_list = dat.search_paths(folder_list, file_list, [exts[0]])
excel_sets = [[dat.open_excel(os.path.join(dir, data_path)) for data_path in data_paths] for data_paths in data_path_list]

# create dictionary for index of channel data
i = {'time': 0,
     'sp_trans': 1,
     'sp_ref': 2,
     'cp_trans': 3,
     'cp_ref': 4}
# make labels for the plots of said data
labels = {key:i[key] for key in i.keys() if key != 'time'}

# find index of the polarisation values
tpa_pol_1550 = [value for pol in pol_1550 for (key, value) in fol_i.items() if pol in key]
tpa_pol_995 = [value for pol in pol_995 for (key, value) in fol_i.items() if pol in key]
ref_pol_1550 = [value for pol in pol_1550 for (key, value) in fil_i[fol_i['1550_solo']].items() if pol in key]
ref_pol_995 = [value for pol in pol_995 for (key, value) in fil_i[fol_i['995_solo']].items() if pol in key]
# create dictionary for index of polarisation max / min - sp is for the folder index, rsp, rcp are for file indexing
p_i = {'tpa_sph': tpa_pol_1550[0],
       'tpa_spl': tpa_pol_1550[1],
       'max_sp': ref_pol_1550[0],
       'min_sp': ref_pol_1550[1],
       'max_cp': ref_pol_995[0],
       'min_cp': ref_pol_995[1]}

# plot 1550 reference data to check assignment
x = '1550_solo'
fol = fol_i[x]
fig, ax = plot_scope(excel_sets[fol][0][:,i['time']], [excel_sets[fol][0][:,i['sp_trans']], excel_sets[fol][0][:,i['sp_ref']], excel_sets[fol][0][:,i['cp_trans']], excel_sets[fol][0][:,i['cp_ref']]], titles=labels, multi=True)
print(x)

# plot 1550 reference data to check assignment
x = '995_solo'
fol = fol_i[x]
fig, ax = plot_scope(excel_sets[fol][0][:,i['time']], [excel_sets[fol][0][:,i['sp_trans']], excel_sets[fol][0][:,i['sp_ref']], excel_sets[fol][0][:,i['cp_trans']], excel_sets[fol][0][:,i['cp_ref']]], titles=labels, multi=True)
print(x)

# plot 1550 reference data to check assignment
x = '1550_HWP_230'
fol = fol_i[x]
fig, ax = plot_scope(excel_sets[fol][0][:,i['time']], [excel_sets[fol][0][:,i['sp_trans']], excel_sets[fol][0][:,i['sp_ref']], excel_sets[fol][0][:,i['cp_trans']], excel_sets[fol][0][:,i['cp_ref']]], titles=labels, multi=True)
print(x)

# plot 1550 reference data to check assignment
x = '1550_HWP_280'
fol = fol_i[x]
fig, ax = plot_scope(excel_sets[fol][0][:,i['time']], [excel_sets[fol][0][:,i['sp_trans']], excel_sets[fol][0][:,i['sp_ref']], excel_sets[fol][0][:,i['cp_trans']], excel_sets[fol][0][:,i['cp_ref']]], titles=labels, multi=True)
print(x)

# area for maximum sp and maximum cp polarisation
area_sph_cph = simpson(y=excel_sets[p_i['tpa_sph']][p_i['max_cp']][:,i['sp_trans']], x=excel_sets[p_i['tpa_sph']][p_i['max_cp']][:,i['time']])
area_sprh_cph = simpson(y=excel_sets[p_i['tpa_sph']][p_i['max_cp']][:,i['sp_ref']], x=excel_sets[p_i['tpa_sph']][p_i['max_cp']][:,i['time']])
# area for minimum sp and maximum cp polarisation
area_spl_cph = simpson(y=excel_sets[p_i['tpa_spl']][p_i['max_cp']][:,i['sp_trans']], x=excel_sets[p_i['tpa_spl']][p_i['max_cp']][:,i['time']])
area_sprl_cph = simpson(y=excel_sets[p_i['tpa_spl']][p_i['max_cp']][:,i['sp_ref']], x=excel_sets[p_i['tpa_spl']][p_i['max_cp']][:,i['time']])
# area for maximum sp and minimum cp polarisation
area_sph_cpl = simpson(y=excel_sets[p_i['tpa_sph']][p_i['min_cp']][:,i['sp_trans']], x=excel_sets[p_i['tpa_sph']][p_i['min_cp']][:,i['time']])
area_sprh_cpl = simpson(y=excel_sets[p_i['tpa_sph']][p_i['min_cp']][:,i['sp_ref']], x=excel_sets[p_i['tpa_sph']][p_i['min_cp']][:,i['time']])
# area for minimum sp and minimum cp polarisation
area_spl_cpl = simpson(y=excel_sets[p_i['tpa_spl']][p_i['min_cp']][:,i['sp_trans']], x=excel_sets[p_i['tpa_spl']][p_i['min_cp']][:,i['time']])
area_sprl_cpl = simpson(y=excel_sets[p_i['tpa_spl']][p_i['min_cp']][:,i['sp_ref']], x=excel_sets[p_i['tpa_spl']][p_i['min_cp']][:,i['time']])

# area for sp when only cp is present
area_sp_cph = simpson(y=excel_sets[fol_i['995_solo']][p_i['max_cp']][:,i['sp_trans']], x=excel_sets[fol_i['995_solo']][p_i['max_cp']][:,i['time']])
area_sp_cpl = simpson(y=excel_sets[fol_i['995_solo']][p_i['min_cp']][:,i['sp_trans']], x=excel_sets[fol_i['995_solo']][p_i['min_cp']][:,i['time']])

# normalised pulse areas (sp_trans when cp on - leakage when only cp solo (sp_trans) / sp_ref when cp on)
norm = {'norm_sph_cph': normalise(area_sph_cph, area_sp_cph, area_sprh_cph),
        'norm_sph_cpl': normalise(area_sph_cpl, area_sp_cpl, area_sprh_cpl),
        'norm_spl_cpl': normalise(area_spl_cpl, area_sp_cpl, area_sprl_cpl),
        'norm_spl_cph': normalise(area_spl_cph, area_sp_cph, area_sprl_cph)}