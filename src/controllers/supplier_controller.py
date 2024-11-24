from src.services.supplier_service import SupplierService


class SupplierController:
    @staticmethod
    def add_supplier(data):
        try:
            supplier_name = data.get("supplier_name")
            contact_number = data.get("contact_number")
            # Call the service layer to add the supplier
            # Return the response and status code directly
            return SupplierService.add_supplier(supplier_name, contact_number)

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_all_supplier():
        try:
            return SupplierService.get_all_suppliers()
        except Exception as e:
            return {"error": str(e)}, 500
