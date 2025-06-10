from django.shortcuts import render
import mysql.connector
# Create your views here.

def orderlist(request):
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        host = "localhost",
        database = "project"
    )

    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM ordermast order by ordid")
    orderlist = mycur.fetchall()

    totalOrders = 0
    total = 0
    for order in orderlist:
        totalOrders += 1
        if order[5] is None:
            continue
        else:
            total = total + order[5]
    return render(request,"dashboard.html",{"orderlist":orderlist,"totalOrders":totalOrders,"Total":total})

def orderdetails(request):
    mydb = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="project"
    )

    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM orderdetail order by oid")
    orderdetails = mycur.fetchall()
    totalOrders = 0
    total = 0
    for order in orderdetails:
        totalOrders+=1
        total = total + order[5]

    return render(request, "dashboard.html", {"orderdetails": orderdetails,"totalOrders":totalOrders,"Total":total})


def showDetails(request):
    oid = str(request.POST["ordid"])

    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        host = "localhost",
        database = "project"
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM orderdetail WHERE oid = '"+oid+"' ")
    details = mycur.fetchall()
    print(oid)
    print(details)
    mydb.commit()
    mydb.close()
    return render(request,"details.html",{"details":details})