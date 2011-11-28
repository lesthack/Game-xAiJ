import os

#data_py = os.path.abspath(os.path.dirname(__file__))
#data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))
data_dir = 'data'

def filepath(filename):
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    return open(os.path.join(data_dir, filename), mode)


#Declaracion de constantes
FONT_NAME = "MAKISUPA.TTF"