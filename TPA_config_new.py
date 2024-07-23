"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\sk88\Heriot-Watt University Team Dropbox\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\TPA\0509_TPA\Pulse_width",
    file                = r"10us",
    exceptions          = ['avg', '.png'],
    extensions          = ['.csv'],
    refs_995            = ['solo_995'],
    refs_1550           = ['solo_1550'],

    # polarisation for maximum and minimum absorption of both 1550 and 995 pulses

    pol_1550 = ['slow', 'fast'],
    pol_995 = ['slow', 'fast'],
    
    # Index positions for relevant column data in excel files
    
    data_indexes = dict(

    time = 0,
    sp_trans = 3,
    sp_ref = 4,
    cp_trans = 1,
    cp_ref = 2

    )

)

