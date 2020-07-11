# coding: UTF-8
import os
import configparser
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import sys
from redis import Redis, RedisError
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

reload(sys)
sys.setdefaultencoding('utf-8')

config = configparser.ConfigParser()
config.read(r'/home/docker/ini/config.ini')

host = config['BASE']['host']
dbhost = config['BASE']['dbhost']
dbname = config['BASE']['dbname']
user = config['BASE']['user']
password = config['BASE']['password']

UPLOAD_FOLDER = 'uploads'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'])
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def json_import(UPLOAD_FOLDER, filename):
    import json
    f = open(os.path.join(UPLOAD_FOLDER, filename), 'r')
    json_data = json.load(f)
    f.close()
    return(json_data)

def get_DPE_from_json(json_data):
    x = len(json_data["Structures"][0]["Bases"][0]["Modules"])
    x = x + 1
    DPE_list = [[] for i in range(x)]
    DPE_list[0].append(json_data["Structures"][0]["Bases"][0]["Id"])
    DPE_list[0].append(json_data["Structures"][0]["Bases"][0]["Qty"])
    for i in range(1,x):
        DPE_list[i].append(json_data["Structures"][0]["Bases"][0]["Modules"][i-1]["Options"][0]["Id"])  # Add model number
        DPE_list[i].append(json_data["Structures"][0]["Bases"][0]["Modules"][i-1]["Options"][0]["Qty"])  # Add qty
    return(DPE_list)

def get_DAE_from_json(json_data):
    y = len(json_data["Structures"][0]["Bases"])
    if y > 1:
        y = y -1
        DAE_list = [[] for i in range(y)]
        for j in range(0,y):
            DAE_list[j].append(json_data["Structures"][0]["Bases"][j+1]["Id"])
            DAE_list[j].append(json_data["Structures"][0]["Bases"][j+1]["Qty"])
        return(DAE_list)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            json_data = json_import(UPLOAD_FOLDER, filename) 
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
            DPE_list = get_DPE_from_json(json_data)
            DAE_list = get_DAE_from_json(json_data)

            #import DB
            import psycopg2
            conn = psycopg2.connect(host=dbhost, dbname=dbname, user=user, password=password, port=5432)
            x = len(json_data["Structures"][0]["Bases"][0]["Modules"])
            x = x + 1
            for i in range(0,x):
                strCur = "SELECT * FROM master_tb where model_number = '" + DPE_list[i][0] + "';"
                cur = conn.cursor()
                cur.execute(strCur)
                for row in cur:
                    DPE_list[i].append(row)
            y = len(json_data["Structures"][0]["Bases"])
            if y > 1:
                y = y -1
                for j in range(0,y):
                    strCur = "SELECT * FROM master_tb where model_number = '" + DAE_list[j][0] + "';"
                    cur = conn.cursor()
                    cur.execute(strCur)
                    for row in cur:
                        DAE_list[j].append(row)
            cur.close()
            conn.close()

            #for HTML
            #DPE_model = DPE_list[0][0]
            #DPE_Qty = DPE_list[0][1]
            html_DPE = ""
            for temp in DPE_list[0][2]:
                temp1 = str(temp)
                temp1 = "<td>" + temp1 + "</td>"
                html_DPE = html_DPE + temp1
            
            #for Excel
            Excel_DPE = []
            for buf in DPE_list[0][2]:
                buf1 = str(buf)
                try:
                    buf1 = float(buf1)
                except ValueError:
                    buf1 = str(buf1)
                Excel_DPE.append(buf1)

            #for html
            y = len(json_data["Structures"][0]["Bases"])
            if y > 1:
                y = y -1
                html_DAE = "<tr>"
                Excel_DAE = []
                for j in range(0,y):
                    #DAE_model = DAE_list[j][0]
                    #DAE_Qty = DAE_list[j][1]        
                    for buf in DAE_list[j][2]:
                        temp2 = str(buf)
                        temp2 = "<td>" + temp2 + "</td>"
                        html_DAE = html_DAE + temp2
                    #for Excel
                    for buf in DAE_list[j][2]:
                        buf2 = str(buf)
                        try:
                           buf2 = float(buf2)
                        except ValueError:
                           buf2 = str(buf2)
                        Excel_DAE.append(buf2)
            else:
                html_DAE = ""
                Excel_DAE = []

        return render_template('index.html',html_DPE=html_DPE,html_DAE=html_DAE,Excel_DPE=Excel_DPE,Excel_DAE=Excel_DAE)
    html = '''
           <!doctype html>
           <title>Upload new File</title>
           <h1>Upload new File</h1>
           <br>Request served by server: {hostname}<br>
           <form action="" method=post enctype=multipart/form-data>
           <p><input type=file name=file>
           <input type=submit value=Upload>
           </form>
           '''.format(hostname=socket.gethostname())
    return html 
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host=host, port=80)