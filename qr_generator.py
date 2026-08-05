"""
QR Code Generator
Generates QR codes for URLs
"""

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
    
    def generate_qr(self, url, filename=None):
        """Generate QR code from URL"""
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)
        
        img = self.qr.make_image(fill_color="black", back_color="white")
        
        if filename:
            img.save(filename)
            return filename
        else:
            # Return as bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            return img_bytes.getvalue()
    
    def generate_qr_with_logo(self, url, logo_path=None, filename=None):
        """Generate QR code with logo in center"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Add logo if provided
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                
                # Calculate logo size (20% of QR code)
                qr_width, qr_height = img.size
                logo_size = int(qr_width * 0.2)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Position logo in center
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                img.paste(logo, pos)
            except Exception as e:
                print(f"Logo paste error: {e}")
        
        if filename:
            img.save(filename)
            return filename
        else:
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            return img_bytes.getvalue()