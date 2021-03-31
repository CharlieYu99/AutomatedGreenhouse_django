from django.http import HttpResponse
from django.shortcuts import render

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
    sqlcmd = "select * from test order by id desc limit 1"
    df=pd.read_sql(sqlcmd,dbconn)
    data_dic = df.to_dict("list")
    return render(request, 'testHTML.html', {"data_dic": data_dic})

def runoob(request):
    views_dict = {"name":"菜鸟教程"}
    return render(request, 'runoob.html', {"views_dict": views_dict})
