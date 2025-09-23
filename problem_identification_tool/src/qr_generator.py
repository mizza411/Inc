#!/usr/bin/env python3
"""
QR Code Generator for Problem Identification Tool
Creates QR codes for easy questionnaire sharing
"""

import qrcode
import argparse
import os
from datetime import datetime
from urllib.parse import urlencode

class QRCodeGenerator:
    def __init__(self, base_url="https://yoursite.com", output_dir="qr_codes"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_qr(self, url, filename=None, context="general"):
        """Generate QR code for a given URL"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"questionnaire_{context}_{timestamp}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
        
        return filepath
    
    def generate_contextual_qrs(self, questionnaire_path="/web/index.html"):
        """Generate QR codes for different sharing contexts"""
        base_url = f"{self.base_url}{questionnaire_path}"
        
        contexts = {
            "business_cards": {
                "url": f"{base_url}?source=business_card",
                "filename": "qr_business_card.png"
            },
            "posters": {
                "url": f"{base_url}?source=poster",
                "filename": "qr_poster.png"
            },
            "social_media": {
                "url": f"{base_url}?source=social",
                "filename": "qr_social_media.png"
            },
            "email_signature": {
                "url": f"{base_url}?source=email",
                "filename": "qr_email_signature.png"
            },
            "events": {
                "url": f"{base_url}?source=event",
                "filename": "qr_event.png"
            }
        }
        
        generated_files = []
        
        for context, config in contexts.items():
            filepath = self.generate_qr(
                config["url"], 
                config["filename"], 
                context
            )
            generated_files.append({
                "context": context,
                "filepath": filepath,
                "url": config["url"]
            })
            print(f"Generated QR code for {context}: {filepath}")
        
        return generated_files
    
    def generate_utm_qr(self, utm_source, utm_medium, utm_campaign, questionnaire_path="/web/index.html"):
        """Generate QR code with UTM tracking parameters"""
        base_url = f"{self.base_url}{questionnaire_path}"
        
        utm_params = {
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
            "utm_content": "qr_code"
        }
        
        url_with_utm = f"{base_url}?{urlencode(utm_params)}"
        
        filename = f"qr_utm_{utm_source}_{utm_medium}_{utm_campaign}.png"
        filepath = self.generate_qr(url_with_utm, filename, "utm_tracked")
        
        return {
            "filepath": filepath,
            "url": url_with_utm,
            "utm_params": utm_params
        }

def main():
    parser = argparse.ArgumentParser(description="Generate QR codes for questionnaire sharing")
    parser.add_argument("--url", default="https://yoursite.com", help="Public site base URL, e.g., https://mysite.netlify.app")
    parser.add_argument("--path", default="/web/index.html", help="Questionnaire path on site (default: /web/index.html). Use '/' for root index.html")
    parser.add_argument("--output", default="qr_codes", help="Output directory for QR codes")
    parser.add_argument("--context", choices=["all", "business_cards", "posters", "social_media", "email_signature", "events"], 
                       default="all", help="Context for QR code generation")
    parser.add_argument("--utm-source", help="UTM source parameter")
    parser.add_argument("--utm-medium", help="UTM medium parameter")
    parser.add_argument("--utm-campaign", help="UTM campaign parameter")
    
    args = parser.parse_args()
    
    generator = QRCodeGenerator(args.url, args.output)
    
    if args.utm_source and args.utm_medium and args.utm_campaign:
        # Generate UTM-tracked QR code
        result = generator.generate_utm_qr(args.utm_source, args.utm_medium, args.utm_campaign)
        print(f"UTM-tracked QR code generated: {result['filepath']}")
        print(f"URL: {result['url']}")
    elif args.context == "all":
        # Generate all contextual QR codes
        results = generator.generate_contextual_qrs(args.path)
        print(f"\nGenerated {len(results)} QR codes in {args.output}/")
        for result in results:
            print(f"- {result['context']}: {result['filepath']}")
    else:
        # Generate single context QR code
        base_url = f"{args.url.rstrip('/')}{args.path}"
        url = f"{base_url}?source={args.context}"
        filepath = generator.generate_qr(url, context=args.context)
        print(f"QR code generated: {filepath}")

if __name__ == "__main__":
    main()
