from operator import length_hint

from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from mysql.connector import Error
import qrcode
from io import BytesIO
import base64

from records.views import totalProducts



def lengthOfCustomers():
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost",
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM `ordermast` WHERE netamount IS NOT NULL")
    customers = mycur.fetchall()
    return len(customers)

def lengthOfPRoducts():
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost",
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM `products`")
    products = mycur.fetchall()
    return len(products)

def lengthOfPurchasedOrders():
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost",
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM `pomast`")
    orders = mycur.fetchall()
    return len(orders)

def lengthOfBills():
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost",
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM `ordermast` WHERE netamount IS NOT NULL")
    bills = mycur.fetchall()
    return len(bills)

def lengthOfOrderDetails():
    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        database = "project",
        host = "localhost",
    )
    mycur = mydb.cursor()
    mycur.execute("SELECT * FROM `orderdetail` ")
    orderDetails = mycur.fetchall()
    return len(orderDetails)



# Create your views here.

def home(request):
    if 'uid' not in request.session:
        return render(request,"index.html")
    return render(request, "index.html")


def dashboard(request):
    # Check if the user is logged in
    if 'uid' not in request.session:
        return redirect('login')  # Redirect to the login page if not logged in

    # Create a context dictionary
    context = {
        "boxes": "record boxes",
        "totalCustomers": lengthOfCustomers(),
        "totalProducts": lengthOfPRoducts(),
        "totalPurchasedOrders": lengthOfPurchasedOrders(),
        "totalBills": lengthOfBills(),
        "totalOrderDetails": lengthOfOrderDetails(),
        "brand_name": "Jayesh Supershop"
    }
    return render(request, "dashboard.html", context)


# def dashboard(request):
#     # Check if the user is logged in
#     if 'uid' not in request.session:
#         return redirect('login')  # Redirect to the login page if not logged in
#
#     return render(request, "dashboard.html",
#                   {"boxes": "record boxes", "totalCustomers": lengthOfCustomers(), "totalProducts": lengthOfPRoducts(),
#                    "totalPurchasedOrders": lengthOfPurchasedOrders(), "totalBills": lengthOfBills(),
#                    "totalOrderDetails": lengthOfOrderDetails(),"brand_name":"Jayesh Supershop"})  # Redirect to the dashboard


def login(request):
    try:
        if request.method == "POST":
            uid = request.POST.get("uid")
            upass = request.POST.get("upass")

            if not uid or not upass:
                return HttpResponse("<h1><font color='red'><i>Missing user ID or password</i></font></h1>")

            # Connect to the database
            mydb = mysql.connector.connect(
                user="root",
                password="",
                host="localhost",
                database="project"
            )
            mycur = mydb.cursor()

            # Use parameterized query to prevent SQL injection
            query = "SELECT id, password FROM usermast WHERE id = %s"
            mycur.execute(query, (uid,))
            user = mycur.fetchone()
            mycur.close()
            mydb.close()
            if user is None:
                return HttpResponse("<h1><font color='red'><i>Unauthorized access</i></font></h1>")

            # Verify password
            if user[0] == uid and user[1] == upass:
                request.session['uid'] = user[0]  # Set session for the logged-in user
                return render(request,"dashboard.html",{"boxes":"record boxes","totalCustomers":lengthOfCustomers(),"totalProducts":lengthOfPRoducts(),"totalPurchasedOrders":lengthOfPurchasedOrders(),"totalBills":lengthOfBills(),"totalOrderDetails":lengthOfOrderDetails(),"brand_name":"Jayesh Supershop"})  # Redirect to the dashboard
            else:
                return HttpResponse("<h1><font color='red'><u>Invalid user ID or password</u></font></h1>")
        else:
            return render(request, "login.html")  # Render the login page for GET requests

    except Error as e:
        return HttpResponse(f"<h1><font color='red'>Database Error: {str(e)}</font></h1>")
    except Exception as e:
        return HttpResponse(f"<h1><font color='red'>Error: {str(e)}</font></h1>")
    finally:
        if 'mycur' in locals() and mycur:
            mycur.close()
        if 'mydb' in locals() and mydb.is_connected():
            mydb.close()

def add_product_form(request):
    if 'uid' not in request.session:
        return redirect('login')  # Redirect to login if the user is not authenticated

    return render(request, "dashboard.html", {"form": "form for add product"})

def add_product(request):
    if 'uid' not in request.session:
        return redirect('login')  # Redirect to login if the user is not authenticated

    if request.method == "POST":
        # Get form data
        pname = request.POST.get("pname")
        pdesc = request.POST.get("pdesc")
        price = request.POST.get("price")

        mydb = mysql.connector.connect(
            user="root",
            password="",
            database="project",
            host="localhost",
        )
        cursor = mydb.cursor()

        cursor.execute("SELECT pname FROM products WHERE pname=%s", (pname,))
        product = cursor.fetchone()
        if product:
            return HttpResponse("Product already Available!!")
        else:
            cursor.execute(
                "INSERT INTO products(pname, price, pdesc) VALUES (%s, %s, %s)",
                (pname, price, pdesc),
            )
            mydb.commit()
        cursor.execute("SELECT MAX(pid) FROM products")
        pid = cursor.fetchone()[0]
        print(pid)
        # Generate QR Code
        data = {
            "product_id": pid,
            "name": pname,
            "description": pdesc,
            "price": price,
        }
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        # Save QR Code to Memory
        qr_image = BytesIO()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_image, format="PNG")
        qr_image.seek(0)

        # Convert QR Code to Base64 for Embedding
        qr_code_base64 = base64.b64encode(qr_image.getvalue()).decode("utf-8")
        mydb.close()

        # Pass the QR Code and Form to Dashboard
        return render(request, "dashboard.html", {
            "qr_code": qr_code_base64,
            "pid": pid,
            "pname": pname,
            "pdesc": pdesc,
            "price": price,
        })
    else:
        return HttpResponse("Invalid method. Please use POST Method!")

def logout(request):
    request.session.flush()
    return redirect('login')