import sys
import os
import string
import json
import datetime

from twython import Twython

now = datetime.datetime.now()
day = int(now.day)
month = int(now.month)
year = int(now.year)


class TwitterCrawler:
    def __init__(self):
        # INSTANCIA DE TWYTHON PARA HACER PETICIONES A LA API
        self.t = Twython(app_key='LWUB2D0iQyHPXHhpC8pT55nzV', app_secret='TNR1bvtYIky6WEgaT2asIXMTn7tw4tCxyASiyIkWtO6I3Ai1dM', oauth_token='961677984758411265-tgePBQJu08Ua4IseoCGwGvRv8GtWoj5', oauth_token_secret='MIAdan29KJWiWioDYoQAlaCMbjmISEsCEtZipO1wDWVmL')
        self.trends = list()


    def get_mexico_locations(self):
        """Encontrar locaciones con trending topics en Mexico"""
        mexico_locations = list()
        locations = self.t.get_available_trends()
        for l in locations:
            if l['countryCode'] == 'MX':
                mexico_locations.append(l)

        return mexico_locations


    def get_city_woeid(self, city, locations):
        """Encuentra el woeid de una locacion particular en una lista de locaciones"""
        for i in locations:
            if i['name'] == city:
                interest_woeid = i['woeid']
                return interest_woeid


    def set_interest_trends(self, woeid):
        """Encuentra todos los trending topics de la locacion de interes"""
        trends = self.t.get_place_trends(id=woeid)  # CONSULTA POR TRENDS
        self.trends = trends[0]['trends']           # EL DICCIONARIO CON LOS TRENDS


    def print_trend_list(self):
        print('lista de trends:')
        for trend in self.trends:
            print(trend['name'], ':', trend['tweet_volume'])


    def depurate_trends(self):
        """Depura la lista de trendig topics"""
        # ELIMINAMOS TRENDS SIN TWEETS
        for t in self.trends:
            if t['tweet_volume'] is None:
                self.trends.remove(t)


    def sort_trends(self):
        error = 1
        while error == 1:
            try:
                # ORDENAMOS LISTA DE TRENDS SEGUN VOLUMEN DE TWEETS DE MAYOR A MENOR
                self.trends = sorted(self.trends, key=lambda k: k['tweet_volume'], reverse=True)
                error = 0
            except Exception as e:
                self.depurate_trends()


    def get_tweets_of_topic(self, q):
        """Obtiene lista de tweets de un tag particular"""
        tweets = self.t.search(q=q, lang='en', tweet_mode='extended')
        tweets = tweets['statuses']
        tweet_list = list()
        for tweet in tweets:
            tweet_dict = dict()
            tweet_dict['text'] = tweet['full_text']
            tweet_dict['datetime'] = tweet['created_at']

            tweet_list.append(tweet_dict)

        return tweet_list


    def get_tweets(self):
        tweets = dict()
        for trend in self.trends:
            trend_name = trend['name']
            #print('recuperando', trend_name)
            trend_q = trend['query']
            trend_volume = trend['tweet_volume']

            # OBTENEMOS LISTA DE TEXTOS DE TWEETS DEL TREND
            tweet_list = self.get_tweets_of_topic(trend_q)

            tweets[trend_name] = dict()
            tweets[trend_name]['tweet_list'] = tweet_list
            tweets[trend_name]['tweet_count'] = trend_volume

        return tweets


    def dump2json(self, tweets):
        nowStr = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.json_name = nowStr + '.json'
        json_folder = 'json_db'
        if not os.path.exists(json_folder):
            os.mkdir(json_folder)
        with open(os.path.join(json_folder, self.json_name), mode='w', encoding='utf-8') as f:
            json.dump(tweets, f)


    def pipeline(self):
        mexico_locations = self.get_mexico_locations()
        mexico_city = self.get_city_woeid('Mexico City', mexico_locations)
        self.set_interest_trends(mexico_city)
        #self.print_trend_list()
        self.depurate_trends()
        self.sort_trends()
        tweets = self.get_tweets()
        self.dump2json(tweets)
        return self.json_name


if __name__ == '__main__':
    myCrawler = TwitterCrawler()
    myCrawler.pipeline()
