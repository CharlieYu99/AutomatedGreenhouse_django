from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render

from .camera import Camera

import pandas as pd
import pymysql
 
def hello(request):
    return HttpResponse("Hello world ! ")

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
    sqlcmd = "select * from experiment_data order by id desc limit 1"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")
    return render(request, 'testHTML.html', {"data_dic": data_dic})

def runoob(request):
    views_dict = {"name":"菜鸟教程"}
    return render(request, 'runoob.html', {"views_dict": views_dict})

def video_feed(request):
        """
        视频流路由。将其放入img标记的src属性中。
        例如：<img src='http://your_ip:port/camera/video_feed/' >
        """
        # 此处应用使用StreamingHttpResponse，而不是用HttpResponse
        return StreamingHttpResponse(gen(Camera()),
                                        content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
        #此处的模板请自行创建 例如:<html><body><img src='http://your_ip:port/camera/video_feed/' >
        return render(request,'camera.html')  

def gen(camera):
        """视频流生成器功能。"""
        while True:
                frame = camera.get_frame()
                yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def ControlPanel(request):

    dbconn=pymysql.connect(
    host="localhost",
    database="GreenhouseDB",
    user="Greenhouseadmin",
    password="adminpassword",
    port=3306,
    charset='utf8'
    )
    
    # read the latest data
    sqlcmd = "select * from experiment_data order by id desc limit 1"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")
    return render(request, 'ControlPanel.html', {"data_dic": data_dic})