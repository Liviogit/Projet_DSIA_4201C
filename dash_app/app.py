import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import callback
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from views import create_views
from fame import create_fame
from runtime import create_runtime
from hours import create_hours
from country import create_country
from title import create_title

# Connexion à MongoDB
mongo_client = MongoClient("mongodb://root:example@mongodb:27017/")
mongo_db = mongo_client['netflix_data']
mongo_collection = mongo_db['top10']

# Connexion à Elasticsearch
es_client = Elasticsearch(["http://elasticsearch:9200"])

# Initialisation de l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1("Dashboard Netflix",style={'textAlign': 'center', 'color': '#FF0000', 'fontWeight': 'bold','font-family': 'Arial, sans-serif'}),
    
    html.Nav([
        dcc.Link('Durée dans le top', href='/fame',style={'color': '#ff0000', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Vues', href='/views',style={'color': '#ff0000', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Durée', href='/runtime',style={'color': '#ff0000', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link("Nombre d'heures visionnées", href='/hours',style={'color': '#ff0000', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Dans le monde', href='/country',style={'color': '#ff0000', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Recherche un titre', href='/title',style={'color': '#ff0000', 'textDecoration': 'none','font-family': 'Arial, sans-serif'})
    ],style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'padding': '10px',
                'backgroundColor': '#000000',  # Noir profond
                'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'}
    ),
    html.Div(id='page-content',style={
                'backgroundColor': '#121212',  # Noir clair
                'color': '#FF0000',  # Texte rouge
                'padding': '20px',
                'minHeight': '100vh'})
])

# Callback to update the page content based on the URL
@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return None
    elif pathname == '/views':
        return create_views()   # Display the vma histogram page
    elif pathname == '/fame':
        return create_fame()       # Display home page
    elif pathname == '/runtime':
        return create_runtime()   # Display the age histogram page
       # Display the vma histogram page
    
    elif pathname == '/hours':          
        return create_hours()  # Display the grav histogram page
    elif pathname == '/country':          
        return create_country()  # Display the grav histogram page
    elif pathname == '/title':          
        return create_title()  # Display the grav histogram page
    else:
        return html.Div("Nothing here...", style={'padding': '20px'})  # Home page


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)
