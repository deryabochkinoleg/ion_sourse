import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash 
from dash import Dash, dcc, html, Input, Output
from to_frame import to_frame
from collector import collector
from number_of_ions import number_of_ions
from time_to_energy import time_to_energy

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Input and clean data ---------------------------------------------------------------

# tube data----------------------------------------------------------------

path_to_folder = '/home/oleg/projects/backup/ions_data'

df_tube = to_frame(path_to_folder)

# energy data -------------------------------------------------------------------------
path_to_mass_file = '/home/oleg/projects/backup/Elements.csv'

df_energy = time_to_energy(path_to_folder, path_to_mass_file)

# # collector data ---------------------------------------------------------------

path_to_signal = '/home/oleg/projects/backup/collector_ions_data/collector'

df_collector = collector(path_to_signal)

# # calculating number of ions -------------------------------------------------------------------------

df_number_of_ions = number_of_ions(path_to_signal)

# # app layout bootstrap --------------------------------------------------------------------

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(
            html.H1("Ions Analysis Dashboard", className='text-center text-primary mb-4'),
            width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H1("Target:", style={'fontSize':15, 'text-align':'center'}),
            dcc.Dropdown(id='target_dpdn',
                         options=[{'label': tg, 'value': tg} for tg in sorted(df_tube.target.unique())],
                         multi=True
                        ),
    
            html.H1("Ions:", style={'fontSize':15, 'text-align':'center'}),
            dcc.Dropdown(id='ion_dpdn', 
                         options=[],
                         multi=True
                        ),
    
            dcc.Graph(id='tube_graph', figure={})
        ], width={'size': 6, 'offset': 0, 'order':1}),

        dbc.Col([
            html.H1("", style={'fontSize':15, 'text-align':'center'}),
            # dcc.Dropdown(id='target_dpdn',
            #              options=[{'label': tg, 'value': tg} for tg in sorted(df_tube.target.unique())],
            #              multi=True
            #             ),
    
            html.H1("", style={'fontSize':15, 'text-align':'center'}),
            # dcc.Dropdown(id='ion_dpdn', 
            #              options=[],
            #              multi=True
            #             ),
    
            dcc.Graph(id='energy_graph', figure={})
        ], width={'size': 6, 'offset': 0, 'order':2})
    
    ], justify='around', align='end'),


    dbc.Row([
            dbc.Col([
            html.H1("Target_collector:", style={'fontSize':15, 'text-align':'center'}),
            dcc.Dropdown(id='target_col_dpdn',
                         options=[{'label': col_tg, 'value': col_tg} for col_tg in sorted(df_collector.element.unique())],
                         multi=False
                        ),
            dcc.Graph(id='graph_collector', figure={})

            ], width={'size': 5, 'offset': 0, 'order':1}),

            dbc.Col([
            html.H1("Number of ions", style={'fontSize':15, 'text-align':'center'}),
            # dcc.Dropdown(id='pie_dpdn',
            #              options=[{'label': elnt, 'value': elnt} for elnt in sorted(number_of_ions.element.unique())],
            #              multi=False),
            
            dcc.Graph(id='pie_graph', figure={})
        ], width={'size': 5, 'offset': 0, 'order':2})
    ], justify='around')
    
], fluid=True)
# app callbacks -----------------------------------------------------


# Populate the options of ions dropdown based on target dropdown
@app.callback(
    Output('ion_dpdn', 'options'),
    [Input('target_dpdn', 'value')]
)

def set_ions_options(chosen_target):
    if chosen_target is None:
        return dash.no_update
    else:
        df_tube_copy = df_tube.loc[df_tube['target'].isin(chosen_target)]
        return [{'label': ion, 'value': ion} for ion in sorted(df_tube_copy.ion.unique())]
# # populate initial values of ions dropdown

# # create graph

@app.callback(
    Output('tube_graph', 'figure'),
    [Input('ion_dpdn', 'value'),
     Input('target_dpdn', 'value')]
)

def update_grpah(selected_ions, selected_target):
    if selected_target is not None and selected_ions is not None:
        
        df_tube_copy = df_tube[(df_tube.target.isin(selected_target)) & (df_tube.ion.isin(selected_ions))]

        fig = px.line(df_tube_copy, x="time", y="n_ions", color="ion", markers=True)
            
        return fig
    else:
        return dash.no_update
    
@app.callback(
    Output('energy_graph', 'figure'),
    [Input('ion_dpdn', 'value'),
     Input('target_dpdn', 'value')]
)

def update_grpah(selected_ions, selected_target):
    if selected_target is not None and selected_ions is not None:
        
        df_energy_copy = df_energy[(df_energy.target.isin(selected_target)) & (df_energy.ion.isin(selected_ions))]

        fig = px.line(df_energy_copy, x="energy", y="n_ions", color="ion", markers=True)
            
        return fig
    else:
        return dash.no_update
        
    
# # create graph for collector results

@app.callback(
    Output('graph_collector', 'figure'),
    Input('target_col_dpdn', 'value')
)


def update_grpah(selected_target):
    
    df_collector_copy = df_collector[df_collector.element == selected_target]

    ind = df_collector_copy['signal'][(df_collector_copy['signal'] > 0)].index

    right_edge = ind[ind > 100][0]

    fig = px.line(abs(df_collector_copy[['signal', 'time']].loc[0:right_edge]), x="time", y="signal", markers=False)
        
    return fig

@app.callback(
    Output('pie_graph', 'figure'),
    Input('target_col_dpdn', 'value')
)

def update_pie_grpah(selected_element):

    dff = df_number_of_ions[df_number_of_ions.element==selected_element]
    fig = px.pie(dff, values='n_ions', names='ion', hole=.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)



    # host='0.0.0.0', port=8080
