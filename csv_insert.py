import os,csv
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read(r'/home/takeshi/test/ini')

host = config['BASE']['host']
dbhost = config['BASE']['dbhost']
dbname = config['BASE']['dbname']
user = config['BASE']['user']
password = config['BASE']['password']

conn = psycopg2.connect(host=dbhost, dbname=dbname, user=user, password=password, port=5432)
cursor = conn.cursor()
cursor.execute("DELETE FROM XXXXXX_tb;")

with open(r"/home/takeshi/Master.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        
        cursor.execute("INSERT INTO master_tb (model_number,product,component,powerconsumption_w, \
        powerconsumption_va,heat_dissipation_btu_hr,heat_dissipation_kj_hr,width,depth,height,height_u_value, \
        weight_kg,current_a_100v,current_a_200v,voltage_v,temperature,humidity_noncondensing, \
        power_cord_qty,plug_type,Note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
        (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], \
        row[13],row[14],row[15],row[16],row[17],row[18],row[19]))
        
conn.commit()
cursor.close()
conn.close()