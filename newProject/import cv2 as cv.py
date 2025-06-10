# def scan_qr_code(request):
#     import cv2
#     import json  # For parsing JSON data

#     # Initialize the webcam (0 is usually the default camera)
#     cap = cv2.VideoCapture(0)

#     # Initialize the QR code detector
#     qr_code_detector = cv2.QRCodeDetector()

#     print("Press 'SPACE' to scan a QR code. Press 'q' to quit.")
#     total = 0

#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
        
#         if not ret:
#             print("Failed to grab frame. Exiting...")
#             break

#         # Display the current frame
#         cv2.imshow("QR Code Scanner", frame)

#         # Wait for a key press
#         key = cv2.waitKey(1) & 0xFF
        
#         # If 'SPACE' is pressed, scan for a QR code
#         if key == ord(' '):  # Spacebar key
#             data, vertices, _ = qr_code_detector.detectAndDecode(frame)
#             if data:
#                 try:
#                     # Parse the decoded data as JSON
#                     product_info = json.loads(data)
                    
#                     # Extract the price
#                     price = int(product_info.get("price", 0))  # Default to 0 if 'price' is not found
#                     total += price
#                     print(f"Decoded Data: {product_info}")
#                     print(f"Product Price: {price}")
#                     print(f"Current Total: {total}")

#                 except json.JSONDecodeError:
#                     print("Error: Decoded data is not in valid JSON format.")
#             else:
#                 print("No QR code detected. Please try again.")

#         # If 'q' is pressed, exit the loop
#         if key == ord('q'):
#             cap.release()
#             cv2.destroyAllWindows()
#             print(f"Final Total: {total}")
#             break
#             # return render(request, "dashboard.html", {"total": total})


import datetime

od = datetime.datetime.now()
od = str(od)
print(od)