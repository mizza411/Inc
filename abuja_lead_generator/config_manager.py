"""
Configuration Manager Module
============================

Handles loading and managing configuration settings for the lead generator.
"""

import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages configuration settings for the lead generator"""
    
    def __init__(self, config_file: str = "lead_generator_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file or create default"""
        default_config = {
            "linkedin": {
                "enabled": True,
                "api_key": "",
                "search_keywords": [
                    "IT solutions Abuja",
                    "business automation Nigeria",
                    "digital transformation Abuja",
                    "software development Abuja"
                ],
                "target_locations": ["Abuja", "FCT", "Nigeria"],
                "target_industries": [
                    "Real Estate",
                    "Legal Services", 
                    "Healthcare",
                    "Hospitality",
                    "Education",
                    "Manufacturing",
                    "Financial Services"
                ]
            },
            "whatsapp": {
                "enabled": True,
                "api_key": "",
                "business_phone": "",
                "auto_messages": [
                    "Hello! I'm an IT solutions consultant helping businesses in Abuja improve their operations through technology. Would you be interested in a free consultation?",
                    "Hi there! I help businesses automate their processes and implement digital solutions. Would you like to discuss how technology could benefit your business?",
                    "Good day! I'm reaching out to businesses in Abuja about IT solutions that can improve efficiency and reduce costs. Are you interested in learning more?"
                ]
            },
            "email": {
                "enabled": True,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "subject_templates": [
                    "IT Solutions for {business_name} - Improve Your Operations",
                    "Digital Transformation Opportunity for {business_name}",
                    "Automate Your Business Processes - {business_name}"
                ]
            },
            "scraping": {
                "enabled": True,
                "delay_between_requests": 2,
                "max_requests_per_session": 50,
                "business_directories": [
                    "https://www.yellowpages.ng",
                    "https://www.nigerianpages.com", 
                    "https://www.abuja.com.ng"
                ]
            },
            "target_businesses": {
                "real_estate": [
                    "Broll Nigeria", "Knight Frank Nigeria", "CBRE Nigeria", "JLL Nigeria",
                    "First City Monument Bank Real Estate", "UAC Property Development Company"
                ],
                "law_firms": [
                    "Aluko & Oyebode", "Banwo & Ighodalo", "Olaniwun Ajayi LP",
                    "Udo Udoma & Belo-Osagie", "Templars Law", "Jackson, Etti & Edu"
                ],
                "medical": [
                    "Cedarcrest Hospitals", "Primus International Hospital", "Nizamiye Hospital",
                    "National Hospital Abuja", "Asokoro General Hospital"
                ],
                "hotels": [
                    "Transcorp Hilton Abuja", "Sheraton Abuja Hotel", "Nicon Luxury Hotel",
                    "Rockview Hotel", "Bolton White Hotel"
                ],
                "education": [
                    "Baze University", "Nile University", "University of Abuja",
                    "Nigerian Turkish Nile University", "Veritas University"
                ],
                "banks": [
                    "GTBank Abuja", "Access Bank Abuja", "First Bank Abuja",
                    "Zenith Bank Abuja", "UBA Abuja", "Fidelity Bank Abuja"
                ]
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default config
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                logger.info(f"Loaded configuration from {self.config_file}")
            else:
                config = default_config
                self.save_config(config)
                logger.info(f"Created default configuration file: {self.config_file}")
                
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            config = default_config
            
        return config
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        self.save_config()
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        for key, value in updates.items():
            self.set(key, value) 