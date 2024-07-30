"""
Config file for TPA measurements
"""


    
# Path to load data from and arguments used to disriminate files loaded
    
root                = r"c:\Users\sk88\Heriot-Watt University Team Dropbox\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\TPA\0725_TPA"
file                = r"Resonant_3\HP"
exceptions          = ['.csv', '.png']
extensions          = ['CP_avg.json']
refs_995            = ['solo_995']
refs_1550           = ['solo_1550']

c_axis = dict(

cph = 1,
cpl = 2,
sph = 2,
spl = 1

)



