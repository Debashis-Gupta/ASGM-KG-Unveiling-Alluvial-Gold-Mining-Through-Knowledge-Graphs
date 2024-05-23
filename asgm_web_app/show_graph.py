from pyvis.network import Network
import pandas as pd 
import math
import streamlit as st
@st.cache_resource
def create_vis(graph_data):
    net = Network(height="800px", width="100%", bgcolor="#ffffff", font_color="black", notebook=True,directed=True)

    # Count occurrences of all nodes
    all_nodes = pd.DataFrame(list(graph_data['n']) + list(graph_data['m']), columns=['node'])
    node_counts = all_nodes['node'].value_counts().to_dict()

    # Define color and size scale based on occurrence
    max_occurrence = max(node_counts.values(), default=1)
    print(f"Max occurrence : {max_occurrence}")
    color_scale = lambda x: f"rgb({255 - x/max_occurrence*255}, {x/max_occurrence*255}, 100)"
    # size_scale = lambda x: 5 + (x/max_occurrence * 10)  # Base size of 10, scale up to 30
    size_scale = lambda x: 10 + (math.log(x + 1) / math.log(max_occurrence + 1) * 20) if x > 0 else 10
    seen_nodes = set()

    for index, row in graph_data.iterrows():
        n = row['n']
        m = row['m']
        r = row['r']

        if n not in seen_nodes:
            node_color = color_scale(node_counts.get(n, 0))
            # node_size = size_scale(node_counts.get(n, 0))
            node_size = size_scale(node_counts.get(n, 0))
           
            truncated_label = (n if len(n) < 6 else n[:6])  # Truncate label if too long
    
            net.add_node(n, label=truncated_label, title=f"{n}\nCount: {node_counts.get(n, 0)}", size=node_size, shape='circle')
            seen_nodes.add(n)
        if m not in seen_nodes:
            node_color = color_scale(node_counts.get(m, 0))
            
            node_size = size_scale(node_counts.get(m, 0))
            truncated_label = (m if len(m) < 6 else m[:6])  # Truncate label if too long
            net.add_node(m, label=truncated_label, title=f"{m}\nCount: {node_counts.get(m, 0)}", size=node_size, shape='circle')
            seen_nodes.add(m)

        if n and m and r:
            net.add_edge(n, m, title=r, label=r, font={'color':'red'})

    return net

def format_data_for_vis(graph_data):
    nodes = []
    edges = []
    node_ids = set()

    for index, row in graph_data.iterrows():
        if row['source_id'] not in node_ids:
            nodes.append({'id': row['source_id'], 'label': row['source_name']})
            node_ids.add(row['source_id'])
        if row['target_id'] not in node_ids:
            nodes.append({'id': row['target_id'], 'label': row['target_name']})
            node_ids.add(row['target_id'])
        edges.append({'from': row['source_id'], 'to': row['target_id'], 'label': row['relationship_type']})
    
    return nodes, edges
