from flask import Blueprint
from flask_restful import Api
from src.resources.material_resource import MaterialResource
from src.resources.order_resource import OrderResource
from src.resources.reversal_order_resource import ReversalOrderResource
from src.resources.supplier_resource import SupplierResource

# Create a Blueprint for the materials module
material_blueprint = Blueprint('materials', __name__)
material_api = Api(material_blueprint)

# Register MaterialResource with the Blueprint
material_api.add_resource(MaterialResource, '/materials')

suppliers_blueprint = Blueprint('suppliers', __name__)
suppliers_api = Api(suppliers_blueprint)

suppliers_api.add_resource(SupplierResource, '/suppliers')

reversal_orders_blueprint = Blueprint('reversal_orders', __name__)
reversal_orders_api = Api(reversal_orders_blueprint)

reversal_orders_api.add_resource(ReversalOrderResource, '/reversal_orders')

order_blueprint = Blueprint('orders_v1', __name__)
order_api = Api(order_blueprint)

order_api.add_resource(OrderResource, '/orders_v1')


# order_api.add_resource(OrderResource, "/orders",endpoint="order_operations")
# order_api.add_resource(ManageOrderResource, "/orders/review_pending")
#
# order_api.add_resource(ManageOrderResource, '/orders_v1/<int:order_id>', endpoint="manage_order")
#

# Registering the resources
# order_api.add_resource(GetReviewPendingOrdersResource, "/orders/review_pending",endpoint="get_review_pending_orders")
# order_api.add_resource(ApproveOrderResource, '/orders/<int:order_id>', endpoint="approve_order")
