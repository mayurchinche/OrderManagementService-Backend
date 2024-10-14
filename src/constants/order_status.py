# src/constants/order_status.py

class OrderStatus:
    # Regular order statuses
    REVIEW_PENDING = "Review_Pending"
    PO_PENDING = "PO_Pending"
    ORDER_PLACED = "Order_Placed"
    ORDER_DELIVERED = "Order_Delivered"

    # Reversal order statuses
    REVERSAL_REVIEW_PENDING = "Reversal_Review_Pending"
    DC_PENDING = "DC_Pending"
    REVERSAL_ORDER_PLACED = "Reversal_Order_Placed"
    REVERSAL_ORDER_DELIVERED = "Reversal_Order_Delivered"

    CANCELLED = "Cancelled"
