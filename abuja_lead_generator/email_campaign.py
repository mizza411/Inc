"""
Email Campaign Module
=====================

Handles email campaign management and automation.
"""

import time
import random
from typing import List, Dict, Any
from .database_manager import DatabaseManager
from .config_manager import ConfigManager
import logging

logger = logging.getLogger(__name__)

class EmailCampaign:
    """Manages email campaigns"""
    
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
    
    def run_campaign(self) -> Dict[str, Any]:
        """Run email campaign"""
        if not self.config.get('email.enabled', True):
            logger.info("Email campaigns are disabled")
            return {'emails_sent': 0, 'errors': []}
        
        logger.info("Starting email campaign management...")
        
        emails_sent = []
        errors = []
        
        try:
            # Get leads with email addresses
            leads = self.db.get_leads(status='new', limit=100)
            
            for lead in leads:
                if not lead['email']:
                    continue
                
                try:
                    # Select random subject template
                    subject_templates = self.config.get('email.subject_templates', [])
                    if not subject_templates:
                        continue
                        
                    subject_template = random.choice(subject_templates)
                    subject = subject_template.replace("{business_name}", lead['name'])
                    
                    # Create email content
                    email_content = self.create_email_content(lead)
                    
                    # PROMPT USER BEFORE SENDING
                    print(f"\n📧 Email Preview:")
                    print(f"To: {lead['name']} ({lead['email']})")
                    print(f"Industry: {lead['industry']}")
                    print(f"Location: {lead['location']}")
                    print(f"Subject: {subject}")
                    print(f"Content Preview: {email_content[:150]}...")
                    print(f"\nOptions:")
                    print("1. Send this email")
                    print("2. Skip this lead")
                    print("3. Edit subject")
                    print("4. Edit content")
                    print("5. Stop automation")
                    
                    while True:
                        choice = input("\nEnter your choice (1-5): ").strip()
                        
                        if choice == '1':
                            # Send the email
                            logger.info(f"Sending email to {lead['name']}: {subject}")
                            
                            email_data = {
                                'lead_id': lead['id'],
                                'lead_name': lead['name'],
                                'email': lead['email'],
                                'subject': subject,
                                'content': email_content,
                                'timestamp': time.time()
                            }
                            
                            emails_sent.append(email_data)
                            
                            # Update lead status
                            self.db.update_lead_status(lead['id'], 'emailed')
                            
                            # Add contact log
                            self.db.add_contact_log(
                                lead['id'], 
                                'Email', 
                                f"Subject: {subject}\n\n{email_content[:200]}..."
                            )
                            
                            print(f"✅ Email sent to {lead['name']}")
                            break
                            
                        elif choice == '2':
                            # Skip this lead
                            print(f"⏭️  Skipped {lead['name']}")
                            break
                            
                        elif choice == '3':
                            # Edit subject
                            print(f"\nCurrent subject: {subject}")
                            new_subject = input("Enter new subject (or press Enter to keep current): ").strip()
                            if new_subject:
                                subject = new_subject
                            print(f"📝 Subject updated")
                            continue
                            
                        elif choice == '4':
                            # Edit content
                            print(f"\nCurrent content preview: {email_content[:200]}...")
                            print("Enter new content (or press Enter to keep current):")
                            new_content = input().strip()
                            if new_content:
                                email_content = new_content
                            print(f"📝 Content updated")
                            continue
                            
                        elif choice == '5':
                            # Stop automation
                            print("🛑 Email automation stopped by user")
                            return {
                                'emails_sent': len(emails_sent),
                                'errors': errors,
                                'stopped_by_user': True
                            }
                            
                        else:
                            print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                    
                    # Add delay between emails
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    error_msg = f"Error processing email for {lead.get('name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    continue
            
            logger.info(f"Email campaign completed. Sent {len(emails_sent)} emails")
            
        except Exception as e:
            error_msg = f"Error during email campaign: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
        return {
            'emails_sent': len(emails_sent),
            'errors': errors
        }
    
    def create_email_content(self, lead: Dict) -> str:
        """Create personalized email content for a lead"""
        content = f"""
Dear {lead['contact_person'] or 'Business Owner'},

I hope this email finds you well. My name is [Your Name], and I'm an IT solutions consultant based in Abuja, helping businesses like {lead['name']} improve their operations through technology.

I noticed that {lead['name']} operates in the {lead['industry']} sector, and I believe there are several opportunities where technology could significantly benefit your business:

• Process Automation: Streamline repetitive tasks and improve efficiency
• Digital Transformation: Modernize your business operations
• Data Management: Better organize and utilize your business data
• Customer Relationship Management: Improve customer interactions and retention

I would love to schedule a brief 15-minute consultation to discuss how we can help {lead['name']} achieve its technology goals. This consultation is completely free and comes with no obligations.

Would you be available for a call this week? I'm flexible and can work around your schedule.

Best regards,
[Your Name]
IT Solutions Consultant
[Your Phone Number]
[Your Email]

P.S. I've helped several {lead['industry']} businesses in Abuja implement cost-effective IT solutions that have improved their operations by 20-40%.
        """
        return content.strip() 