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
    """Crée la mise en page initiale avec la barre de recherche et l'affichage des résultats."""
    return html.Div([
        html.H2("Recherche de films"),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Entrez le nom du film...',
            debounce=True  # Met à jour après la fin de la saisie
        ),
        html.Div(id='search-results')  # Conteneur pour les résultats
    ])

@callback(
    Output('search-results', 'children'),
    Input('search-input', 'value')
)
def update_search(query):
    """Met à jour les résultats de la recherche selon le titre du film."""
    if not query:
        return html.Div("Veuillez entrer un nom de film.", style={'color': 'gray'})

    df = fetch_data_from_elasticsearch()    
    df['num_countries'] = df['sources'].apply(len)
    df = df.groupby('title').apply(keep_max_sources).reset_index(drop=True)
    # Filtrer les données en fonction du titre recherché (insensible à la casse)
    filtered_df = df[df['title'].str.contains(query, case=False, na=False)]

    if filtered_df.empty:
        return html.Div("Aucun film trouvé.", style={'color': 'red'})
    results = []
    for _, row in filtered_df.iterrows():
        results.append(html.Div([
            html.H3(row['title']),
            html.P(f"Catégorie : {', '.join(row['categorie'])}"),
            html.P(f"Pays disponibles : {', '.join(row['sources'])}")
        ], style={'margin-bottom': '20px', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}))

    # Affichage des résultats sous forme de liste
    
    return results
