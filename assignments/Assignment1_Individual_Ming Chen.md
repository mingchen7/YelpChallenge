## MIS510 - Web Computing and Mining
## Spring 2016 - Individual Assignment 1: Design

*Created by Ming Chen*  
*March 7th, 2016*

### Problem description
In this project, we will use the Yelp data as our main data source and develop machine learning algorithms to discover the factors that drive the success of Yelp's businesses and improve Yelp's review and recommendation systems. In particular, the goal of the project can be three folds.

1. Identify the how much of a business's success is related to location and geographical factors.
2. Improve Yelp's review system by proving its truthfulness and usefulness.
3. Improve Yelp's recommendation system to support user-based recommendation by leveraging the Yelp's own social network.

There are couple of interesting things about this project:

1. First, in order to acquire more meaningful features that would affect a business's success, i.e.,rating, we will use the Google Map API to extract location and geographical related features such as nearby business environment, existence of large malls or stores, public transit accesses, availability of parking, etc.

2. Second, the Yelp's review system has been challenged a lot and facing lawsuits to justify its truthfulness and usefulness. In other words, some reviews may be fake or even are slanders by purpose. Its truthfulness and usefulness are await to be proved.  
3. Third, Yelp's current recommendation system is mostly based on location and ratings. There is no information of user flavor involved in the recommendation system. The proposed user-based recommendation system would be able to incorporate user's review history and his social network relations (e.g., best friend's recommendation) to provide better user specific recommendations.

### Algorithms

The pipeline of machine learning algorithm to be developed in this project is shown in the figure below. The idea of the pipeline is to provide a framework for developing machine learning applications. There are primarily three layers of algorithms: pre-processing & correlation, NLP layer, and application layer.

- Correlation layer: In this layer, we will correlate the Yelp dataset by their matching the keys such as business id and user id to connect the features from different subsets together.
- NLP layer: In this layer, we will develop NLP algorithm to process the Yelp's review data (mostly text data) into meaningful and quantitative measures and information.
- Application layer: In this layer, we will develop three separate applications to achieve the project objectives mentioned earlier. All the three applications take the NLP review processing results and correlate other features as inputs to generate outputs. Three applications are parallel but support each other in the high level.

![Pipeline](https://www.lucidchart.com/publicSegments/view/e757d6fb-2d81-43e9-a826-f89a17f4198f/image.png "Machine Learning Pipeline")

### Dataset description

The primary datasets to be used in this project are the Yelp dataset and the Google Map API.

#### Yelp dataset

The organization of the Yelp dataset is as following. The data can be downloaded or requested from the Yelp's website for academic challenges. We have already obtained this dataset.
- Business: information related to the business on Yelp
- Review: text content of the review given by a user to a business
- User: Yelp's user information
- Check-in: Yelp's number of check-in for different time of day
- tip: A tip given by a user to a business, simplified version of comments

A detailed composition of fields of the dataset is shown in the appendix. For the given Yelp dataset, we will be able to connect users, business to the reviews and check-in. This will help to determine what kinds of users have given to what kind f business of what specific reviews. By taking consideration of the user and business features, we should be able to determine which are the useful and truthful reviews.

In the users dataset, it also has the information of friends for a user. Based on these variables, we will be able to look at what are the business that his friends have visited frequently and what are the reviews/stars his friend have given to those business. These information will help to build user-based recommendation system.

#### Google Map API

The second data source I will use is the Google Map's Places API Web Service. By providing a location with longitude and latitude with a radius as range, the API can get the list of places within the that range. The information available includes everything that you can search on the google map such as type of place, address, opening hours and ratings, etc.

By consolidating the places from this API, we can actually collect the information about location features such as number of malls around the Yelp's business (e.g., restaurant). It helps to correlate the success of Yelp's business with these location features.

The data returned by the API are json objects. Details of the available information of places can be found at: [Google Map Places API response](https://developers.google.com/places/web-service/)

#### Data Processing Activities

The data processing can be summarized into the following main steps:

1. Transform json objects file into tabular style in a csv file. Both the Yelp's dataset and web service response from Google Map API are json objects, it is essential to transform them into tables that can be loaded for developing machine learning algorithms.

2. Join Yelp's five datasets so that data across different datasets can be queried and aggregated. THis is mostly based on business id and user id. Both the review and tip dataset has keys of business id and user id. ALso, users data has user id as the key for connecting their friends.

3. Associate the Google Map API data with the Yelp's business data. The key for join these two data sources will be location, e.g., longitude and latitude. For each Yelp's business, we have its coordinates and they can be used to request nearby places on the Google Map. Therefore, for each business in the Yelp's dataset, we need to aggregate all the nearby places features.

The above are the initial ideas of how to process data but there might be more efforts to expect when implementing.
