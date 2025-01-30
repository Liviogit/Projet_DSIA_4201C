from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd

def convert_to_minutes(duration):
    try:
        # Vérifie si le format correspond à "heure:minutes"
        if ":" not in duration:
            return 0
        hours, minutes = map(int, duration.split(":"))
        if hours < 0 or minutes < 0 or minutes >= 60:  # Vérification des valeurs
            return 0
        total_minutes = hours * 60 + minutes
        return total_minutes
    except (ValueError, AttributeError):
        # Retourne 0 si une erreur se produit lors de la conversion
        return 0


def create_runtime():
    """Crée la mise en page initiale du tableau de bord sans figure."""
    return html.Div([
        html.H2("durée des titres"),
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
        html.Div(id='runtime-container')  # Conteneur pour le graphique généré dynamiquement
    ])

@callback(
    Output('runtime-container', 'children'),
    [Input('url-path', 'value')]
)
def update_runtime(url_path):
    """Met à jour la vue en fonction de la sélection du dropdown."""
    from app import mongo_collection  # Importer la collection depuis app.py

    # Récupération des données depuis MongoDB
    data = list(mongo_collection.find({'source': url_path}, {'_id': 0, 'rank': 1, 'runtime': 1, 'title':1}))
    df = pd.DataFrame(data)

    if df.empty:
        return html.Div("Aucune donnée disponible.", style={'color': 'red'})

    df['runtime'] = df['runtime'].apply(convert_to_minutes)
    fig = px.bar(df, x='rank', y='runtime', title=f"durée par rang du top 10 dans la catégorie: - {url_path.capitalize()}",hover_data=['title'])

    return dcc.Graph(figure=fig)
