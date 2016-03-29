setwd("/home/ming/Documents/Github/YelpChallenge/")
business = read.csv("dataset/yelp_academic_dataset_business.csv", header = TRUE)
out_city = summary(business$city, maxsum = 10000)
out_categories = summary(business$categories, maxsum = 10000)
write.table(out_categories, "Categories count.txt", sep = "\t")
write.table(out_city, "City count.txt", sep = "\t")

# subsetting
phoenix = business[which(business$city == 'Phoenix'
                        | business$city == 'Pheonix'
                        | business$city == 'phoenix'
                        | business$city == 'Phoenix '
                        | business$city == 'Gilbert'
                        | business$city == 'Glendale'
                        | business$city == 'Chandler'
                        | business$city == 'Scottsdale'),]

i <- sapply(phoenix, is.factor)
phoenix[i] <- lapply(phoenix[i], as.character)

N <- 1e5  # some magic number, possibly an overestimate
# you don't know levels yet
subset <- data.frame(business_id=rep("", N), 
                     name = rep("", N),
                     latitude = rep(NA, N), 
                     longitude = rep(NA, N), 
                     categoies = rep("", N), 
                     stringsAsFactors=FALSE)

for(i in 1:nrow(phoenix)){
  categories = phoenix[i,21]
  # string match
  if(grepl('Food', categories) | grepl('Restaurants', categories)){
    business_id = phoenix[i,16]
    name = phoenix[i,24]
    latitude = phoenix[i,67]
    longitude = phoenix[i,70]
    subset[i,]  = c(business_id, name, latitude, longitude, categories)
  }
}

data = subset[which(subset$business_id != ""), ]
write.csv(data, "Dataset_Phoenix_Restaurants.csv", row.names = FALSE)
