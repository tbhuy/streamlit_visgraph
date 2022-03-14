
import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import VisGraph from 'react-vis-graph-wrapper';



/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class StreamlitVisGraph extends StreamlitComponentBase {


  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    var graph = JSON.parse(this.props.args["graph"]);
    
    var nodes = graph.nodes.slice();;
    for (let i = 0; i < nodes.length; i++) {
      if(nodes[i].title)
        nodes[i].title = this.htmlTitle(nodes[i].title);
      
    }
  
    const options = JSON.parse(this.props.args["options"]);
    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.

    const events = {
      doubleClick: (event:any) => {
        console.log(event.nodes);
        let link = graph.nodes[event.nodes[0]].url;
        if(link)
          window.open(link);
      }

     
    };

    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    return (
      <span>
    
      <VisGraph
      graph={graph}
      options={options}
      events={events}
      getNetwork={(network: any) => {
        //  if you want access to vis.js network api you can set the state in a parent component using this property
        
        //console.log(network);
      }}/>
       
      </span>
    )
  }

  private htmlTitle = (html):any => {   
    const container = document.createElement("div");
    container.innerHTML = html;
    return container;
  }
}


// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(StreamlitVisGraph)
