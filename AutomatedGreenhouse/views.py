from django.http import HttpResponse
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render

from .camera import Camera

import pandas as pd
import pymysql
import threading
import time
import json
import datetime

# smart plug libraries
from .smartplug import SmartPlug
from .Reco4lifeP10A import on
from .Reco4lifeP10A import off

scale_size = 10000

# device_setting
Humidifier_setting = ("192.168.0.103", "Edimax")
Heater_setting = ("192.168.0.102", "Edimax")
Fan0_setting = ("192.168.0.106", "Reco4life")
Fan1_setting = ("192.168.0.105", "Reco4life")
Pump_setting = ("192.168.0.107", "Reco4life")
Light0_setting = ("192.168.0.104", "Reco4life")
Light1_setting = ("192.168.0.108","Reco4life")

class Device:
    def __init__(self, ip, type):
        self._IP = ip
        self._type = type

    def on(self):
        if self._type == "Edimax":
            SmartPlug(self._IP, ('admin', 'password')).state = 'ON'
        elif self._type == "Reco4life":
            on(self._IP)

    def off(self):
        if self._type == "Edimax":
            SmartPlug(self._IP, ('admin', 'password')).state = 'OFF'
        elif self._type == "Reco4life":
            off(self._IP)

# Device inits
Humidifier = Device(Humidifier_setting[0], Humidifier_setting[1])
Heater = Device(Heater_setting[0], Heater_setting[1])
Fan0 = Device(Fan0_setting[0], Fan0_setting[1])
Fan1 = Device(Fan1_setting[0], Fan1_setting[1])
Pump = Device(Pump_setting[0], Pump_setting[1])
Light0 = Device(Light0_setting[0], Light0_setting[1])
Light1 = Device(Light1_setting[0], Light1_setting[1])



