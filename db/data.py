from db import conn as co
import pandas as pd
import numpy as np

def retrieve_and_save_data():
    data = retrieve_data()
    print("데이터 저장됨.")

def retrieve_data():
    #DB 연결
    conn, cursor = co.connect_to_mysql(
        host='121.155.34.16',
        port='33063',
        user='sysop',
        password='data001!',
        database='fms'
    )
    # farm_id, tank_id, date, do, temperature, ph 값 불러오기
    query = "SELECT farm_id, tank_id, date, do, temperature, ph FROM water_quality_day_tb WHERE date > '2023-12-31'"
    r = co.execute_query(cursor, query)


    #data 와 온도만 불러오기
    query = "SELECT date, temperature FROM water_quality_day_tb WHERE date > '2023-12-31'"
    r2 = co.execute_query(cursor, query)
    df2 = pd.DataFrame(r2, columns=['date', 'temperature'])
        # NULL 값 존재하는 경우 해당 열의 평균으로 대체
    df2.to_csv('/Users/smin/visualstudiocode/aquaponix/csv/test.csv', mode='r+', index=False)
    # DF 형태로 만든 후 CSV 파일로 저장
    df = pd.DataFrame(r, columns=['farm_id', 'tank_id', 'date', 'do', 'temperature','ph'])
        # NULL 값 존재하는 경우 해당 열의 평균으로 대체
    df.fillna({"do":df["do"].mean(),"ph":df["ph"].mean()}, inplace=True)

    df.to_csv(r'/Users/smin/visualstudiocode/aquaponix/csv/table.csv')
    # DF의 NULL값 개수 확인
    #df.info()
    
    # DB 연결 종료
    co.close_connection(conn, cursor)

    return df

def rcv_dt():
    conn, cursor = co.connect_to_mysql(
        host='121.155.34.16',
        port='33063',
        user='sysop',
        password='data001!',
        database='fms'
    )
    query = "SELECT farm_id, tank_id, date, do, temperature, ph FROM water_quality_day_tb WHERE date > '2023-12-31'"
    r = co.execute_query(cursor, query)
    print(f'SUCCESS!! : {r.count()}')
    df = pd.DataFrame(r, columns=['farm_id', 'tank_id', 'date', 'do', 'temperature','ph'])
    df.to_csv()

#.Is Sensor alive
def rcv_sensor_status():
    conn, cursor = co.connect_to_mysql()
    query = "SELECT eq_id, status, mea_dt FROM sensor_status_tb"
    r = co.execute_query(cursor, query)
    df = pd.DataFrame(r, columns=['eq_id', 'status', 'mea_dt'] )
    list = df.values.tolist()
    return list
    # 130,1,1,PH 센서
    # 131,1,1,용존산소(DO) 센서
    # 132,1,1,염도센서
    # 133,1,1,수온 센서
    # 142,1,2,PH 센서
    # 143,1,2,용존산소(DO) 센서
    # 145,1,2,염도센서
    # 146,1,2,수온 센서

#.센서값 각각 CSV 파일에 저장
def sensor_value():
    conn, cursor = co.connect_to_mysql()
    
    query_146 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 146"
    query_145 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 145"
    query_143 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 143"
    query_142 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 142"
    
    query_133 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 133"
    query_130 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 130"
    query_131 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 131"
    query_132 = "SELECT mea_dt, value_mod FROM sensor_value_tb WHERE mea_dt > '2024-03-31 00:00:00' and eq_id = 132"


    r_146 = co.execute_query(cursor, query_146)
    r_145= co.execute_query(cursor, query_145)
    r_143 = co.execute_query(cursor, query_143)
    r_142 = co.execute_query(cursor, query_142)

    r_133 = co.execute_query(cursor, query_133)
    r_132 = co.execute_query(cursor, query_132)
    r_131 = co.execute_query(cursor, query_131)
    r_130 = co.execute_query(cursor, query_130)

    df_146 = pd.DataFrame(r_146, columns=['mea_dt', 'value'])
    df_146.to_csv('csv/146.csv', index=False, mode='r+')
    df_145 = pd.DataFrame(r_145, columns=['mea_dt', 'value'])
    df_145.to_csv('csv/145.csv', index=False, mode='r+')
    df_143 = pd.DataFrame(r_143, columns=['mea_dt', 'value'])
    df_143.to_csv('csv/143.csv', index=False, mode='r+')
    df_142 = pd.DataFrame(r_142, columns=['mea_dt', 'value'])
    df_142.to_csv('csv/142.csv', index=False, mode='r+')

    df_133 = pd.DataFrame(r_133, columns=['mea_dt', 'value'])
    df_133.to_csv('csv/133.csv', index=False, mode='r+')
    df_132 = pd.DataFrame(r_132, columns=['mea_dt', 'value'])
    df_132.to_csv('csv/132.csv', index=False, mode='r+')
    df_131 = pd.DataFrame(r_131, columns=['mea_dt', 'value'])
    df_131.to_csv('csv/131.csv', index=False, mode='r+')
    df_130 = pd.DataFrame(r_130, columns=['mea_dt', 'value'])
    df_130.to_csv('csv/130.csv', index=False, mode='r+')

    list = [142, 143, 145, 146, 130, 131, 132, 133]
    list2 = {}
    for i in list:
        df = pd.read_csv(f'csv/{i}.csv')
        list2[i] = df.loc[:, 'mea_dt'].tail(1).item()
    return list2 