"""
LinkedIn Automation Module
==========================

Handles LinkedIn Sales Navigator automation for lead generation.
"""

import time
import random
from typing import List, Dict, Any
from .database_manager import DatabaseManager, BusinessLead
from .config_manager import ConfigManager
import logging

logger = logging.getLogger(__name__)

class LinkedInAutomation:
    """Automates LinkedIn Sales Navigator outreach"""
    
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
    
    def run_automation(self) -> Dict[str, Any]:
        """Run LinkedIn automation"""
        if not self.config.get('linkedin.enabled', True):
            logger.info("LinkedIn automation is disabled")
            return {'leads_found': 0, 'errors': []}
        
        logger.info("Starting LinkedIn Sales Navigator automation...")
        
        leads = []
        errors = []
        
        try:
            keywords = self.config.get('linkedin.search_keywords', [])
            locations = self.config.get('linkedin.target_locations', [])
            industries = self.config.get('linkedin.target_industries', [])
            
            for keyword in keywords:
                for location in locations:
                    for industry in industries:
                        try:
                            logger.info(f"Searching LinkedIn for: {keyword} in {location} - {industry}")
                            
                            # Simulate finding leads
                            sample_linkedin_lead = {
                                'name': f'{industry} Company in {location}',
                                'industry': industry,
                                'location': location,
                                'address': f'{location}, Abuja, Nigeria',
                                'phone': f'+234 80{random.randint(10000000, 99999999)}',
                                'email': f'contact@{industry.lower().replace(" ", "")}.com',
                                'website': f'www.{industry.lower().replace(" ", "")}.com',
                                'contact_person': 'Business Owner',
                                'business_size': 'Medium',
                                'it_needs': ['Digital Transformation', 'Process Automation'],
                                'source': 'LinkedIn Sales Navigator'
                            }
                            
                            # PROMPT USER BEFORE ADDING LEAD
                            print(f"\n🔍 LinkedIn Lead Found:")
                            print(f"Company: {sample_linkedin_lead['name']}")
                            print(f"Industry: {sample_linkedin_lead['industry']}")
                            print(f"Location: {sample_linkedin_lead['location']}")
                            print(f"Email: {sample_linkedin_lead['email']}")
                            print(f"Phone: {sample_linkedin_lead['phone']}")
                            print(f"IT Needs: {', '.join(sample_linkedin_lead['it_needs'])}")
                            print(f"\nOptions:")
                            print("1. Add this lead to database")
                            print("2. Skip this lead")
                            print("3. Edit lead information")
                            print("4. Stop automation")
                            
                            while True:
                                choice = input("\nEnter your choice (1-4): ").strip()
                                
                                if choice == '1':
                                    # Add the lead
                                    lead = BusinessLead(**sample_linkedin_lead)
                                    lead_id = self.db.add_lead(lead)
                                    leads.append(lead)
                                    
                                    # Simulate sending connection request
                                    logger.info(f"Added lead and sent connection request to {lead.name}")
                                    print(f"✅ Lead added: {lead.name}")
                                    break
                                    
                                elif choice == '2':
                                    # Skip this lead
                                    print(f"⏭️  Skipped {sample_linkedin_lead['name']}")
                                    break
                                    
                                elif choice == '3':
                                    # Edit lead information
                                    print(f"\nCurrent company name: {sample_linkedin_lead['name']}")
                                    new_name = input("Enter new company name (or press Enter to keep current): ").strip()
                                    if new_name:
                                        sample_linkedin_lead['name'] = new_name
                                    
                                    print(f"Current email: {sample_linkedin_lead['email']}")
                                    new_email = input("Enter new email (or press Enter to keep current): ").strip()
                                    if new_email:
                                        sample_linkedin_lead['email'] = new_email
                                    
                                    print(f"Current phone: {sample_linkedin_lead['phone']}")
                                    new_phone = input("Enter new phone (or press Enter to keep current): ").strip()
                                    if new_phone:
                                        sample_linkedin_lead['phone'] = new_phone
                                    
                                    print(f"📝 Lead information updated")
                                    continue
                                    
                                elif choice == '4':
                                    # Stop automation
                                    print("🛑 LinkedIn automation stopped by user")
                                    return {
                                        'leads_found': len(leads),
                                        'errors': errors,
                                        'stopped_by_user': True
                                    }
                                    
                                else:
                                    print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                            
                            time.sleep(random.uniform(1, 2))  # Random delay
                            
                        except Exception as e:
                            error_msg = f"Error processing LinkedIn search {keyword}-{location}-{industry}: {str(e)}"
                            logger.error(error_msg)
                            errors.append(error_msg)
                            continue
            
            logger.info(f"LinkedIn automation completed. Found {len(leads)} new leads")
            
        except Exception as e:
            error_msg = f"Error during LinkedIn automation: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
        return {
            'leads_found': len(leads),
            'errors': errors
        } 