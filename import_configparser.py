import configparser

config = configparser.ConfigParser()
config.read(r'C:\Users\kurodt1\Desktop\temp\docker\config.ini')

print(config['BASE']['aaaa'])
print(config['TYPE']['number'])