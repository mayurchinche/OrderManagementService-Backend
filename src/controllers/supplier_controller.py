from src.services.supplier_service import SupplierService

class SupplierController:
    @staticmethod
    def add_supplier(data):
        try:
            supplier_name = data.get("supplier_name")
            contact_number = data.get("contact_number")
            # Call the service layer to add the supplier
            response, status_code = SupplierService.add_supplier(supplier_name, contact_number)

            # Return the response and status code directly
            return response, status_code

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_all_supplier():
        try:
            return SupplierService.get_all_suppliers()
        except Exception as e:
            return {"error": str(e)}, 500