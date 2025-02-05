from dash import dcc, html, callback, Output, Input
import pandas as pd
from elasticsearch import Elasticsearch

def keep_max_sources(group):
    return group.loc[group['sources'].apply(len).idxmax()]

# Connexion à Elasticsearch (utilisation du client défini dans app.py)
def fetch_data_from_elasticsearch():
    from app import es_client as es
    """Récupère toutes les données depuis Elasticsearch."""
    index_name = "netflix_top10"  # Remplace par le nom de ton index
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    response = es.search(index=index_name, body=query, size=1000)
    data = [hit["_source"] for hit in response["hits"]["hits"]]
    
    return pd.DataFrame(data)

def create_title():
    return html.Div([
        html.H2("Recherche de contenu",style={'textAlign': 'center', 'color': '#FF0000', 'fontWeight': 'bold','font-family': 'Arial, sans-serif'}),
        html.H4("Cette page permet de rechercher un contenu en fonction de son titre parmis les titres tendances dans le monde. La categorie de ce titre ainsi que la liste des pays dans lequel ce titre est présent dans le top 10 sera aussi affiché.",style={'textAlign': 'center', 'color': '#fff','font-family': 'Arial, sans-serif'}),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder="Entrez le nom d'un contenu...",
            debounce=True,  # Met à jour après la fin de la saisie
            style={
                'width': '50%',
                'height': '50px',
                'fontSize': '20px',
                'display': 'block',
                'margin': 'auto'
            }
        ),
        html.Div(id='search-results', style={'textAlign': 'center'})  # Conteneur pour les résultats
    ])

@callback(
    Output('search-results', 'children'),
    Input('search-input', 'value')
)
def update_search(query):
    """Met à jour les résultats de la recherche selon le titre du film."""
    if not query:
        return html.Div("Veuillez entrer le nom d'un contenu...", style={'color': 'gray'})

    df = fetch_data_from_elasticsearch()    
    df['num_countries'] = df['sources'].apply(len)
    df = df.groupby('title').apply(keep_max_sources).reset_index(drop=True)
    # Filtrer les données en fonction du titre recherché
    filtered_df = df[df['title'].str.contains(query, case=False, na=False)]

    if filtered_df.empty:
        return html.H1("Aucun titre trouvé.",style={'color': '#FF0000', 'fontWeight': 'bold','font-family': 'Arial, sans-serif'})
    results = []
    for _, row in filtered_df.iterrows():
        results.append(html.Div([
            html.H3(row['title'],style={'color': '#FF0000', 'fontWeight': 'bold','font-family': 'Arial, sans-serif'}),
            html.P(f"Catégorie : {', '.join(row['categorie'])}"),
            html.P(f"Top 10 Netflix : {', '.join(row['sources'])}")
        ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px','color':'fff','backgroundColor':'#121212'}))

    return html.Div(results, style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #fff', 'border-radius': '5px','color':'#fff','backgroundColor':'#303030'})
