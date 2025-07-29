"""
Gadget Business CLI Automation App
Chains all automation scripts in sequence for a specific gadget.
Displays a notice that a GUI may be needed later.
"""

import sys
import argparse
import os
from demand_driven_sourcing import get_demand_driven_gadgets

# Import all automation modules
from funding_application import apply_for_grants, launch_crowdfunding_campaign, send_pitch_to_investors
from supplier_api_integration import fetch_supplier_inventory
from inventory_monitor import monitor_inventory, automate_restock
from product_listing_automation import bulk_generate_listings
from price_comparison_bot import scrape_competitor_prices, suggest_optimal_price
from ad_campaign_manager import launch_ad_campaign, monitor_ad_performance
from lead_generation_bot import capture_lead_via_chatbot, capture_lead_via_landing_page
from order_fulfillment import process_payment, arrange_shipping
from shipping_tracker import track_shipment
from support_chatbot import handle_customer_query
from feedback_collector import send_feedback_request
from dashboard_automation import generate_dashboard
from alert_system import check_and_alert

BORDER = "=" * 60
NOTICE = f"""
{BORDER}
GADGET BUSINESS AUTOMATION CLI (MVP)
NOTE: This is a CLI prototype. A GUI may be needed for non-technical users in the future.
{BORDER}
"""

def display_gadgets(gadgets):
    """Display available gadgets with demand analysis and sourcing options."""
    print("\nAvailable Gadgets (Demand-Driven Sourcing):")
    print("-" * 120)
    print(f"{'Index':<6} {'Name':<25} {'Demand':<8} {'Score':<6} {'Trend':<10} {'Best Source':<20}")
    print("-" * 120)
    for idx, gadget in enumerate(gadgets):
        demand_level = gadget.get('demand_level', 'N/A')
        demand_score = gadget.get('demand_score', 0)
        trend = gadget.get('trend', 'N/A')  # Changed from 'trending' to 'trend'
        
        # Use the best_source field from demand-driven sourcing
        best_source = gadget.get('best_source', 'N/A')  # Use the calculated best source
        
        print(f"{idx:<6} {gadget['name']:<25} {demand_level:<8} {demand_score:<6} {trend:<10} {best_source:<20}")
    print("-" * 120)

def main():
    print(NOTICE)
    parser = argparse.ArgumentParser(description="Run the full gadget business automation pipeline for a specific gadget.")
    parser.add_argument('--list', action='store_true', help='List all available gadgets with demand analysis')
    parser.add_argument('--gadget-index', type=int, help='Process gadget by index (from --list)')
    parser.add_argument('--all', action='store_true', help='Run all stages in sequence for the gadget')
    parser.add_argument('--stage', type=str, help='Run a specific stage for the gadget (funding, sourcing, inventory, listing, pricing, marketing, leads, fulfillment, shipping, support, feedback, dashboard, alerts)')
    args = parser.parse_args()

    # Get demand-driven gadgets
    print("Analyzing demand and finding sourcing options...")
    gadgets = get_demand_driven_gadgets()
    if not gadgets:
        print("No gadgets found!")
        return

    # Handle --list argument
    if args.list:
        display_gadgets(gadgets)
        return

    # Determine which gadget to process
    selected_gadget = None
    if args.gadget_index is not None and 0 <= args.gadget_index < len(gadgets):
        selected_gadget = gadgets[args.gadget_index]
    else:
        print("Please select a gadget by index:")
        display_gadgets(gadgets)
        try:
            idx = int(input("Enter gadget index: ").strip())
            if 0 <= idx < len(gadgets):
                selected_gadget = gadgets[idx]
            else:
                print("Invalid gadget index!")
                return
        except Exception:
            print("Invalid input!")
            return

    # Run the automation
    if args.all:
        run_all_stages(selected_gadget)
    elif args.stage:
        run_stage(args.stage, selected_gadget)
    else:
        parser.print_help()

