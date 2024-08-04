from fastapi import FastAPI, Form
import networkx as nx
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: str = Form(...)):
    pipeline_data = json.loads(pipeline)  
    
    # Create a directed graph from the edges
    G = nx.DiGraph()
    nodes = pipeline_data.get('nodes', [])
    edges = pipeline_data.get('edges', [])

    for node in nodes:
        G.add_node(node['id'])
    
    for edge in edges:
        G.add_edge(edge['source'], edge['target'])

    # Calculate number of nodes and edges
    num_nodes = len(G.nodes)
    num_edges = len(G.edges)
    
    # Check if the graph is a DAG
    is_dag = nx.is_directed_acyclic_graph(G)
    
    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}
