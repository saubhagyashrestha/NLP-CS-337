import json

def get_nominees():
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

    relevant_tweets = []
    with open('pruned_tweets.json',encoding="utf8") as infile:
        for line in infile:
            tweet = json.loads(line)
            relevant_tweets.append(tweet)
    infile.close()

    carol_award = {}
    cecil_award = {}
    animated = {}

    for tweet in relevant_tweets:
        split_tweet = set(tweet['text'].split())
        if ('carol' in split_tweet or 'burnett' in split_tweet) and (len(tweet['tags'][0]) > 0):
            for person in tweet['tags'][0]:
                if person not in carol_award:
                    carol_award[person] = 1
                else:
                    carol_award[person] += 1
        if ('cecil' in split_tweet or 'demille' in split_tweet) and (len(tweet['tags'][0]) > 0):
            for person in tweet['tags'][0]:
                if person not in cecil_award:
                    cecil_award[person] = 1
                else:
                    cecil_award[person] += 1
        if ('animated' in split_tweet) and (len(tweet['tags'][1]) > 0):
            for movies in tweet['tags'][1]:
                if movies not in animated:
                    animated[movies] = 1
                else:
                    animated[movies] += 1

    print("\nMost likely people for the Carol Burnett Award, (Actual Winner was Ellen DeGeneres)")
    for name,vote in carol_award.items():
        if vote > 2:
            print("Potential Winner: ", name, "  Votes: ", vote)

    print("\nMost likely people for the Cecil B. deMille Burnett Award, (Actual Winner was Tom Hanks)")
    for name,vote in cecil_award.items():
        if vote > 2:
            print("Potential Winner: ", name, "  Votes: ", vote)

    print("\nMost likely movies for the Best Motion Picture - Animated")
    for name,vote in animated.items():
        if vote > 0:
            print("Potential Winner: ", name, "  Votes: ", vote)

print("GETTING RECIPIENTS FOR THE CAROL BURNETT AND CECIL B. DEMILLE AWARDS...")
get_nominees()
