"""
Report Generator Module
=======================

Generates comprehensive reports and analytics for lead generation campaigns.
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from .database_manager import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates reports and analytics"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive lead generation report"""
        logger.info("Generating comprehensive report...")
        
        try:
            # Get database statistics
            stats = self.db.get_statistics()
            
            # Create comprehensive report
            report = {
                'total_leads': stats['total_leads'],
                'leads_by_status': stats['leads_by_status'],
                'leads_by_industry': stats['leads_by_industry'],
                'leads_by_source': stats['leads_by_source'],
                'leads_this_week': stats['leads_this_week'],
                'generated_date': datetime.now().isoformat(),
                'summary': self.generate_summary(stats),
                'recommendations': self.generate_recommendations(stats)
            }
            
            # Save report to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'lead_report_{timestamp}.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Report saved to {filename}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {
                'error': str(e),
                'generated_date': datetime.now().isoformat()
            }
    
    def generate_summary(self, stats: Dict[str, Any]) -> str:
        """Generate summary text for the report"""
        total_leads = stats['total_leads']
        leads_this_week = stats['leads_this_week']
        
        summary = f"""
Lead Generation Summary Report
==============================

Total Leads in Database: {total_leads}
New Leads This Week: {leads_this_week}

Lead Status Distribution:
"""
        
        for status, count in stats['leads_by_status'].items():
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            summary += f"• {status.title()}: {count} ({percentage:.1f}%)\n"
        
        summary += "\nTop Industries:\n"
        sorted_industries = sorted(stats['leads_by_industry'].items(), 
                                 key=lambda x: x[1], reverse=True)[:5]
        
        for industry, count in sorted_industries:
            summary += f"• {industry}: {count} leads\n"
        
        summary += "\nLead Sources:\n"
        for source, count in stats['leads_by_source'].items():
            summary += f"• {source}: {count} leads\n"
        
        return summary.strip()
    
    def generate_recommendations(self, stats: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on statistics"""
        recommendations = []
        
        total_leads = stats['total_leads']
        leads_this_week = stats['leads_this_week']
        
        if total_leads == 0:
            recommendations.append("Start lead generation immediately - no leads in database")
            recommendations.append("Focus on business directory scraping first")
            recommendations.append("Set up LinkedIn Sales Navigator automation")
        
        elif leads_this_week < 10:
            recommendations.append(f"Increase lead generation efforts - only {leads_this_week} leads this week")
            recommendations.append("Expand target industries and locations")
            recommendations.append("Optimize message templates for better response rates")
        
        # Check lead status distribution
        new_leads = stats['leads_by_status'].get('new', 0)
        contacted_leads = stats['leads_by_status'].get('contacted', 0)
        
        if new_leads > contacted_leads * 2:
            recommendations.append("Focus on contacting existing leads before generating new ones")
            recommendations.append("Implement automated follow-up sequences")
        
        # Check industry distribution
        if len(stats['leads_by_industry']) < 3:
            recommendations.append("Diversify target industries for better market coverage")
        
        # Check source distribution
        if len(stats['leads_by_source']) < 2:
            recommendations.append("Expand lead sources for better reach")
        
        return recommendations 