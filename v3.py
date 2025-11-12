#!/usr/bin/env python3
"""
PDF Steganography Tool
Hide and extract secret messages in PDF files
"""

import argparse
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
import zlib
import base64

# Fix the email import issue
try:
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
except ImportError as e:
    print(f"Email import error: {e}")
    sys.exit(1)

class PDFSteganography:
    def __init__(self):
        self.metadata_key = "/Keywords"
    
    def hide_message(self, pdf_path, message, output_path=None):
        """
        Hide a message in PDF metadata
        """
        try:
            # Read the original PDF
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Encode the message
            encoded_message = base64.b64encode(
                zlib.compress(message.encode('utf-8'))
            ).decode('utf-8')
            
            # Add metadata with hidden message
            writer.add_metadata({
                self.metadata_key: encoded_message,
                "/Producer": "PDF Steganography Tool",
                "/Title": "Document"
            })
            
            # Set output path
            if output_path is None:
                base_name = os.path.splitext(pdf_path)[0]
                output_path = f"{base_name}_hidden.pdf"
            
            # Save the new PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"Message hidden successfully in: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error hiding message: {e}")
            return None
    
    def extract_message(self, pdf_path):
        """
        Extract hidden message from PDF metadata
        """
        try:
            reader = PdfReader(pdf_path)
            metadata = reader.metadata
            
            if self.metadata_key in metadata:
                encoded_message = metadata[self.metadata_key]
                
                # Decode the message
                decoded_message = zlib.decompress(
                    base64.b64decode(encoded_message)
                ).decode('utf-8')
                
                return decoded_message
            else:
                print("No hidden message found in PDF metadata")
                return None
                
        except Exception as e:
            print(f"Error extracting message: {e}")
            return None
    
    def hide_in_text(self, pdf_path, message, output_path=None):
        """
        Advanced: Hide message in PDF text content (basic implementation)
        """
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            # Simple text-based steganography
            # This is a basic implementation - real implementation would be more sophisticated
            encoded_message = base64.b64encode(message.encode()).decode()
            
            for page in reader.pages:
                writer.add_page(page)
            
            # Add message as custom metadata
            writer.add_metadata({
                "/HiddenData": encoded_message,
                "/Producer": "Advanced PDF Steganography"
            })
            
            if output_path is None:
                base_name = os.path.splitext(pdf_path)[0]
                output_path = f"{base_name}_advanced_hidden.pdf"
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"Advanced message hidden in: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error in advanced hiding: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='PDF Steganography Tool')
    parser.add_argument('action', choices=['hide', 'extract', 'hide_advanced'], 
                       help='Action to perform')
    parser.add_argument('--input', '-i', required=True, help='Input PDF file')
    parser.add_argument('--output', '-o', help='Output PDF file')
    parser.add_argument('--message', '-m', help='Message to hide')
    
    args = parser.parse_args()
    
    stego = PDFSteganography()
    
    if args.action == 'hide':
        if not args.message:
            print("Error: Message is required for hide action")
            sys.exit(1)
        
        result = stego.hide_message(args.input, args.message, args.output)
        if not result:
            sys.exit(1)
    
    elif args.action == 'hide_advanced':
        if not args.message:
            print("Error: Message is required for hide_advanced action")
            sys.exit(1)
        
        result = stego.hide_in_text(args.input, args.message, args.output)
        if not result:
            sys.exit(1)
    
    elif args.action == 'extract':
        message = stego.extract_message(args.input)
        if message:
            print(f"Extracted message: {message}")
        else:
            sys.exit(1)

def test_functionality():
    """
    Test the PDF steganography functionality
    """
    print("Testing PDF Steganography...")
    
    # Create a simple test PDF first (you'll need an existing PDF file)
    test_pdf = "test.pdf"
    
    # If test PDF doesn't exist, create a simple one
    if not os.path.exists(test_pdf):
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            c = canvas.Canvas(test_pdf, pagesize=letter)
            c.drawString(100, 750, "Test PDF for Steganography")
            c.drawString(100, 730, "This is a test document.")
            c.save()
            print("Created test PDF file")
        except ImportError:
            print("ReportLab not installed. Please provide an existing PDF file.")
            return
    
    stego = PDFSteganography()
    
    # Test hiding message
    test_message = "This is a secret message!"
    print(f"Hiding message: {test_message}")
    
    output_pdf = stego.hide_message(test_pdf, test_message, "test_hidden.pdf")
    
    if output_pdf:
        # Test extracting message
        extracted = stego.extract_message(output_pdf)
        if extracted:
            print(f"Extracted message: {extracted}")
            if extracted == test_message:
                print("✓ Test passed! Message successfully hidden and extracted.")
            else:
                print("✗ Test failed! Extracted message doesn't match.")
        else:
            print("✗ Failed to extract message")
    else:
        print("✗ Failed to hide message")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run test
        test_functionality()
    else:
        main()
