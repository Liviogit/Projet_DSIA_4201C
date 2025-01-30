import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlparse
class NetflixTop10Spider(scrapy.Spider):
    name = 'netflix_top10'
    start_urls = ['https://www.netflix.com/tudum/top10','https://www.netflix.com/tudum/top10/films-non-english','https://www.netflix.com/tudum/top10/tv','https://www.netflix.com/tudum/top10/tv-non-english']

    # Méthode pour effectuer une requête avec Splash
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                args={'wait': 5}  # Attendre que le JavaScript soit exécuté
            )

    def parse(self, response):
        url_path = urlparse(response.url).path.lstrip('/').replace('tudum/top10/', '')
        if url_path=='':
            url_path='films'
        # Parcourir les lignes du tableau dans le <tbody>
        for r in response.css('tbody').css('tr'):
            title = r.css('td.title button::text').get()  # Extraire le titre
            rank= r.css('td.title span::text').get()
            weekinrow = r.css('td:nth-child(2)::text').get()  # Extraire le nombre de semaines
            views = r.css('td:nth-child(3)::text').get()
            runtime = r.css('td:nth-child(4)::text').get()
            Hours = r.css('td:nth-child(5)::text').get()

            # Renvoyer les résultats sous forme de dictionnaire
            if title and weekinrow and views and runtime and Hours and rank:
                yield {'title': title.strip(),'rank':rank, 'week': weekinrow.strip(),'views':views,'runtime':runtime,'hours':Hours,'source': url_path}