def run_all_stages(gadget):
    print(f"\nProcessing gadget: {gadget['name']} (Demand: {gadget['demand_level']})\n")
    # 1. Funding & Capital Acquisition
    print("[1] Funding & Capital Acquisition...")
    grants = ["https://example.com/grant1", "https://example.com/loan2"]
    business = {"name": f"{gadget['name']} Business", "owner": "Jane Doe"}
    print(apply_for_grants(grants, business))
    print(launch_crowdfunding_campaign("Kickstarter", {"title": f"{gadget['name']} Launch", "goal": 10000}))
    investors = ["investor1@email.com", "investor2@email.com"]
    print(send_pitch_to_investors(investors, "pitch_deck.pdf"))

    # 2. Supplier Sourcing & Inventory Management
    print("\n[2] Supplier Sourcing & Inventory Management...")
    suppliers = [f"https://api.supplier1.com/inventory/{gadget['name']}", f"https://api.supplier2.com/inventory/{gadget['name']}"]
    inventory_data = fetch_supplier_inventory(suppliers)
    print(inventory_data)

    # 3. Inventory Monitoring
    print("\n[3] Inventory Monitoring...")
    stock = {gadget['name']: 5}
    print(monitor_inventory(stock))
    print(automate_restock(gadget['name'], 20))

    # 4. Product Listing & Pricing
    print("\n[4] Product Listing & Pricing...")
    products = [
        {"name": gadget['name'], "features": "N/A", "price": "$299"}
    ]
    listings = bulk_generate_listings(products)
    print(listings)
    competitors = [f"https://competitor1.com/product/{gadget['name']}", f"https://competitor2.com/product/{gadget['name']}"]
    prices = scrape_competitor_prices(gadget['name'], competitors)
    print(prices)
    print(suggest_optimal_price(prices, 100.0))

    # 5. Customer Acquisition & Marketing
    print("\n[5] Customer Acquisition & Marketing...")
    ad = {"headline": f"Buy the latest {gadget['name']}!", "image": "ad.jpg", "budget": 100}
    print(launch_ad_campaign("Facebook", ad))
    print(monitor_ad_performance("Facebook", "campaign123"))
    chatbot_lead = {"name": "Alice", "email": "alice@email.com", "interest": gadget['name']}
    print(capture_lead_via_chatbot(chatbot_lead))
    landing_lead = {"email": "bob@email.com", "interest": gadget['name']}
    print(capture_lead_via_landing_page(landing_lead))

    # 6. Order Processing & Fulfillment
    print("\n[6] Order Processing & Fulfillment...")
    payment = {"card": "****1234", "amount": 100}
    shipping = {"address": "123 Main St", "courier": "DHL"}
    print(process_payment("order001", payment))
    print(arrange_shipping("order001", shipping))
    print(track_shipment("TRACK123", "DHL"))

    # 7. Customer Support & Retention
    print("\n[7] Customer Support & Retention...")
    print(handle_customer_query(f"How do I track my {gadget['name']} order?"))
    customers = ["alice@email.com", "bob@email.com"]
    print(send_feedback_request(customers, "order001"))

    # 8. Analytics & Optimization
    print("\n[8] Analytics & Optimization...")
    metrics = {"sales": 10000, "inventory": 250, "returns": 5}
    print(generate_dashboard(metrics))
    thresholds = {"stock": 10, "reviews": 4.0}
    print(check_and_alert({"stock": 5, "returns": 10, "reviews": 3.5}, thresholds))

    print("\nPipeline complete.\n")

def run_stage(stage, gadget):
    print(f"\nRunning stage: {stage} for gadget: {gadget['name']} (Demand: {gadget['demand_level']})")
    # Map stage names to functions
    if stage == "funding":
        grants = ["https://example.com/grant1", "https://example.com/loan2"]
        business = {"name": f"{gadget['name']} Business", "owner": "Jane Doe"}
        print(apply_for_grants(grants, business))
        print(launch_crowdfunding_campaign("Kickstarter", {"title": f"{gadget['name']} Launch", "goal": 10000}))
        investors = ["investor1@email.com", "investor2@email.com"]
        print(send_pitch_to_investors(investors, "pitch_deck.pdf"))
    elif stage == "sourcing":
        suppliers = [f"https://api.supplier1.com/inventory/{gadget['name']}", f"https://api.supplier2.com/inventory/{gadget['name']}"]
        print(fetch_supplier_inventory(suppliers))
    elif stage == "inventory":
        stock = {gadget['name']: 5}
        print(monitor_inventory(stock))
        print(automate_restock(gadget['name'], 20))
    elif stage == "listing":
        products = [
            {"name": gadget['name'], "features": "N/A", "price": "$299"}
        ]
        print(bulk_generate_listings(products))
    elif stage == "pricing":
        competitors = [f"https://competitor1.com/product/{gadget['name']}", f"https://competitor2.com/product/{gadget['name']}"]
        prices = scrape_competitor_prices(gadget['name'], competitors)
        print(prices)
        print(suggest_optimal_price(prices, 100.0))
    elif stage == "marketing":
        ad = {"headline": f"Buy the latest {gadget['name']}!", "image": "ad.jpg", "budget": 100}
        print(launch_ad_campaign("Facebook", ad))
        print(monitor_ad_performance("Facebook", "campaign123"))
    elif stage == "leads":
        chatbot_lead = {"name": "Alice", "email": "alice@email.com", "interest": gadget['name']}
        print(capture_lead_via_chatbot(chatbot_lead))
        landing_lead = {"email": "bob@email.com", "interest": gadget['name']}
        print(capture_lead_via_landing_page(landing_lead))
    elif stage == "fulfillment":
        payment = {"card": "****1234", "amount": 100}
        shipping = {"address": "123 Main St", "courier": "DHL"}
        print(process_payment("order001", payment))
        print(arrange_shipping("order001", shipping))
    elif stage == "shipping":
        print(track_shipment("TRACK123", "DHL"))
    elif stage == "support":
        print(handle_customer_query(f"How do I track my {gadget['name']} order?"))
    elif stage == "feedback":
        customers = ["alice@email.com", "bob@email.com"]
        print(send_feedback_request(customers, "order001"))
    elif stage == "dashboard":
        metrics = {"sales": 10000, "inventory": 250, "returns": 5}
        print(generate_dashboard(metrics))
    elif stage == "alerts":
        thresholds = {"stock": 10, "reviews": 4.0}
        print(check_and_alert({"stock": 5, "returns": 10, "reviews": 3.5}, thresholds))
    else:
        print("Unknown stage. Please specify a valid stage.")

if __name__ == "__main__":
    main() 