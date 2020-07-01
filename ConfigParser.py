import configparser

config = configparser.ConfigParser()

config['BASE'] = {
    'host': '127.0.0.1',
    'dbhost': 'localhost',
    'dbname': 'powercalcmaster',
    'user': 'postgres',
    'password': 'tak96tak'
}
with open(r'C:\Users\kurodt1\Desktop\temp\docker\config.ini', 'w') as file:
    config.write(file)