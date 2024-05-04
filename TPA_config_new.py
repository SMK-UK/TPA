"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\sk88\Dropbox (Heriot-Watt University Team)\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\TPA\2404_TPA",
    file                = r"Resonant",
    exceptions          = ['.png'],
    extensions          = ['avg.csv'],
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

    ),

    # Index positions for trimming the data

    trim_indexes = dict(
    
    trig                = 50026, 
    ref_off             = 300,
    off                 = 1100, 
    ramp                = 65026,

    ),

    # Guess T1 times for the data

    guess_ref_T1 = 1E-6,
    guess_T1 = 10E-6

)

