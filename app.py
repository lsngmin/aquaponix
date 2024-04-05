from flask import Flask, render_template, session
import pandas as pd
import numpy as np
import glob
import json
from datetime import datetime, timedelta
import calendar, time
import csv, os, sys
from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify
from db import conn, data
import logging, logging.handlers



## LOG SET CODE S###
def log_init__():
    try:
        logger = logging.getLogger(name='[LOG]')
        logger.setLevel(logging.INFO)
        logger.propagate = False
        formatter = logging.Formatter('%(name)s[%(levelname)s] %(asctime)s | %(message)s', "%Y-%m-%d %H:%M:%S")

        if logger.hasHandlers():
            logger.handlers.clear()

        timedfilehandler = logging.handlers.TimedRotatingFileHandler(filename='log/tmp' ,when='midnight', interval=1, encoding='utf-8')
        timedfilehandler.setFormatter(formatter)
        timedfilehandler.suffix = "%Y%m%d.log"
        logger.addHandler(timedfilehandler)
    except Exception as e:
       logger.error(f'[SERVER] {e}')
    else:
       return logger
logger = log_init__()
app = Flask(__name__)
app.secret_key = 'app'
## LOG SET CODE E###

                                                    # *** 스케쥴 작업을 위한 함수는 본 주석 밑에서 구현 *** #
### DB에서 EQ_STATUS 테이블의 값을 리스트에 저장 S###
def SQ_rcv_eq_status():
    try:
        global sensor_status_list
        sensor_status_list  = data.rcv_sensor_status()
    except Exception as e:
        logger.error(f'[DATABASE] {e}')
    else:
        logger.info(f'[SCHEDULER] SQ_rcv_eq_status() (SUCCESS)HEAD OF CUR LIST : {sensor_status_list[0]}')
        return sensor_status_list
### DB에서 EQ_STATUS 테이블의 값을 리스트에 저장 E###

### DB에서 EQ_STATUS 테이블의 값을 리스트에 저장 S###
def SQ_rcv_ss_value():
    try:
        list = data.sensor_value()
    except Exception as e:
        logger.error(f'[DATABASE] {e}')
    else:
        for k, v in list.items():
            logger.info(f'[SCHEDULER] SQ_rcv_ss_value() (SUCCESS)CUR LIST :  EQ_ID = {k}, VALUE =  {v} ')
### DB에서 EQ_STATUS 테이블의 값을 리스트에 저장 E###

### HTML에 값 넘겨주기 위한 전역변수 할당 S###
global sensor_status_list
sensor_status_list = SQ_rcv_eq_status()
### HTML에 값 넘겨주기 위한 전역변수 할당 E###

                                                    # *** 스케줄러 초기화 및 실행 모든 스케줄러 구문은 본 주석 밑에서 구현 *** #
## SCHEDULER SET CODE S##
schedule = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
#schedule.add_job(scheduler, 'interval', seconds=15) #현재 서버 오류로 15초 단위 측정 불가
schedule.add_job(SQ_rcv_eq_status, 'interval', seconds=3600)
schedule.add_job(SQ_rcv_ss_value, 'interval', seconds=15)
schedule.start() 
## SCHEDULER SET CODE E##

#### !FLASK HTML MAPPING CODE! S####
@app.route('/')
def index():
    ## 로그파일을 index.html로 전송 하는 코드 S##
    global sensor_status_list
    tmp = open('log/tmp', mode='r')
    lines = tmp.readlines()
    li = lines[-10:]
    ## 로그파일을 index.html로 전송 하는 코드 E##
    ## 전역변수인 센서상태리스트가 선언 되어있지 않은 경우 초기화 하는 코드 S##
    if sensor_status_list == None:
       sensor_status_list = SQ_rcv_eq_status()
    ## 전역변수인 센서상태리스트가 선언 되어있지 않은 경우 초기화 하는 코드 E##
    return render_template('index.html', sensor_status_list=sensor_status_list, tmp=li)

@app.route('/temperature')
def temperature():
 return render_template('temperature.html')

@app.route('/ph')
def ph():
 return render_template('ph.html')

@app.route('/do')
def do():
 return render_template('do.html')

    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 S##
