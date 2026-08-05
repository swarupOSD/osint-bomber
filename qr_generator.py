# qr_generator.py
import qrcode
from PIL import Image
import io
import os

class QRGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    
    def generate_qr(self, url):
        """
        Generate QR code from URL and return as PIL Image object
        """
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)
        
        img = self.qr.make_image(fill_color="black", back_color="white")
        return img  # PIL Image object
    
    def get_qr_bytes(self, url):
        """
        Generate QR code and return as bytes (for download)
        """
        img = self.generate_qr(url)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    
    def generate_qr_with_logo(self, url, logo_path=None):
        """
        Generate QR code with center logo and return as PIL Image object
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.2)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                img.paste(logo, pos)
            except Exception:
                pass
        
        return img
    
    def get_qr_bytes_with_logo(self, url, logo_path=None):
        """
        Generate QR code with logo and return as bytes (for download)
        """
        img = self.generate_qr_with_logo(url, logo_path)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()