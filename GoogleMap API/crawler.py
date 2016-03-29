import json
import time
import urllib
import urllib2
import pymongo
import csv
import os
import logging
import datetime

class GooglePlaces:
    MAPS_KEY = 'AIzaSyD5PRJPguFUMtpE-Z_ABzfY5nS5JvfSCrM'
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    LOG_FILE = 'history.log'
    
    def __init__(self):
        # set up logging configuration
        logging.basicConfig(filename = self.LOG_FILE, level = logging.DEBUG)        

        
    def run(self, radius, types):                     
        startTime = datetime.datetime.now()               
        logging.debug("%s: Lauching google map places request... " % startTime)
        curPage = 1
        numPages = 3
        count = 0
        firstline = True        
        totalPlaces = 0
        numOfRequests = 0

        processed_ids = self.load_processed_ids()
        ids_set = set(processed_ids)

        with open('Dataset_Phoenix_Restaurants.csv', 'rb') as f:            
            reader = csv.reader(f)
            for row in reader:                
                if firstline: 
                    firstline = False
                    continue                
                count = count + 1                
                business_id = row[0]
                if business_id in ids_set:
                    continue
                latitude = float(row[2])
                longitude = float(row[3])
                                               
                for place_type in types:
                    curPage = 1
                    results = [] 
                    # initial query url                    
                    url = self.BASE_URL + '?' + urllib.urlencode({
                                                         'location': "%s,%s" % (latitude, longitude),
                                                         'radius': radius,
                                                         'key': self.MAPS_KEY,
                                                         'type': place_type,
                                                         })
                    
                    while curPage <= numPages:        
                        response = self.Request(url)                        
                        numOfRequests = numOfRequests + 1                        
                        if(response['status'] == 'OK'):                            
                            results.extend(response['results'])
                        
                        logging.debug("#%s, business id: %s, place: %s, page: %s, # of places found: %d" % (count, business_id, place_type, curPage, len(results)))                                                
                        print "#%s, business id: %s, place: %s, page: %s, # of places found: %d" % (count, business_id, place_type, curPage, len(results)) 

                        if response.has_key('next_page_token'):
                            time.sleep(5)
                            # updating url with next_page_token
                            url = self.BASE_URL + '?' + urllib.urlencode({        
                                                         'pagetoken': response['next_page_token'],
                                                         'key': self.MAPS_KEY,                                                     
                                                         })                                                    
                            curPage = curPage + 1
                        else:
                            break
                    
                    # insert into MongoDB    
                    self.insert(results, business_id, place_type)                                        
                    totalPlaces = totalPlaces + len(results)
                    logging.debug("Total number of places so far: %d" % totalPlaces) 

                with open('processed ids.csv', 'a') as f_write:
                        writer = csv.writer(f_write)
                        writer.writerow([business_id])                    
                                
                # if(count >= 5):
                #     break

                # exceed maximum limits
                td = datetime.datetime.now() - startTime
                if(numOfRequests >= 140000 and td.seconds < 311040000):
                    logging.warning('Exceeding maximum request limit')
                    print "Exceeding maximum request limit. Quiting the program."
                    break
                
    # single request
    def Request(self, url):
        current_delay = 0.1
        max_delay = 3600

        while True:
            try:
                # Get the API response.
                response = str(urllib2.urlopen(url).read())                
            except IOError:
                pass  # Fall through the to the retry loop.
            else:
                # If we didn't get an IOError then parse the result.
                response = json.loads(response.replace('\\n', ''))
                if response['status'] == 'OK':
                    return response
                elif response['status'] == 'ZERO_RESULTS':
                    return response
                elif response['status'] != 'UNKNOWN_ERROR':
                    # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                    # ZERO_RESULTS. There is no point retrying these requests.
                    logging.warning("Error: %s" % json.dumps(response, indent = 2))
                    raise Exception(response['error_message'])

            if current_delay > max_delay:
                logging.warning('Too many retry attemps. Quiting the program.')
                raise Exception('Too many retry attempts.')
            print 'Waiting', current_delay, 'seconds before retrying.'
            time.sleep(current_delay)
            current_delay *= 2  # Increase the delay each time we retry.
                    
    def insert(self, placeList, business_id, placetype):
        # logging.debug("%d places to be inserted for business id: %s" % (len(placeList), business_id))
        # print "%d places to be inserted for business id: %s" % (len(placeList), business_id)

        try:
            client = pymongo.MongoClient()
            db = client.googlemap 
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to server: %s" % e

        for place in placeList:            
            # adding yelp id to the place
            place['yelp_id'] = business_id
            place['place_type'] = placetype                                    
            db.places.insert_one(place)
        
        client.close()

    def load_processed_ids(self):
        processed_ids = []
        filename = 'processed ids.csv'
        if(os.path.exists(filename) == False):
            print "File does not exist! Returning an empty list..."
            return processed_ids
        else:    
            with open(filename, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    processed_ids.append(row[0])
        print "%d rows in the processed business ids!" % (len(processed_ids))                    
        return processed_ids


            
if __name__ == "__main__":
    #types = ["cafe"]
    types = ('restaurant','bar','shopping_mall','food','cafe','grocery_or_supermarket','movie_theater','lodging','night_club', \
                  'parking','bus_station','subway_station','transit_station','university','school')     
    GooglePlaces().run(500, types)



        
        
            
    
    