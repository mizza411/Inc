"""
Main Controller Module
======================

Orchestrates all lead generation modules and provides the main interface.
"""

import logging
from typing import Dict, Any
from .config_manager import ConfigManager
from .database_manager import DatabaseManager
from .lead_scraper import LeadScraper
from .linkedin_automation import LinkedInAutomation
from .whatsapp_automation import WhatsAppAutomation
from .email_campaign import EmailCampaign
from .report_generator import ReportGenerator

logger = logging.getLogger(__name__)

class MainController:
    """Main controller for the lead generation system"""
    
    def __init__(self, config_file: str = "lead_generator_config.json"):
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('abuja_lead_generator.log'),
                logging.StreamHandler()
            ]
        )
        
        # Initialize components
        self.config = ConfigManager(config_file)
        self.db = DatabaseManager()
        self.scraper = LeadScraper(self.config, self.db)
        self.linkedin = LinkedInAutomation(self.config, self.db)
        self.whatsapp = WhatsAppAutomation(self.config, self.db)
        self.email = EmailCampaign(self.config, self.db)
        self.reporter = ReportGenerator(self.db)
        
        logger.info("Main controller initialized")
    
    def run_full_campaign(self) -> Dict[str, Any]:
        """Run a complete lead generation campaign"""
        logger.info("Starting full lead generation campaign...")
        
        results = {
            'scraped_leads': [],
            'linkedin_leads': [],
            'whatsapp_messages': [],
            'email_campaigns': [],
            'report': {},
            'errors': []
        }
        
        try:
            # 1. Scrape business directories
            if self.config.get('scraping.enabled', True):
                logger.info("Step 1: Business directory scraping")
                scraping_results = self.scraper.run_full_scraping()
                results['scraped_leads'] = scraping_results.get('total_leads', 0)
                results['errors'].extend(scraping_results.get('errors', []))
            
            # 2. LinkedIn automation
            if self.config.get('linkedin.enabled', True):
                logger.info("Step 2: LinkedIn automation")
                linkedin_results = self.linkedin.run_automation()
                results['linkedin_leads'] = linkedin_results.get('leads_found', 0)
                results['errors'].extend(linkedin_results.get('errors', []))
                
                # Check if user stopped the automation
                if linkedin_results.get('stopped_by_user', False):
                    logger.info("LinkedIn automation stopped by user")
                    results['stopped_by_user'] = True
                    return results
            
            # 3. WhatsApp automation
            if self.config.get('whatsapp.enabled', True):
                logger.info("Step 3: WhatsApp automation")
                whatsapp_results = self.whatsapp.run_automation()
                results['whatsapp_messages'] = whatsapp_results.get('messages_sent', 0)
                results['errors'].extend(whatsapp_results.get('errors', []))
                
                # Check if user stopped the automation
                if whatsapp_results.get('stopped_by_user', False):
                    logger.info("WhatsApp automation stopped by user")
                    results['stopped_by_user'] = True
                    return results
            
            # 4. Email campaigns
            if self.config.get('email.enabled', True):
                logger.info("Step 4: Email campaigns")
                email_results = self.email.run_campaign()
                results['email_campaigns'] = email_results.get('emails_sent', 0)
                results['errors'].extend(email_results.get('errors', []))
                
                # Check if user stopped the automation
                if email_results.get('stopped_by_user', False):
                    logger.info("Email automation stopped by user")
                    results['stopped_by_user'] = True
                    return results
            
            # 5. Generate report
            logger.info("Step 5: Generating report")
            results['report'] = self.reporter.generate_report()
            
            logger.info("Full campaign completed successfully!")
            
        except Exception as e:
            error_msg = f"Error during campaign: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results
    
    def run_scraping_only(self) -> Dict[str, Any]:
        """Run only the scraping module"""
        logger.info("Running scraping only...")
        return self.scraper.run_full_scraping()
    
    def run_linkedin_only(self) -> Dict[str, Any]:
        """Run only LinkedIn automation"""
        logger.info("Running LinkedIn automation only...")
        return self.linkedin.run_automation()
    
    def run_whatsapp_only(self) -> Dict[str, Any]:
        """Run only WhatsApp automation"""
        logger.info("Running WhatsApp automation only...")
        return self.whatsapp.run_automation()
    
    def run_email_only(self) -> Dict[str, Any]:
        """Run only email campaigns"""
        logger.info("Running email campaigns only...")
        return self.email.run_campaign()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a report of current leads"""
        logger.info("Generating report...")
        return self.reporter.generate_report()
    
    def get_leads(self, status: str = None, industry: str = None, limit: int = 100):
        """Get leads from database"""
        return self.db.get_leads(status, industry, limit)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self.db.get_statistics()
    
    def update_lead_status(self, lead_id: int, status: str):
        """Update lead status"""
        self.db.update_lead_status(lead_id, status)
    
    def add_contact_log(self, lead_id: int, contact_method: str, message: str, response: str = ""):
        """Add contact log entry"""
        self.db.add_contact_log(lead_id, contact_method, message, response) 