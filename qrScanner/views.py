from importlib.metadata import pass_none

from django.shortcuts import redirect, render
from django.http import HttpResponse
import mysql.connector
import cv2
import winsound  # For sound feedback
import datetime
import qrcode
import base64
import io
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog


global ordid
global od
def db():
    od = datetime.datetime.now()
    od = str(od)
    # Establish database connection
    mydb = mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    database="project",
    )
    mycur = mydb.cursor()
    mycur.execute("insert into ordermast(orddate) values('"+od+"')")
    mydb.commit()
    mycur.execute("select max(ordid) from ordermast")
    mydata=mycur.fetchone()
    ordid=str(mydata[0])
    return ordid
    
def checkName():
    mydb = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="project",
    )
    mycur = mydb.cursor()
    mycur.execute("select max(ordid) from ordermast")
    mydata = mycur.fetchall()
    uname = str(mydata[2]) # user name
    print(uname)
    print(mydata)
    return uname

def get_quantity(product_name,qty):
    # Create the root window
    root = tk.Tk()
    root.title("Quantity Input")
    root.geometry("300x150")
    root.resizable(False, False)

    # Center the window on the screen
    root.eval('tk::PlaceWindow . center')

    # Variable to store the user's quantity input
    quantity_var = tk.IntVar()
    quantity_var.set(1)  # Default quantity

    # Variable to store the result
    result = {"quantity": None}

    # Function to handle submission
    def submit(event=None):  # Optional event argument to handle "Enter" key
        try:
            quantity = int(entry.get())

            if quantity > 0:
                if quantity <= qty:
                    quantity_var.set(quantity)  # Update the variable with the entered value
                    result["quantity"] = quantity
                    root.destroy()
                else:
                    msg = "Quantity insufficient, Available Quantity " +str(qty)
                    error_label.config(text=msg)
            else:
                error_label.config(text="Quantity must be greater than 0!")
        except ValueError:
            error_label.config(text="Please enter a valid number!")

    # Function to increment the quantity
    def increment(event=None):
        current_value = quantity_var.get()
        quantity_var.set(current_value + 1)
        error_label.config(text="")  # Clear any error messages

    # Function to decrement the quantity
    def decrement(event=None):
        current_value = quantity_var.get()
        if current_value > 1:
            quantity_var.set(current_value - 1)
            error_label.config(text="")  # Clear any error messages
        else:
            error_label.config(text="Quantity cannot be less than 1!")

    # Add a label
    label = tk.Label(
        root,
        text=f"How many {product_name} do you want to purchase?",
        font=("Arial", 12),
        wraplength=250,
        anchor="center",
    )
    label.pack(pady=10)

    # Add an entry box for quantity input
    entry = ttk.Entry(root, textvariable=quantity_var, font=("Arial", 14), justify="center")
    entry.pack(pady=5)
    entry.focus()  # Set focus to the entry field

    # Bind keys
    entry.bind("<Return>", submit)  # Submit on pressing Enter
    entry.bind("<Up>", increment)  # Increment on pressing Up Arrow
    entry.bind("<Down>", decrement)  # Decrement on pressing Down Arrow

    # Add a Submit button
    submit_button = ttk.Button(root, text="Submit", command=submit)
    submit_button.pack(pady=5)

    # Add an error label for validation messages
    error_label = tk.Label(root, text="", font=("Arial", 10), fg="red")
    error_label.pack()

    # Run the Tkinter main loop
    root.mainloop()

    return result["quantity"]

