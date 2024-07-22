"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\keena\Downloads\0720_TPA\Resonant",
    file                = r"HP",
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
    sp_trans = 4,
    sp_ref = 3,
    cp_trans = 2,
    cp_ref = 1

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