def video_feed(request):
        return StreamingHttpResponse(gen(Camera()),content_type='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
        while True:
                frame = camera.get_frame()
                yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ControlPanel(request):
    if 'button_light_on' in request.POST:
        Light0.on()
        user_control_tag("light")
    elif 'button_light_off' in request.POST:
        Light0.off()
        user_control_tag("light")
    if 'button_fan0_on' in request.POST:
        Fan0.on()
        user_control_tag("fan0")
    elif 'button_fan0_off' in request.POST:
        Fan0.off()
        user_control_tag("fan0")
    if 'button_fan1_on' in request.POST:
        Fan1.on()
        user_control_tag("fan1")
    elif 'button_fan1_off' in request.POST:
        Fan1.off()
        user_control_tag("fan1")
    elif 'button_waterpump_on' in request.POST:
        device_control_single(Pump,6)
        user_control_tag("waterpump")
    elif 'button_humidifier_on_strong' in request.POST:
        device_control_single(Humidifier,60*30,30,30)
        user_control_tag("humidifier")
    elif 'button_humidifier_on_weak' in request.POST:
        device_control_single(Humidifier,60*30,30,30)
        user_control_tag("humidifier")
    elif 'button_humidifier_off' in request.POST:
        Humidifier.off()
        user_control_tag("humidifier")
    elif 'button_heeter_on_strong' in request.POST:
        device_control_single(Heater,60*30,30,150)
        user_control_tag("heater")
    elif 'button_heater_on_weak' in request.POST:
        device_control_single(Heater,60*30,30,90)
        user_control_tag("heater")
    elif 'button_heater_off' in request.POST:
        Heater.off()
        user_control_tag("heater")
    elif 'button_setting_submit' in request.POST:
        light_limit_low = request.POST.get("Input_light_low") if request.POST.get("Input_light_low") != "" else None
        light_limit_high = request.POST.get("Input_light_high") if request.POST.get("Input_light_high") != "" else None
        temperature_limit_low = request.POST.get("Input_temperature_low") if request.POST.get("Input_temperature_low") != "" else None
        temperature_limit_high = request.POST.get("Input_temperature_high") if request.POST.get("Input_temperature_high") != "" else None
        humidity_limit_low = request.POST.get("Input_humidity_low") if request.POST.get("Input_humidity_low") != "" else None
        humidity_limit_high = request.POST.get("Input_humidity_high") if request.POST.get("Input_humidity_high") != "" else None
        moisture_limit_low = request.POST.get("Input_moisture_low") if request.POST.get("Input_moisture_low") != "" else None
        conn=pymysql.connect(host='localhost',
                                port=3306,
                                user='Greenhouseadmin',
                                password='adminpassword',
                                db='GreenhouseDB',
                                charset='utf8')
        cur=conn.cursor()
        sql = "INSERT INTO user_settings (light_limit_low, light_limit_high, temperature_limit_low, temperature_limit_high, humidity_limit_low, humidity_limit_high, moisture_limit_low) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        val = (light_limit_low, light_limit_high, temperature_limit_low, temperature_limit_high, humidity_limit_low, humidity_limit_high, moisture_limit_low)
        cur.execute(sql,val)
        conn.commit()
        cur.close()
        conn.close()


    dbconn=pymysql.connect(
    host="localhost",
    database="GreenhouseDB",
    user="Greenhouseadmin",
    password="adminpassword",
    port=3306,
    charset='utf8'
    )
    
    # read the latest data
    sqlcmd = "select * from environment_status order by id desc limit 48"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")

    return_data_dic = {}
    return_data_dic["time"] = data_dic["time"][0][0:19]
    return_data_dic["sensor_light"] = int(data_dic["sensor_light_0"][0] / scale_size)
    return_data_dic["sensor_CO2"] = int((data_dic["sensor_CO2_0"][0] + data_dic["sensor_CO2_1"][0]) / 2 / scale_size)
    return_data_dic["sensor_moisture"] = int((data_dic["sensor_moisture_0"][0] + data_dic["sensor_moisture_1"][0] + data_dic["sensor_moisture_2"][0] + data_dic["sensor_moisture_3"][0]) / 4 / scale_size)
    return_data_dic["sensor_temperature_inside"] = data_dic["sensor_temperature_inside"][0] if data_dic["sensor_humidity_inside"][0] < 100 and data_dic["sensor_humidity_inside"][0] != 0 else "null"
    return_data_dic["sensor_temperature_outside"] = data_dic["sensor_temperature_outside"][0] if data_dic["sensor_humidity_outside"][0] < 100  and data_dic["sensor_humidity_outside"][0] != 0 else "null"
    return_data_dic["sensor_humidity_inside"] = data_dic["sensor_humidity_inside"][0] if data_dic["sensor_humidity_inside"][0] < 100 and data_dic["sensor_humidity_inside"][0] != 0 else "null"
    return_data_dic["sensor_humidity_outside"] = data_dic["sensor_humidity_outside"][0] if data_dic["sensor_humidity_outside"][0] < 100 and data_dic["sensor_humidity_outside"][0] != 0 else "null"

    # return_data_dic["light"] = "On" if data_dic["device_light"][0] else "Off"
    # return_data_dic["waterpump"] = "On" if data_dic["device_waterpump"][0] else "Off"
    # return_data_dic["fan0"] = "On" if data_dic["device_fan_0"][0] else "Off"
    # return_data_dic["fan1"] = "On" if data_dic["device_fan_1"][0] else "Off"
    # return_data_dic["humidifier"] = "On" if data_dic["device_humidifier"][0] else "Off"
    # return_data_dic["heater"] = "On" if data_dic["device_heater"][0] else "Off"

    return_data_dic["light"] = data_dic["device_light"][0]
    return_data_dic["waterpump"] = data_dic["device_waterpump"][0]
    return_data_dic["fan0"] = data_dic["device_fan_0"][0]
    return_data_dic["fan1"] = data_dic["device_fan_1"][0]
    return_data_dic["humidifier"] = data_dic["device_humidifier"][0]
    return_data_dic["heater"] = data_dic["device_heater"][0]

    visualization_data_dic = {}
    visualization_data_dic["light_24h"] = data_for_visualization_scale(data_dic["sensor_light_0"],2)
    CO2_24h = data_dic["sensor_CO2_0"]
    CO2_24h_ = data_dic["sensor_CO2_1"]
    for i in range(len(CO2_24h)):
        CO2_24h[i] += CO2_24h_[i]
        CO2_24h[i] = int(CO2_24h[i] / 2)
    visualization_data_dic["CO2_24h"] = data_for_visualization_scale(CO2_24h,2)
    visualization_data_dic["moisture_24h_0"] = data_for_visualization_scale(data_dic["sensor_moisture_0"],2)
    visualization_data_dic["moisture_24h_1"] = data_for_visualization_scale(data_dic["sensor_moisture_1"],2)
    visualization_data_dic["moisture_24h_2"] = data_for_visualization_scale(data_dic["sensor_moisture_2"],2)
    visualization_data_dic["moisture_24h_3"] = data_for_visualization_scale(data_dic["sensor_moisture_3"],2)
    visualization_data_dic["temperature_24h"] = data_for_visualization(data_dic["sensor_temperature_inside"],2)
    visualization_data_dic["humidity_24h"] = data_for_visualization(data_dic["sensor_humidity_inside"],2)


    return render(request, 'ControlPanel.html', {"data_dic": return_data_dic, "visualization_data_dic": visualization_data_dic})



def HistoryData(request):

    dbconn=pymysql.connect(
    host="localhost",
    database="GreenhouseDB",
    user="Greenhouseadmin",
    password="adminpassword",
    port=3306,
    charset='utf8'
    )
    
    visualization_data_dic = {}

    # read the latest data
    sqlcmd = "select * from environment_status order by id desc limit 48"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")

    visualization_data_dic["light_24h"] = data_for_visualization(data_dic["device_light"],2)
    visualization_data_dic["waterpump_24h"] = data_for_visualization(data_dic["device_waterpump"],2)
    visualization_data_dic["fan0_24h"] = data_for_visualization(data_dic["device_fan_0"],2)
    visualization_data_dic["fan1_24h"] = data_for_visualization(data_dic["device_fan_1"],2)
    visualization_data_dic["humidifier_24h"] = data_for_visualization(data_dic["device_humidifier"],2)
    visualization_data_dic["heater_24h"] = data_for_visualization(data_dic["device_heater"],2)

    # read the latest data
    sqlcmd = "select * from environment_status order by id desc limit 336"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")

    step_7d = 2*6

    visualization_data_dic["light_7d"] = data_for_visualization_scale(data_dic["sensor_light_0"],step_7d)
    CO2_7d = data_dic["sensor_CO2_0"]
    CO2_7d_ = data_dic["sensor_CO2_1"]
    for i in range(len(CO2_7d)):
        CO2_7d[i] += CO2_7d_[i]
        CO2_7d[i] = int(CO2_7d[i] / 2)
    visualization_data_dic["CO2_7d"] = data_for_visualization_scale(CO2_7d,step_7d)
    visualization_data_dic["moisture_7d_0"] = data_for_visualization_scale(data_dic["sensor_moisture_0"],step_7d)
    visualization_data_dic["moisture_7d_1"] = data_for_visualization_scale(data_dic["sensor_moisture_1"],step_7d)
    visualization_data_dic["moisture_7d_2"] = data_for_visualization_scale(data_dic["sensor_moisture_2"],step_7d)
    visualization_data_dic["moisture_7d_3"] = data_for_visualization_scale(data_dic["sensor_moisture_3"],step_7d)
    visualization_data_dic["temperature_7d"] = data_for_visualization(data_dic["sensor_temperature_inside"],step_7d)
    visualization_data_dic["humidity_7d"] = data_for_visualization(data_dic["sensor_humidity_inside"],step_7d)

    sqlcmd = "select * from environment_status order by id desc limit 1440"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")

    step_30d = 2*24
    visualization_data_dic["light_30d"] = data_for_visualization_scale(data_dic["sensor_light_0"],step_30d)
    CO2_30d = data_dic["sensor_CO2_0"]
    CO2_30d_ = data_dic["sensor_CO2_1"]
    for i in range(len(CO2_30d)):
        CO2_30d[i] += CO2_30d_[i]
        CO2_30d[i] = int(CO2_30d[i] / 2)
    visualization_data_dic["CO2_30d"] = data_for_visualization_scale(CO2_30d,step_30d)
    visualization_data_dic["moisture_30d_0"] = data_for_visualization_scale(data_dic["sensor_moisture_0"],step_30d)
    visualization_data_dic["moisture_30d_1"] = data_for_visualization_scale(data_dic["sensor_moisture_1"],step_30d)
    visualization_data_dic["moisture_30d_2"] = data_for_visualization_scale(data_dic["sensor_moisture_2"],step_30d)
    visualization_data_dic["moisture_30d_3"] = data_for_visualization_scale(data_dic["sensor_moisture_3"],step_30d)
    visualization_data_dic["temperature_30d"] = data_for_visualization(data_dic["sensor_temperature_inside"],step_30d)
    visualization_data_dic["humidity_30d"] = data_for_visualization(data_dic["sensor_humidity_inside"],step_30d)



    return render(request,'HistoryData.html', {"visualization_data_dic": visualization_data_dic})

def index(request):
    return render(request,'index.html')


def device_control_single(device, on_time):
    t = threading.Thread(target=device_control_helper,args=(device,on_time))
    t.start()

def device_control_helper(device, on_time):
    device.on()
    time.sleep(on_time)
    device.off()

def device_control_single(device, duration, on_time, off_time):
    t = threading.Thread(target=device_control_helper,args=(device,duration,on_time,off_time))
    t.start()

def device_control_helper(device, duration, on_time, off_time):
    for i in range(int(duration/ (on_time + off_time))):
        device.on()
        time.sleep(on_time)
        device.off()
        time.sleep(off_time)


def data_for_visualization(data_list,step):
    list_return = []
    for i in range(int(len(data_list)/step)):
        list_return.append([i,data_list[i*step]if data_list[i*step] != 0 else data_list[i*step +1]])
    return list_return

def data_for_visualization_scale(data_list,step):
    list_return = []
    for i in range(int(len(data_list)/step)):
        list_return.append([i,int(data_list[i*step]/scale_size if data_list[i*step] != 0 else data_list[i*step +1]/scale_size)])
    return list_return


def user_control_tag(device_name):
    t = threading.Thread(target=user_control_tag_helper,args=[device_name])
    t.start()

def user_control_tag_helper(device_name):
    conn=pymysql.connect(host='localhost',
                             port=3306,
                             user='Greenhouseadmin',
                             password='adminpassword',
                             db='GreenhouseDB',
                             charset='utf8')
    cur=conn.cursor()
    sql = "INSERT INTO user_control (time, " + device_name + ") VALUES (%s, %s);"
    val = ( datetime.datetime.now(), True)
    cur.execute(sql,val)
    conn.commit()
    cur.close()
    conn.close()

    # wait for 30min
    time.sleep(30 *60)

    cur=conn.cursor()
    sql = "INSERT INTO user_control (time," + device_name + ") VALUES (%s, %s);"
    val = ( datetime.datetime.now(), False)
    cur.execute(sql,val)
    conn.commit()
    cur.close()
    conn.close()


def greenhouseDBRead(request):
    dbconn=pymysql.connect(
    host="localhost",
    database="GreenhouseDB",
    user="Greenhouseadmin",
    password="adminpassword",
    port=3306,
    charset='utf8'
    )
    # read the latest data
    sqlcmd = "select * from experiment_data order by id desc limit 48"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")

    dic_return = {}
    dic_return["time"] = data_dic["time"][0][0:19]
    dic_return["sensor_light"] = data_dic["sensor_light_0"][0]
    dic_return["sensor_CO2"] = (int)(data_dic["sensor_CO2_0"][0] + data_dic["sensor_CO2_1"][0]) / 2
    dic_return["sensor_moisture"] = (int)(data_dic["sensor_moisture_0"][0] + data_dic["sensor_moisture_1"][0] + data_dic["sensor_moisture_2"][0] + data_dic["sensor_moisture_3"][0]) / 4
    dic_return["sensor_temperature_inside"] = data_dic["sensor_temperature_inside"][0]
    dic_return["sensor_temperature_outside"] = data_dic["sensor_temperature_outside"][0] if data_dic["sensor_humidity_outside"][0] < 100 else "null"
    dic_return["sensor_humidity_inside"] = data_dic["sensor_humidity_inside"][0]
    dic_return["sensor_humidity_outside"] = data_dic["sensor_humidity_outside"][0] if data_dic["sensor_humidity_outside"][0] < 100 else "null"

    dic_return["light"] = "On" if data_dic["device_light"][0] else "Off"
    dic_return["waterpump"] = "On" if data_dic["device_waterpump"][0] else "Off"
    dic_return["fan0"] = "On" if data_dic["device_fan_0"][0] else "Off"
    dic_return["fan1"] = "On" if data_dic["device_fan_1"][0] else "Off"
    dic_return["humidifier"] = "On" if data_dic["device_humidifier"][0] else "Off"
    dic_return["heater"] = "On" if data_dic["device_heater"][0] else "Off"

    dic_return["light_24h"] = data_dic["sensor_light_0"]
    CO2_24h = data_dic["sensor_light_0"]
    CO2_24h_ = data_dic["sensor_light_1"]
    for i in range(len(CO2_24h)):
        CO2_24h[i] += CO2_24h_[i]
    dic_return["moisture_24h_0"] = data_dic["sensor_moisture_0"]
    dic_return["moisture_24h_1"] = data_dic["sensor_moisture_1"]
    dic_return["moisture_24h_2"] = data_dic["sensor_moisture_2"]
    dic_return["moisture_24h_3"] = data_dic["sensor_moisture_3"]
    dic_return["temperature_24h"] = data_dic["sensor_temperature_inside"]
    dic_return["humidity_24h"] = data_dic["sensor_humidity_inside"]

    sqlcmd = "select * from user_control order by id desc limit 48"
    df=pd.read_sql(sqlcmd,dbconn)
    controlInfo_dic = df.to_dict("list")

    sqlcmd = "select light from user_control order by id desc limit 48"
    df=pd.read_sql(sqlcmd,dbconn)
    light_controlInfo_dic = df.to_dict("list")["light"][0] == True

    sqlcmd = "select humidifier from user_control order by humidifier desc limit 48"
    df=pd.read_sql(sqlcmd,dbconn)
    humidifier_controlInfo_dic = df.to_dict("list")

    return render(request, 'testHTML.html', {"data_dic": dic_return, "controlInfo_dic":controlInfo_dic, "light_controlInfo_dic":light_controlInfo_dic, "humidifier_controlInfo_dic":humidifier_controlInfo_dic})