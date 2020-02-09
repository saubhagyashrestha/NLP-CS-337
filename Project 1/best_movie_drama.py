

def movie_filter(tweet):
	if(size(tweet.tweet_tags[1]) > 0)
		return True
	else
		return False

def mov_search(mov_name, mov_arr):
	for x in mov_arr:
		if(mov_name == x[0]):
			x[1]++
			return True
	return False 

def best_movie_drama():
    relevant_tweets = []
    with open('pruned_tweets.json',encoding="utf8") as infile:
        for line in infile:
            text = json.loads(line)['text']
            relevant_tweets.append(text)
    infile.close()

    rel_tweet_filtered = filter(movie_filter, relevant_tweets)

    mov_nominees = []

    for text in relevant_tweets:
    	result = text.find('best')
    	if(result != -1):
    		if(mov_search(text.tweet_tags[1], mov_nominees) == False):
    			mov_nominees.append((text.tweet_tags[1], 1))
