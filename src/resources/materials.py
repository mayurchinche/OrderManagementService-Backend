def add_material():
    """
    Add a new material
            ---
            tags:
              - Materials
            parameters:
              - in: body
                name: body
                schema:
                  type: object
                  required:
                    - material_name
                    - model
                  properties:
                    material_name:
                      type: string
                      description: The name of the material
                    model:
                      type: string
                      description: Model of the material
            responses:
              201:
                description: Material added successfully!
              400:
                description: Invalid input, Please check your request.
              500:
                description: Server error occurred while adding the material.
    """
