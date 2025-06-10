from django.shortcuts import render
import mysql.connector
# Create your views here.

def plist(request):
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost"
    )

    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM products")
    products_data = mycur.fetchall()
    mydb.close()
    return render(request,"dashboard.html",{"pdata":products_data})
