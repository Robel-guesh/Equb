import cv2
try:
    def decode_qr(frame):
        # Initialize the QRCode detector
        detector = cv2.QRCodeDetector()
        # Detect and decode the QR code
        data, vertices, _ = detector.detectAndDecode(frame)
        return data

    def scan_qrcode():
        # Open a connection to the webcam
        cap = cv2.VideoCapture(0)
        qr_data = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Decode QR codes in the frame
            qr_data = decode_qr(frame)
            
            # Display the frame
            cv2.imshow("QR Code Scanner", frame)
            
            # Exit if QR code data is found
            if qr_data:
                break
            
            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the webcam and close windows
        cap.release()
        cv2.destroyAllWindows()
        
        return qr_data

##    if __name__ == "__main__":
##        qr_code_data = scan_qrcode()
##        if qr_code_data:
##            return(qr_code_data)
except:
    pass
##        print(f"QR Code Data: {qr_code_data}")
