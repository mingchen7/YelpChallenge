setwd("/home/ming/Documents/Github/YelpChallenge/GoogleMap")
business = read.csv(file.choose(), header = TRUE)
out = summary(business$city, maxsum = 10000)
write.table(out, "City count.txt", sep = "\t")
subset = business[which(business$city == 'Phoenix'
                        | business$city == 'Pheonix'
                        | business$city == 'phoenix'
                        | business$city == 'Phoenix '
                        | business$city == 'Gilbert'
                        | business$city == 'Glendale'
                        | business$city == 'Chandler'
                        | business$city == 'Scottsdale'),]
write.csv(subset, "Dataset_Business_Phoenix.csv", row.names = FALSE)
names(subset)