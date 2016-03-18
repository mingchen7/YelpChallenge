import json
import time
import urllib
import urllib2

class GooglePlaces:
    MAPS_KEY = 'AIzaSyD5PRJPguFUMtpE-Z_ABzfY5nS5JvfSCrM'
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    def run(self, longitude, latitude, radius, types):                                    
        current_delay = 0
        max_delay = 3600
        
        # while True:
        while True:
            for place_type in types:            
                url = self.BASE_URL + '?' + urllib.urlencode({
                                                     'location': "%s,%s" % (longitude, latitude),
                                                     'radius': radius,
                                                     'key': self.MAPS_KEY,
                                                     'type': 'restaurant',
                                                     })
        
                pages = self.SingleRequest(url)
                
                
                if current_delay > max_delay:
                    raise Exception('Too many retry attemps.')
                print 'Waiting', current_delay, 'seconds before retrying.'
                
                time.sleep(current_delay)
                current_delay *= 2
                
    def SingleRequest(self, url):
        pages = []
        
        try:
            response = str(urllib2.urlopen(url).read())
        except IOError:
            pass
        else:
            result = json.loads(response.replace('\\n', ''))
            print type(result)
            if result['status'] == 'OK':
                pages.append(response)
                # if there is next page     
                if(result.has_key('next_page_token')):
                    url = self.BASE_URL + '?' + urllib.urlencode({        
                                                     'pagetoken': result['next_page_token'],
                                                     'key': self.MAPS_KEY,                                                     
                                                     })
                    
                
            elif result['status'] != 'UNKNOWN_ERROR':
                raise Exception(result['error_message'])
            
        return pages
        
            
    def parseJson(self, content):
        print json.dumps([s for s in content['results']], indent=2)
        

if __name__ == "__main__":
    types = ('bakery','bar','book_store','bus_station','cafe','gas_station','grocery_or_supermarket','gym','library', \
         'movie_theater','lodging','night_club','park','parking','restaurant','school','store','subway_station','university') 
    GooglePlaces().run(47.659788, -122.313182, 500, types)

        
        
            
    
    