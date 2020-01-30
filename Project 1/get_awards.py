from prune import *


#takes a file name and gets a list of awards from it
def get_awards(file_name):
    award_words = ["motion","picture","movie","tv","television","series","performance","director","actor","actress","drama","comedy","animated","foreign","original","score",
    "song","cecil","demille","musical","role","supporting","limited","carol","burnett","best","language","award"]

    start_and_end = ["best", "drama","comedy","television","series","picture","language","award","cecil","carol","animated"]

    relevant_tweets_obj = prune(file_name)

    award_names = {}
    award_tweets = []

    for i in relevant_tweets_obj:
        tweet = i.tweet_text
        #print(tweet)
        #print(set(tweet.split()))
        #print(set(award_words))
        if len(set(tweet.split()).intersection(set(award_words))) > 3:
            award_tweets.append(tweet)
    for text in award_tweets:
        start = float('inf')
        end = float('-inf')
        for key_word in start_and_end:
            try:
                point = text.index(key_word)
                point2 = point + len(key_word)
                if point2 > end:
                    end = point2
                if point < start:
                    start = point
            except:
                pass
        if start != float('inf') and end != float('-inf'):
            name = text[start: end]
            if len(name.split()) > 3 :
                if name not in award_names:
                    award_names[name] = 1
                else:
                    award_names[name] += 1

    OFFICIAL_AWARDS_2020 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama',
    'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy',
    'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture',
    'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture',
    'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture',
    'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television',
    'best performance by an actress in a limited series or a motion picture made for television',
    'best performance by an actor in a limited series or a motion picture made for television',
    'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama',
    'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy',
    'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
    'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award', 'carol burnett award']

    final_names = []
    num = 0
    for name, count in award_names.items():
        if count > 9:
            num += 1
            final_names.append(name)
    final_names = set(final_names)

    print("\n\n*******AWARD NAMES**********\n")
    for i in final_names:
        print("Name of award: ", i)

    print("\n\nTotal awards: ", num)
    print("Success Rate: ", len(set(OFFICIAL_AWARDS_2020).intersection(final_names))/len(OFFICIAL_AWARDS_2020))
    print("\n\nAward names that matched: ")
    for i in set(OFFICIAL_AWARDS_2020).intersection(final_names):
        print(i)


#get_awards('gg2020.json')
