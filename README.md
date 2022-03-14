# streamlit_visgraph
A streamlit component for graph visualization <br />
Based on [React graph vis](https://www.npmjs.com/package/react-vis-graph-wrapper) <br />
Compatible with [vis-network customization](https://visjs.github.io/vis-network/docs/network/) <br />
Support HTML title, openable node link (double-click to open link) <br />

## Install

`pip install streamlit-visgraph`

## Use 
Visualizing a Game of Thrones character network [from pyvis](https://pyvis.readthedocs.io/en/latest/tutorial.html#networkx-integration)
```python
    from streamlit_visgraph import visgraph
    import streamlit as st
    import pandas as pd
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
      nodes.append(Node(id=i, label=node_data[i], title=node_data[i], value=nodes_all.count(node_data[i]), url="http://example/"+node_data[i], node_config=node_config))   

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]
        edges.append(Edge(source=node_data.index(src), target=node_data.index(dst), edge_config=edge_config))
 
    v = visgraph(nodes=nodes, edges=edges, config=options)
```

![](https://github.com/tbhuy/streamlit_visgraph/blob/main/examples/example1.png)

Representation of a process
![](https://github.com/tbhuy/streamlit_visgraph/blob/main/examples/example2.png)

