
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import csv
from matplotlib import cm
import plotly.graph_objects as go
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from addEdge import addEdge
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
viridis = cm.get_cmap('viridis',101)

def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l
 
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0.0000001, xcenter = 0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    G: the graph (must be a tree)
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    width: horizontal space allocated for this branch - avoids overlap with other branches
    vert_gap: gap between levels of hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments
        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed
        '''
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)






input_data = pd.read_csv('citrus_odpairs.csv', index_col=0)
emergent_countries = ["Indonesia", "Thailand", "Singapore", "Malaysia"]
year_list = input_data.Year.unique()


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Graph(id='graphic'),
    dcc.Slider(
        id='year_slider',
        min=min(year_list),
        max=max(year_list),
        step= None,
        value= max(year_list),
        marks = {str(year): str(year) for year in year_list}
        ),
        dcc.RadioItems(
            id = "view_toggle",
        options=[
        {'label': 'First Introduction', 'value': 'first'},
        {'label': 'All Introduction', 'value': 'all'},
        
    ],
    value='first',
    labelStyle={'display': 'inline-block'}
)  
    
])




@app.callback(
    Output('graphic', 'figure'),
    [Input('year_slider', 'value'),
        Input('view_toggle', 'value')
        ])
def update_graph(YearVal, ViewOpts):
        G=nx.DiGraph()
        for country in emergent_countries:
            G.add_edge("Origin", country, year = 0)

        year_selection = YearVal
        for index, row in input_data.iterrows():
            #if ViewOpts == 'first':    
                
             #   if not G.has_node(row["Destination"]) :
                #print(row["Destination"])

                 if row["Year"] <= year_selection:
                     G.add_edge(row["Origin"], row["Destination"], year = row["Year"])
            #else: 
             #   if row["Year"] <= year_selection:
              #      print(row["Origin"], row["Destination"])
               #     G.add_edge(row["Origin"], row["Destination"], year = row["Year"])
            # print(row["Destination"])
                #predescessors = G.predecessors(row["Destination"])
                #print(len(list(predescessors)))

                #if len(list(predescessors)) < 3:
                    #print("adding ", row["Origin"] , row["Destination"] )
                # G.add_edge(row["Origin"], row["Destination"], year = row["Year"])
                # print("Edge list from", row["Origin"], G.edges(row["Origin"]))


        
       
        nodelist = list(G.nodes())
        checklist = nodelist
        coNames = {}
        
        H = G.subgraph(nodelist)
        #H = [x for x,y in G.edges(data=True) if y['year'] >= 2011]



        complete_edgelist = list(H.edges())
        
        print(complete_edgelist)
        tree = nx.bfs_tree(H, 'Origin')
        pos = hierarchy_pos(tree, "Origin")
        H = tree

        selection = list(H.nodes())
        tree_edgelist = list(H.edges())
        #print(edgelist)

        master_years = nx.get_edge_attributes(G,'year')
        selection_edge_years = []

        for edge in tree_edgelist:
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])
            selection_edge_years.append(master_years[edge])


        #print(nx.get_edge_attributes)
        #print(pos)
        ###edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )

        #nx.draw(G, pos)
        #nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
        #nx.draw_networkx_nodes(G,pos,node_size=500 , labels = labels, with_labels=True, node_color=color)



        #print(pos)


        
        nx.set_node_attributes(H, pos, "pos")

        edge_x = []
        edge_y = []

        #print(pos)

        if ViewOpts == 'all':
            selected_edges = complete_edgelist

        else:
            selected_edges = tree_edgelist

        

        for edge in selected_edges:
            start = H.nodes[edge[0]]['pos']
            end = H.nodes[edge[1]]['pos']
            
            edge_x, edge_y = addEdge(start, end, edge_x, edge_y, 1, 'end', .02, 6, 20)


        def SetColorEdge(x):
            if(x > 0):
                return "green"
            elif(x < 1):
                return "red"
        


        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=4, color= "darkgrey"),
            hoverinfo='text',
            
            mode='lines')

        node_x = []
        node_y = []
        for node in H.nodes():
            x, y = H.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)


        subPhytoSan = []


        #for node in H.nodes():
        #    
        #   subPhytoSan.append(G.nodes[node]['phytoSan'])
            

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Portland',
                reversescale=False,
                
                color=[],
                size=40,
                colorbar=dict(
                    thickness=15,
                    title='Transmission Probability',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=5,
                line_color = list(map(SetColorEdge, subPhytoSan))))


        node_risk = []
        node_text = []





        #subRisk = []
        #for node in G.nodes():
        #    
        #  subRisk.append(G.nodes[node]['risk'])

        """
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            
        print(node_adjacencies)
        """



        node_trace.marker.color = "Green"
        node_trace.text = selection
        edge_trace.text = selection_edge_years

        fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        plot_bgcolor='#19191a',
                        
                        
                        titlefont_size=16,
                        showlegend=False,
                        
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            showarrow=True,
                            arrowhead = 5,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),
                    )
        return fig 
if __name__ == '__main__':
    app.run_server(debug=True)