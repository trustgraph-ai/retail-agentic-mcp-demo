#!/bin/bash
# retail_MCP_setup.sh

echo "Loading Customer and Product data..."
tg-load-knowledge -i customers customers.ttl
tg-load-knowledge -i products products.ttl
echo "Data loading complete!"

echo "Setting up MCP tools.."

# Configure MCP tools (the underlying MCP service references)
echo "Configuring MCP tool endpoints..."
tg-set-mcp-tool --id get_stock_level \
  --tool-url "http://host.docker.internal:9870/mcp"

tg-set-mcp-tool --id get_order_status \
  --tool-url "http://host.docker.internal:9870/mcp"

# Verify MCP tools are configured
echo "Verifying MCP tool configuration..."
tg-show-mcp-tools

# Remove default agent tools
echo "Removing default agent tools..."
tg-delete-tool --id knowledge-query
tg-delete-tool --id knowledge-extraction
tg-delete-tool --id llm-completion

# Configure agent tools (the tools agents can use)
echo "Configuring agent tools..."

tg-set-tool --id check_stock \
  --name "check_stock" \
  --type mcp-tool --mcp-tool get_stock_level \
  --description "Use this to check the inventory of a product at a specific store location" \
  --argument 'product_name:string:Product name' \
  'store_location:string:Store location' \
  'stock_level:string:Stock level' \
  'status:string:Status'

tg-set-tool --id check_order_status \
  --name "check_order_status" \
  --type mcp-tool --mcp-tool get_order_status \
  --description "Use this to get the status of a customer's order by its ID." \
  --argument 'order_id:string:Order ID'

tg-set-tool --id product_query \
  --name "product_query" \
  --type knowledge-query \
  --collection products \
  --description "Query the product catalog for information about the products."

 tg-set-tool --id customer_query \
  --name "customer_query" \
  --type knowledge-query \
  --collection customers \
  --description "Query the customer records."

# Verify agent tools are configured
echo "Verifying agent tool configuration..."
tg-show-tools

echo "Demo setup complete!"
