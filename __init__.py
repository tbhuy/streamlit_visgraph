import os
import streamlit.components.v1 as components
import csv
import json
from operator import itemgetter
from typing import List, Set
import streamlit as st


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _visgraph = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "visgraph",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    _visgraph = components.declare_component("visgraph", path=build_dir)


class NodeConfig:
  def __init__(self,          
              size=25, #The size is used to determine the size of node shapes that do not have the label inside of them. These shapes are: image, circularImage, diamond, dot, star, triangle, triangleDown, hexagon, square and icon        
              shape="text", #The types with the label inside of it are: ellipse, circle, database, box, text. The ones with the label outside of it 
              color="#F03967",
              **kwargs
               ):  
    self.color=color
    self.size=size
    self.shape=shape
    self.__dict__.update(kwargs)

  def to_dict(self):
    return self.__dict__

class Node:
  def __init__(self,
    id,
    #color="#F03967",
    #size=25, #The size is used to determine the size of node shapes that do not have the label inside of them. These shapes are: image, circularImage, diamond, dot, star, triangle, triangleDown, hexagon, square and icon        
    #shape="text", #The types with the label inside of it are: ellipse, circle, database, box, text. The ones with the label outside of it are: image, circularImage, diamond, dot, star, triangle, triangleDown, hexagon, square and icon.
    #title="", #	Title to be displayed in a pop-up when the user hovers over the node. The title can be an HTML element or a string containing plain text.
    #image="", #  When the shape is set to image or circularImage, this option should be the URL to an image. If the image cannot be found, the brokenImage option can be used. 
    #label="", #The label is the piece of text shown in or under the node, depending on the shape.            
    #url="",
    #value=1, 
    node_config=None,
    **kwargs): 
    if node_config is not None:   
      self.__dict__.update(**node_config.to_dict())
    self.id=id  
    self.__dict__.update(kwargs)


  def to_dict(self):
    return self.__dict__

class EdgeConfig:
  def __init__(self,
              color="lightblue", 
              dashes=False,
              **kwargs
               ):
    self.color=color   
    self.dashes=dashes
    self.__dict__.update(kwargs)

  def to_dict(self):
    return self.__dict__


class Edge:
  def __init__(self, 
              source, 
              target,              
              edge_config=None,
              **kwargs):
    if edge_config is not None:
      self.__dict__.update(**edge_config.to_dict())
    self.source=source
    self.to=target
    self.__dict__.update(kwargs) 
    self.__dict__['from']=source

  def to_dict(self):

    return self.__dict__



class Config:
  def __init__(self, height=800, width=1500, node_config=None, edge_config=None, **kwargs):
    self.height = str(height)+'px'
    self.width = str(width)+'px'
    if node_config is not None:
      self.__dict__.update(**node_config.to_dict()) 
    if edge_config is not None:  
      self.__dict__.update(**edge_config.to_dict()) 
    self.__dict__.update(kwargs) 
   
  def to_dict(self):
    return self.__dict__


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def visgraph(nodes, edges, config, key=None): 

    nodes_data = [ node.to_dict() for node in nodes]
    edges_data = [ edge.to_dict() for edge in edges]
    
    config_json = json.dumps(config.__dict__)
    #st.write(config_json)

    data = { "nodes": nodes_data, "edges": edges_data}
    #st.write(data)
    data_json = json.dumps(data)  

    component_value = _visgraph(graph=data_json, options=config_json)

    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
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
   