@app.route('/eq_id_146_t2_temperature')
def get_146():
    data = pd.read_csv('csv/146.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 S##
@app.route('/eq_id_145_t2_salinity')
def get_145():
    data = pd.read_csv('csv/145.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##
        ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 S##
@app.route('/eq_id_143_t2_do')
def get_143():
    data = pd.read_csv('csv/143.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##
        ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 S##
@app.route('/eq_id_142_t2_ph')
def get_142():
    data = pd.read_csv('csv/142.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##

    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 S##
@app.route('/eq_id_130_t1_ph')
def get_130():
    data = pd.read_csv('csv/130.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##
@app.route('/eq_id_131_t1_do')
def get_131():
    data = pd.read_csv('csv/131.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##
@app.route('/eq_id_132_t1_salinity')
def get_132():
    data = pd.read_csv('csv/132.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##
@app.route('/eq_id_133_t1_temperature')
def get_133():
    data = pd.read_csv('csv/133.csv')
    return jsonify(data.to_dict(orient='records'))
    ## ?실시간 동기화를 위한 데이터 세트 매핑 함수2 E##

#### !FLASK HTML MAPPING CODE! E####

### 사용 X 함수1 S###
def graphs():
    files = glob.glob("csv/table.csv")
    df = pd.read_csv(files[0])

    renderTo = ['DO','TEMPERATURE','PH']
    option =['do','temperature','ph']
    ttext=['용존 산소량','수온', '수소 이온 농도']
    ytext=['DO','TEMPERATURE','PH']
    chartInfo = []
    chart_type = 'line'
    chart_height = 500
    for i in range(3):
        chart = {"renderTo": renderTo[i], "type": chart_type, "height": chart_height}
        series = getSeries(df,option[i])
        title = {"text":ttext[i]}
        xAxis = {"type":"datetime", 'lineWidth':3,"dateTimeLabelFormats": {
            "minute": '%m월 %d일'
        },
        "startOnTick": 'true',
        "endOnTick": 'true',
        "showLastLabel": 'true',
        "labels": {
            "rotation": 0,
            "style":{
                "fontSize":8
            }
        },}
        yAxis = {"title":{"text":ytext[i]},"min":0, "max":20, 'lineWidth':1, 
                 "labels": {
                    "rotation": 0,
                    "style":{
                        "fontSize":10
                     }
                }
                 
                 }
        
        chartInfo.append([chart, series, title, xAxis, yAxis])

    return chartInfo
### 사용 X 함수1 E###

### 사용 X 함수2 S###
def getSeries(df,option):
    #수조 탱크의 구분을 위한 프로세스
    tank_type = df.tank_id.unique()
    series = '['
    for i in range(len(tank_type)):
        #수조 탱크는 현재 1,2 가 끝
        tank = tank_type[i]
        series += '{"name" : "Tank-' + str(tank) + '", "data" : ['
        for index, row in df.iterrows():
            if row['tank_id'] == tank and index % 4 == 0:
                series += '[' + str(calendar.timegm(time.strptime(row['date'], '%Y-%m-%d'))) + ',' + str(int(row[option])) + '],'                   
        series = series[:-1]
        series += ']},'
       
    series = series[:-1] + ']'
    return series
### 사용 X 함수2 E###

#### !FLASK MAIN FUNCTION CODE! S####
if __name__ == "__main__":
    port = 5002 ;debug=False ;use_reloader=False ;host='0.0.0.0'
    # ** LOG RECORD ** S#
    logger.info(f'[SERVER] CRT_PORT : {port} #CRT_HOST : {host} #CRT_DEBUG : {debug} #CRT_RELOADER : {use_reloader}')
    # ** LOG RECORD ** E#
    app.run(debug = debug,use_reloader=use_reloader, host=host, port=port, passthrough_errors=True)
#### !FLASK MAIN FUNCTION CODE! E####

### 사용 X 함수3 S###
def scheduler():
    f = open('csv/test.csv','a', newline='')
    wr = csv.writer(f)
    wr.writerow(['2024-04-02',36.5])
    print("SUCCESS! {}".format(time.time()))
    # print(f'TEST!! : {time.time()} {os.getpid()}')
    # wr.writerow(['2024-04-03',13.0])
    # print("SUCCESS! {}".format(time.time()))
    # wr.writerow(['2024-04-04',11.0])
    # print("SUCCESS! {}".format(time.time()))
    # wr.writerow(['2024-04-05',16.0])
    # print("SUCCESS! {}".format(time.time()))
    f.close()
    print("스케쥴 종료")
### 사용 X 함수3 E###