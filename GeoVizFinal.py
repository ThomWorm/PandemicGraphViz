
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

nodeColor = 'Blue'
nodeSize = 20
lineWidth = 2
lineColor = '#000000'
viridis = cm.get_cmap('viridis',101)
def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l
 




input_data = pd.read_csv('citrus_odpairs.csv', index_col=0)


G=nx.DiGraph()

for index, row in input_data.iterrows():

    G.add_edge(row["Origin"], row["Destination"], year = row["Year"])
    


##### make dict to rekey nodes

nodelist = list(G.nodes())
checklist = nodelist
print(checklist)
coNames = {}
for i in range(len(G.nodes() )):

    
    country = nodelist[i]

    coNames[str(country)] = str(country)
    #phytoSan[str(country)] = attributes['phytoSan'][i+1]
    #presence[str(country)] = attributes['presence'][i+1]
    #cumuTrade[str(country)] = attributes['cumuTrade'][i+1]
    #risk[str(country)] = attributes['risk'][i+1]
    #color[str(country)] = viridis(attributes['risk'][i+1])

#nx.set_node_attributes(G, phytoSan,'phytoSan')
nx.set_node_attributes(G, coNames,'coNames')
#nx.set_node_attributes(G, risk, 'risk') 






#colormap = list(color.values())




selection = ['Indonesia', 'China']
H = G.subgraph(selection)


pos = nx.circular_layout(H)


###edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )

#nx.draw(G, pos)
#nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
#nx.draw_networkx_nodes(G,pos,node_size=500 , labels = labels, with_labels=True, node_color=color)


nx.set_node_attributes(G, pos, "pos")

edge_x = []
edge_y = []
for edge in H.edges():
    start = H.nodes[edge[0]]['pos']
    end = H.nodes[edge[1]]['pos']
    edge_x, edge_y = addEdge(start, end, edge_x, edge_y, .8, 'end', .04, 30, nodeSize)


def SetColorEdge(x):
    if(x > 0):
        return "green"
    elif(x < 1):
        return "red"
   

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=4, color= "darkgrey"),
    hoverinfo='none',
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
    mode='markers',
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

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                plot_bgcolor='#19191a',
                
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=True,
                    arrowhead = 5,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),
               )
fig.show()