# Instantiate Tweet objects with text and tag arguments
# e.g. tweet_1 = Tweet("1975", ["movie"])
class Tweet:
	def __init__(self, text, tags):
		self.tweet_text = text
		self.tweet_tags = tags
	def printTweet(self):
		print([self.tweet_text,self.tweet_tags])

# Instantiate Actor objects with name argument
# e.g. actor_george = Actor("George Clooney")
# Add to counts for instances of word relation
# e.g. if(sentence == "george nominated") { actor_george.nomination_count +=1 }
class Actor:
	nomination_count = 0
	win_count = 0
	def __init__(self, name):
		self.name = name

# Instantiate Movie objects with name argument
# e.g. movie_mm = Movie("Mamma Mia")
# Add to counts for instances of word relation
# e.g. if(sentence == "Mamma Mia nominated") { actor_mm.nomination_count +=1 }
class Movie:
	nomination_count = 0
	win_count = 0
	cast = []
	def __init__(self, name):
		self.name = name

# Instantiate Award objects with name argument
# e.g. award_ba = Award("Best Actor")
class Award:
	nominees = []
	winner = []
	host = ""
	presenters = []
	def __init__(self, name):
		self.name = name
