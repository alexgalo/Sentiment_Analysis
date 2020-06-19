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
    # Instancia para hacer peticiones al API
    def __init__(self):
        self.t = Twython(app_key= 't3cyFSkiWB4bSbUCOfKFQfdmU', 
                            app_secret= 'NMNpeBPl4Xb7Fppk3K2jGkuvEqut0X4xHv4Mi0n4PAvHlBMQmr',
                            oauth_token= '612153534-YdrJtLDMP4q5PzXNvlkVKQYAKK8manQOfdIorIfd', 
                            oauth_token_secret= 'wJFbjSZSYT4raoMYMTsaA76WUTklEYgW7gQzMG4h6xNFs')
        self.trends = list()

    #*Encontrar locaciones con trending topics en Mexico
    def get_mexico_locations(self):
        
        mexico_locations = list()
        locations = self.t.get_available_trends()

        for l in locations:
            if l['countryCode'] == 'MX':
                mexico_locations.append(l)

        return mexico_locations

    #*Encuentra el woeid de una locacion particular en una lista de locaciones
    def get_city_woeid(self, city, locations):
    
        for i in locations:
            if i['name'] == city:
                interest_woeid = i['woeid']

        return interest_woeid

    #*Encuentra todos los trending topics de la locacion de interes
    def set_interest_trends(self, woeid):
        
        trends = self.t.get_place_trends(id=woeid)  # CONSULTA POR TRENDS
        self.trends = trends[0]['trends']           # EL DICCIONARIO CON LOS TRENDS
        
        #print(trends[0])


    def print_trend_list(self):
        print('lista de trends:')
        
        for trend in self.trends:
            print(trend['name'], ':', trend['tweet_volume'])

    #*
    def depurate_trends(self):
        """Depura la lista de trendig topics"""
        # ELIMINAMOS TRENDS SIN TWEETS
        for t in self.trends:
            if t['tweet_volume'] is None:
                self.trends.remove(t)

    #*
    def sort_trends(self):
        error = 1
        while error == 1:
            try:
                # ORDENAMOS LISTA DE TRENDS SEGUN VOLUMEN DE TWEETS DE MAYOR A MENOR
                self.trends = sorted(self.trends, key=lambda k: k['tweet_volume'], reverse=True)
                error = 0

            except Exception as e:
                self.depurate_trends()

    def reduce_trends(self):
        """El trending es ..."""
        redu_trends= list()
        redu= self.trends

        for i in range(5):
            redu_trends.append(redu[i])

        #print(redu_trends)

        return redu_trends
        

    # Obtiene lista de tweets de un tag particular
    def get_tweets_of_topic(self, q):
        
        tweets = self.t.search(q=q, lang='es', tweet_mode='extended')
        tweets = tweets['statuses']
        tweet_list = list()
        
        for tweet in tweets:
            tweet_dict = dict()
            tweet_dict['text'] = tweet['full_text']
            tweet_dict['datetime'] = tweet['created_at']

            tweet_list.append(tweet_dict)

        return tweet_list

    #*
    def get_tweets(self, lR):
    #def get_tweets(self):
        tweets = dict()

        for trend in lR:
        #for trend in self.trends:
            trend_name = trend['name']
            print('recuperando', trend_name)
            trend_q = trend['query']
            trend_volume = trend['tweet_volume']

            # OBTENEMOS LISTA DE TEXTOS DE TWEETS DEL TREND
            tweet_list = self.get_tweets_of_topic(trend_q)

            tweets[trend_name] = dict()
            tweets[trend_name]['tweet_list'] = tweet_list
            tweets[trend_name]['tweet_count'] = trend_volume

            #print(tweets)

        return tweets

    #*
    def dump2json(self, tweets):
        nowStr = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        self.json_name = nowStr + '.json'
        json_folder = 'json_db'

        if not os.path.exists(json_folder):
            os.mkdir(json_folder)

        with open(os.path.join(json_folder, self.json_name), mode='w', encoding='utf-8') as f:
            json.dump(tweets, f)



    def pipeline(self):
        print('Iniciando pipeline Crawler')
        # Encontrar locaciones con trending topic en México
        mexico_locations = self.get_mexico_locations()

        # Encuentra el woeid de una locacion particular en una lista de locaciones
        mexico_city = self.get_city_woeid('Mexico City', mexico_locations)

        #*Encuentra todos los trending topics de la locacion de interes
        self.set_interest_trends(mexico_city)

        
        #self.print_trend_list()
        self.depurate_trends()
        self.sort_trends()

        #self.reduce_trends()
        lR= self.reduce_trends()
        tweets= self.get_tweets(lR)
        #tweets = self.get_tweets()

        self.dump2json(tweets)
        print('Terminando pipeline Crawler')

        return self.json_name


if __name__ == '__main__':
    myCrawler = TwitterCrawler()
    myCrawler.pipeline()
