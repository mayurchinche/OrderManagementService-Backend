def add_suplier():
    """
    Add a new supplier
            ---
            tags:
              - Suppliers
            parameters:
              - in: body
                name: body
                schema:
                  type: object
                  required:
                    - supplier_name
                    - contact_number
                  properties:
                    supplier_name:
                      type: string
                      description: The name of the supplier
                    contact_number:
                      type: string
                      description: The contact number of the supplier
                    address:
                      type: string
                      description: Address of the supplier
            responses:
              201:
                description: Supplier added successfully!
              400:
                description: Invalid input, Please check your request.
              500:
                description: Server error occurred while adding the supplier.
    """
    pass
