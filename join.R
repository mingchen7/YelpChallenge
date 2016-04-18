setwd('/home/ming/Documents/Github/YelpChallenge')
restaurant_phx = read.csv('dataset/phoenix_restaurants_business.csv', header = TRUE)
business_all = read.csv('dataset/origin/yelp_academic_dataset_business.csv', header = TRUE)
business_google = read.csv('dataset/extracted_location_features.csv', header = TRUE)

# only keep id
myvars.yelp = c("business_id", "name", "full_address", "city", "state", "stars", "categories", "attributes.Price.Range")
business_all_subset = business_all[myvars.yelp]

myvars.id = c("business_id")
restaurant_phx_id = restaurant_phx[myvars.id]

myvars.google = c("business_id","restaurant_avg","bar_avg","food_avg","cafe_avg","movie_theater_avg","lodging_avg","night_club_avg","parking","bus_station","transit_station","university")
business_google_subset = business_google[myvars.google]

# join tables
join1 = merge(restaurant_phx_id, business_all_subset, by = "business_id", all.x = TRUE)
join2 = merge(join1, business_google_subset, by = "business_id", all.x = TRUE)

# handle -1 to NA
# join2$restaurant_avg[join2$restaurant_avg == -1] <- NULL
# join2$bar_avg[join2$bar_avg == -1] <- NULL
# join2$food_avg[join2$food_avg == -1] <- NULL
# join2$cafe_avg[join2$cafe_avg == -1] <- NULL
# join2$movie_theater_avg[join2$movie_theater_avg == -1] <- NULL
# join2$lodging_avg[join2$lodging_avg == -1] <- NULL
# join2$night_club_avg[join2$night_club_avg == -1] <- NULL

names(join2) = c("business_id","name","address","city","state","stars","categories","price",
                 "restaurant_stars","bar_stars","food_stars","cafe_stars","movie_theater_stars","lodging_stars","night_club_stars",
                 "parking","bus_station","transit_station","university")


write.csv(join2, 'dataset/data_business_backend.csv', row.names = FALSE, eol = "\n")