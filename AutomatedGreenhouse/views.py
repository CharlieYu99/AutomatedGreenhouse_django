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

# smart plug libraries
from .smartplug import SmartPlug
from .Reco4lifeP10A import on
from .Reco4lifeP10A import off
 
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

    dic_return["light"] = "On" if data_dic["device_light"][0] == 1 else "Off"
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
    dic_return["CO2_24h"] = CO2_24h
    dic_return["moisture_24h_0"] = data_dic["sensor_moisture_0"]
    dic_return["moisture_24h_1"] = data_dic["sensor_moisture_1"]
    dic_return["moisture_24h_2"] = data_dic["sensor_moisture_2"]
    dic_return["moisture_24h_3"] = data_dic["sensor_moisture_3"]
    dic_return["temperature_24h"] = data_dic["sensor_temperature_inside"]
    dic_return["humidity_24h"] = data_dic["sensor_humidity_inside"]

    return render(request, 'testHTML.html', {"data_dic": dic_return})


def runoob(request):
    views_dict = {"name":"菜鸟教程"}
    return render(request, 'runoob.html', {"views_dict": views_dict})


# def camera(request):
#         return render(request,'camera.html')  


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
    elif 'button_light_off' in request.POST:
        Light0.off()
    elif 'button_waterpump_on' in request.POST:
        device_control_single(Pump,10)
    elif 'button_humidifier_on_strong' in request.POST:
        device_control_single(Humidifier,60*30,30,30)
    elif 'button_humidifier_on_weak' in request.POST:
        device_control_single(Humidifier,60*30,30,30)
    elif 'button_heeter_on_strong' in request.POST:
        device_control_single(Heater,60*30,30,150)
    elif 'button_humidifier_on_weak' in request.POST:
        device_control_single(Heater,60*30,30,90)

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

    dic_return["light"] = "On" if data_dic["device_light"][0] == 1 else "Off"
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
    dic_return["CO2_24h"] = CO2_24h
    dic_return["moisture_24h_0"] = data_dic["sensor_moisture_0"]
    dic_return["moisture_24h_1"] = data_dic["sensor_moisture_1"]
    dic_return["moisture_24h_2"] = data_dic["sensor_moisture_2"]
    dic_return["moisture_24h_3"] = data_dic["sensor_moisture_3"]
    dic_return["temperature_24h"] = data_dic["sensor_temperature_inside"]
    dic_return["humidity_24h"] = data_dic["sensor_humidity_inside"]

    temp24h = data_dic["sensor_temperature_inside"]
    temp_24h = []
    for i in range(int(len(temp24h)/2)):
        temp_24h.append([24-i,temp24h[i*2]])
        


    return render(request, 'ControlPanel.html', {"data_dic": dic_return, "temp_list": json.dumps(temp_24h)})

def index(request):
    return render(request, 'index.html')




# def ButtonActions(request):

#     if 'button_light_on' in request.POST:
#         Light0.on()
#     elif 'button_light_off' in request.POST:
#         Light0.off()
#     elif 'button_waterpump_on' in request.POST:
#         device_control_single(Pump,10)

#     dbconn=pymysql.connect(
#     host="localhost",
#     database="GreenhouseDB",
#     user="Greenhouseadmin",
#     password="adminpassword",
#     port=3306,
#     charset='utf8'
#     )
    
#     # read the latest data
#     sqlcmd = "select * from experiment_data order by id desc limit 1"
#     df=pd.read_sql(sqlcmd,dbconn)
#     data_dic = df.to_dict("list")
#     return render(request, 'ControlPanel.html', {"data_dic": data_dic})

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


        