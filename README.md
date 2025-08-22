# Retail Agentic MCP Demo

This demo simulates an architecture that would be representative of a retail store that has both online orders and fulfillment in additional to in-store inventory. The demo includes:
- Customer records as a knowledge graph
- Product Catalog as a knowledge graph
- MCP server for order status
- MCP server for store inventory
- Agentic Tools configuration

## Deploy TrustGraph

Begin with a [TrustGraph deployment](https://docs.trustgraph.ai/deployment/) of your choice.

## Remove Default Agent Tools

On launch, TrustGraph will feature basic agent tools for testing. These can be removed through the Workbench. Open the Workbench at:
```
http://localhost:8888
```

Select `Agent Tools` from the left pane. There will be three default agent tools:
- knowledge-extraction
- knowledge-query
- llm-completion

Click each tool and then hit `Delete`.

## Download the Files

You can either `clone` this repo or download the 4 necessary files. The files are:
```
customers.ttl
products.ttl
retail_mcp_setup.sh
retail_MCP_server.py
```

## Launch the MCP Server

Once TrustGraph is fully running, launch the MCP server. It first may be necessary to install the MCP python library.
```python
pip3 install mcp
```

To launch the MCP server:
```
python3 retail_MCP_server.py
```

You will need to leave the MCP server terminal window open. Open a new terminal window to continue configuration.

## Configure the MCP and Agent Tools

The MCP and Agent tools can be configured manually through the Workbench. However, there is a script that will configure all tools automatically. To launch the script:
```bash
bash retail_mcp_setup.sh
```

Under `MCP Tools` you should see:

![MCP Tools](screenshots/mcp_config.png)

Under `Agent Tools` you should see:

![Agent Tools](screenshots/tools_config.png)

## Test the Agent

The Agentic flow can be used from the `Agent` chat in the Workbench or the CLI. Below is a question that will test all aspects of the demo:
```
I'm Alice Johnson. My order ID is ORD-99887. Can you check my order status, contents, arrival date, address, and email address on file? I also need a 'NordicWave Comfort 20' sleeping bag. Is it in stock in Denver? And what headlamp would you recommend as an accessory for the 'TrailSeeker Pro' tent?
```

With the CLI:
```bash
tg-invoke-agent -v -q "I'm Alice Johnson. My order ID is ORD-99887. Can you check my order status, contents, arrival date, address, and email address on file? I also need a 'NordicWave Comfort 20' sleeping bag. Is it in stock in Denver? And what headlamp would you recommend as an accessory for the 'TrailSeeker Pro' tent?"
```

