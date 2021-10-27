import instascrape as inst

google = inst.profile('https://www.instagram.com/google/')
google_post = inst.post('https://www.instagram.com/p/CG0UU3ylXnv/')
google_hashtag = inst.hastage('https://www.instagram.com/explore/tags/google/')

# Scrape their respective data
google.scrape()
google_post.scrape()
google_hashtag.scrape()

print(google.followers)
print(google_post['hashtags'])
print(google_hashtag.amount_of_posts)