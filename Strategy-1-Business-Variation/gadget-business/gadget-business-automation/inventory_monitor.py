"""
Inventory Monitor Script
Tracks stock levels and automates restocking for the gadget business.
"""

from typing import Dict

def monitor_inventory(stock_data: Dict[str, int], threshold: int = 10) -> Dict[str, str]:
    """
    Monitor inventory and flag items for restocking.
    Args:
        stock_data: Dictionary mapping product names to stock counts.
        threshold: Minimum stock before restocking is triggered.
    Returns:
        dict: Mapping of product to restock status.
    """
    # Placeholder for monitoring logic
    return {product: ('restock needed' if count < threshold else 'sufficient') for product, count in stock_data.items()}

def automate_restock(product: str, quantity: int):
    """
    Automate the restocking process for a product.
    Args:
        product: Product name.
        quantity: Quantity to restock.
    Returns:
        str: Restock status.
    """
    # Placeholder for restocking logic
    return f'Restock order placed for {quantity} units of {product} (mock)'

if __name__ == "__main__":
    stock = {"Smartphone": 5, "Tablet": 15, "Smartwatch": 8}
    print(monitor_inventory(stock))
    print(automate_restock("Smartphone", 20)) 