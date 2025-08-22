import dataclasses
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Retail Demo Expanded", host="0.0.0.0", port=9870)

# --- Expanded Simulated Inventory Management System (IMS) ---
@dataclasses.dataclass
class StockInfo:
    product_name: str
    store_location: str
    stock_level: int
    status: str

@mcp.tool()
def get_stock_level(product_name: str, store_location: str) -> StockInfo:
    """Return the current stock level for a product at a specific store"""
    mock_inventory = {
        "TrailSeeker Pro": {"downtown Seattle": 5, "Bellevue": 0, "Portland": 3, "Denver": 8},
        "HikerLite": {"downtown Seattle": 12, "Bellevue": 8, "Portland": 15, "Denver": 10},
        "NordicWave Comfort 20": {"downtown Seattle": 15, "Bellevue": 3, "Portland": 11, "Denver": 0},
        "SummitPack 60L": {"downtown Seattle": 8, "Bellevue": 10, "Portland": 6, "Denver": 9},
        "BlazeField Camp Stove": {"downtown Seattle": 20, "Bellevue": 15, "Portland": 18, "Denver": 12},
        "Iso-Pro Fuel Canister 230g": {"downtown Seattle": 50, "Bellevue": 45, "Portland": 60, "Denver": 30},
        "Photon Beam Headlamp": {"downtown Seattle": 25, "Bellevue": 30, "Portland": 22, "Denver": 18},
        "PureFlow Water Filter": {"downtown Seattle": 18, "Bellevue": 22, "Portland": 14, "Denver": 16},
    }
    stock = mock_inventory.get(product_name, {}).get(store_location, 0)
    status = "In Stock" if stock > 0 else "Out of Stock"
    return {"product_name": product_name, "store_location": store_location, "stock_level": stock, "status": status}

# --- Expanded Simulated Order Management System (OMS) ---
@dataclasses.dataclass
class OrderStatus:
    order_id: str
    status: str
    estimated_delivery: str
    items: list[str]

@mcp.tool()
def get_order_status(order_id: str) -> OrderStatus:
    """Return the status and contents of a customer's order"""
    mock_orders = {
        "ORD-12345": {"status": "Delivered", "estimated_delivery": "2025-08-10", "items": ["HikerLite"]},
        "ORD-67890": {"status": "Processing", "estimated_delivery": "2025-08-18", "items": ["SummitPack 60L", "PureFlow Water Filter"]},
        "ORD-99887": {"status": "Shipped", "estimated_delivery": "2025-08-16", "items": ["TrailSeeker Pro", "Photon Beam Headlamp"]},
        "ORD-54321": {"status": "Pending", "estimated_delivery": "2025-08-20", "items": ["BlazeField Camp Stove", "Iso-Pro Fuel Canister 230g"]},
    }
    status = mock_orders.get(order_id, {"status": "Not Found", "estimated_delivery": "N/A", "items": []})
    return {"order_id": order_id, "items": status["items"], "status": status["status"], "estimated_delivery": status["estimated_delivery"]}

# --- New Customer Information System (CIS) Tool ---
@dataclasses.dataclass
class CustomerInfo:
    customer_id: str
    name: str
    loyalty_member: bool
    email: str

@mcp.tool()
def get_customer_details(customer_id: str) -> CustomerInfo:
    """Returns details for a given customer ID."""
    mock_customers = {
        "CUST-001": {"name": "Alice Johnson", "loyalty_member": True, "email": "alice.j@example.com"},
        "CUST-002": {"name": "Bob Williams", "loyalty_member": False, "email": "bob.w@example.com"},
    }
    details = mock_customers.get(customer_id, {"name": "Unknown", "loyalty_member": False, "email": "N/A"})
    return {"customer_id": customer_id, **details}

mcp.run(transport="streamable-http")