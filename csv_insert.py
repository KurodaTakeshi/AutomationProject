import os,csv
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read(r'/home/takeshi/test/ini/config.ini')

host = config['BASE']['host']
dbhost = config['BASE']['dbhost']
dbname = config['BASE']['dbname']
user = config['BASE']['user']
password = config['BASE']['password']

conn = psycopg2.connect(host=dbhost, dbname=dbname, user=user, password=password, port=5432)
cursor = conn.cursor()
cursor.execute("DELETE FROM master_tb;")

with open(r"/home/takeshi/Master.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        
        cursor.execute("INSERT INTO master_tb (model_number,high_or_low,nomal_or_recharge_or_100load,product,component,max_potential_power_w,input_typical_power_w, \
        max_potential_power_va,input_typical_power_va,heat_dissipation_btu_hr,heat_dissipation_kj_hr,width,depth,height,height_u_value, \
        weight_kg,current_a,voltage_v,temperature,humidity_noncondensing,sound_power_bels,sound_pressure_db,rated_power_w,rated_current_a, \
        power_cord_qty,plug_type,note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
        (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], \
        row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26]))
        
conn.commit()
cursor.close()
conn.close()