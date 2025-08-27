# Retail Agentic MCP Demo

This demo simulates an architecture that would be representative of a retail store that has both online orders and fulfillment in additional to in-store inventory. The demo includes:
- Customer records as a knowledge graph
- Product Catalog as a knowledge graph
- MCP server for order status
- MCP server for store inventory
- Agentic Tools configuration

[![Agentic MCP Demo](https://img.youtube.com/vi/mUCL1b1lmbA/maxresdefault.jpg)](https://www.youtube.com/watch?v=mUCL1b1lmbA)

## Deploy TrustGraph

Begin with a [TrustGraph deployment](https://docs.trustgraph.ai/deployment/) of your choice.

## Download the Files

You can either `clone` this repo or download the 4 necessary demo files. The files are:
```
customers.ttl
products.ttl
retail_MCP_setup.sh
retail_MCP_server.py
```

## Using the Included TrustGraph Config

A configuation of TrustGraph is included in the `trustgraph_config` folder. It uses `Mistral Medium 3.1` and `Docker`. If you would like to use this configuration begin by cloning the repo or downloading the files:

> [!NOTE]
> The Docker Engine must be running prior to launching TrustGraph. If it is your first time launching TrustGraph, the Docker Engine will need to pull all of the containers from the Docker Hub.

```
cd trustgraph_config
export MISTRAL_TOKEN=<your-mistral-token>
pip3 install trustgraph-cli==1.2.20
docker compose up -d
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
bash retail_MCP_setup.sh
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

## Data Access Controls

During the load process, the customers records are added to a `customers` collection, and the product catalog is loaded to a `products` collection. The tools that queries for this information are limited to each individual collection. For instance, if you were to delete the `customer_query` agent tool, the agentic flow will no longer have access to the customer records in the `customers.ttl` file. If you re-run the test prompt, you will see a different response, as the agent can no longer find the customer's personal information.

## Knowledge Cores and Flows

The first command in the config script creates a new flow with the id `create-cores` using a flow class that includes knowledge core creation:

```
tg-start-flow \
  -n "document-rag+graph-rag+kgcore" \ # Flow Class
  -i "create-cores" \ # Flow ID
  -d "Create knowledge cores on ingest" # Flow Description
```

When a knowledge set is loaded, in this case `customers.ttl` and `products.ttl`, not only are they loaded into indvidual collections but also connected to the `create-cores` flow by adding the `-f` option.

```
tg-load-knowledge -i urn:customers1 \
  -f create-cores \ # Flow that will generate knowledge core
  -C customers \
  customers.ttl

tg-load-knowledge -i urn:products1 \
  -f create-cores \ # Flow that will generate knowledge core
  -C products \
  products.ttl
```

Not only are the customer records and product catalog loaded into the graph under two separate collections, but now they will generate knowledge cores which can be downloaded for future re-use.

## Testing the Collections

To demonstrate that access is limited to a specified collection, use the following GraphRAG test:

```
tg-invoke-graph-rag -C customers -q "Tell me about Alice Johnson."
```

Because this request includes the `customers` collection, it should return:

```
Based on the provided knowledge statements, here is the information about **Alice Johnson**:

- **Name**: Alice Johnson
- **Type**: `http://xmlns.com/foaf/0.1/Person` (Person)
- **Customer ID**: CUST-001
- **Loyalty Member**: `true`
- **Contact Information**:
  - Email: `alice.j@example.com`
  - Telephone: `+1-555-0101`
- **Address**:
  - Street: `123 Maple St`
  - Locality: `Seattle`
  - Region: `WA`
  - Postal Code: `98101`
- **Orders**: Has one order with ID `http://example.com/orders/ORD-99887`.
```

Now, change the collection:

```
tg-invoke-graph-rag -C products -q "Tell me about Alice Johnson."
```

Since there is no information about Alice Johnson in the product catalog, it will return:

```
I cannot provide any information about **Alice Johnson** because this name does not appear in the provided set of knowledge statements.
```

## Loading Data Directly from Knowledge Cores

The customer records and prodcut catalog are also available as knowledge cores in the `knowledge_cores` folder. Loading knowledge cores is a two step process. The first step stages the knowledge cores in the system. The second step makes the knowledge cores live in the system in a particular collection.

```
# To stage the knowledge cores

tg-put-kg-core --id urn:customers1 -i urn-customers1.core
tg-put-kg-core --id urn:products1 -i urn-products1.core

# To make the knowledge cores live within a collection

tg-load-kg-core -i urn:customers1 --collection customers
tg-load-kg-core -i urn:products1 --collection products
```
