import json
from tagger import partial_award_check

ENTITY_AWARDS = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best motion picture - comedy or musical', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language',  'best original score - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television',  'best animated feature film', 'best foreign language film', 'best television series - comedy or musical', 'best mini-series or motion picture made for television']
PEOPLE_AWARDS = ['best performance by an actress in a motion picture - drama','best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy','best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture',
        'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best original song - motion picture', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical',  'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award', 'carol burnett award', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
def get_curr_index(name, lst):
	count = 0
	for x in lst:
		if(x[0].lower() == name.lower()):
			return count
			break
		count += 1
	return -1

def voter(year, award_list):
	lst = []
	file_name_2 = 'tagged_tweets_' + year +'.json'
	with open(file_name_2,encoding="utf8") as infile:
		for line in infile:
			tweet = json.loads(line)
			lst.append(tweet)
	infile.close()

	for award in award_list:
		curr_votes_list = []
		award = award.lower()
		# try:
		# 	people_bool = PEOPLE_AWARDS.index(award)
		# except:
		# 	people_bool = -1
		# try:
		# 	mov_bool = ENTITY_AWARDS.index(award)
		# except:
		# 	mov_bool = -1
		
		
		for tweet in lst:
			tweet_text = tweet["text"]
			tweet_tags = tweet["tags"]
			people = tweet_tags[0]
			movies = tweet_tags[1]
			# contains = award in tweet_text
			contains = partial_award_check(award.lower(), tweet_text)
			if(contains):
				for person in people:
					ind = get_curr_index(person, curr_votes_list)
					if(ind != -1):
						curr_votes_list[ind][1] = curr_votes_list[ind][1] + 1
					else:
						curr_votes_list.append([person, 1])
				for movie in movies:
					ind = get_curr_index(movie, curr_votes_list)
					if(ind != -1):
						curr_votes_list[ind][1] = int(curr_votes_list[ind][1]) + 1
					else:
						curr_votes_list.append([movie, 1])
				# if(people_bool != -1):
					# for person in people:
					# 	ind = get_curr_index(person, curr_votes_list)
					# 	if(ind != -1):
					# 		curr_votes_list[ind][1] = curr_votes_list[ind][1] + 1
					# 	else:
					# 		curr_votes_list.append([person, 1])
				# elif(mov_bool != -1):
					# for movie in movies:
					# 	ind = get_curr_index(movie, curr_votes_list)
					# 	if(ind != -1):
					# 		curr_votes_list[ind][1] = int(curr_votes_list[ind][1]) + 1
					# 	else:
					# 		curr_votes_list.append([movie, 1])
		print(award + "*****" )
		print(curr_votes_list)

