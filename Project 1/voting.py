import json
from tagger import partial_award_check

from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import Person
from tmdbv3api import TV
tmdb = TMDb()
tmdb.api_key = '5c25bb6fa9590f49afafbb9fe8c3be4a'

ENTITY_AWARDS = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best motion picture - comedy or musical', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language',  'best original score - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television',  'best animated feature film', 'best foreign language film', 'best television series - comedy or musical', 'best mini-series or motion picture made for television']
PEOPLE_AWARDS = ['best performance by an actress in a motion picture - drama','best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy','best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture',
        'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best original song - motion picture', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical',  'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award', 'carol burnett award', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def vote_sort(target):
	return target[1]

def get_curr_index(name, lst):
	count = 0
	for x in lst:
		if(x[0].lower() == name.lower()):
			return count
			break
		count += 1
	return -1

def clean_votes(award, vote_list):
	actor_contain = 'performance' in award or 'director' in award or 'screenplay' in award or 'score' in award or 'actor' in award or 'actress' in award
	if(not actor_contain):
		actor_contain = award in PEOPLE_AWARDS
	mov_contain = 'motion picture' in award or 'feature' in award or 'film' in award
	if(not mov_contain):
		mov_contain = award in ENTITY_AWARDS
	tv_contain = 'television' in award
	cleaned_votes = []
	if(actor_contain):
		for vote in vote_list:
			text = vote[0]
			person = Person()
			result = person.search(text)
			if(len(result) > 0):
				res = str(result[0])
				ind = get_curr_index(res, cleaned_votes)
				if(ind != -1):
					cleaned_votes[ind][1] = cleaned_votes[ind][1] + vote[1]
				else:
					cleaned_votes.append([res, vote[1]])
	elif(mov_contain):
		for vote in vote_list:
			text = vote[0]
			movie = Movie()
			result = movie.search(text)
			if(len(result) > 0):
				res = str(result[0])
				ind = get_curr_index(res, cleaned_votes)
				if(ind != -1):
					cleaned_votes[ind][1] = cleaned_votes[ind][1] + vote[1]
				else:
					cleaned_votes.append([res, vote[1]])
	if(tv_contain and not actor_contain):
		for vote in vote_list:
			text = vote[0]
			tv = TV()
			result = tv.search(text)
			if(len(result) > 0):
				res = str(result[0])
				ind = get_curr_index(res, cleaned_votes)
				if(ind != -1):
					cleaned_votes[ind][1] = cleaned_votes[ind][1] + vote[1]
				else:
					cleaned_votes.append([res, vote[1]])
	return cleaned_votes



def voter(year, award_list):
	plst = []
	year = str(year)
	file_name_1 = 'presenter_tweets_' + year +'.json'
	with open(file_name_1,encoding="utf8") as infile:
		for line in infile:
			tweet = json.loads(line)
			plst.append(tweet)
	infile.close()

	lst = []
	file_name_2 = 'tagged_tweets_' + year +'.json'
	with open(file_name_2,encoding="utf8") as infile:
		for line in infile:
			tweet = json.loads(line)
			lst.append(tweet)
	infile.close()

	voting_result = {}

	for award in award_list:
		winner = ""
		curr_votes_list = []
		# x`award = award.lower()
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
		cleaned_votes_list = clean_votes(award, curr_votes_list)
		# print(award + "*****" )
		# print(curr_votes_list)
		# print(award + " cleaned *************")
		# print(cleaned_votes_list)

		cleaned_votes_list.sort(key=vote_sort, reverse=True)
		count = 0
		nominees_list = []
		for vote in cleaned_votes_list:
			if(count == 5):
				break
			nominees_list.append(vote[0])
			count += 1
		# if(len(nominees_list) == 0):
		# 	print("******Award: "+ award)
		# 	print("******no winners")
		# 	continue
		if(len(nominees_list) != 0):
			winner = nominees_list[0]
		presenters = present_voter(plst, award, nominees_list)
		x = {
				"nominees":nominees_list,
				"presenters":presenters,
				"winner": winner
			}
		voting_result[award] = x
		#print(award + "***")
		#print(x)
	#print("***********" + year + "******* Result")
	#print(voting_result)
	#print("Writing the voting_results for ", year, " to a results json.")
	out_name = 'voting_results_' + str(year) + '.json'
	with open(out_name,'w') as outfile:
		#print("lalalal")
		#print(voting_result)
		json.dump(voting_result, outfile)
	outfile.close()
	#return voting_result


def present_voter(tweets, award, nom_list):
	
	curr_votes_list = []
	for tweet in tweets:
		tweet_text = tweet["text"]
		tweet_tags = tweet["tags"]
		people = tweet_tags[0]
		# contains = award in tweet_text
		contains = partial_award_check(award.lower(), tweet_text)
		if(contains):
			for person in people:
				ind = get_curr_index(person, curr_votes_list)
				if(ind != -1):
					curr_votes_list[ind][1] = curr_votes_list[ind][1] + 1
				else:
					curr_votes_list.append([person, 1])
	cleaned_votes = []
	for vote in curr_votes_list:
		text = vote[0]
		person = Person()
		result = person.search(text)
		if(len(result) > 0):
			res = str(result[0])
			if(res in nom_list):
				continue
			ind = get_curr_index(res, cleaned_votes)
			if(ind != -1):
				cleaned_votes[ind][1] = cleaned_votes[ind][1] + vote[1]
			else:
				cleaned_votes.append([res, vote[1]])

	cleaned_votes.sort(key=vote_sort, reverse=True)
	count = 0
	presenters_list = []
	for vote in cleaned_votes:
		if(count == 1):
			break
		presenters_list.append(vote[0])
		count += 1
	return presenters_list



