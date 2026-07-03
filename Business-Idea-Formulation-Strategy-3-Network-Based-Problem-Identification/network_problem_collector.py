#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 3: Network-Based Problem Identification
Automated script to help identify business problems from your network.

Classic mode (default):
    python network_problem_collector.py

Paid distributor mode (Phase B2):
    python network_problem_collector.py --distributor
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from distributor_links import (
    DistributorLinkManager,
    count_responses_by_ref,
    load_survey_responses_export,
)


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
    def __init__(self) -> None:
        self.contacts: list[dict[str, Any]] = []
        self.distributors: list[dict[str, Any]] = []
        self.problems: list[dict[str, Any]] = []
        self.workflow = "classic"
        self.output_file = f"network_problems_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.strategy_dir = Path(__file__).resolve().parent
        self.link_manager = DistributorLinkManager(strategy_dir=self.strategy_dir)

    def collect_contacts(self) -> list[dict[str, Any]]:
        """Step 1: Collect network contacts"""
        print("\n" + "=" * 60)
        print("STEP 1: Map Your Network")
        print("=" * 60)
        print("\nEnter your network contacts (one per line).")
        print("Press Enter twice when done.\n")

        contacts: list[dict[str, Any]] = []
        while True:
            contact = input("Contact name (or press Enter to finish): ").strip()
            if not contact:
                break

            industry = input(f"  Industry/Company for {contact}: ").strip()
            relationship = input(f"  Relationship with {contact}: ").strip()
            channel = input(f"  Best contact channel (LinkedIn/WhatsApp/Email/Phone): ").strip()

            contacts.append(
                {
                    "name": contact,
                    "industry": industry,
                    "relationship": relationship,
                    "channel": channel,
                    "contacted": False,
                    "responded": False,
                }
            )
            print()

        self.contacts = contacts
        print(f"\n✓ Collected {len(contacts)} contacts")
        return contacts

    def collect_distributors(self) -> list[dict[str, Any]]:
        """Step 1 (distributor mode): Register paid sharers with unique survey links."""
        print("\n" + "=" * 60)
        print("STEP 1: Register Paid Distributors")
        print("=" * 60)
        print("\nEnter people you'll pay to share the I'll pay to.. survey.")
        print("Press Enter on name when done.\n")

        distributors: list[dict[str, Any]] = []
        while True:
            name = input("Distributor name (or press Enter to finish): ").strip()
            if not name:
                break

            channel = input(f"  Best channel for {name} (WhatsApp/LinkedIn/Email): ").strip()
            payout = input(f"  Payout terms for {name}: ").strip()
            industry = input(f"  Network niche / industry (optional): ").strip()
            notes = input(f"  Internal notes (optional): ").strip()

            record = self.link_manager.add_distributor(
                name=name,
                channel=channel,
                payout_terms=payout,
                industry=industry,
                notes=notes,
            )
            record["contact_type"] = "paid_distributor"
            record["contacted"] = False
            record["responded"] = False
            distributors.append(record)
            print(f"  ✓ Link: {record['link']}\n")

        self.distributors = distributors
        print(f"\n✓ Registered {len(distributors)} distributors")
        return distributors

    def generate_message_templates(self) -> list[dict[str, str]]:
        """Step 2: Generate personalized message templates"""
        print("\n" + "=" * 60)
        print("STEP 2: Message Templates Generated")
        print("=" * 60)

        templates: list[dict[str, str]] = []
        for contact in self.contacts:
            if contact["channel"].lower() == "linkedin":
                template = (
                    f"Hi {contact['name']}, I hope you're doing well! I'm working on identifying "
                    f"business problems that could benefit from digital solutions. Given your experience "
                    f"in {contact['industry']}, I'd love to hear about any challenges, inefficiencies, "
                    f"or frustrations you or your team face regularly. Would you be open to a quick chat about this?"
                )
            elif contact["channel"].lower() == "whatsapp":
                template = (
                    f"Hey {contact['name']}! 👋 Quick question - I'm researching business problems that need "
                    f"digital solutions. As someone in {contact['industry']}, what's the biggest challenge or "
                    f"frustration you face in your work? Would appreciate your insights!"
                )
            else:
                template = (
                    f"Hi {contact['name']}, I'm reaching out because I'm working on identifying business "
                    f"problems that could benefit from digital solutions. Given your background in "
                    f"{contact['industry']}, I'd love to hear about any challenges or inefficiencies you "
                    f"encounter. Would you be open to sharing your thoughts?"
                )

            templates.append(
                {
                    "contact": contact["name"],
                    "channel": contact["channel"],
                    "template": template,
                }
            )

        print("\nGenerated message templates:")
        for i, msg in enumerate(templates, 1):
            print(f"\n{i}. For {msg['contact']} ({msg['channel']}):")
            print("-" * 50)
            print(msg["template"])

        with open(self.strategy_dir / "message_templates.txt", "w", encoding="utf-8") as handle:
            for msg in templates:
                handle.write(f"\n{'=' * 60}\n")
                handle.write(f"To: {msg['contact']} via {msg['channel']}\n")
                handle.write(f"{'=' * 60}\n")
                handle.write(msg["template"])
                handle.write("\n\n")

        print("\n✓ Templates saved to 'message_templates.txt'")

        user_input = input("\nDo you want to review/edit these templates? (y/n): ").strip().lower()
        if user_input == "y":
            print("\nYou can edit the templates in 'message_templates.txt' before sending.")

        return templates

    def generate_distributor_outreach(self) -> Path:
        """Step 2 (distributor mode): Generate outreach from B1 templates."""
        print("\n" + "=" * 60)
        print("STEP 2: Distributor Outreach Messages")
        print("=" * 60)

        ids = [d["id"] for d in self.distributors]
        out_path = self.link_manager.generate_outreach_file(distributor_ids=ids)
        print(f"\n✓ Outreach saved to '{out_path.name}'")
        open_file_automatically(str(out_path))
        return out_path

    def confirm_contacts(self) -> bool:
        """Step 3: Confirm contacts before sending"""
        print("\n" + "=" * 60)
        print("STEP 3: Confirm Contacts")
        print("=" * 60)

        print("\nContacts to reach out to:")
        for i, contact in enumerate(self.contacts, 1):
            print(f"{i}. {contact['name']} - {contact['industry']} ({contact['channel']})")

        confirm = input("\nProceed with these contacts? (y/n): ").strip().lower()
        if confirm != "y":
            print("Please update your contacts and run again.")
            return False

        print("\n✓ Contacts confirmed. You can now send the messages using the templates.")
        return True

    def confirm_distributors(self) -> bool:
        """Step 3 (distributor mode): Confirm distributors before outreach."""
        print("\n" + "=" * 60)
        print("STEP 3: Confirm Distributors")
        print("=" * 60)

        print("\nDistributors to pay and brief:")
        for i, dist in enumerate(self.distributors, 1):
            print(f"{i}. {dist['name']} ({dist['id']}) — {dist.get('channel') or 'n/a'}")
            print(f"   Payout: {dist.get('payout_terms') or 'n/a'}")
            print(f"   Link: {dist['link']}")

        confirm = input("\nProceed with these distributors? (y/n): ").strip().lower()
        if confirm != "y":
            print("Please update distributors and run again.")
            return False

        print("\n✓ Distributors confirmed. Send each person their section from the outreach file.")
        return True

    def sync_response_counts_from_export(self) -> None:
        """Optional: update registry counts from exported survey JSON."""
        print("\n" + "=" * 60)
        print("STEP 4b: Sync Response Counts (optional)")
        print("=" * 60)
        print("\nExport responses from the survey dashboard, then provide the JSON file path.")
        print("Press Enter to skip.\n")

        path_str = input("Path to questionnaire export JSON: ").strip()
        if not path_str:
            print("Skipped response sync.")
            return

        export_path = Path(path_str)
        if not export_path.exists():
            print(f"⚠ File not found: {export_path}")
            return

        try:
            responses = load_survey_responses_export(export_path)
            counts = count_responses_by_ref(responses)
            self.link_manager.update_response_counts(counts)
            self.distributors = self.link_manager.list_distributors()
            print("\n✓ Response counts updated in distributor_registry.json:")
            for dist_id, count in sorted(counts.items()):
                print(f"  {dist_id}: {count}")
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            print(f"⚠ Could not sync counts: {exc}")

    def collect_problems(self) -> list[dict[str, Any]]:
        """Step 4: Collect problems from responses"""
        print("\n" + "=" * 60)
        print("STEP 4: Document Problems")
        print("=" * 60)
        print("\nAs you receive responses, enter the problems here.")
        print("Press Enter twice when done.\n")

        problems: list[dict[str, Any]] = []
        while True:
            contact_name = input("Contact name (or press Enter to finish): ").strip()
            if not contact_name:
                break

            problem = input("  Problem description: ").strip()
            frequency = input("  Frequency (Daily/Weekly/Monthly/Occasional): ").strip()
            urgency = input("  Urgency (High/Medium/Low): ").strip()
            current_solution = input("  Current workaround/solution: ").strip()
            willing_to_pay = input("  Willingness to pay (Yes/No/Maybe): ").strip()
            source_ref = ""
            if self.workflow == "distributor":
                source_ref = input("  Distributor ref id (optional): ").strip()

            entry: dict[str, Any] = {
                "contact": contact_name,
                "problem": problem,
                "frequency": frequency,
                "urgency": urgency,
                "current_solution": current_solution,
                "willing_to_pay": willing_to_pay,
                "timestamp": datetime.now().isoformat(),
            }
            if source_ref:
                entry["distributor_ref"] = source_ref
            problems.append(entry)
            print()

        self.problems = problems
        print(f"\n✓ Collected {len(problems)} problems")
        return problems

    def analyze_patterns(self) -> list[dict[str, Any]] | None:
        """Step 5: Analyze patterns in problems"""
        print("\n" + "=" * 60)
        print("STEP 5: Pattern Analysis")
        print("=" * 60)

        if not self.problems:
            print("No problems collected yet. Please collect problems first.")
            return None

        frequency_count: dict[str, int] = {}
        urgency_count: dict[str, int] = {}

        for problem in self.problems:
            freq = problem["frequency"]
            urgency = problem["urgency"]
            frequency_count[freq] = frequency_count.get(freq, 0) + 1
            urgency_count[urgency] = urgency_count.get(urgency, 0) + 1

        print("\nFrequency Distribution:")
        for freq, count in sorted(frequency_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {freq}: {count} problems")

        print("\nUrgency Distribution:")
        for urg, count in sorted(urgency_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {urg}: {count} problems")

        high_value = [
            p
            for p in self.problems
            if p["frequency"] in ["Daily", "Weekly"] and p["urgency"] == "High"
        ]

        print(f"\n✓ Found {len(high_value)} high-value problems (High frequency + High urgency)")

        if high_value:
            print("\nHigh-Value Problems:")
            for i, problem in enumerate(high_value, 1):
                print(f"\n{i}. From {problem['contact']}:")
                print(f"   Problem: {problem['problem']}")
                print(f"   Frequency: {problem['frequency']}, Urgency: {problem['urgency']}")

        return high_value

    def generate_chatgpt_prompt(self) -> str | None:
        """Step 6: Generate ChatGPT prompt"""
        print("\n" + "=" * 60)
        print("STEP 6: ChatGPT Prompt Generation")
        print("=" * 60)

        if not self.problems:
            print("No problems to analyze. Please collect problems first.")
            return None

        print("\nSelect problems to analyze (enter numbers separated by commas, or 'all'):")
        for i, problem in enumerate(self.problems, 1):
            print(f"{i}. [{problem['frequency']}/{problem['urgency']}] {problem['problem'][:60]}...")

        selection = input("\nSelection: ").strip()

        if selection.lower() == "all":
            selected_problems = self.problems
        else:
            indices = [int(x.strip()) - 1 for x in selection.split(",")]
            selected_problems = [self.problems[i] for i in indices if 0 <= i < len(self.problems)]

        prompt = (
            "Ideas to solve business problems from your network. Request for business problems "
            "to solve from people in your network.\n\nProblems identified:\n"
        )
        for i, problem in enumerate(selected_problems, 1):
            prompt += f"\n{i}. From {problem['contact']}:\n"
            prompt += f"   Problem: {problem['problem']}\n"
            prompt += f"   Frequency: {problem['frequency']}\n"
            prompt += f"   Urgency: {problem['urgency']}\n"
            prompt += f"   Current solution: {problem['current_solution']}\n"
            prompt += f"   Willingness to pay: {problem['willing_to_pay']}\n"
            if problem.get("distributor_ref"):
                prompt += f"   Distributor ref: {problem['distributor_ref']}\n"

        prompt += "\n\nPlease provide business ideas that can solve these problems with digital solutions."

        prompt_path = self.strategy_dir / "chatgpt_prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")

        print("\n✓ ChatGPT prompt generated and saved to 'chatgpt_prompt.txt'")
        print("\nYou can now copy this prompt to ChatGPT.")
        return prompt

    def save_data(self) -> None:
        """Save all data to JSON file"""
        data: dict[str, Any] = {
            "workflow": self.workflow,
            "contacts": self.contacts,
            "distributors": self.distributors,
            "problems": self.problems,
            "timestamp": datetime.now().isoformat(),
        }

        output_path = self.strategy_dir / self.output_file
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)

        print(f"\n✓ All data saved to '{self.output_file}'")
        open_file_automatically(str(output_path))

    def run(self) -> None:
        """Classic main execution flow (unchanged behavior)."""
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 3")
        print("Network-Based Problem Identification")
        print("=" * 60)

        self.collect_contacts()
        self.generate_message_templates()

        if not self.confirm_contacts():
            return

        input("\nPress Enter when you're ready to start collecting problem responses...")
        self.collect_problems()
        self.analyze_patterns()
        self.generate_chatgpt_prompt()
        self.save_data()

        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Copy the prompt from 'chatgpt_prompt.txt' to ChatGPT")
        print("2. Use Prompt 1b from the main strategy document for detailed analysis")
        print("3. Review the generated business ideas")
        print("4. Select top 3-5 ideas for further validation")

    def run_distributor(self) -> None:
        """Paid distributor workflow using ill_pay_to_v1 survey links."""
        self.workflow = "distributor"
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 3")
        print("Paid Distributor Survey Sharing (Phase B2)")
        print("=" * 60)
        print("\nSurvey: I'll pay to.. (ill_pay_to_v1)")
        print("See distributor_brief.md for qualified-response rules.\n")

        self.collect_distributors()
        if not self.distributors:
            print("No distributors registered. Exiting.")
            return

        self.generate_distributor_outreach()
        if not self.confirm_distributors():
            return

        input("\nPress Enter when distributors have shared the survey and responses are coming in...")
        self.sync_response_counts_from_export()
        self.collect_problems()
        self.analyze_patterns()
        self.generate_chatgpt_prompt()
        self.save_data()

        print("\n" + "=" * 60)
        print("Distributor Workflow Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Pay distributors per your agreed terms")
        print("2. Copy the prompt from 'chatgpt_prompt.txt' to ChatGPT")
        print("3. Review distributor_registry.json for response counts")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Strategy 3 network-based problem identification",
    )
    parser.add_argument(
        "--distributor",
        action="store_true",
        help="Run paid distributor survey workflow (default: classic network outreach)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    identifier = NetworkProblemIdentifier()
    if args.distributor:
        identifier.run_distributor()
    else:
        identifier.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
