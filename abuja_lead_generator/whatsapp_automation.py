"""
WhatsApp Automation Module
==========================

Handles WhatsApp Business automation for lead outreach.
"""

import time
import random
from typing import List, Dict, Any
from .database_manager import DatabaseManager
from .config_manager import ConfigManager
import logging

logger = logging.getLogger(__name__)

class WhatsAppAutomation:
    """Automates WhatsApp Business outreach"""
    
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
    
    def run_automation(self) -> Dict[str, Any]:
        """Run WhatsApp automation"""
        if not self.config.get('whatsapp.enabled', True):
            logger.info("WhatsApp automation is disabled")
            return {'messages_sent': 0, 'errors': []}
        
        logger.info("Starting WhatsApp Business automation...")
        
        messages_sent = []
        errors = []
        
        try:
            # Get leads that haven't been contacted via WhatsApp
            leads = self.db.get_leads(status='new', limit=50)
            
            for lead in leads:
                if not lead['phone']:
                    continue
                
                try:
                    # Select random message template
                    auto_messages = self.config.get('whatsapp.auto_messages', [])
                    if not auto_messages:
                        continue
                        
                    message = random.choice(auto_messages)
                    
                    # Personalize message
                    personalized_message = message.replace("{business_name}", lead['name'])
                    
                    # PROMPT USER BEFORE SENDING
                    print(f"\n📱 WhatsApp Message Preview:")
                    print(f"To: {lead['name']} ({lead['phone']})")
                    print(f"Industry: {lead['industry']}")
                    print(f"Location: {lead['location']}")
                    print(f"Message: {personalized_message}")
                    print(f"\nOptions:")
                    print("1. Send this message")
                    print("2. Skip this lead")
                    print("3. Edit message")
                    print("4. Stop automation")
                    
                    while True:
                        choice = input("\nEnter your choice (1-4): ").strip()
                        
                        if choice == '1':
                            # Send the message
                            logger.info(f"Sending WhatsApp message to {lead['name']}: {personalized_message[:50]}...")
                            
                            message_data = {
                                'lead_id': lead['id'],
                                'lead_name': lead['name'],
                                'phone': lead['phone'],
                                'message': personalized_message,
                                'timestamp': time.time()
                            }
                            
                            messages_sent.append(message_data)
                            
                            # Update lead status
                            self.db.update_lead_status(lead['id'], 'contacted')
                            
                            # Add contact log
                            self.db.add_contact_log(
                                lead['id'], 
                                'WhatsApp', 
                                personalized_message
                            )
                            
                            print(f"✅ Message sent to {lead['name']}")
                            break
                            
                        elif choice == '2':
                            # Skip this lead
                            print(f"⏭️  Skipped {lead['name']}")
                            break
                            
                        elif choice == '3':
                            # Edit message
                            print(f"\nCurrent message: {personalized_message}")
                            new_message = input("Enter new message (or press Enter to keep current): ").strip()
                            if new_message:
                                personalized_message = new_message
                            print(f"📝 Message updated")
                            continue
                            
                        elif choice == '4':
                            # Stop automation
                            print("🛑 WhatsApp automation stopped by user")
                            return {
                                'messages_sent': len(messages_sent),
                                'errors': errors,
                                'stopped_by_user': True
                            }
                            
                        else:
                            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                    
                    # Add delay between messages
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    error_msg = f"Error processing WhatsApp for {lead.get('name', 'Unknown')}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    continue
            
            logger.info(f"WhatsApp automation completed. Sent {len(messages_sent)} messages")
            
        except Exception as e:
            error_msg = f"Error during WhatsApp automation: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
        return {
            'messages_sent': len(messages_sent),
            'errors': errors
        } 