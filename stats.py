from sportsreference.nfl.boxscore import Boxscore
from sportsreference.nfl.boxscore import BoxscorePlayer
from sportsreference.nfl.schedule import Schedule
from IPython.display import display
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np

global numQBStats
numQBStats = 16

def seperateGames(stats, PlayerBoxscoreElements):
    numPlayerBoxscoreElements = PlayerBoxscoreElements
    week = len(stats)/ numPlayerBoxscoreElements
    playerBoxscores = np.array_split(stats, week)

    return playerBoxscores

def checkIfDone(lst):
    lst_to_remove = ['$','<','@','<t','*','<td','U']
    for index in lst:
        if index in lst_to_remove:
            return False
        else:
            return True
def removeJunk(lst):
    lst_to_remove = ['$','<','@','<t','*','<td','U']
    done =  False
    while done == False:
        for index in lst:
            if index in lst_to_remove:
                lst.remove(index)
        done = checkIfDone(lst)
    return lst

class Player:
    def __init__(self, nameFirst, nameLast, team):
        self.nameFirst = nameFirst
        self.nameLast = nameLast
        self.name = nameFirst+' '+nameLast
        self.team = team

    def get_Player_ID(self):
        int_one = 0
        int_two = 0
        is_correct = False
        first_name = self.nameFirst
        last_name = self.nameLast
        name = self.name
        last_initial = last_name[0]
        guessed_id = last_name[0:4]+first_name[0:2]+str(int_one)+str(int_two)
        while is_correct == False:
            url = 'https://www.pro-football-reference.com'
            r = requests.get(url+'/players/'+last_initial+'/'+guessed_id+'.htm')
            soup = BeautifulSoup(r.content, 'html.parser')
            check = str(soup.find_all('span')[8])
            check = check[6:len(name)+6]
            check = check.upper()
            name = name.upper()
            if check == name:
                is_correct = True
            else:
                int_two = int_two+1
                if int_two == 10:
                    int_two = 0
                    int_one = int_one+1
                guessed_id = guessed_id[0:6]+str(int_one)+str(int_two)
        return guessed_id


    def get_Player_schedule(self):
        team = self.team.upper()
        teams = {
        'EAGLES':'PHI',
        'CARDINALS':'ARI',
        'FALCONS': 'ATL',
        'RAVENS': 'BAL',
        'BILLS':'BUF',
        'PANTHERS': 'CAR',
        'BEARS':'CHI',
        'BENGALS':'CIN',
        'BROWNS': 'CLE',
        'COWBOYS':'DAL',
        'BRONCOS':'DEN',
        'LIONS': 'DET',
        'PACKERS':'GB',
        'TEXANS': 'HOU',
        'COLTS': 'IND',
        'JAGUARS': 'JAC',
        'CHIEFS': 'KC',
        'RAIDERS': 'LV',
        'CHARGERS': 'LAC',
        'RAMS':'LAR',
        'DOLPHINS': 'MIA',
        'VIKINGS':'MIN',
        'PATRIOTS': 'NE',
        'SAINTS': 'NO',
        'GIANTS': 'NYG',
        'JETS':'NYJ',
        'STEELERS':'PIT',
        '49ERS': 'SF',
        'SEAHAWKS': 'SEA',
        'BUCCANEERS': 'TB',
        'TITANS': 'TEN',
        'WASHINGTON FOOTBALL TEAM': 'WFT'
        }

        teamSched = Schedule(teams[team])

        return teamSched


