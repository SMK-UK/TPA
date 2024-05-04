"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\sk88\Dropbox (Heriot-Watt University Team)\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\TPA\1804_TPA",
    file                = r"Resonant",
    exceptions          = ['.png'],
    extensions          = ['.json'],
    refs_995            = ['solo_995'],
    refs_1550           = ['solo_1550'],

    c_axis = dict(

    cph = 1,
    cpl = 2,
    sph = 2,
    spl = 1

    )

)

