"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\keena\Desktop\TPA_test",
    file                = r"Json Data",
    exceptions          = ['.png'],
    extensions          = ['.json'],
    refs_995            = ['995_solo'],
    refs_1550           = ['1550_solo'],

    c_axis = dict(

    cph = 1,
    cpl = 2,
    sph = 2,
    spl = 1

    )

)