class Quarterback(Player):

    def getStats(self):
        Name_first = self.nameFirst
        Name_last = self.nameLast
        last_initial =  Name_last[0]
        ID = self.get_Player_ID()
        url = 'https://www.pro-football-reference.com'
        r = requests.get(url+'/players/'+last_initial+'/'+ID+'.htm')
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all('tbody')[0]
        mess = str(table).split()
        stats = []
        for index in mess:
            for i in range(len(index)+1):
                if index[0] == 'd' and index[1] == 'a' and index[2] == 't' and index[3] == 'a' and index[4 ]== '-' and index[5] == 's' and index[6] == 't' and index[7] == 'a' and index[8] == 't':
                    try:
                        if index[10:20] == '"pass_cmp"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:20] == '"pass_att"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:25] == '"pass_cmp_perc"':
                            if index[i] == '>':
                                if index[i+5] == '0' or index[i+5] == '1' or index[i+5] == '2' or index[i+5] == '3' or index[i+5] == '4' or index[i+5] == '5' or index[i+5] == '6' or index[i+5] == '7' or index[i+5] == '8' or index[i+5] == '9':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:20] == '"pass_yds"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    if index[i+3] == '0' or index[i+3] == '1' or index[i+3] == '2' or index[i+3] == '3' or index[i+3] == '4' or index[i+3] == '5' or index[i+3] == '6' or index[i+3] == '7' or index[i+3] == '8' or index[i+3] == '9':
                                        stats.append(index[i+1]+index[i+2]+index[i+3])
                                    else:
                                        stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:19] == '"pass_td"':
                            if index[i] == '>':
                                stats.append(index[i+1])
                        elif index[10:20] == '"pass_int"':
                            if index[i] == '>':
                                stats.append(index[i+1])
                        elif index[10:23] == '"pass_rating"':
                            if index[i] == '>':
                                if index[i+4] == '.':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:23] == '"pass_sacked"':
                            if index[i] == '>':
                                stats.append(index[i+1])
                        elif index[10:28] == '"pass_yds_per_att"':
                            if index[i] == '>':
                                if index[i+3] == '.':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:32] == '"pass_adj_yds_per_att"':
                            if index[i] == '>':
                                if index[i+3] == '.':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:20] == '"rush_att"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:20] == '"rush_yds"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    if index[i+3] == '0' or index[i+3] == '1' or index[i+3] == '2' or index[i+3] == '3' or index[i+3] == '4' or index[i+3] == '5' or index[i+3] == '6' or index[i+3] == '7' or index[i+3] == '8' or index[i+3] == '9':
                                        stats.append(index[i+1]+index[i+2]+index[i+3])
                                    else:
                                        stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:28] == '"rush_yds_per_att"':
                            if index[i] == '>':
                                if index[i+3] == '.':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:19] == '"rush_td"':
                            if index[i] == '>':
                                stats.append(index[i+1])
                        elif index[10:19] == '"offense"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    if index[i+3] == '0' or index[i+3] == '1' or index[i+3] == '2' or index[i+3] == '3' or index[i+3] == '4' or index[i+3] == '5' or index[i+3] == '6' or index[i+3] == '7' or index[i+3] == '8' or index[i+3] == '9':
                                        stats.append(index[i+1]+index[i+2]+index[i+3])
                                    else:
                                        stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append[index[i+1]]
                        elif index[10:19] == '"off_pct"':
                            if index[i] == '>':
                                if index[i+4] == '%':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                                elif index[i+3] == '%':
                                    stats.append(index[i+1]+index[i+2]+index[i+3])
                                else:
                                    stats.append(index[i+1]+index[i+2])



                    except:
                        continue
        stats = removeJunk(stats)
        gameLogs = seperateGames(stats,numQBStats)

        return gameLogs


    def dataframe(self):
         playerBoxscore = self.getStats()
         sched = self.get_Player_schedule()
         rows = []
         val = len(playerBoxscore)
         for i in range(val):
             rows.append(sched[i]._opponent_abbr)
         df = pd.DataFrame(data = playerBoxscore, index = rows, columns=['Passes Completed', 'Passes Attempted', 'Completion Percentage', 'Pass Yards', 'Pass TDs', 'Interceptions Thrown', 'Quarterback Rating', 'Fumbles', 'Pass Yds / Attempt', 'Pass Adj Yds / Attempt', 'Rush Attempts', 'Rush Yards', 'Rush Yds / Attempt', 'Rush TDs', 'Snaps Played', '% Total Snaps Played'])
         display(df)

Hurts = Quarterback('Jalen', 'Hurts', "Eagles")
Hurts.dataframe()
