#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 3: Network-Based Problem Identification
Automated script to help identify business problems from your network.
"""

import json
import csv
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def open_file_automatically(file_path: str) -> None:
    """
    Automatically open a file in the default system application (text editor/viewer).
    Works cross-platform: Windows, macOS, and Linux.
    """
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            print(f"\n⚠ File not found: {file_path}")
            return

        if sys.platform == "win32":
            os.startfile(str(file_path_obj.resolve()))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path_obj.resolve())])
        else:
            subprocess.run(["xdg-open", str(file_path_obj.resolve())])
        
        print(f"✓ Opened file automatically: {file_path}")
    except Exception as e:
        print(f"\n⚠ Could not open file automatically ({e}).")
        print(f"Please open manually: {file_path}")

class NetworkProblemIdentifier:
    def __init__(self):
        self.contacts = []
        self.problems = []
        self.output_file = f"network_problems_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def collect_contacts(self):
        """Step 1: Collect network contacts"""
        print("\n" + "="*60)
        print("STEP 1: Map Your Network")
        print("="*60)
        print("\nEnter your network contacts (one per line).")
        print("Press Enter twice when done.\n")
        
        contacts = []
        while True:
            contact = input("Contact name (or press Enter to finish): ").strip()
            if not contact:
                break
            
            industry = input(f"  Industry/Company for {contact}: ").strip()
            relationship = input(f"  Relationship with {contact}: ").strip()
            channel = input(f"  Best contact channel (LinkedIn/WhatsApp/Email/Phone): ").strip()
            
            contacts.append({
                'name': contact,
                'industry': industry,
                'relationship': relationship,
                'channel': channel,
                'contacted': False,
                'responded': False
            })
            print()
        
        self.contacts = contacts
        print(f"\n✓ Collected {len(contacts)} contacts")
        return contacts
    
    def generate_message_templates(self):
        """Step 2: Generate personalized message templates"""
        print("\n" + "="*60)
        print("STEP 2: Message Templates Generated")
        print("="*60)
        
        templates = []
        for contact in self.contacts:
            if contact['channel'].lower() == 'linkedin':
                template = f"""Hi {contact['name']}, I hope you're doing well! I'm working on identifying business problems that could benefit from digital solutions. Given your experience in {contact['industry']}, I'd love to hear about any challenges, inefficiencies, or frustrations you or your team face regularly. Would you be open to a quick chat about this?"""
            elif contact['channel'].lower() == 'whatsapp':
                template = f"""Hey {contact['name']}! 👋 Quick question - I'm researching business problems that need digital solutions. As someone in {contact['industry']}, what's the biggest challenge or frustration you face in your work? Would appreciate your insights!"""
            else:
                template = f"""Hi {contact['name']}, I'm reaching out because I'm working on identifying business problems that could benefit from digital solutions. Given your background in {contact['industry']}, I'd love to hear about any challenges or inefficiencies you encounter. Would you be open to sharing your thoughts?"""
            
            templates.append({
                'contact': contact['name'],
                'channel': contact['channel'],
                'template': template
            })
        
        print("\nGenerated message templates:")
        for i, msg in enumerate(templates, 1):
            print(f"\n{i}. For {msg['contact']} ({msg['channel']}):")
            print("-" * 50)
            print(msg['template'])
        
        # Save templates
        with open('message_templates.txt', 'w', encoding='utf-8') as f:
            for msg in templates:
                f.write(f"\n{'='*60}\n")
                f.write(f"To: {msg['contact']} via {msg['channel']}\n")
                f.write(f"{'='*60}\n")
                f.write(msg['template'])
                f.write("\n\n")
        
        print(f"\n✓ Templates saved to 'message_templates.txt'")
        
        user_input = input("\nDo you want to review/edit these templates? (y/n): ").strip().lower()
        if user_input == 'y':
            print("\nYou can edit the templates in 'message_templates.txt' before sending.")
        
        return templates
    
    def confirm_contacts(self):
        """Step 3: Confirm contacts before sending"""
        print("\n" + "="*60)
        print("STEP 3: Confirm Contacts")
        print("="*60)
        
        print("\nContacts to reach out to:")
        for i, contact in enumerate(self.contacts, 1):
            print(f"{i}. {contact['name']} - {contact['industry']} ({contact['channel']})")
        
        confirm = input("\nProceed with these contacts? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Please update your contacts and run again.")
            return False
        
        print("\n✓ Contacts confirmed. You can now send the messages using the templates.")
        return True
    
    def collect_problems(self):
        """Step 4: Collect problems from responses"""
        print("\n" + "="*60)
        print("STEP 4: Document Problems")
        print("="*60)
        print("\nAs you receive responses, enter the problems here.")
        print("Press Enter twice when done.\n")
        
        problems = []
        while True:
            contact_name = input("Contact name (or press Enter to finish): ").strip()
            if not contact_name:
                break
            
            problem = input("  Problem description: ").strip()
            frequency = input("  Frequency (Daily/Weekly/Monthly/Occasional): ").strip()
            urgency = input("  Urgency (High/Medium/Low): ").strip()
            current_solution = input("  Current workaround/solution: ").strip()
            willing_to_pay = input("  Willingness to pay (Yes/No/Maybe): ").strip()
            
            problems.append({
                'contact': contact_name,
                'problem': problem,
                'frequency': frequency,
                'urgency': urgency,
                'current_solution': current_solution,
                'willing_to_pay': willing_to_pay,
                'timestamp': datetime.now().isoformat()
            })
            print()
        
        self.problems = problems
        print(f"\n✓ Collected {len(problems)} problems")
        return problems
    
    def analyze_patterns(self):
        """Step 5: Analyze patterns in problems"""
        print("\n" + "="*60)
        print("STEP 5: Pattern Analysis")
        print("="*60)
        
        if not self.problems:
            print("No problems collected yet. Please collect problems first.")
            return
        
        # Frequency analysis
        frequency_count = {}
        urgency_count = {}
        
        for problem in self.problems:
            freq = problem['frequency']
            urgency = problem['urgency']
            frequency_count[freq] = frequency_count.get(freq, 0) + 1
            urgency_count[urgency] = urgency_count.get(urgency, 0) + 1
        
        print("\nFrequency Distribution:")
        for freq, count in sorted(frequency_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {freq}: {count} problems")
        
        print("\nUrgency Distribution:")
        for urg, count in sorted(urgency_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {urg}: {count} problems")
        
        # High-value problems (high frequency + high urgency)
        high_value = [p for p in self.problems 
                     if p['frequency'] in ['Daily', 'Weekly'] 
                     and p['urgency'] == 'High']
        
        print(f"\n✓ Found {len(high_value)} high-value problems (High frequency + High urgency)")
        
        if high_value:
            print("\nHigh-Value Problems:")
            for i, problem in enumerate(high_value, 1):
                print(f"\n{i}. From {problem['contact']}:")
                print(f"   Problem: {problem['problem']}")
                print(f"   Frequency: {problem['frequency']}, Urgency: {problem['urgency']}")
        
        return high_value
    
    def generate_chatgpt_prompt(self):
        """Step 6: Generate ChatGPT prompt"""
        print("\n" + "="*60)
        print("STEP 6: ChatGPT Prompt Generation")
        print("="*60)
        
        if not self.problems:
            print("No problems to analyze. Please collect problems first.")
            return
        
        print("\nSelect problems to analyze (enter numbers separated by commas, or 'all'):")
        for i, problem in enumerate(self.problems, 1):
            print(f"{i}. [{problem['frequency']}/{problem['urgency']}] {problem['problem'][:60]}...")
        
        selection = input("\nSelection: ").strip()
        
        if selection.lower() == 'all':
            selected_problems = self.problems
        else:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_problems = [self.problems[i] for i in indices if 0 <= i < len(self.problems)]
        
        # Generate prompt
        prompt = "Ideas to solve business problems from your network. Request for business problems to solve from people in your network.\n\n"
        prompt += "Problems identified:\n"
        for i, problem in enumerate(selected_problems, 1):
            prompt += f"\n{i}. From {problem['contact']}:\n"
            prompt += f"   Problem: {problem['problem']}\n"
            prompt += f"   Frequency: {problem['frequency']}\n"
            prompt += f"   Urgency: {problem['urgency']}\n"
            prompt += f"   Current solution: {problem['current_solution']}\n"
            prompt += f"   Willingness to pay: {problem['willing_to_pay']}\n"
        
        prompt += "\n\nPlease provide business ideas that can solve these problems with digital solutions."
        
        # Save prompt
        with open('chatgpt_prompt.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print("\n✓ ChatGPT prompt generated and saved to 'chatgpt_prompt.txt'")
        print("\nYou can now copy this prompt to ChatGPT.")
        
        return prompt
    
    def save_data(self):
        """Save all data to JSON file"""
        data = {
            'contacts': self.contacts,
            'problems': self.problems,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ All data saved to '{self.output_file}'")
        open_file_automatically(self.output_file)
    
    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("Business Idea Formulation Strategy 3")
        print("Network-Based Problem Identification")
        print("="*60)
        
        # Step 1: Collect contacts
        self.collect_contacts()
        
        # Step 2: Generate templates
        self.generate_message_templates()
        
        # Step 3: Confirm contacts
        if not self.confirm_contacts():
            return
        
        # Step 4: Collect problems (user will do this after sending messages)
        input("\nPress Enter when you're ready to start collecting problem responses...")
        self.collect_problems()
        
        # Step 5: Analyze patterns
        high_value = self.analyze_patterns()
        
        # Step 6: Generate ChatGPT prompt
        self.generate_chatgpt_prompt()
        
        # Save all data
        self.save_data()
        
        print("\n" + "="*60)
        print("Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Copy the prompt from 'chatgpt_prompt.txt' to ChatGPT")
        print("2. Use Prompt 1b from the main strategy document for detailed analysis")
        print("3. Review the generated business ideas")
        print("4. Select top 3-5 ideas for further validation")

if __name__ == "__main__":
    identifier = NetworkProblemIdentifier()
    identifier.run()

