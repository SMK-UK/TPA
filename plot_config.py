"""
Config file for TPA measurements
"""

config_params = dict(
    
    # Path to load data from and arguments used to disriminate files loaded
    
    root                = r"C:\Users\sk88\Downloads\TPA",
    file                = r"1901_Json",
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

