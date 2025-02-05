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
    html.Div(children=[
        dcc.Link(
            html.H1("Dashboard Netflix", style={
                'textAlign': 'center',
                'color': '#FF0000',
                'fontWeight': 'bold',
                'font-family': 'Arial, sans-serif',
                'cursor': 'pointer',
                'textDecoration': 'none'  # Supprime le soulignement du lien
            }),
            href='/'
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'padding': '10px',
        'backgroundColor': '#000000'
    }),
    
    html.Nav([
        dcc.Link('Durée dans le top 10', href='/fame',style={'color': '#fff', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Nombre de vues', href='/views',style={'color': '#fff', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Durée du contenu', href='/runtime',style={'color': '#fff', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link("Nombre d'heures visionnées", href='/hours',style={'color': '#fff', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link('Contenu international', href='/country',style={'color': '#fff', 'textDecoration': 'none','font-family': 'Arial, sans-serif'}),
        dcc.Link("Recherche d'un titre", href='/title',style={'color': '#fff', 'textDecoration': 'none','font-family': 'Arial, sans-serif'})
    ],style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'padding': '10px',
                'backgroundColor': '#000000'}
    ),
    html.Div(id='page-content',style={
                'backgroundColor': '#303030',
                'padding': '20px',
                'minHeight': '100vh'})
],style={
                'padding': '10px',
                'backgroundColor': '#303030'})

# Callback to update the page content based on the URL
@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return html.Div([html.H3(
    "Ce projet étudiant, réalisé dans le cadre de la matière DSIA-4201C, vise à faciliter la recherche de films tendances dans le monde sur la plateforme Netflix. "
    "Pour cela, deux spiders Scrapy collectent des données depuis Netflix Tudum. "
    "Ces informations sont ensuite stockées dans Elasticsearch ou MongoDB, "
    "avant d’être affichées dynamiquement sur cette page grâce à Dash.",style={
                'textAlign': 'center',
                'color': '#fff',
                'font-family': 'Arial, sans-serif',
                'maxWidth': '60%',
                'margin': 'auto'
            }
)])
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
        return html.Div("Nothing here...", style={'padding': '20px','color':'#fff'})  # Home page


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)
