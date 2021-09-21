import configparser
import os

def load_sw_base_conf():
    config = configparser.ConfigParser()
    # config.read(os.path.join(os.path.expanduser('~'), "config.text"))
    #config.read("config.text") #local file reading
    config.read(os.path.abspath(os.path.join(os.sep, 'usr', 'lib', 'capt', 'config.text')))


    global orion_un
    global orion_pw
    global orion_sv




    orion_un = config['ORION']['username']
    orion_pw = config['ORION']['password']
    orion_sv = config['ORION']['server']