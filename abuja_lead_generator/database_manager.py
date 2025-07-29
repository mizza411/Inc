"""
Database Manager Module
=======================

Handles all database operations for storing and managing leads.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class BusinessLead:
    """Data class for business lead information"""
    name: str
    industry: str
    location: str
    address: str
    phone: str
    email: str
    website: str
    contact_person: str
    business_size: str
    it_needs: List[str]
    source: str
    status: str = "new"
    notes: str = ""
    created_date: str = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().isoformat()

class DatabaseManager:
    """Manages SQLite database operations for leads"""
    
    def __init__(self, db_path: str = "abuja_leads.db"):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Setup SQLite database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                industry TEXT,
                location TEXT,
                address TEXT,
                phone TEXT,
                email TEXT,
                website TEXT,
                contact_person TEXT,
                business_size TEXT,
                it_needs TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                notes TEXT,
                created_date TEXT,
                last_contact_date TEXT,
                contact_count INTEGER DEFAULT 0
            )
        ''')
        
        # Campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT,
                status TEXT DEFAULT 'active',
                created_date TEXT,
                target_count INTEGER,
                success_count INTEGER DEFAULT 0
            )
        ''')
        
        # Contact log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                contact_method TEXT,
                message TEXT,
                response TEXT,
                contact_date TEXT,
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database setup completed")
    
    def add_lead(self, lead: BusinessLead) -> int:
        """Add a new lead to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO leads (
                name, industry, location, address, phone, email, website,
                contact_person, business_size, it_needs, source, status, notes, created_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            lead.name, lead.industry, lead.location, lead.address, lead.phone,
            lead.email, lead.website, lead.contact_person, lead.business_size,
            json.dumps(lead.it_needs), lead.source, lead.status, lead.notes, lead.created_date
        ))
        
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Added new lead: {lead.name} (ID: {lead_id})")
        return lead_id
    
    def get_leads(self, status: str = None, industry: str = None, limit: int = 100) -> List[Dict]:
        """Get leads from database with optional filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM leads WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if industry:
            query += " AND industry = ?"
            params.append(industry)
        
        query += " ORDER BY created_date DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        leads = []
        for row in rows:
            lead = {
                'id': row[0],
                'name': row[1],
                'industry': row[2],
                'location': row[3],
                'address': row[4],
                'phone': row[5],
                'email': row[6],
                'website': row[7],
                'contact_person': row[8],
                'business_size': row[9],
                'it_needs': json.loads(row[10]) if row[10] else [],
                'source': row[11],
                'status': row[12],
                'notes': row[13],
                'created_date': row[14],
                'last_contact_date': row[15],
                'contact_count': row[16]
            }
            leads.append(lead)
        
        conn.close()
        return leads
    
    def update_lead_status(self, lead_id: int, status: str):
        """Update lead status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE leads 
            SET status = ?, last_contact_date = ?, contact_count = contact_count + 1
            WHERE id = ?
        ''', (status, datetime.now().isoformat(), lead_id))
        
        conn.commit()
        conn.close()
        logger.info(f"Updated lead {lead_id} status to {status}")
    
    def add_contact_log(self, lead_id: int, contact_method: str, message: str, response: str = ""):
        """Add contact log entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contact_log (lead_id, contact_method, message, response, contact_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (lead_id, contact_method, message, response, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        logger.info(f"Added contact log for lead {lead_id}")
    
    def get_contact_history(self, lead_id: int) -> List[Dict]:
        """Get contact history for a lead"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM contact_log WHERE lead_id = ? ORDER BY contact_date DESC
        ''', (lead_id,))
        
        rows = cursor.fetchall()
        history = []
        
        for row in rows:
            entry = {
                'id': row[0],
                'lead_id': row[1],
                'contact_method': row[2],
                'message': row[3],
                'response': row[4],
                'contact_date': row[5]
            }
            history.append(entry)
        
        conn.close()
        return history
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total leads
        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]
        
        # Leads by status
        cursor.execute("SELECT status, COUNT(*) FROM leads GROUP BY status")
        leads_by_status = dict(cursor.fetchall())
        
        # Leads by industry
        cursor.execute("SELECT industry, COUNT(*) FROM leads GROUP BY industry")
        leads_by_industry = dict(cursor.fetchall())
        
        # Leads by source
        cursor.execute("SELECT source, COUNT(*) FROM leads GROUP BY source")
        leads_by_source = dict(cursor.fetchall())
        
        # Recent activity (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM leads 
            WHERE created_date >= ?
        """, ((datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - 
               datetime.timedelta(days=7)).isoformat(),))
        leads_this_week = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_leads': total_leads,
            'leads_by_status': leads_by_status,
            'leads_by_industry': leads_by_industry,
            'leads_by_source': leads_by_source,
            'leads_this_week': leads_this_week
        } 