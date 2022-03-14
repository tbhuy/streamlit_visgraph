from streamlit_visgraph import Node, Edge, Config, NodeConfig, EdgeConfig, visgraph
import pandas as pd
import streamlit as st

    st.set_page_config(layout="wide")
    st.title("Streamlit VisGraph - Game of Thrones example")

    got_data = pd.read_csv('https://www.macalester.edu/~abeverid/data/stormofswords.csv')

    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']
    nodes = []
    edges = []
    node_config = NodeConfig(shape='dot')
    edge_config = EdgeConfig()
    options = Config()
    edge_data = zip(sources, targets, weights)
    nodes_all = sources.tolist() + targets.tolist()
    node_data = list(set(nodes_all))
    for i in range(0, len(node_data)):
      nodes.append(Node(id=i, label=node_data[i], title=node_data[i], value=nodes_all.count(node_data[i]), node_config=node_config))   

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]
        edges.append(Edge(source=node_data.index(src), target=node_data.index(dst), edge_config=edge_config))
 
    visgraph(nodes=nodes, edges=edges, config=options)