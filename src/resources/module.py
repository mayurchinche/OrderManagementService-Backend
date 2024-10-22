from flask import Blueprint, request, jsonify

from src.constants.roles import Roles
from src.controllers.module_controller import ModuleController
from src.sequrity.decorators import apply_decorators
module_bp = Blueprint('module', __name__)

@module_bp.route('/add', methods=['POST'])
@apply_decorators()
def add_module():
    """
    Add a new module to a material
    ---
    tags:
      - Module
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            material_name:
              type: string
              example: "Material1"
            module_name:
              type: string
              example: "Module1"
    responses:
      200:
        description: Module added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Module added successfully"
      400:
        description: Bad Request
    """
    data = request.json
    return ModuleController.add_module(data)

@module_bp.route('/update/<string:material_name>/<string:module_name>', methods=['PUT'])
@apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
def update_module(material_name, module_name):
    """
    Update an existing module for a material
    ---
    tags:
      - Module
    parameters:
      - name: material_name
        in: path
        required: true
        type: string
        example: "Material1"
      - name: module_name
        in: path
        required: true
        type: string
        example: "Module1"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            module_name:
              type: string
              example: "UpdatedModule1"
    responses:
      200:
        description: Module updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Module updated successfully"
      404:
        description: Module not found
    """
    data = request.json
    return ModuleController.update_module(material_name, module_name, data)

@module_bp.route('/get/<string:material_name>', methods=['GET'])
@apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
def get_modules(material_name):
    """
    Get all modules for a material
    ---
    tags:
      - Module
    parameters:
      - name: material_name
        in: path
        required: true
        type: string
        example: "Material1"
    responses:
      200:
        description: List of modules retrieved successfully
        schema:
          type: object
          properties:
            modules:
              type: array
              items:
                type: object
                properties:
                  material_name:
                    type: string
                    example: "Material1"
                  module_name:
                    type: string
                    example: "Module1"
      404:
        description: Material not found
    """
    return ModuleController.get_modules(material_name)

@module_bp.route('/delete/<string:material_name>/<string:module_name>', methods=['DELETE'])
@apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
def delete_module(material_name, module_name):
    """
    Delete a module from a material
    ---
    tags:
      - Module
    parameters:
      - name: material_name
        in: path
        required: true
        type: string
        example: "Material1"
      - name: module_name
        in: path
        required: true
        type: string
        example: "Module1"
    responses:
      200:
        description: Module deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Module deleted successfully"
      404:
        description: Module not found
    """
    return ModuleController.delete_module(material_name, module_name)
