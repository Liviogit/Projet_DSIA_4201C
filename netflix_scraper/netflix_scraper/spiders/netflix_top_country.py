import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlparse
import urllib.parse

class NetflixTop10_country(scrapy.Spider):
    name = 'netflix_top10_country'
    
    pays = ["Argentina", "Australia", "Austria", "Bahamas", "Bahrain", "Bangladesh", "Belgium",
    "Bolivia", "Brazil", "Bulgaria", "Canada", "Chile", "Colombia", "Costa Rica", "Croatia"]
    """"Cyprus",
    "Czech Republic", "Denmark", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Estonia",
    "Finland", "France", "Germany", "Greece", "Guadeloupe", "Guatemala", "Honduras", "Hong Kong",
    "Hungary", "Iceland", "India", "Indonesia", "Ireland", "Israel", "Italy", "Jamaica", "Japan",
    "Jordan", "Kenya", "Kuwait", "Latvia", "Lebanon", "Lithuania", "Luxembourg", "Malaysia", "Maldives",
    "Malta", "Martinique", "Mauritius", "Mexico", "Morocco", "Netherlands", "New Caledonia", "New Zealand",
    "Nicaragua", "Nigeria", "Norway", "Oman", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Qatar", "Romania", "Réunion", "Saudi Arabia", "Serbia", "Singapore", "Slovakia",
    "Slovenia", "South Africa", "South Korea", "Spain", "Sri Lanka", "Sweden", "Switzerland", "Taiwan",
    "Thailand", "Trinidad and Tobago", "Türkiye", "Ukraine", "United Arab Emirates", "United Kingdom",
    "United States", "Uruguay", "Venezuela", "Vietnam"
]"""
    custom_settings = {
        'ITEM_PIPELINES': {
            'netflix_scraper.pipelines.NetflixTop10Pipelinecountry': 1,
        }
    }
  # Liste des pays à scraper
    types_contenu = ['', 'tv']  # Types de contenu : films et séries

    def start_requests(self):
        # Créer les URLs à partir des pays et types de contenu
        for pays in self.pays:
            for type_contenu in self.types_contenu:
                url = f'https://www.netflix.com/tudum/top10/{pays}/{type_contenu}'
                yield SplashRequest(
                    url=url,
                    callback=self.parse,
                    args={'wait': 2}  # Attendre que le JavaScript soit exécuté
                )

    def parse(self, response):
        country = urlparse(response.url).path.lstrip('/').replace('tudum/top10/', '')
        country= urllib.parse.unquote(country)
        if '/' in country:
            country=country[:-3]
            cat='tv'
        else:
            cat='movie'
        # Extraire les données du classement
        for r in response.css('tbody').css('tr'):
            title = r.css('td.title button::text').get()  # Extraire le titre
            if title:
                yield {
                    'title': title.strip(),
                    'source': country.strip(),  # Ajouter l'URL de la source
                    'categorie':cat
                }
