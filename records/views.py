from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
# Create your views here.

def customers(request):
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost"
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT uname,netamount FROM ordermast")
    data = mycur.fetchall()
    print(data)
    return render(request,"customers.html",{"data":data})


def totalProducts(request):
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost"
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * from products")
    products = mycur.fetchall()
    print(products)
    return render(request,"dashboard.html",{"products":products})

