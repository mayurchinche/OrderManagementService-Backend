from datetime import datetime


def get_order_color(order):
    if order.status in ["Order_Delivered", "Partially_Delivered"]:
        return "GREEN" if order.pending_quantity == 0 else "YELLOW+GREEN"

    # Calculate TAT color
    if order.order_date:
        days_since_order = (datetime.utcnow() - order.order_date).days
        if days_since_order < 5:
            return "YELLOW"
        elif days_since_order < 10:
            return "ORANGE"
        else:
            return "RED"
    return "GRAY"  # Default for unknown states
