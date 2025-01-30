from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
from elasticsearch import Elasticsearch

# Connexion à Elasticsearch (remplace l'URL par celle de ton conteneur Docker)
def fetch_data_from_elasticsearch():
    from app import es_client as es
    """Récupère les données depuis Elasticsearch."""
    index_name = "netflix_top10"  # Remplace par le nom de ton index
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    response = es.search(index=index_name, body=query, size=1000)
    data = [hit["_source"] for hit in response["hits"]["hits"]]
    
    return data

def create_country():
    """Crée la mise en page initiale du tableau de bord avec filtre par catégorie."""
    return html.Div([
        html.H2("Titres avec le plus grand nombre de pays par catégorie"),
        dcc.Dropdown(
            id='category-filter',
            options=[
                {'label': 'Films', 'value': 'movie'},
                {'label': 'TV', 'value': 'tv'}
            ],
            value='movie',  # Valeur par défaut
            clearable=False
        ),
        dcc.Graph(id='bar-graph'),
        dcc.Interval(
            id='interval-update',
            interval=5000,  # Rafraîchissement toutes les 5 secondes
            n_intervals=0
        )
    ])

@callback(
    Output('bar-graph', 'figure'),
    [Input('interval-update', 'n_intervals'),
     Input('category-filter', 'value')]
)
def update_graph(n_intervals, selected_category):
    """Met à jour le graphique avec les données filtrées par catégorie."""
    data = fetch_data_from_elasticsearch()
    df = pd.DataFrame(data)

    # Filtrer les données par catégorie sélectionnée
    df = df[df['categorie'].apply(lambda x: selected_category in x)]

    # Calcul du nombre de pays par titre
    df['num_countries'] = df['sources'].apply(len)
    df = df.groupby('title').agg({'num_countries': 'max'}).reset_index()

    # Trier les titres par nombre de pays décroissant et prendre les 15 premiers
    df_sorted = df.sort_values(by='num_countries', ascending=False).head(15)

    # Création du graphique Plotly
    fig = px.bar(
        df_sorted,
        x='title',
        y='num_countries',
        title=f"Nombre de pays par titre - {selected_category.capitalize()}",
        labels={'title': 'Titre', 'num_countries': 'Nombre de pays'},
        text_auto=True
    )

    fig.update_traces(marker_color='rgb(26, 118, 255)')
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},
        xaxis_tickangle=-45  # Inclinaison pour lisibilité des titres
    )

    return fig
