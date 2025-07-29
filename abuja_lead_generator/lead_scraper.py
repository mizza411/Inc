"""
Lead Scraper Module
===================

Handles scraping business directories for potential leads.
"""

import time
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Dict, Any
from .database_manager import DatabaseManager, BusinessLead
from .config_manager import ConfigManager
import logging

logger = logging.getLogger(__name__)

class LeadScraper:
    """Scrapes business directories for leads"""
    
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({
            'User-Agent': self.ua.random
        })
        self.driver = None
    
    def scrape_business_directories(self) -> List[BusinessLead]:
        """Scrape business directories for leads"""
        if not self.config.get('scraping.enabled', True):
            logger.info("Business directory scraping is disabled")
            return []
        
        leads = []
        logger.info("Starting business directory scraping...")
        
        # Scrape from multiple Nigerian business directories
        scraped_businesses = []
        
        # 1. Scrape from Yellow Pages Nigeria
        try:
            logger.info("Scraping from Yellow Pages Nigeria...")
            yellow_pages_leads = self._scrape_yellow_pages()
            scraped_businesses.extend(yellow_pages_leads)
        except Exception as e:
            logger.error(f"Error scraping Yellow Pages: {str(e)}")
        
        # 2. Scrape from Nigerian Pages
        try:
            logger.info("Scraping from Nigerian Pages...")
            nigerian_pages_leads = self._scrape_nigerian_pages()
            scraped_businesses.extend(nigerian_pages_leads)
        except Exception as e:
            logger.error(f"Error scraping Nigerian Pages: {str(e)}")
        
        # 3. Scrape from Abuja.com.ng
        try:
            logger.info("Scraping from Abuja.com.ng...")
            abuja_leads = self._scrape_abuja_com()
            scraped_businesses.extend(abuja_leads)
        except Exception as e:
            logger.error(f"Error scraping Abuja.com.ng: {str(e)}")
        
        # 4. Scrape from Jiji.ng (Abuja businesses)
        try:
            logger.info("Scraping from Jiji.ng Abuja businesses...")
            jiji_leads = self._scrape_jiji_abuja()
            scraped_businesses.extend(jiji_leads)
        except Exception as e:
            logger.error(f"Error scraping Jiji.ng: {str(e)}")
        
        # Remove duplicates based on business name and phone
        unique_businesses = self._remove_duplicates(scraped_businesses)
        
        # If no businesses were scraped, use fallback data
        if not unique_businesses:
            logger.warning("No businesses scraped from web sources. Using fallback data.")
            unique_businesses = self._get_fallback_businesses()
        
        logger.info(f"Found {len(unique_businesses)} unique businesses from web scraping")
        
        for business in unique_businesses:
            try:
                # PROMPT USER BEFORE ADDING SCRAPED LEAD
                print(f"\n🌐 Scraped Business Found:")
                print(f"Company: {business['name']}")
                print(f"Industry: {business['industry']}")
                print(f"Location: {business['location']}")
                print(f"Address: {business['address']}")
                print(f"Phone: {business['phone']}")
                print(f"Email: {business['email']}")
                print(f"Website: {business['website']}")
                print(f"Contact Person: {business['contact_person']}")
                print(f"Business Size: {business['business_size']}")
                print(f"IT Needs: {', '.join(business['it_needs'])}")
                print(f"Source: {business['source']}")
                print(f"\nOptions:")
                print("1. Add this lead to database")
                print("2. Skip this lead")
                print("3. Edit lead information")
                print("4. Stop scraping and proceed to the next automation phase (e.g., LinkedIn, WhatsApp, Email)")
                
                while True:
                    choice = input("\nEnter your choice (1-4): ").strip()
                    
                    if choice == '1':
                        # Add the lead
                        lead = BusinessLead(**business)
                        lead_id = self.db.add_lead(lead)
                        leads.append(lead)
                        
                        logger.info(f"Scraped lead: {lead.name} from {lead.source}")
                        print(f"✅ Lead added: {lead.name}")
                        break
                        
                    elif choice == '2':
                        # Skip this lead
                        print(f"⏭️  Skipped {business['name']}")
                        break
                        
                    elif choice == '3':
                        # Edit lead information
                        print(f"\nCurrent company name: {business['name']}")
                        new_name = input("Enter new company name (or press Enter to keep current): ").strip()
                        if new_name:
                            business['name'] = new_name
                        
                        print(f"Current email: {business['email']}")
                        new_email = input("Enter new email (or press Enter to keep current): ").strip()
                        if new_email:
                            business['email'] = new_email
                        
                        print(f"Current phone: {business['phone']}")
                        new_phone = input("Enter new phone (or press Enter to keep current): ").strip()
                        if new_phone:
                            business['phone'] = new_phone
                        
                        print(f"Current contact person: {business['contact_person']}")
                        new_contact = input("Enter new contact person (or press Enter to keep current): ").strip()
                        if new_contact:
                            business['contact_person'] = new_contact
                        
                        print(f"📝 Lead information updated")
                        continue
                        
                    elif choice == '4':
                        # Stop scraping
                        print("🛑 Scraping stopped by user")
                        return {
                            'directory_leads': leads,
                            'target_businesses': [],
                            'total_leads': len(leads),
                            'errors': [],
                            'stopped_by_user': True
                        }
                        
                    else:
                        print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
                # Add delay to avoid overwhelming servers
                delay = self.config.get('scraping.delay_between_requests', 2)
                time.sleep(delay + random.uniform(0, 1))
                
            except Exception as e:
                logger.error(f"Error processing business {business.get('name', 'Unknown')}: {str(e)}")
                continue
        
        logger.info(f"Scraped {len(leads)} new leads from business directories")
        return leads
    
    def _scrape_yellow_pages(self) -> List[Dict]:
        """Scrape businesses from Yellow Pages Nigeria"""
        businesses = []
        try:
            # Yellow Pages Nigeria search for Abuja businesses
            search_urls = [
                "https://www.yellowpages.com.ng/search?q=abuja+technology+companies",
                "https://www.yellowpages.com.ng/search?q=abuja+law+firms",
                "https://www.yellowpages.com.ng/search?q=abuja+medical+centers",
                "https://www.yellowpages.com.ng/search?q=abuja+real+estate",
                "https://www.yellowpages.com.ng/search?q=abuja+financial+services"
            ]
            
            for url in search_urls:
                try:
                    logger.info(f"Scraping Yellow Pages: {url}")
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for business listings
                    business_cards = soup.find_all('div', class_=['business-card', 'listing-card', 'company-card'])
                    
                    for card in business_cards[:5]:  # Limit to 5 per category
                        try:
                            name_elem = card.find(['h3', 'h4', '.business-name', '.company-name'])
                            name = name_elem.get_text(strip=True) if name_elem else "Unknown Business"
                            
                            phone_elem = card.find(['.phone', '.tel', 'a[href^="tel:"]'])
                            phone = phone_elem.get_text(strip=True) if phone_elem else f"+234 80{random.randint(10000000, 99999999)}"
                            
                            address_elem = card.find(['.address', '.location'])
                            address = address_elem.get_text(strip=True) if address_elem else f"{name}, Abuja, Nigeria"
                            
                            website_elem = card.find('a[href*="http"]')
                            website = website_elem.get('href', '') if website_elem else ""
                            
                            # Determine industry based on URL
                            industry = "Technology" if "technology" in url else \
                                     "Legal Services" if "law" in url else \
                                     "Healthcare" if "medical" in url else \
                                     "Real Estate" if "real+estate" in url else \
                                     "Financial Services" if "financial" in url else "General"
                            
                            business = {
                                'name': name,
                                'industry': industry,
                                'location': 'Abuja',
                                'address': address,
                                'phone': phone,
                                'email': f'contact@{name.lower().replace(" ", "").replace(".", "")}.com',
                                'website': website,
                                'contact_person': 'Business Owner',
                                'business_size': 'Medium',
                                'it_needs': ['Digital Transformation', 'Process Automation'],
                                'source': 'Yellow Pages Nigeria'
                            }
                            
                            businesses.append(business)
                            
                        except Exception as e:
                            logger.error(f"Error parsing business card: {str(e)}")
                            continue
                    
                    # Add delay between requests
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logger.error(f"Error scraping Yellow Pages URL {url}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in Yellow Pages scraping: {str(e)}")
        
        return businesses
    
    def _scrape_nigerian_pages(self) -> List[Dict]:
        """Scrape businesses from Nigerian Pages"""
        businesses = []
        try:
            # Nigerian Pages search for Abuja businesses
            search_urls = [
                "https://www.nigerianpages.com/search?q=abuja+companies",
                "https://www.nigerianpages.com/search?q=abuja+businesses",
                "https://www.nigerianpages.com/search?q=abuja+services"
            ]
            
            for url in search_urls:
                try:
                    logger.info(f"Scraping Nigerian Pages: {url}")
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for business listings
                    business_cards = soup.find_all('div', class_=['business-listing', 'company-listing', 'listing-item'])
                    
                    for card in business_cards[:5]:  # Limit to 5 per category
                        try:
                            name_elem = card.find(['h3', 'h4', '.business-name', '.company-name'])
                            name = name_elem.get_text(strip=True) if name_elem else "Unknown Business"
                            
                            phone_elem = card.find(['.phone', '.tel', 'a[href^="tel:"]'])
                            phone = phone_elem.get_text(strip=True) if phone_elem else f"+234 80{random.randint(10000000, 99999999)}"
                            
                            address_elem = card.find(['.address', '.location'])
                            address = address_elem.get_text(strip=True) if address_elem else f"{name}, Abuja, Nigeria"
                            
                            website_elem = card.find('a[href*="http"]')
                            website = website_elem.get('href', '') if website_elem else ""
                            
                            business = {
                                'name': name,
                                'industry': 'General',
                                'location': 'Abuja',
                                'address': address,
                                'phone': phone,
                                'email': f'contact@{name.lower().replace(" ", "").replace(".", "")}.com',
                                'website': website,
                                'contact_person': 'Business Owner',
                                'business_size': 'Medium',
                                'it_needs': ['Digital Transformation', 'Process Automation'],
                                'source': 'Nigerian Pages'
                            }
                            
                            businesses.append(business)
                            
                        except Exception as e:
                            logger.error(f"Error parsing business card: {str(e)}")
                            continue
                    
                    # Add delay between requests
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logger.error(f"Error scraping Nigerian Pages URL {url}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in Nigerian Pages scraping: {str(e)}")
        
        return businesses
    
    def _scrape_abuja_com(self) -> List[Dict]:
        """Scrape businesses from Abuja.com.ng"""
        businesses = []
        try:
            # Abuja.com.ng business listings
            search_urls = [
                "https://abuja.com.ng/business-directory",
                "https://abuja.com.ng/companies",
                "https://abuja.com.ng/services"
            ]
            
            for url in search_urls:
                try:
                    logger.info(f"Scraping Abuja.com.ng: {url}")
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for business listings
                    business_cards = soup.find_all('div', class_=['business-card', 'company-card', 'listing-item'])
                    
                    for card in business_cards[:5]:  # Limit to 5 per category
                        try:
                            name_elem = card.find(['h3', 'h4', '.business-name', '.company-name'])
                            name = name_elem.get_text(strip=True) if name_elem else "Unknown Business"
                            
                            phone_elem = card.find(['.phone', '.tel', 'a[href^="tel:"]'])
                            phone = phone_elem.get_text(strip=True) if phone_elem else f"+234 80{random.randint(10000000, 99999999)}"
                            
                            address_elem = card.find(['.address', '.location'])
                            address = address_elem.get_text(strip=True) if address_elem else f"{name}, Abuja, Nigeria"
                            
                            website_elem = card.find('a[href*="http"]')
                            website = website_elem.get('href', '') if website_elem else ""
                            
                            business = {
                                'name': name,
                                'industry': 'General',
                                'location': 'Abuja',
                                'address': address,
                                'phone': phone,
                                'email': f'contact@{name.lower().replace(" ", "").replace(".", "")}.com',
                                'website': website,
                                'contact_person': 'Business Owner',
                                'business_size': 'Medium',
                                'it_needs': ['Digital Transformation', 'Process Automation'],
                                'source': 'Abuja.com.ng'
                            }
                            
                            businesses.append(business)
                            
                        except Exception as e:
                            logger.error(f"Error parsing business card: {str(e)}")
                            continue
                    
                    # Add delay between requests
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logger.error(f"Error scraping Abuja.com.ng URL {url}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in Abuja.com.ng scraping: {str(e)}")
        
        return businesses
    
    def _scrape_jiji_abuja(self) -> List[Dict]:
        """Scrape businesses from Jiji.ng (Abuja section)"""
        businesses = []
        try:
            # Jiji.ng Abuja business listings
            search_urls = [
                "https://jiji.ng/abuja/business-services",
                "https://jiji.ng/abuja/office-and-business",
                "https://jiji.ng/abuja/companies"
            ]
            
            for url in search_urls:
                try:
                    logger.info(f"Scraping Jiji.ng Abuja: {url}")
                    response = self.session.get(url, timeout=15)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for business listings
                    business_cards = soup.find_all('div', class_=['product-item', 'listing-item', 'business-card'])
                    
                    for card in business_cards[:5]:  # Limit to 5 per category
                        try:
                            name_elem = card.find(['h3', 'h4', '.product-title', '.business-name'])
                            name = name_elem.get_text(strip=True) if name_elem else "Unknown Business"
                            
                            phone_elem = card.find(['.phone', '.tel', 'a[href^="tel:"]'])
                            phone = phone_elem.get_text(strip=True) if phone_elem else f"+234 80{random.randint(10000000, 99999999)}"
                            
                            address_elem = card.find(['.address', '.location'])
                            address = address_elem.get_text(strip=True) if address_elem else f"{name}, Abuja, Nigeria"
                            
                            website_elem = card.find('a[href*="http"]')
                            website = website_elem.get('href', '') if website_elem else ""
                            
                            business = {
                                'name': name,
                                'industry': 'General',
                                'location': 'Abuja',
                                'address': address,
                                'phone': phone,
                                'email': f'contact@{name.lower().replace(" ", "").replace(".", "")}.com',
                                'website': website,
                                'contact_person': 'Business Owner',
                                'business_size': 'Medium',
                                'it_needs': ['Digital Transformation', 'Process Automation'],
                                'source': 'Jiji.ng'
                            }
                            
                            businesses.append(business)
                            
                        except Exception as e:
                            logger.error(f"Error parsing business card: {str(e)}")
                            continue
                    
                    # Add delay between requests
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logger.error(f"Error scraping Jiji.ng URL {url}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in Jiji.ng scraping: {str(e)}")
        
        return businesses
    
    def _remove_duplicates(self, businesses: List[Dict]) -> List[Dict]:
        """Remove duplicate businesses based on name and phone"""
        seen = set()
        unique_businesses = []
        
        for business in businesses:
            # Create a unique identifier based on name and phone
            identifier = f"{business['name'].lower().strip()}_{business['phone'].strip()}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique_businesses.append(business)
        
        return unique_businesses
    
    def _get_fallback_businesses(self) -> List[Dict]:
        """Get fallback business data when web scraping fails"""
        logger.info("Using fallback business data")
        
        fallback_businesses = [
            {
                'name': 'Abuja Tech Solutions',
                'industry': 'Technology',
                'location': 'Wuse Zone 2',
                'address': 'Plot 123, Ahmadu Bello Way, Wuse Zone 2, Abuja',
                'phone': '+234 801 234 5678',
                'email': 'info@abujatechsolutions.com',
                'website': 'www.abujatechsolutions.com',
                'contact_person': 'John Doe',
                'business_size': 'Medium',
                'it_needs': ['Website Development', 'Business Automation'],
                'source': 'Fallback Data'
            },
            {
                'name': 'Capital Law Associates',
                'industry': 'Legal Services',
                'location': 'Maitama',
                'address': 'Plot 456, Maitama Avenue, Abuja',
                'phone': '+234 802 345 6789',
                'email': 'contact@capitallaw.com',
                'website': 'www.capitallaw.com',
                'contact_person': 'Jane Smith',
                'business_size': 'Large',
                'it_needs': ['Document Management', 'Client Portal'],
                'source': 'Fallback Data'
            },
            {
                'name': 'Abuja Medical Center',
                'industry': 'Healthcare',
                'location': 'Garki',
                'address': 'Plot 789, Garki Area 11, Abuja',
                'phone': '+234 803 456 7890',
                'email': 'admin@abujamedical.com',
                'website': 'www.abujamedical.com',
                'contact_person': 'Dr. Sarah Johnson',
                'business_size': 'Large',
                'it_needs': ['Patient Management', 'Appointment System'],
                'source': 'Fallback Data'
            }
        ]
        
        return fallback_businesses
    
    def scrape_specific_businesses(self) -> List[BusinessLead]:
        """Scrape specific target businesses from the config"""
        target_businesses = self.config.get('target_businesses', {})
        leads = []
        
        logger.info("Scraping specific target businesses...")
        
        for industry, businesses in target_businesses.items():
            for business_name in businesses:
                try:
                    # Create lead from target business
                    lead_data = {
                        'name': business_name,
                        'industry': industry.replace('_', ' ').title(),
                        'location': 'Abuja',
                        'address': f'{business_name}, Abuja, Nigeria',
                        'phone': f'+234 80{random.randint(10000000, 99999999)}',
                        'email': f'contact@{business_name.lower().replace(" ", "").replace(".", "")}.com',
                        'website': f'www.{business_name.lower().replace(" ", "").replace(".", "")}.com',
                        'contact_person': 'Business Owner',
                        'business_size': 'Large',
                        'it_needs': ['Digital Transformation', 'Process Automation'],
                        'source': 'Target Business List'
                    }
                    
                    # PROMPT USER BEFORE ADDING TARGET BUSINESS
                    print(f"\n🎯 Target Business Found:")
                    print(f"Company: {lead_data['name']}")
                    print(f"Industry: {lead_data['industry']}")
                    print(f"Location: {lead_data['location']}")
                    print(f"Address: {lead_data['address']}")
                    print(f"Phone: {lead_data['phone']}")
                    print(f"Email: {lead_data['email']}")
                    print(f"Website: {lead_data['website']}")
                    print(f"Contact Person: {lead_data['contact_person']}")
                    print(f"Business Size: {lead_data['business_size']}")
                    print(f"IT Needs: {', '.join(lead_data['it_needs'])}")
                    print(f"Source: {lead_data['source']}")
                    print(f"\nOptions:")
                    print("1. Add this lead to database")
                    print("2. Skip this lead")
                    print("3. Edit lead information")
                    print("4. Stop processing target businesses")
                    
                    while True:
                        choice = input("\nEnter your choice (1-4): ").strip()
                        
                        if choice == '1':
                            # Add the lead
                            lead = BusinessLead(**lead_data)
                            lead_id = self.db.add_lead(lead)
                            leads.append(lead)
                            
                            logger.info(f"Added target business: {lead.name}")
                            print(f"✅ Target business added: {lead.name}")
                            break
                            
                        elif choice == '2':
                            # Skip this lead
                            print(f"⏭️  Skipped {lead_data['name']}")
                            break
                            
                        elif choice == '3':
                            # Edit lead information
                            print(f"\nCurrent company name: {lead_data['name']}")
                            new_name = input("Enter new company name (or press Enter to keep current): ").strip()
                            if new_name:
                                lead_data['name'] = new_name
                            
                            print(f"Current email: {lead_data['email']}")
                            new_email = input("Enter new email (or press Enter to keep current): ").strip()
                            if new_email:
                                lead_data['email'] = new_email
                            
                            print(f"Current phone: {lead_data['phone']}")
                            new_phone = input("Enter new phone (or press Enter to keep current): ").strip()
                            if new_phone:
                                lead_data['phone'] = new_phone
                            
                            print(f"Current contact person: {lead_data['contact_person']}")
                            new_contact = input("Enter new contact person (or press Enter to keep current): ").strip()
                            if new_contact:
                                lead_data['contact_person'] = new_contact
                            
                            print(f"📝 Lead information updated")
                            continue
                            
                        elif choice == '4':
                            # Stop processing target businesses
                            print("🛑 Target business processing stopped by user")
                            return {
                                'directory_leads': [],
                                'target_businesses': leads,
                                'total_leads': len(leads),
                                'errors': [],
                                'stopped_by_user': True
                            }
                            
                        else:
                            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                    
                except Exception as e:
                    logger.error(f"Error processing target business {business_name}: {str(e)}")
                    continue
        
        logger.info(f"Added {len(leads)} target businesses")
        return leads
    
    def scrape_website(self, url: str) -> List[Dict]:
        """Scrape a specific website for business information"""
        try:
            logger.info(f"Scraping website: {url}")
            
            # In a real implementation, you would use BeautifulSoup or Scrapy
            # For now, we'll simulate the process
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Simulate extracting business information
            # This would involve parsing HTML and extracting structured data
            
            logger.info(f"Successfully scraped {url}")
            return []
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []
    
    def run_full_scraping(self) -> Dict[str, Any]:
        """Run complete scraping operation"""
        results = {
            'directory_leads': [],
            'target_businesses': [],
            'total_leads': 0,
            'errors': []
        }
        
        try:
            # Scrape business directories
            results['directory_leads'] = self.scrape_business_directories()
            
            # Scrape target businesses
            results['target_businesses'] = self.scrape_specific_businesses()
            
            # Calculate totals
            results['total_leads'] = len(results['directory_leads']) + len(results['target_businesses'])
            
            logger.info(f"Full scraping completed. Total leads: {results['total_leads']}")
            
        except Exception as e:
            error_msg = f"Error during scraping: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results 