import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt
from agent import CampusAgent

st.set_page_config(page_title="Smart Campus Navigation Agent", layout="wide")

st.title("The Smart Campus Navigation Agent")

@st.cache_data
def load_data():
    with open("data/campus_graph.json") as f:
        return json.load(f)

campus_data = load_data()
coords = campus_data["nodes"]
nodes_list = list(coords.keys())

agent = CampusAgent(campus_data, coords)

st.sidebar.header("Agent Percept Controls")
start_node = st.sidebar.selectbox("Start Location", nodes_list, index=0)
goal_node = st.sidebar.selectbox("Destination Goal", nodes_list, index=3)
selected_algorithm = st.sidebar.selectbox("Algorithm", ["BFS", "UCS", "Greedy Best-First", "A* Search"])

blocked_input = st.sidebar.multiselect(
    "Blocked Pathways (Obstacles)",
    options=[f"{e['from']} ↔ {e['to']}" for e in campus_data["edges"]]
)
blocked_edges = set()
for item in blocked_input:
    u, v = item.split(" ↔ ")
    blocked_edges.add((u, v))

# Execute path search when button is clicked
result = None
if st.button("Find Optimal Route"):
    result = agent.find_route(start_node, goal_node, selected_algorithm, blocked_edges)

col1, col2 = st.columns([1, 1])

with col1:
    if result:
        if result["path"]:
            st.success(f"**Path Found:** {' ➔ '.join(result['path'])}")
            st.metric("Total Path Distance", f"{result['cost']} meters")
            st.metric("Nodes Expanded", result["expanded"])
            st.metric("Search Time", f"{result['time_ms']} ms")
        else:
            st.error("No valid path exists between selected nodes due to obstacles!")

with col2:
    st.subheader("Campus Map Visualization")
    G = nx.Graph()
    for node, pos in coords.items():
        G.add_node(node, pos=(pos['x'], pos['y']))
    for edge in campus_data["edges"]:
        G.add_edge(edge['from'], edge['to'], weight=edge['weight'])

    fig, ax = plt.subplots(figsize=(10, 7))
    pos = {n: (coords[n]['x'], coords[n]['y']) for n in G.nodes()}
    
    # Define edge labels dictionary
    edge_labels = {(e['from'], e['to']): e['weight'] for e in campus_data["edges"]}

    # Draw base graph
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="#474677", ax=ax)
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=10, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=2, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

    # Highlight path if search has been run
    if result and result["path"]:
        path_edges = list(zip(result["path"][:-1], result["path"][1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="green", width=3, ax=ax)

    st.pyplot(fig)