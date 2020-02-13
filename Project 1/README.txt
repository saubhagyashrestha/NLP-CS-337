Github Repo: https://github.com/saubhagyashrestha/NLP-CS-337.git
Authors: Emily Jenkins, Saubhagya Shrestha,  Swapnanil Deb

General Overview:
We take the dataset of tweets and first prune and group the data. As we go through each tweet, we pull any tweet that has specific key words in it such as best, nominee, goes to, etc. The key words are partitioned by which function we want to run on those set of tweets later. For example, if we are looking for best dressed, then we would group the tweets that have the words 'dressed' for example, and write those tweets to a separate json file for later processing. In addition to this, the tweets that correspond with an award title are filtered out and a tagger is used that will identify specific movie names and person names that exist in those tweet. (The names are determined usings spacy while the movie titles are identified using an imdb movie database). During this process, they also also implemented into a voting system that will keep a hash table running where the votes are the frequency of those names that correspond with those award titles. This hash table is used to extract the nominees and winners. The top five names/movie titles correspond with the nominees while the top one corresponds with the winner.

For get awards, a similar partition method is used in the beginning where the key word is 'best'. Following this, we go through each of the tweets and pick out substrings of the tweets that start with the word 'best' while using various methods to identify where in the tweet to stop. The list of potential award names is cut down by using various filtering methods, and the top 27 potential award names with the most votes are outputted. The function for get_hosts uses a similar method.

For additional goals, we implemented sentiment analysis and we determined best/worst/most controversially dressed. For the dressed category, we searched for various keywords and searched the tweets for names to identify a list of people, then looked for various positive or negative comments about how they were dressed. Using these tweets, we developed a voting system, weighing different positive and negative statements by the vocabulary used; the person with the most positive and negative tweets about their outfit choice won best and worst dressed, respectively, while the person with the most even ratio of good to bad comments (scaled by how many comments were made) received the most controversially dressed title. For sentiment analysis, we searched tweets by keywords to find the person with the best acceptance speech, biggest political statement, best joke delivery, most deserving win, and biggest snub of the night.


What file(s) to run:
Running just autograder.py should work. We added a helper function: run_prune_vote, that will run the initial pruning/voting/writing-files process once for each year. The outputted files are then used to run the rest of the functions. When doing testing, we saw that the final function the autograder runs was the get_awards function. So, we added a call to our write_summary function that is responsible for outputting a human readable file that summarizes the golden globes along with the additional goals.
The write_summary function can be run seperately with a year as an input. Note: this function also generates the file 'gg' + year + 'results.json' which is the json with the summary of all the minimum requirements.

What packages to download / where to find them:
Refer to requirements.txt, do pip install
We had problems with dowloading a specific package that is part of spacy. We tried to incorparte this package in the requirements.txt, but doing pip install on it did not work.
So, FOLLOWING pip install requirements.txt, please RUN THE FOLLOWING COMMAND on the teminal to download this addition package: python -m spacy download en_core_web_sm


Outputted files:
There are several files that are outputted. The 'voting_results_' + year + '.json' is a result of the voting system and the nominees, winners, and presenters are extracted from this json. The 'gg' + year + 'results.json' is the voting_result json with an additional entry of hosts added to it. The format for this json follows the standards as outlined in the example json file on canvas.

Another outputted file is the year + 'golden_globes_summary.txt' which will have the information in a human readable format. This file will also hold information corresponding with the additional goals outlined above.

Note: Emily and Saubhagya did pair programming since the environment was not set up on Saubhagya's computer; thus, commits made by Emily were work done by both.