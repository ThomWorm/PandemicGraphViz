# -*- coding: utf-8 -*-

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
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

viridis = cm.get_cmap('viridis',101)
def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l



nodeColor = 'Blue'
nodeSize = 20
lineWidth = 4
lineColor = '#000000'



input_data = pd.read_csv('citrus_odpairs.csv', index_col=0)


G=nx.DiGraph()

for index, row in input_data.iterrows():

    G.add_edge(row["Origin"], row["Destination"], year = row["Year"])
    

######## ,make dicts for different attributes
phytoSan = {}
presence = {}
cumuTrade = {}
risk = {}
color = {}
coNames = {}
#print(attributes['phytoSan'][1])



nodelist = list(G.nodes())
checklist = nodelist
print(checklist)

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





colormap = list(color.values())

#print(colormap)
###############
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors1 = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors1['background']}, children=[
    

    html.Div(children='Network Visualization of Pandemic Model Output', style={
        'textAlign': 'center',
        'color': colors1['text']
    }),


    dcc.Graph(id='graphic'),
    dcc.RadioItems(id = "viewopts", options=[
        {'label': 'Circular Layout', 'value': 'circular'},
        {'label': 'Kamada Kawai Layout', 'value': 'kamada'},
        {'label': 'Random Layout', 'value': 'random'}
    ],style = {'overflow': 'auto','height': 400}, value= 'random'),
    dcc.Checklist(id = "myCheckList", style = {'overflow': 'auto','height': 400}, value=['Indonesia'] ),
    
    html.Button('Fill Checklist', id='list-btn', n_clicks=0) ])
   
                
                
        
    
    


@app.callback(
	Output('myCheckList', 'options'),
	[Input('list-btn', 'n_clicks')]
	)
def fillChecklist(n_clicks):
    data = nodelist
    
    return [{'label': x[0] , 'value' : x[0] } for x in data]




@app.callback(
    Output('graphic', 'figure'),
    [Input('myCheckList', 'value'),
        Input('viewopts', 'value')])
def update_graph(ChecklistVals, ViewParam):
    selection = ChecklistVals
    H = G.subgraph(selection)
    if ViewParam == 'random':
        
        pos = nx.random_layout(H)
    elif ViewParam == 'kamada':
         pos = nx.kamada_kawai_layout(H)

    else: 
         pos = nx.circular_layout(H)  

       
    nx.set_node_attributes(H, pos, "pos")
    node_x = []
    node_y = []
    for node in H.nodes():
        x, y = H.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
    
    
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

    


    subPhytoSan = []
    for node in H.nodes():
        
        subPhytoSan.append(G.nodes[node]['phytoSan'])
        

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
            colorscale='Viridis',
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
            #line_color = list(map(SetColorEdge, subPhytoSan))
            ))
        


    



    subNames = []
    
    for node in H.nodes():
        
        #subRisk.append(H.nodes[node]['risk'])
        subNames.append(H.nodes[node]['coNames'])


    """
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        
    print(node_adjacencies)
    """

    node_trace.marker.color = "green"
    node_trace.text = subNames
    

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












'''id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor' : '#111111',
                'paper_bgcolor' : '#111111',
                'font': {
                    'color': colors1['text']
                },
                'title': 'Dash Data Visualization'
            }
        }'''
    