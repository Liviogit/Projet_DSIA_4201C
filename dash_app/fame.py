from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd

def create_fame():
    """Crée la mise en page initiale du tableau de bord sans figure."""
    return html.Div([
        html.H2("Duree dans le top"),
        dcc.Dropdown(
            id='url-path',
            options=[
                {'label': 'Films', 'value': 'tudum/top10'},
                {'label': 'Films Non-English', 'value': 'films-non-english'},
                {'label': 'TV', 'value': 'tv'},
                {'label': 'TV Non-English', 'value': 'tv-non-english'}
            ],
            value='tudum/top10'
        ),
        html.Div(id='fame-container')  # Conteneur pour le graphique généré dynamiquement
    ])

@callback(
    Output('fame-container', 'children'),
    [Input('url-path', 'value')]
)
def update_fame(url_path):
    """Met à jour la vue en fonction de la sélection du dropdown."""
    from app import mongo_collection  # Importer la collection depuis app.py

    # Récupération des données depuis MongoDB
    data = list(mongo_collection.find({'source': url_path}, {'_id': 0, 'rank': 1, 'week': 1, 'title':1}))
    df = pd.DataFrame(data)

    if df.empty:
        return html.Div("Aucune donnée disponible.", style={'color': 'red'})

    df['week'] = df['week'].astype(str).str.replace(',', '').replace(' ', '').astype(int)
    fig = px.bar(df, x='rank', y='week', title=f"Nombre de semaine - {url_path.capitalize()}",hover_data=['title'])

    return dcc.Graph(figure=fig)
