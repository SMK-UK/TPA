"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\sk88\Dropbox (Heriot-Watt University Team)\RES_EPS_Quantum_Photonics_Lab\Experiments\Current Experiments\BB Telecom QM\2024_PrYSO\TPA",
    file                = r"1901_unlocked_HP_p4GHz",
    exceptions          = ['.png'],
    extensions          = ('avg.csv')
    exceptionss         = ['.png']
    refs_995            = ['995_solo']
    refs_1550           = ['1550_solo']

    # polarisation for maximum and minimum absorption of both 1550 and 995 pulses

    pol_1550 = ['280', '330']
    pol_995 = ['40', '85']
    
    # Index positions for relevant column data in excel files
    
    data_indexes = dict(

    time = 0,
    sp_trans = 1,
    sp_ref = 2,
    cp_trans = 3,
    cp_ref = 4

    ),

    # Index positions for trimming the data

    trim_indexes = dict(
    
    trig                = 50026, 
    ref_off             = 300,
    off                 = 1100, 
    ramp                = 65026

    ),

    # Guess T1 times for the data

    guess_ref_T1 = 1E-6,
    guess_T1 = 10E-6

)

