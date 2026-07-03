#!/usr/bin/env python3
"""
Sharing Utilities for Problem Identification Tool
Email templates, sharing scripts, and distribution tools
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

DEFAULT_SURVEY_URL = (
    "https://mizza411.github.io/Inc/problem_identification_tool/web/index.html"
)
DEFAULT_SURVEY_ID = "ill_pay_to_v1"
STRATEGY3_UTM_MEDIUM = "strategy3"
STRATEGY3_UTM_CAMPAIGN = "ill_pay_to"


def build_tracked_survey_url(
    base_url: str,
    *,
    survey_id: str = DEFAULT_SURVEY_ID,
    ref: Optional[str] = None,
    utm_source: Optional[str] = None,
    utm_medium: str = STRATEGY3_UTM_MEDIUM,
    utm_campaign: str = STRATEGY3_UTM_CAMPAIGN,
    utm_content: Optional[str] = None,
) -> str:
    """Build a survey URL with ref + UTM params (matches Strategy 3 distributor_links)."""
    params: Dict[str, str] = {}
    if survey_id:
        params["survey"] = survey_id
    if ref:
        params["ref"] = ref
        params["utm_source"] = utm_source or ref
    elif utm_source:
        params["utm_source"] = utm_source
    if utm_medium:
        params["utm_medium"] = utm_medium
    if utm_campaign:
        params["utm_campaign"] = utm_campaign
    if utm_content:
        params["utm_content"] = utm_content
    if not params:
        return base_url
    return f"{base_url}?{urlencode(params)}"

class SharingUtilities:
    def __init__(self, config_file="config/sharing_config.json"):
        self.config_file = config_file
        self.load_config()
        self.templates = self.load_templates()
    
    def load_config(self):
        """Load sharing configuration"""
        default_config = {
            "questionnaire_url": DEFAULT_SURVEY_URL,
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "sender_name": "Problem Research Team"
            },
            "email_lists": {
                "contacts": [],
                "newsletter_subscribers": [],
                "community_leaders": []
            },
            "sharing_settings": {
                "include_utm": True,
                "default_utm_source": "email",
                "default_utm_medium": "newsletter",
                "default_utm_campaign": "problem_research",
                "strategy3_registry_path": "",
                "default_survey_id": DEFAULT_SURVEY_ID,
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = {**default_config, **json.load(f)}
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_templates(self):
        """Load email and sharing templates"""
        return {
            "email_intro": {
                "subject": "Help us understand community challenges - Quick Survey",
                "html": """
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Help Us Understand Community Challenges</h2>
                        
                        <p>Hi there,</p>
                        
                        <p>We're conducting research to better understand the problems and challenges people face in their daily lives. Your insights would be incredibly valuable in helping us identify common issues and develop better solutions.</p>
                        
                        <p>The survey takes just 3-5 minutes and is completely anonymous. Your responses will help us:</p>
                        <ul>
                            <li>Identify the most pressing problems in our community</li>
                            <li>Develop targeted solutions and resources</li>
                            <li>Create better tools and services</li>
                        </ul>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{url}" style="background: #3498db; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">Take the Survey</a>
                        </div>
                        
                        <p>Thank you for your time and for helping us build a better understanding of community needs.</p>
                        
                        <p>Best regards,<br>
                        {sender_name}</p>
                        
                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                        <p style="font-size: 12px; color: #666;">
                            This email was sent because you're part of our community. 
                            <a href="{unsubscribe_url}">Unsubscribe</a> if you no longer wish to receive these emails.
                        </p>
                    </div>
                </body>
                </html>
                """,
                "text": """
                Help Us Understand Community Challenges
                
                Hi there,
                
                We're conducting research to better understand the problems and challenges people face in their daily lives. Your insights would be incredibly valuable in helping us identify common issues and develop better solutions.
                
                The survey takes just 3-5 minutes and is completely anonymous. Your responses will help us:
                - Identify the most pressing problems in our community
                - Develop targeted solutions and resources
                - Create better tools and services
                
                Take the Survey: {url}
                
                Thank you for your time and for helping us build a better understanding of community needs.
                
                Best regards,
                {sender_name}
                
                ---
                This email was sent because you're part of our community. Unsubscribe: {unsubscribe_url}
                """
            },
            "email_reminder": {
                "subject": "Quick reminder: Help us understand community challenges",
                "html": """
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Quick Reminder</h2>
                        
                        <p>Hi there,</p>
                        
                        <p>Just a quick reminder about our community challenges survey. We're still collecting responses and would love to include your insights.</p>
                        
                        <p>The survey takes just 3-5 minutes and is completely anonymous. Your input helps us understand what problems matter most to people like you.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{url}" style="background: #e74c3c; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">Take the Survey Now</a>
                        </div>
                        
                        <p>Thank you for your time!</p>
                        
                        <p>Best regards,<br>
                        {sender_name}</p>
                    </div>
                </body>
                </html>
                """,
                "text": """
                Quick Reminder
                
                Hi there,
                
                Just a quick reminder about our community challenges survey. We're still collecting responses and would love to include your insights.
                
                The survey takes just 3-5 minutes and is completely anonymous. Your input helps us understand what problems matter most to people like you.
                
                Take the Survey Now: {url}
                
                Thank you for your time!
                
                Best regards,
                {sender_name}
                """
            },
            "email_thank_you": {
                "subject": "Thank you for participating in our research!",
                "html": """
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #27ae60;">Thank You!</h2>
                        
                        <p>Hi there,</p>
                        
                        <p>Thank you for taking the time to complete our community challenges survey. Your responses are incredibly valuable and will help us better understand the problems people face.</p>
                        
                        <p>We'll be analyzing the data over the next few weeks and will share insights about common challenges and potential solutions with our community.</p>
                        
                        <p>If you're interested in seeing the results, we'll be posting updates on our website and social media channels.</p>
                        
                        <p>Thanks again for your participation!</p>
                        
                        <p>Best regards,<br>
                        {sender_name}</p>
                    </div>
                </body>
                </html>
                """,
                "text": """
                Thank You!
                
                Hi there,
                
                Thank you for taking the time to complete our community challenges survey. Your responses are incredibly valuable and will help us better understand the problems people face.
                
                We'll be analyzing the data over the next few weeks and will share insights about common challenges and potential solutions with our community.
                
                If you're interested in seeing the results, we'll be posting updates on our website and social media channels.
                
                Thanks again for your participation!
                
                Best regards,
                {sender_name}
                """
            }
        }
    
    def create_utm_url(
        self,
        source: str,
        medium: str,
        campaign: str = None,
        ref: str = None,
        survey_id: str = None,
    ):
        """Create UTM-tracked URL (optional ref + survey_id for Strategy 3 distributors)."""
        if not campaign:
            campaign = self.config["sharing_settings"]["default_utm_campaign"]

        if ref or survey_id:
            return build_tracked_survey_url(
                self.config["questionnaire_url"],
                survey_id=survey_id or self.config["sharing_settings"].get(
                    "default_survey_id", DEFAULT_SURVEY_ID
                ),
                ref=ref,
                utm_source=source if not ref else ref,
                utm_medium=medium,
                utm_campaign=campaign,
                utm_content=f"email_{datetime.now().strftime('%Y%m%d')}",
            )

        utm_params = {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": campaign,
            "utm_content": f"email_{datetime.now().strftime('%Y%m%d')}",
        }

        base_url = self.config["questionnaire_url"]
        return f"{base_url}?{urlencode(utm_params)}"

    def create_distributor_url(self, distributor_ref: str, survey_id: str = None) -> str:
        """Strategy 3 paid distributor link (ref + utm_source = distributor id)."""
        return build_tracked_survey_url(
            self.config["questionnaire_url"],
            survey_id=survey_id
            or self.config["sharing_settings"].get("default_survey_id", DEFAULT_SURVEY_ID),
            ref=distributor_ref,
            utm_source=distributor_ref,
            utm_medium=STRATEGY3_UTM_MEDIUM,
            utm_campaign=STRATEGY3_UTM_CAMPAIGN,
        )

    def load_distributor_registry(self, registry_path: str) -> Dict[str, Any]:
        path = Path(registry_path)
        if not path.exists():
            raise FileNotFoundError(f"Distributor registry not found: {path}")
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    def generate_strategy3_distributor_kit(self, registry_path: str) -> Dict[str, Any]:
        """Build a sharing kit with per-distributor links from Strategy 3 registry."""
        registry = self.load_distributor_registry(registry_path)
        distributors = registry.get("distributors", [])
        kit: Dict[str, Any] = {
            "kit_type": "strategy3_distributors",
            "questionnaire_url": self.config["questionnaire_url"],
            "survey_id": registry.get("survey_id", DEFAULT_SURVEY_ID),
            "registry_path": str(Path(registry_path).resolve()),
            "distributors": [],
            "generated_at": datetime.now().isoformat(),
        }

        for dist in distributors:
            dist_id = dist.get("id") or dist.get("name", "")
            link = dist.get("link") or self.create_distributor_url(dist_id)
            kit["distributors"].append(
                {
                    "id": dist_id,
                    "name": dist.get("name", ""),
                    "channel": dist.get("channel", ""),
                    "payout_terms": dist.get("payout_terms", ""),
                    "link": link,
                    "sharing_links": self.create_sharing_links(link),
                    "responses_tracked": dist.get("responses_tracked", 0),
                }
            )

        return kit
    
    def generate_email_campaign(self, template_name: str, recipient_list: str = "contacts"):
        """Generate email campaign content"""
        if template_name not in self.templates:
            return None
        
        template = self.templates[template_name]
        utm_url = self.create_utm_url("email", "campaign", template_name)
        
        # Template variables
        variables = {
            "url": utm_url,
            "sender_name": self.config["email"]["sender_name"],
            "unsubscribe_url": f"{self.config['questionnaire_url']}/unsubscribe"
        }
        
        # Generate content
        html_content = template["html"].format(**variables)
        text_content = template["text"].format(**variables)
        
        return {
            "subject": template["subject"],
            "html": html_content,
            "text": text_content,
            "url": utm_url,
            "recipients": self.config["email_lists"][recipient_list]
        }
    
    def save_email_campaign(self, campaign: Dict[str, Any], filename: str = None):
        """Save email campaign to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_campaign_{timestamp}.json"
        
        filepath = os.path.join("generated_content", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        return filepath
    
    def create_sharing_links(self, base_url: str = None):
        """Create sharing links for different platforms"""
        base_url = base_url or self.config["questionnaire_url"]
        from urllib.parse import quote

        encoded = quote(base_url, safe="")
        text = "Help us understand problems you'd pay to solve - take our quick survey!"

        sharing_links = {
            "direct": base_url,
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={encoded}",
            "twitter": f"https://twitter.com/intent/tweet?url={encoded}&text={quote(text, safe='')}",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={encoded}",
            "whatsapp": f"https://wa.me/?text={quote(text + ' ' + base_url, safe='')}",
            "telegram": f"https://t.me/share/url?url={encoded}&text={quote(text, safe='')}",
            "email": (
                "mailto:?subject="
                + quote("Quick survey - problems you'd pay to solve", safe="")
                + "&body="
                + quote(f"Take our quick survey: {base_url}", safe="")
            ),
        }

        return sharing_links

    def save_sharing_kit(self, kit: Dict[str, Any], filename: str = None, output_dir: str = None):
        """Save complete sharing kit to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prefix = "strategy3_distributor_kit" if kit.get("kit_type") == "strategy3_distributors" else "sharing_kit"
            filename = f"{prefix}_{timestamp}.json"

        base_dir = output_dir or "generated_content"
        filepath = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as handle:
            json.dump(kit, handle, indent=2)

        return filepath

    def generate_sharing_kit(self):
        """Generate complete sharing kit with all assets"""
        sharing_kit = {
            "questionnaire_url": self.config["questionnaire_url"],
            "sharing_links": self.create_sharing_links(),
            "email_campaigns": {},
            "social_posts": {},
            "generated_at": datetime.now().isoformat(),
        }

        for template_name in ["email_intro", "email_reminder", "email_thank_you"]:
            campaign = self.generate_email_campaign(template_name)
            if campaign:
                sharing_kit["email_campaigns"][template_name] = campaign

        return sharing_kit

    def print_sharing_guide(self):
        """Print a comprehensive sharing guide"""
        print("📧 Sharing Utilities Guide")
        print("=" * 50)
        print(f"Questionnaire URL: {self.config['questionnaire_url']}")
        
        print("\n📱 Social Media Sharing Links:")
        sharing_links = self.create_sharing_links()
        for platform, url in sharing_links.items():
            print(f"{platform.upper()}: {url}")
        
        print("\n📧 Email Campaigns Available:")
        for template_name in self.templates.keys():
            campaign = self.generate_email_campaign(template_name)
            if campaign:
                print(f"\n{template_name.upper()}:")
                print(f"Subject: {campaign['subject']}")
                print(f"URL: {campaign['url']}")
                print(f"Recipients: {len(campaign['recipients'])} contacts")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Sharing Utilities for Problem Identification Tool")
    parser.add_argument("--generate", action="store_true", help="Generate sharing kit")
    parser.add_argument("--email", choices=["intro", "reminder", "thank_you"], help="Generate specific email campaign")
    parser.add_argument("--guide", action="store_true", help="Print sharing guide")
    parser.add_argument("--config", help="Update questionnaire URL in config")
    parser.add_argument(
        "--distributor-ref",
        help="Print Strategy 3 distributor URL for a ref id (e.g. jane_doe)",
    )
    parser.add_argument(
        "--strategy3-kit",
        metavar="REGISTRY",
        help="Generate per-distributor sharing kit from Strategy 3 distributor_registry.json",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for generated JSON kits (default: generated_content)",
    )

    args = parser.parse_args()

    utilities = SharingUtilities()

    if args.config:
        utilities.config["questionnaire_url"] = args.config
        utilities.save_config()
        print(f"Updated questionnaire URL to: {args.config}")

    if args.distributor_ref:
        print(utilities.create_distributor_url(args.distributor_ref))

    if args.strategy3_kit:
        kit = utilities.generate_strategy3_distributor_kit(args.strategy3_kit)
        filepath = utilities.save_sharing_kit(kit, output_dir=args.output_dir)
        print(f"Strategy 3 distributor sharing kit saved to: {filepath}")

    if args.generate:
        kit = utilities.generate_sharing_kit()
        filepath = utilities.save_sharing_kit(kit)
        print(f"Sharing kit saved to: {filepath}")
    
    if args.email:
        campaign = utilities.generate_email_campaign(f"email_{args.email}")
        if campaign:
            filepath = utilities.save_email_campaign(campaign)
            print(f"Email campaign saved to: {filepath}")
    
    if args.guide:
        utilities.print_sharing_guide()
    
    if not any(
        [args.generate, args.email, args.guide, args.config, args.distributor_ref, args.strategy3_kit]
    ):
        utilities.print_sharing_guide()

if __name__ == "__main__":
    main()
