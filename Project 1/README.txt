Github Repo: https://github.com/saubhagyashrestha/NLP-CS-337.git
Authors: Swapnanil Deb, Emily Jenkins, Saubhagya Shrestha

General Overview:
We take the dataset of tweets and first prune and group the data. As we go
through each tweet, we pull any tweet that has a proper noun in it (actor name,
movie title, etc) and add it to a running list of relevant tweets. We then tag
each of these tweets in our new list based on the noun(s) used in the tweet
with any combination of the following tags: actor, movie/show, awards.
Additionally, we create a running list of actors, movies/shows, and awards based
on the nouns found after running them through the IMDB database to check for
validity.
Finally, then we go through each award found, checking the relevant tagged
tweets for actors names / movies and shows along with keywords, such as "won",
"wins", "nominated", "host", and several others. After identifying actors and
entities mentioned in the tweet, we tally up how often each actor or movie/show
has been used in the same context as "winning", "nominated", etc to identify the
actors and movies that fit in each slot.
Once all awards have been examined and we have filled all the slots, we output
a .json file with the full set of information gathered from the tweets about
winners, nominees, hosts, and presenters.


What file(s) to run:


What packages to download / where to find them:
imdbpy:https://imdbpy.readthedocs.io/en/latest/
numpy: https://numpy.org/
nltk: https://www.nltk.org/