def qr_code_scanner(request):

    # get maximum order id from ordermast table, means get current order id
    ordid=db()
    # uname = str(checkName())

    # Establish database connection
    mydb = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="project",
    )
    mycur = mydb.cursor()
    

    # Initialize the webcam and QR code detector
    cap = cv2.VideoCapture(0)
    qr_code_detector = cv2.QRCodeDetector()

    print("Press 'SPACE' to scan a QR code. Press 'q' to quit.")
    total = 0
    products = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        cv2.imshow("QR Code Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # Spacebar key
            data, vertices, _ = qr_code_detector.detectAndDecode(frame)
            if data:
                try:
                    # Play sound feedback for successful scanning
                    winsound.Beep(1000, 400)  # Beep with 1000Hz frequency for 400ms
                    # Use eval carefully, ensure data is structured like a Python dict
                    product_info = eval(data)

                    # Extract required fields from the data
                    pid = int(product_info.get("product_id"))
                    pname= str(product_info.get("name"))
                    price = int(product_info.get("price"))

                    mydb.commit()

                    # get available quantity from pomast table
                    mycur.execute("SELECT quantity,rate FROM pomast WHERE pcode = %s", (str(pid),))
                    pentrys = mycur.fetchall()
                    tqty = 0
                    for entry in pentrys:
                        tqty = tqty + entry[0]
                        print(entry)

                    print(pid,pname,price)
                    print(tqty)

                    mycur.execute("SELECT quantity  FROM orderdetail WHERE pid = %s", (str(pid),))
                    selled_entrys = mycur.fetchall()
                    selled_qty = 0
                    for entry in selled_entrys:
                        selled_qty = selled_qty + entry[0]
                        print(entry)

                    tq = tqty - selled_qty

                    sqty = get_quantity(pname,tq)
                    if sqty is None:
                        print("Quantity input canceled or invalid. Skipping this product.")
                        continue

                    mycur.execute("SELECT MAX(rate) FROM pomast WHERE pcode="+str(pid)+" ")
                    max_price = mycur.fetchall()
                    print(max_price)
                    print(max_price[0])
                    print(max_price[0][0])
                    tpprice = sqty * int(max_price[0][0])

                    # list to store tuples of multiple products multiple rates and quantities
                    # pvaritys = []
                    # pvt = tuple()
                    #get quantity f+5959+5azrom entrys and check price

                    # This code is very powerful code. used to calculate amount of products per entry

                    # aqty = 0
                    # tpprice = 0
                    # tempsqty = sqty
                    # for entry in pentrys:
                    #     aqty += entry[0]
                    #     if selled_qty < aqty:
                    #         asqty = entry[0]
                    #         if tempsqty <= aqty - selled_qty:
                    #             # cqty = entry[0] - tempsqty
                    #             tpprice += int(tempsqty) * int(entry[1]) # multiply rate and selling quantity from pomast table to calculate total of those products
                    #             break;
                    #         else:
                    #             tempsqty = tempsqty - (aqty-selled_qty)
                    #             tpprice += int(aqty-selled_qty) * int(entry[1])
                    #             selled_qty =  selled_qty + int(aqty - selled_qty)


                    # calculate new quantity
                    # nqty = tqty - sqty

                    # mycur.execute("UPDATE products SET quantity="+str(nqty)+" WHERE pid='"+str(pid)+"' ") # update quantity in products table

                    # Update totals
                    ptotal = int(tpprice) # calculate total of the Products Scanned Currently

                    total += ptotal
                    products += sqty

                    # Insert data into the database
                    mycur.execute(" INSERT INTO orderdetail(oid,pid,pname,price,quantity,total)  VALUES ('"+str(ordid)+"','"+str(pid)+"','"+pname+"','"+str(max_price[0][0])+"',"+str(sqty)+","+str(ptotal)+")")
                    mydb.commit()

                    # Visual feedback: Draw a green bounding box
                    if vertices is not None:
                        vertices = vertices.astype(int)
                        for i in range(len(vertices[0])):
                            pt1 = tuple(vertices[0][i])
                            pt2 = tuple(vertices[0][(i + 1) % len(vertices[0])])
                            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)  # Green box

                    # Display product information on the frame
                    cv2.putText(
                        frame,
                        f"Scanned: {pname} - Rs.{price}",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

                    # print(product_info)
                    print(f"Decoded Data: {product_info}")
                    print(f"Product Price: {price}")
                    print(f"Current Total: {total}")

                except Exception as e:
                    print(f"Error processing QR code data: {e}")
            else:
                # If no QR code is detected, provide visual feedback with a red box
                cv2.putText(
                    frame,
                    "No QR Code Detected!",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
                print("No QR code detected. Please try again.")

        # Display the updated frame with feedback
        cv2.imshow("QR Code Scanner", frame)

        if key == ord('q'):  # Exit on 'q'
            cap.release()
            cv2.destroyAllWindows()

            # fetch all products from the database
            mycur = mydb.cursor()
            mycur.execute(f"SELECT * FROM orderdetail where oid = "+ordid+" ")
            # mydb.commit()
            orderdetail = mycur.fetchall()


            # calculate final amount
            discount = 20
            damount = float(total * (discount/100))
            net_amount = total - damount


            # mycur.execute("UPDATE `ordermast` SET `amount`='"+str(total)+"',`discount`='"+str(discount)+"',`netamount`='"+str(net_amount)+"' WHERE `ordid`='"+str(ordid)+"'")

            # mydb.commit()
            
            # Close the database connection
            mycur.close()
            mydb.close()

            od = datetime.datetime.now()
            od = str(od)
        
            # QR Code for Payment of Purchasing order    
            # print(f"Final Total: {ftotal}")
            return render(
                request,
                "dashboard.html",{"total": total,"discount":discount,"damount":damount,"final_amount":net_amount,"products": products,"orderdetail":orderdetail,"date":od,"ordid":ordid},
            )

def update_bill(request):

    if request.method == "POST":
        mydb = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="project",
        )

        mycur = mydb.cursor()

        uname = request.POST["uname"]
        ordid = request.POST["ordid"]
        total = request.POST["total"]
        damount = request.POST["damount"]
        final_amount = request.POST["final_amount"]

        mycur.execute("UPDATE `ordermast` SET  `uname`= '" +str(uname)+ "',`amount`='" + str(total) + "',`discount`='" + str(damount) + "',`netamount`='" + str(final_amount) + "' WHERE `ordid`='" + str(ordid) + "'  ")
        mydb.commit()

        mycur.execute("select b.ordid,b.orddate,b.uname,b.amount,b.discount, b.netamount,b1.oid,b1.pid,b1.pname,b1.price,b1.quantity,b1.total from ordermast b ,orderdetail b1 where b.ordid=b1.oid and b.ordid=(select max(ordid) from ordermast)")
        mydata = mycur.fetchall()
        mydb.commit()
        # mydb.close()
        print(mydata)
        current_time = datetime.datetime.now().strftime("%H:%M")
        # return HttpResponse("Done")
        return render(request,"userBill.html", {"data": mydata,"uname":uname,"ordid":ordid,"total":total,"damount":damount,"final_amount":final_amount,"current_time":current_time})



def cancel_bill(request):

    mydb = mysql.connector.connect(
        user = "root",
        password = "",
        host = "localhost",
        database = "project"
    )
    mycur = mydb.cursor()

    mycur.execute("SELECT MAX(oid) FROM orderdetail ")
    oid = mycur.fetchone()
    mycur.execute("SELECT * FROM orderdetail WHERE oid='" +str(oid[0])+ "' ")
    qty_list = mycur.fetchall()

    for product in qty_list:
        qty = product[4]
        mycur.execute("SELECT quantity FROM products WHERE pid = '"+str(product[1])+"' ")
        pqty = mycur.fetchone()[0]
        oldqty = int(qty) + int(pqty)
        mycur.execute("UPDATE products SET quantity=" + str(oldqty) + " WHERE pid = " +str(product[1])+ " ")
        mydb.commit()
    mycur.execute("DELETE  from orderdetail where oid='"+str(oid[0])+"' ")
    mydb.commit()
    return render(request, "dashboard.html", {"message": "Bill canceled successfully!"})
