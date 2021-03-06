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

viridis = cm.get_cmap('viridis',101)
def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l




attributes =  pd.read_csv('fullAttributes.csv', index_col=0)
input_data = pd.read_csv('fullTrade.csv', index_col=0)
#print(input_data.head)
#print(input_data.values)
G = nx.DiGraph(input_data.values)
with open('fullTrade.csv', 'r', encoding='utf-8-sig') as f:
    d_reader = csv.DictReader(f)
    headers = d_reader.fieldnames[1:]

##### make dict to rekey nodes
keyList = G.nodes()
renameDict = {}
for i in keyList:
    renameDict[i] =  headers[i]
    
nx.relabel_nodes(G, renameDict, copy = False)
labels=make_label_dict(headers)


checklist = []
for country in keyList:
    slist = []
    slist.append(country)
    slist.append(country)
    checklist.append(slist)

print(checklist)
########,make dicts for different attributes
phytoSan = {}
presence = {}
cumuTrade = {}
risk = {}
color = {}
coNames = {}
#print(attributes['phytoSan'][1])
for i in range(len(G.nodes() )):
    country = labels[i]
    coNames[str(country)] = str(country)
    phytoSan[str(country)] = attributes['phytoSan'][i+1]
    presence[str(country)] = attributes['presence'][i+1]
    cumuTrade[str(country)] = attributes['cumuTrade'][i+1]
    risk[str(country)] = attributes['risk'][i+1]
    color[str(country)] = viridis(attributes['risk'][i+1])

nx.set_node_attributes(G, phytoSan,'phytoSan')
nx.set_node_attributes(G, coNames,'coNames')
nx.set_node_attributes(G, risk, 'risk')
colormap = list(color.values())


print("here")


###############
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors1 = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(style={'backgroundColor': colors1['background']}, children=[
    

    html.Div(children='A Simple Filtering Checklist for Pandemic Model Output', style={
        'textAlign': 'center',
        'color': colors1['text']
    }),


    dcc.Graph(id='graphic'),
    dcc.RadioItems(id = "viewopts", options=[
        {'label': 'Circular Layout', 'value': 'circular'},
        {'label': 'Kamada Kawai Layout', 'value': 'kamada'},
        {'label': 'Random Layout', 'value': 'random'}
    ],style = {'overflow': 'auto','height': 400}, value= 'random'),
    dcc.Checklist(id = "myCheckList", style = {'overflow': 'auto','height': 400}, value=['AUT', 'ARM'] ),
    
    html.Button('Fill Checklist', id='list-btn', n_clicks=0) ])
   
                
                
        
    
    

 
            
            
         



@app.callback(
	Output('myCheckList', 'options'),
	[Input('list-btn', 'n_clicks')]
	)
def fillChecklist(n_clicks):
    data = checklist
    return [{'label': x[0] , 'value' : x[1] } for x in data]




@app.callback(
    Output('graphic', 'figure'),
    [Input('myCheckList', 'value'),
        Input('viewopts', 'value')])
def update_graph(ChecklistVals, ViewParam):
    selection = ChecklistVals
    print(selection)
    H = G.subgraph(selection)
    print(type(ViewParam))
    if ViewParam == 'random':
        
        pos = nx.random_layout(H)
    elif ViewParam == 'kamada':
         pos = nx.kamada_kawai_layout(H)

    else: 
         pos = nx.circular_layout(H)  

       
    nx.set_node_attributes(H, pos, "pos")

    edge_x = []
    edge_y = []
    for edge in H.edges():
        x0, y0 = H.nodes[edge[0]]['pos']
        x1, y1 = H.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)


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
    for node in H.nodes():
        
        subPhytoSan.append(G.nodes[node]['phytoSan'])
        

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


    node_risk = []
    node_text = []





    subRisk = []
    subNames = []
    for node in H.nodes():
        
        subRisk.append(H.nodes[node]['risk'])
        subNames.append(H.nodes[node]['coNames'])


    """
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        
    print(node_adjacencies)
    """

    node_trace.marker.color = subRisk
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
    