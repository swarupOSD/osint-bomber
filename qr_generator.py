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
        Generate QR code from URL and return as bytes (in-memory)
        No file saving required - perfect for Streamlit Cloud
        """
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)
        
        img = self.qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes (in-memory)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    
    def generate_qr_with_logo(self, url, logo_path=None):
        """
        Generate QR code with center logo and return as bytes
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Add logo if provided and exists
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.2)  # Logo size = 20% of QR code
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Position logo in center
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                img.paste(logo, pos)
            except Exception:
                pass  # If logo fails, just return QR without logo
        
        # Convert to bytes (in-memory)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    
    def generate_qr_from_text(self, text):
        """
        Generate QR code from any text and return as bytes
        (Alias for generate_qr)
        """
        return self.generate_qr(text)