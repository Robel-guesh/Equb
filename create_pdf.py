from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# Function to generate QR Code
def generate_qr_code(id_number):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(id_number)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_path = "qr_code.png"
    img.save(img_path)
    return img_path

# Function to create PDF with badge details
def create_pdf(company_name, id_number, full_name, phone_number, profile_photo):
    
    photo_path = profile_photo
    if not company_name or not phone_number or not profile_photo or not id_number or not full_name:
        messagebox.showerror("Missing Data", "Please fill in all fields and upload a photo.")
        return

    # Register a font that supports Unicode (DejaVuSans)
    pdfmetrics.registerFont(TTFont('GeezAble', './font/GeezAble.ttf'))  # Use the correct path to your TTF font file
    
    # Generate QR code
    qr_path = generate_qr_code(id_number)

    # Create the PDF
    pdf_path = "badge.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Set a font that supports Unicode characters
    c.setFont("GeezAble", 20)
    text_width = c.stringWidth(company_name, "GeezAble", 20)
    x_position = (width - text_width) / 2
    c.drawString(x_position, height - 50, f"{company_name}")

    
    # Add company name
##    c.drawString(200, height - 50, f"{company_name}")

    # Add photo
    img = Image.open(photo_path)
    img_path = photo_path
    c.drawImage(img_path, 50, height - 120, width=100, height=100)

    # Add QR code
    c.drawImage(qr_path, 50, height - 220, width=100, height=100)

    # Add name and phone number
    c.setFont("GeezAble", 14)
    c.drawString(200, height - 70, f"Id: {id_number}")
    c.drawString(200, height - 90, f"Full Name: {full_name}")
    c.drawString(200, height - 110, f"Phone: {phone_number}")

    # Save PDF
    c.save()

    # Inform user
##    messagebox.showinfo("PDF Created", f"Badge PDF saved as {pdf_path}")

# Example of usage
##create_pdf('MOYA EQUB', '1', 'ሮቤል', '0943667642', 'logo.png')
