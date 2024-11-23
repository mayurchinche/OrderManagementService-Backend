from locust import HttpUser, task, between


class OrderManagementPerformanceTest(HttpUser):
    # Simulate user behavior with random wait times between tasks
    wait_time = between(1, 5)

    @task(1)
    def fetch_auth_token(self):
        """Simulate fetching orders by an employee"""
        payload = {"contact_number": "+919657491288", "role": "manager"}
        headers = {"content-type": "application/json", "accept": "application/json"}
        self.client.post("/auth/generate_jwt_token", json=payload, headers=headers)

    @task(2)
    def add_new_order(self):
        """Simulate adding a new order"""
        payload = {"customer_name": "perf_test", "material_name": "material_modules1", "model": "Module12",
                   "order_date": "22-12-2024", "order_quantity": 10, "ordered_by": "+919657491288",
                   "user_contact_number": "+919657491288"}
        self.client.post("/api/core/orders/add_order", json=payload,
                         headers={"content-type": "application/json", "accept": "application/json", "role": "manager",
                                  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb250YWN0X251bWJlciI6Iis5MTk2NTc0OTEyODgiLCJyb2xlIjoibWFuYWdlciIsImV4cCI6MTczMjM4MTExMn0.4yXaUfECQJ6qWXVko9vtxf0bT8447CYmhbxZuIPdg_M"}, )  #  # @task(1)  # def fetch_po_pending_orders(self):  #     """Simulate fetching PO pending orders"""  #     self.client.get(  #         "/api/orders/po-pending",  #         headers={"Authorization": "Bearer <mocked_token>"},  #     )
