'''Version 0.35'''
import get_awards_new
import prune
from voting import voter
import os.path
from os import path
from get_hosts import hosts
from get_awards_new import get_awards_fun
import json
from best_worst_dressed import redcarpet
from get_sentiment import get_sentiments


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


def write_final_json(year):
    file_name = 'voting_results_' + str(year) + '.json'
    dic = {}
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            dic = json.loads(line)
    infile.close()

    ###writing answers to a separate json
    host = get_hosts(year)
    ans_file_name = 'gg' + str(year) + 'results.json'
    ans_dic = {}
    ans_dic["Host"] = host
    for i in dic:
        ans_dic[i] = dic[i]
    with open(ans_file_name,'w') as outfile:
        json.dump(ans_dic, outfile)
    outfile.close()


def run_prune_vote(year):
    file_name = 'voting_results_' + str(year) + '.json'
    if path.exists(file_name):
        pass
    else:
        #print('run_prune_vote', year)
        year = int(year)
        OFFICIAL_AWARDS = []
        if year >= 2018:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
        else:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
        prune.prune(year, OFFICIAL_AWARDS)
        voter(year, OFFICIAL_AWARDS)


def write_summary(year):
    write_final_json(year)
    year = str(year)
    dic = {}
    file_name = 'gg' + year + 'results.json'
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            dic = json.loads(line)
    infile.close()

    hu_rd_file = str(year) + 'golden_globes_summary.txt'
    with open(hu_rd_file, "a") as text_file:
        text_file.write("Summary of the Golden Globes " + str(year) + "\n\n\n")
        for i in dic:
            if i == "Host":
                text_file.write("Host:")
                text_file.write("\n")
                for name in dic[i]:
                    text_file.write(name)
                    text_file.write("\n")    
                text_file.write("\n")
            else:
                text_file.write(i.title())
                text_file.write("\n")
                for pnw in dic[i]:
                    if pnw == 'nominees':
                        text_file.write("Nominees:\n")
                        for name in dic[i]['nominees']:
                            text_file.write(name)
                            text_file.write("\n")
                        text_file.write("\n")
                    if pnw == 'presenters':
                        text_file.write("Presenters:\n")
                        for name in dic[i]['presenters']:
                            text_file.write(name)
                            text_file.write("\n")
                        text_file.write("\n")
                    if pnw == 'winner':
                        text_file.write("Winner:\n")
                        text_file.write(dic[i]['winner'])
                        text_file.write("\n\n\n")
        text_file.write("Additional Requirements \n\nBest/Worst/Most Controversially Dressed\n")
        clothes = redcarpet(year)
        for i in clothes:
            text_file.write(i)
            text_file.write('\n')
        text_file.write("\n")

        text_file.write("Sentiment Analysis \n")
        sent = get_sentiments(year)
        for i in sent:
            text_file.write(i)
            text_file.write('\n')
    text_file.close()




def get_hosts(year):
    #print('get_hosts', year)
    run_prune_vote(year)
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts(year)

def get_awards(year):
    #print('get_awards', year)
    run_prune_vote(year)
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return get_awards_fun(year)

def get_nominees(year):
    #print('get_nominees', year)
    run_prune_vote(year)

    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    file_name = 'voting_results_' + str(year) + '.json'
    dic = {}
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            dic = json.loads(line)
    infile.close()
    OFFICIAL_AWARDS = []
    if int(year) >= 2018:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    else:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    ans = {}
    for i in OFFICIAL_AWARDS:
        ans[i] = dic[i]['nominees']

    return ans

def get_winner(year):
    #print('get_winner', year)
    run_prune_vote(year)

    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    file_name = 'voting_results_' + str(year) + '.json'
    dic = {}
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            dic = json.loads(line)
    infile.close()
    OFFICIAL_AWARDS = []
    if int(year) >= 2018:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    else:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    ans = {}
    for i in OFFICIAL_AWARDS:
        ans[i] = dic[i]['winner']
    write_summary(year)
    return ans

def get_presenters(year):
    #print('get_presenters', year)
    run_prune_vote(year)

    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    file_name = 'voting_results_' + str(year) + '.json'
    dic = {}
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            dic = json.loads(line)
    infile.close()
    OFFICIAL_AWARDS = []
    if int(year) >= 2018:
            OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    else:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    ans = {}
    for i in OFFICIAL_AWARDS:
        if dic[i]['presenters'] == []:
            ans[i] = ''
        else:
            ans[i] = dic[i]['presenters'][0]
    return ans

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    #print("HERE")
    pre_ceremony()
    return

if __name__ == '__main__':
    main()
