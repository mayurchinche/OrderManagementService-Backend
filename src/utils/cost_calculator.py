def cost_effectiveness(self):
    """
    Get Cost-Effectiveness
        ---
        tags:
          - Order Management
        parameters:
          - name: order_id
            in: path
            type: integer
            required: true
            description: The ID of the order
        responses:
          200:
            description: Cost-effectiveness details of the order
            schema:
              type: object
              properties:
                expected_price:
                  type: number
                ordered_price:
                  type: number
                savings:
                  type: number
                cost_effective:
                  type: boolean
          404:
            description: Order not found or cost details unavailable
    """
    if self.expected_price and self.ordered_price:
        savings = self.expected_price - self.ordered_price
        return {
            "expected_price": self.expected_price,
            "ordered_price": self.ordered_price,
            "savings": savings,
            "cost_effective": savings > 0,
        }
    return None
