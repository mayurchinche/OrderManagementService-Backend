from flask import Blueprint, request, jsonify
from src.models.materials import Materials
from src.db.db import db

material_bp = Blueprint("materials", __name__)


@material_bp.route("/materials", methods=["POST"])
def add_material():
    """
    Add Material:
    ---
    tags:
      - Materials
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: The name of the material
            description:
              type: string
              description: A brief description of the material
    responses:
      201:
        description: Material added successfully!
      500:
        description: Database error occurred while adding the material.
    """
    data = request.get_json()
    new_material = Materials(name=data["name"], description=data.get("description"))
    db.session.add(new_material)
    db.session.commit()
    return jsonify({"message": "Material added successfully!"}), 201


@material_bp.route("/materials", methods=["GET"])
def get_materials():
    materials = Materials.query.all()
    return jsonify(
        [
            {
                "id": material.id,
                "name": material.name,
                "description": material.description,
            }
            for material in materials
        ]
    )
