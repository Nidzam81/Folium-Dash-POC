import dash
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import folium
import json
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#get data

data = pd.read_csv('location_map.csv')
status = []
for _, row in data.iterrows():
    if row['DNS Status'] == 'NG' or row['ICMP Status'] == 'NG' or row['SNMP Status'] == 'NG':
        status.append("NG")
    else:
        status.append("OK")
data['Status'] = status

loc_val = data.Location.unique()

#create dns donut chart:
dns_data_ok = len(data[data['DNS Status'] == 'OK'])
dns_data_ng = len(data[data['DNS Status'] == 'NG'])
labels = ['OK','NG']
values = [dns_data_ok, dns_data_ng]
fig_dns = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig_dns.update_layout(
    title={
        'text': "DNS Status",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

#create ICMP donut chart:
ICMP_data_ok = len(data[data['ICMP Status'] == 'OK'])
ICMP_data_ng = len(data[data['ICMP Status'] == 'NG'])
labels = ['OK','NG']
values = [ICMP_data_ok, ICMP_data_ng]
fig_icmp = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig_icmp.update_layout(
    title={
        'text': "ICMP Status",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

#create SNMP donut chart:
SNMP_data_ok = len(data[data['SNMP Status'] == 'OK'])
SNMP_data_ng = len(data[data['SNMP Status'] == 'NG'])
labels = ['OK','NG']
values = [SNMP_data_ok, SNMP_data_ng]
fig_snmp = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig_snmp.update_layout(
    title={
        'text': "SNMP Status",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

#create overall donut chart:
status_data_ok = len(data[data['Status'] == 'OK'])
status_data_ng = len(data[data['Status'] == 'NG'])
labels = ['OK','NG']
values = [status_data_ok, status_data_ng]
fig_status = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig_status.update_layout(
    title={
        'text': "Overall Status",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
		
#create map circle
def circle_maker(m,x):

    if x[3] == "OK":
        rad_var = 500
        col_var = 'blue'
    else:
        rad_var = 1000
        col_var = 'red'

    folium.Circle(location = [x[0],x[1]],
                 radius = rad_var,
                 color = col_var,
                 fill =True,
                 popup = "{}".format(x[2])).add_to(m)
				 


controls1 = dbc.Card(
    [

        dbc.FormGroup(
            [
            dcc.Graph(figure=fig_dns),
            html.P(id='dns-title'),
            html.Ul(id='dns-list',style={'color': 'red', 'fontSize': 20})
            ]
        ),
    ],
    body=True,
)
controls2 = dbc.Card(
    [
        dbc.FormGroup(
            [
            dcc.Graph(figure=fig_icmp),
            html.P(id='icmp-title'),
            html.Ul(id='icmp-list',style={'color': 'red', 'fontSize': 20})
            ]
        ),
    ],
    body=True,
)
controls3 = dbc.Card(
    [
        dbc.FormGroup(
            [
            dcc.Graph(figure=fig_snmp),
            html.P(id='snmp-title'),
            html.Ul(id='snmp-list',style={'color': 'red', 'fontSize': 20})
            ]
        ),
    ],
    body=True,
)
controls4 = dbc.Card(
    [
        dbc.FormGroup(
            [
            dcc.Graph(figure=fig_status),
            html.P(id='ov-title'),
            html.Ul(id='ov-list',style={'color': 'red', 'fontSize': 20})
            
            ]
        ),
    ],
    body=True,
)

left_controls = dbc.Card(
    [
        dbc.FormGroup(
            [
			html.H5("Toggle map"),
            dcc.RadioItems(
                id="toggle",
                options=[
                    {'label': ' Show all location', 'value': 'all'},
                    {'label': ' Show Overall NG location only', 'value': 'ov_ng'},
                    {'label': ' Show DNS NG location only', 'value': 'dns_ng'},
                    {'label': ' Show ICMP NG location only', 'value': 'icmp_ng'},
                    {'label': ' Show SNMP NG location only', 'value': 'snmp_ng'},
                    {'label': ' Show OK location only', 'value': 'ok'}
                ],
                value='all'
            ), 
            # html.Br(),
            html.H5("Location details"),
            dcc.Checklist(
                id="toggle_details",
                options=[
                    {'label': ' Show NG Status location', 'value': 'show_ng'},
                ],
                value=[]
            ),  
            # html.Br(),
            html.H5("Select map layout"),
            dcc.Dropdown(
                id="layout",
                options=[
                    {'label': 'Stamen toner', 'value': 'Stamen toner'},
                    {'label': 'Stamen Terrain', 'value': 'Stamen Terrain'},
                    {'label': 'Stamen Watercolor', 'value': 'Stamen Watercolor'},
                    {'label': 'CartoDB positron', 'value': 'CartoDB positron'},
                    {'label': 'CartoDB dark_matter', 'value': 'CartoDB dark_matter'},
                    {'label': 'OpenStreetMap', 'value': 'OpenStreetMap'},
                ],
                value='Stamen toner',
                # multi=True,
            ),
            # html.Br(),
            html.H5("Select location"),
            dcc.Dropdown(
                id="location",
                options=[
                    {"label": loc, "value": loc} for loc in loc_val
                ],
                value="Select location",
                multi=True,
            ),
            html.Br(),
            html.H5("Enable monitoring alert notification"),
            dcc.Checklist(
                id="toggle_notifications",
                options=[
                    {'label': ' Email', 'value': 'mail'},
                    {'label': ' Telegram', 'value': 'telegram'},
                    {'label': ' WhatsApp', 'value': 'whatsapp'},
                ],
                value=[],
                # multi = True
            ), 
            ]
        ),
    ],
    body=True,
),

right_controls = dbc.Card(
    [
        dbc.FormGroup(
            [
			html.H5(id='overall-count',style={'height': 'auto','background-color':'red','textAlign': 'center','margin': 'auto','color':'white','borderRadius': '25px','allignItems':'center'}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5(id='dns-count',style={'height': 'auto','background-color':'red','textAlign': 'center','margin': 'auto','color':'white','borderRadius': '25px','allignItems':'center'}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5(id='icmp-count',style={'height': 'auto','background-color':'red','textAlign': 'center','margin': 'auto','color':'white','borderRadius': '25px','allignItems':'center'}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H5(id='snmp-count',style={'height': 'auto','background-color':'red','textAlign': 'center','margin': 'auto','color':'white','borderRadius': '25px','allignItems':'center'}),
            ]
        ),
    ],
    body=True,
),

app.layout = dbc.Container(
    [
		dbc.Row(
            [
            html.H1("Device Network Monitoring Demo")
            ], justify="center", align="center", className="h-50"
            ),
        html.Br(),
        dbc.Row(
		
            [
				dbc.Col(left_controls,md=2),
                dbc.Col(html.Iframe(id ='map', srcDoc = open('test2.html','r').read(),width = '100%',height='600'), md=8, ), 
				dbc.Col(right_controls,md=2),
            ],
            align="center",
        ),
		html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls4,md=3),
				dbc.Col(controls1,md=3),
				dbc.Col(controls2,md=3),
				dbc.Col(controls3,md=3),            
            ],
            align="center",
        ),

    ],
    fluid=True,
)

@app.callback(
    [Output("map", "srcDoc"), 
    Output("overall-count", "children"),
    Output("dns-count", "children"),
    Output("icmp-count", "children"),
    Output("snmp-count", "children"),
    ],
    [Input("toggle", "value"),
    Input("location", "value"),
    Input("layout","value")]
)

def update_map(val,loc,tiles_var):

    if not tiles_var:
        tiles_var="Stamen toner"

    count_ov_ng = len(data[data['Status'] == "NG"])
    count_ov=html.P(["Total Overall NG count",html.Br(),count_ov_ng])

    count_dns_ng = len(data[data['DNS Status'] == "NG"])
    count_dns=html.P(["Total DNS Status NG count",html.Br(),count_dns_ng])

    count_icmp_ng = len(data[data['ICMP Status'] == "NG"])
    count_icmp=html.P(["Total ICMP Status NG count",html.Br(),count_icmp_ng])

    count_snmp_ng = len(data[data['SNMP Status'] == "NG"])
    count_snmp=html.P(["Total SNMP Status NG count",html.Br(),count_snmp_ng])

    if loc == "Select location" or not loc:
        new_data = data.copy()
    else:
        new_data = data[data['Location'].isin(loc)]

    if val == "all":
        m = folium.Map(location = [3.1910615,101.732700],
                    tiles = tiles_var,
                    zoom_start = 11)
        new_data[['lat','lon','Location','Status']].apply(lambda x: circle_maker(m,x),axis =1)
        m.save('test2.html')
    #Overall NG
    if val == "ov_ng":
        data_ng = new_data[new_data['Status'] == "NG"].reset_index()
        var_check = len(data_ng)
        if var_check > 0:
            init_lat = data_ng['lat'][0]
            init_lon = data_ng['lon'][0]
            m = folium.Map(location = [init_lat,init_lon],
                        tiles = tiles_var,
                        zoom_start = 11)            
            data_ng[['lat','lon','Location','Status']].apply(lambda x: circle_maker(m,x),axis =1)
            m.save('test2.html')
        else:
            m = folium.Map(location = [3.1910615,101.732700],
                        tiles = tiles_var,
                        zoom_start = 11) 
            m.save('test2.html')
    #DNS NG
    if val == "dns_ng":
        data_ng = new_data[new_data['DNS Status'] == "NG"].reset_index()
        var_check = len(data_ng)
        if var_check > 0:
            init_lat = data_ng['lat'][0]
            init_lon = data_ng['lon'][0]
            m = folium.Map(location = [init_lat,init_lon],
                        tiles = tiles_var,
                        zoom_start = 11)            
            data_ng[['lat','lon','Location','Status']].apply(lambda x: circle_maker(m,x),axis =1)
            m.save('test2.html')
        else:
            m = folium.Map(location = [3.1910615,101.732700],
                        tiles = tiles_var,
                        zoom_start = 11) 
            m.save('test2.html')
    #ICMP NG
    if val == "icmp_ng":
        data_ng = new_data[new_data['ICMP Status'] == "NG"].reset_index()
        var_check = len(data_ng)
        if var_check > 0:
            init_lat = data_ng['lat'][0]
            init_lon = data_ng['lon'][0]
            m = folium.Map(location = [init_lat,init_lon],
                        tiles =tiles_var,
                        zoom_start = 11)            
            data_ng[['lat','lon','Location','Status']].apply(lambda x: circle_maker(m,x),axis =1)
            m.save('test2.html')
        else:
            m = folium.Map(location = [3.1910615,101.732700],
                        tiles = tiles_var,
                        zoom_start = 11) 
            m.save('test2.html')
    #SNMP NG
    if val == "snmp_ng":
        data_ng = new_data[new_data['SNMP Status'] == "NG"].reset_index()
        var_check = len(data_ng)
        if var_check > 0:
            init_lat = data_ng['lat'][0]
            init_lon = data_ng['lon'][0]
            print(init_lat,init_lon)
            m = folium.Map(location = [init_lat,init_lon],
                        tiles = tiles_var,
                        zoom_start = 11)            
            data_ng[['lat','lon','Location','Status']].apply(lambda x: circle_maker(m,x),axis =1)
            m.save('test2.html')
        else:
            m = folium.Map(location = [3.1910615,101.732700],
                        tiles = tiles_var,
                        zoom_start = 11) 
            m.save('test2.html')
    if val == "ok":
        data_ok = new_data[new_data['Status'] == "OK"].reset_index()
        var_check = len(data_ok)
        if var_check > 0:
            init_lat = data_ok['lat'][0]
            init_lon = data_ok['lon'][0]
            m = folium.Map(location = [init_lat,init_lon],
                        tiles = tiles_var,
                        zoom_start = 11)            
            data_ok[['lat','lon','Location','Status']].apply(lambda x: circle_maker(m,x),axis =1)
            m.save('test2.html')
        else:
            m = folium.Map(location = [3.1910615,101.732700],
                        tiles = tiles_var,
                        zoom_start = 11) 
            m.save('test2.html')

    return open('test2.html', 'r').read(),count_ov,count_dns,count_icmp,count_snmp

@app.callback(
    [Output("ov-list", "children"),
    Output("dns-list", "children"),
    Output("icmp-list", "children"),
    Output("snmp-list", "children"),
    Output("ov-title", "children"),
    Output("dns-title", "children"),
    Output("icmp-title", "children"),
    Output("snmp-title", "children"),    
    ], 
    [Input("toggle_details", "value"),
    ]
)
def update_list(details):
    if not details:
        return html.P(), html.P(),html.P(),html.P(),html.P(), html.P(),html.P(),html.P()
    elif details[0] == "show_ng":
        status_list = data[data['Status'] == "NG"]
        ov_ng_list = [html.Li(x) for x in status_list.Location]
        title_ov = html.P("Overall Status NG location",style={'color': 'red', 'fontSize': 25})

        status_list = data[data['DNS Status'] == "NG"]
        dns_ng_list = [html.Li(x) for x in status_list.Location]
        title_dns = html.P("DNS Status NG location",style={'color': 'red', 'fontSize': 25})

        status_list = data[data['ICMP Status'] == "NG"]
        icmp_ng_list = [html.Li(x) for x in status_list.Location]
        title_icmp = html.P("ICMP Status NG location",style={'color': 'red', 'fontSize': 25})

        status_list = data[data['SNMP Status'] == "NG"]
        snmp_ng_list = [html.Li(x) for x in status_list.Location]
        title_snmp = html.P("SNMP Status NG location",style={'color': 'red', 'fontSize': 25})

        return ov_ng_list,dns_ng_list,icmp_ng_list,snmp_ng_list,title_ov,title_dns,title_icmp,title_snmp

if __name__ == "__main__":
    app.run_server(debug=True)

