
from django.shortcuts import redirect, render
from django.http import HttpResponse
import mysql.connector
import datetime

from app1.views import dashboard


# Create your views here.
def purchase_entry_form(request):
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        host = "localhost",
        database = "project",
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT pid FROM products ")
    pids = mycur.fetchall()
    mydb.commit()
    mycur.close()
    return render(request,"dashboard.html",{"pids":pids})

def purchase_entry(request):
    supplier_name = request.POST.get("supplier_name")
    pcode = request.POST.get("pocode")
    quantity = request.POST.get("quantity")
    rate = request.POST.get("rate")
    print(rate)
    print(quantity)
    print(pcode)
    print(supplier_name)
    # if len(pcode)>=1:
    po_date = datetime.datetime.now()
    po_date = str(po_date)
    print(quantity)
    amount = int(quantity) * int(rate)
    amount = int(amount)
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        host = "localhost",
        database = "project"
    )

    print(pcode)
    mycur = mydb.cursor()

    mycur.execute(
        "INSERT INTO pomast(date, supplier_name, pcode, quantity, rate, amount) VALUES (%s, %s, %s, %s, %s, %s)",
        (po_date, supplier_name, pcode, quantity, rate, amount)
    )

    mydb.commit()


    mycur.close()
    return redirect('dashboard')


def purchase_details(request):
    mydb = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="project"
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * from pomast ")
    purchase_details = mycur.fetchall()
    return render(request,"dashboard.html",{"purchase_details":purchase_details})
