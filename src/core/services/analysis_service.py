from flask import jsonify

from src.constants.order_status import OrderStatus
from src.controllers.order_controller import OrderController
import json

class AnalysisService:
    @staticmethod
    def get_cost_analysis_highlights(start_date,end_date):
        # Logic to get sum of expected price and sum of ordered price
        response = OrderController.get_sum_of_expected_price_and_sum_of_ordered_price(start_date,end_date)
        data = response.json

        total_expected = data[0].get("total_expected", 0)
        total_ordered = data[0].get("total_ordered", 0)

        # Perform calculations on the extracted values
        total_difference = total_expected - total_ordered
        percentage_difference = (total_difference / total_expected) * 100 if total_expected != 0 else 0

        # Print the results
        print(f"Total Expected: {total_expected}")
        print(f"Total Ordered: {total_ordered}")
        print(f"Total Difference: {total_difference}")
        print(f"Percentage Difference: {percentage_difference}%")

        return jsonify({
            "total_savings": total_difference,
            "percentage_savings": f"{percentage_difference}%"
        },200)

    @staticmethod
    def get_price_trend(start_date, end_date,interval="daily"):
        # Logic to get sum of expected price and sum of ordered price
        return OrderController.get_avg_of_expected_price_and_avg_of_ordered_price(start_date, end_date,interval=interval)

    @staticmethod
    def get_supplier_performance(start_date, end_date):
        return OrderController.get_supplier_performance(start_date=start_date, end_date=end_date)
