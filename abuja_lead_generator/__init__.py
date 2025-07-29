"""
Abuja Lead Generator Package
============================

A modular automated lead generation system for IT solutions in Abuja, Nigeria.
"""

from .config_manager import ConfigManager
from .database_manager import DatabaseManager
from .lead_scraper import LeadScraper
from .linkedin_automation import LinkedInAutomation
from .whatsapp_automation import WhatsAppAutomation
from .email_campaign import EmailCampaign
from .report_generator import ReportGenerator
from .main_controller import MainController

__version__ = "1.0.0"
__author__ = "Business Development Team"

__all__ = [
    'ConfigManager',
    'DatabaseManager', 
    'LeadScraper',
    'LinkedInAutomation',
    'WhatsAppAutomation',
    'EmailCampaign',
    'ReportGenerator',
    'MainController'
] 