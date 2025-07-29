"""
Lead Generation Bot Script
Captures leads via chatbots and landing pages for the gadget business.
"""

from typing import List, Dict

def capture_lead_via_chatbot(user_info: Dict[str, str]) -> str:
    """
    Capture a lead using a chatbot interaction.
    Args:
        user_info: Dictionary with user details (name, email, interest, etc.).
    Returns:
        str: Lead capture status.
    """
    # Placeholder for chatbot lead capture logic
    return f"Lead captured: {user_info.get('name', 'Unknown')} (mock)"

def capture_lead_via_landing_page(form_data: Dict[str, str]) -> str:
    """
    Capture a lead from a landing page form submission.
    Args:
        form_data: Dictionary with form submission data.
    Returns:
        str: Lead capture status.
    """
    # Placeholder for landing page lead capture logic
    return f"Lead captured from landing page: {form_data.get('email', 'No Email')} (mock)"

if __name__ == "__main__":
    chatbot_lead = {"name": "Alice", "email": "alice@email.com", "interest": "Smartphones"}
    print(capture_lead_via_chatbot(chatbot_lead))
    landing_lead = {"email": "bob@email.com", "interest": "Tablets"}
    print(capture_lead_via_landing_page(landing_lead)) 