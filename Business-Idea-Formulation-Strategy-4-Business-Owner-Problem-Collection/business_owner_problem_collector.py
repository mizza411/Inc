#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 4: Business Owner Problem Collection
Automated script to help collect and analyze business problems from business owners.
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

class BusinessOwnerProblemCollector:
    def __init__(self):
        self.business_owners = []
        self.responses = []
        self.problems = []
        self.output_file = f"business_owner_problems_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def generate_questionnaire_template(self):
        """Step 1: Generate questionnaire template"""
        print("\n" + "="*60)
        print("STEP 1: Questionnaire Template")
        print("="*60)
        
        questions = [
            "What is your biggest business challenge right now?",
            "What process in your business takes too much time?",
            "What do you spend too much money on?",
            "What technology tool do you wish existed for your business?",
            "What manual task would you like to automate?",
            "What customer complaint do you hear most often?",
            "What keeps you up at night regarding your business?",
            "If you had a magic wand, what business problem would you solve first?"
        ]
        
        print("\nQuestionnaire Questions:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")
        
        # Save template
        with open('questionnaire_template.txt', 'w', encoding='utf-8') as f:
            f.write("Business Problem Collection Questionnaire\n")
            f.write("="*60 + "\n\n")
            for i, q in enumerate(questions, 1):
                f.write(f"{i}. {q}\n\n")
            f.write("\nNote: You can customize these questions in your Google Form.\n")
            f.write("Link to template: https://docs.google.com/document/d/1FPc4Vo9GiqPG_L_3GdJ1R4tB8u_ajCV9lDmrwESr0H8/edit\n")
        
        print(f"\n✓ Template saved to 'questionnaire_template.txt'")
        return questions
    
    def collect_business_owners(self):
        """Step 2: Collect business owner contacts"""
        print("\n" + "="*60)
        print("STEP 2: Identify Target Business Owners")
        print("="*60)
        print("\nEnter business owner contacts (one per line).")
        print("Press Enter twice when done.\n")
        
        owners = []
        while True:
            name = input("Business owner name (or press Enter to finish): ").strip()
            if not name:
                break
            
            business_name = input(f"  Business name: ").strip()
            industry = input(f"  Industry: ").strip()
            email = input(f"  Email (optional): ").strip()
            phone = input(f"  Phone (optional): ").strip()
            contact_method = input(f"  Preferred contact method (Email/Phone/LinkedIn): ").strip()
            
            owners.append({
                'name': name,
                'business_name': business_name,
                'industry': industry,
                'email': email,
                'phone': phone,
                'contact_method': contact_method,
                'invited': False,
                'responded': False
            })
            print()
        
        self.business_owners = owners
        print(f"\n✓ Collected {len(owners)} business owner contacts")
        return owners
    
    def generate_invitation_messages(self):
        """Step 3: Generate invitation messages"""
        print("\n" + "="*60)
        print("STEP 3: Invitation Messages")
        print("="*60)
        
        messages = []
        for owner in self.business_owners:
            if owner['contact_method'].lower() == 'email':
                message = f"""Subject: Quick Question About Your Business Challenges

Hi {owner['name']},

I hope this email finds you well. I'm {input('Your name: ')} and I'm working on identifying business problems that could benefit from digital solutions.

I'd love to get your insights on the challenges you face running {owner['business_name']}. Would you be willing to take a quick 3-minute survey? Your input would be incredibly valuable.

Here's the link: [Your Google Form Link]

Thank you for your time!

Best regards"""
            else:
                message = f"""Hi {owner['name']}! I'm researching business challenges and would love your input. Would you be open to a quick 3-minute survey about challenges you face at {owner['business_name']}? [Link]"""
            
            messages.append({
                'owner': owner['name'],
                'business': owner['business_name'],
                'method': owner['contact_method'],
                'message': message
            })
        
        # Save messages
        with open('invitation_messages.txt', 'w', encoding='utf-8') as f:
            for msg in messages:
                f.write(f"\n{'='*60}\n")
                f.write(f"To: {msg['owner']} ({msg['business']}) via {msg['method']}\n")
                f.write(f"{'='*60}\n")
                f.write(msg['message'])
                f.write("\n\n")
        
        print("\nGenerated invitation messages:")
        for i, msg in enumerate(messages, 1):
            print(f"\n{i}. For {msg['owner']} ({msg['business']}):")
            print("-" * 50)
            print(msg['message'][:200] + "...")
        
        print(f"\n✓ Messages saved to 'invitation_messages.txt'")
        return messages
    
    def collect_responses(self):
        """Step 4: Collect questionnaire responses"""
        print("\n" + "="*60)
        print("STEP 4: Collect Responses")
        print("="*60)
        print("\nEnter responses as you receive them.")
        print("Press Enter twice when done.\n")
        
        responses = []
        while True:
            owner_name = input("Business owner name (or press Enter to finish): ").strip()
            if not owner_name:
                break
            
            print("\nEnter their responses to key questions:")
            challenge = input("  Biggest business challenge: ").strip()
            time_waster = input("  Process that takes too much time: ").strip()
            money_waster = input("  What they spend too much money on: ").strip()
            wish_tool = input("  Technology tool they wish existed: ").strip()
            automation = input("  Manual task to automate: ").strip()
            
            responses.append({
                'owner': owner_name,
                'challenge': challenge,
                'time_waster': time_waster,
                'money_waster': money_waster,
                'wish_tool': wish_tool,
                'automation': automation,
                'timestamp': datetime.now().isoformat()
            })
            print()
        
        self.responses = responses
        print(f"\n✓ Collected {len(responses)} responses")
        return responses
    
    def analyze_problems(self):
        """Step 5: Analyze and categorize problems"""
        print("\n" + "="*60)
        print("STEP 5: Problem Analysis")
        print("="*60)
        
        if not self.responses:
            print("No responses collected yet.")
            return
        
        # Extract all problems
        all_problems = []
        for response in self.responses:
            if response['challenge']:
                all_problems.append({
                    'type': 'Challenge',
                    'description': response['challenge'],
                    'owner': response['owner']
                })
            if response['time_waster']:
                all_problems.append({
                    'type': 'Time Waster',
                    'description': response['time_waster'],
                    'owner': response['owner']
                })
            if response['money_waster']:
                all_problems.append({
                    'type': 'Money Waster',
                    'description': response['money_waster'],
                    'owner': response['owner']
                })
            if response['wish_tool']:
                all_problems.append({
                    'type': 'Wish Tool',
                    'description': response['wish_tool'],
                    'owner': response['owner']
                })
            if response['automation']:
                all_problems.append({
                    'type': 'Automation Need',
                    'description': response['automation'],
                    'owner': response['owner']
                })
        
        self.problems = all_problems
        
        # Count by type
        type_count = {}
        for problem in all_problems:
            ptype = problem['type']
            type_count[ptype] = type_count.get(ptype, 0) + 1
        
        print("\nProblem Categories:")
        for ptype, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ptype}: {count} mentions")
        
        # Find common themes (simple keyword matching)
        print(f"\n✓ Identified {len(all_problems)} total problems")
        
        return all_problems
    
    def generate_chatgpt_prompt(self):
        """Step 6: Generate ChatGPT prompt"""
        print("\n" + "="*60)
        print("STEP 6: ChatGPT Prompt Generation")
        print("="*60)
        
        if not self.problems:
            print("No problems to analyze.")
            return
        
        # Group by type
        problems_by_type = {}
        for problem in self.problems:
            ptype = problem['type']
            if ptype not in problems_by_type:
                problems_by_type[ptype] = []
            problems_by_type[ptype].append(problem)
        
        print("\nProblems by category:")
        for ptype, probs in problems_by_type.items():
            print(f"\n{ptype} ({len(probs)} problems):")
            for i, prob in enumerate(probs[:3], 1):  # Show first 3
                print(f"  {i}. {prob['description'][:60]}...")
            if len(probs) > 3:
                print(f"  ... and {len(probs) - 3} more")
        
        # Generate prompt
        prompt = "Ideas to solve business owners' self-identified problems.\n\n"
        prompt += "Problems identified from business owner questionnaires:\n\n"
        
        for ptype, probs in problems_by_type.items():
            prompt += f"{ptype}:\n"
            for prob in probs:
                prompt += f"- {prob['description']} (from {prob['owner']})\n"
            prompt += "\n"
        
        prompt += "\nPlease provide business ideas that can solve these problems with digital solutions."
        
        # Save prompt
        with open('chatgpt_prompt.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print("\n✓ ChatGPT prompt generated and saved to 'chatgpt_prompt.txt'")
        return prompt
    
    def save_data(self):
        """Save all data"""
        data = {
            'business_owners': self.business_owners,
            'responses': self.responses,
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
        print("Business Idea Formulation Strategy 4")
        print("Business Owner Problem Collection")
        print("="*60)
        
        # Step 1: Generate questionnaire
        self.generate_questionnaire_template()
        
        # Step 2: Collect business owners
        self.collect_business_owners()
        
        # Step 3: Generate invitations
        self.generate_invitation_messages()
        
        # Step 4: Collect responses
        input("\nPress Enter when you're ready to start collecting responses...")
        self.collect_responses()
        
        # Step 5: Analyze problems
        self.analyze_problems()
        
        # Step 6: Generate ChatGPT prompt
        self.generate_chatgpt_prompt()
        
        # Save data
        self.save_data()
        
        print("\n" + "="*60)
        print("Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Copy the prompt from 'chatgpt_prompt.txt' to ChatGPT")
        print("2. Use Prompt 1b from the main strategy document")
        print("3. Review generated business ideas")

if __name__ == "__main__":
    collector = BusinessOwnerProblemCollector()
    collector.run()

