from sportsreference.nfl.boxscore import Boxscore
from sportsreference.nfl.boxscore import BoxscorePlayer
from sportsreference.nfl.schedule import Schedule
from IPython.display import display
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np

global numQBStats
global numReceiverStats
global numRBStats
global hasAttPass
global realAbbs
numQBStats = 16
numReceiverStats = 9
numRBStats = 13
hasAttPass = True
realAbbs = {
'PHI':'PHI',
'CRD':'ARI',
'ATL': 'ATL',
'RAV': 'BAL',
'BUF':'BUF',
'CAR': 'CAR',
'CHI':'CHI',
'CIN':'CIN',
'CLE': 'CLE',
'DAL':'DAL',
'DEN':'DEN',
'DET': 'DET',
'GNB':'GB',
'HTX':'HOU',
'CLT':'IND',
'JAX': 'JAC',
'KAN': 'KC',
'RAI': 'LV',
'SDG': 'LAC',
'RAM':'LAR',
'MIA': 'MIA',
'MIN':'MIN',
'NWE': 'NE',
'NOR': 'NO',
'NYG': 'NYG',
'NYJ':'NYJ',
'PIT':'PIT',
'SFO':'SF',
'SEA':'SEA',
'TAM':'TB',
'OTI':'TEN',
'WAS': 'WFT'
}

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

def isContained(str, char):
    contained = False
    for index in str:
        if index == char:
            contained = True
    return contained

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
        count = 0
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
            elif count == 100:
                guessed_id = "Sorry! We cannot find the player you're looking for!"
                break
            else:
                int_two = int_two+1
                if int_two == 10:
                    int_two = 0
                    int_one = int_one+1
                guessed_id = guessed_id[0:6]+str(int_one)+str(int_two)
            count = count+1
        return guessed_id


    def get_Player_schedule(self):
        team = self.team.upper()
        teams = {
        'EAGLES':'PHI',
        'CARDINALS':'CRD',
        'FALCONS': 'ATL',
        'RAVENS': 'RAV',
        'BILLS':'BUF',
        'PANTHERS': 'CAR',
        'BEARS':'CHI',
        'BENGALS':'CIN',
        'BROWNS': 'CLE',
        'COWBOYS':'DAL',
        'BRONCOS':'DEN',
        'LIONS': 'DET',
        'PACKERS':'GNB',
        'TEXANS': 'HTX',
        'COLTS': 'CLT',
        'JAGUARS': 'JAX',
        'CHIEFS': 'KAN',
        'RAIDERS': 'RAI',
        'CHARGERS': 'SDG',
        'RAMS':'RAM',
        'DOLPHINS': 'MIA',
        'VIKINGS':'MIN',
        'PATRIOTS': 'NWE',
        'SAINTS': 'NOR',
        'GIANTS': 'NYG',
        'JETS':'NYJ',
        'STEELERS':'PIT',
        '49ERS': 'SFO',
        'SEAHAWKS': 'SEA',
        'BUCCANEERS': 'TAM',
        'TITANS': 'OTI',
        'WASHINGTON FOOTBALL TEAM': 'WAS'
        }

        teamSched = Schedule(teams[team])

        return teamSched

    def find_player_stats_from_html(self):

        Name_first = self.nameFirst
        Name_last = self.nameLast
        last_initial =  Name_last[0]
        ID = self.get_Player_ID()
        url = 'https://www.pro-football-reference.com'
        r = requests.get(url+'/players/'+last_initial+'/'+ID+'.htm')
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all('tbody')[0]
        refined_table = str(table).split()

        return refined_table

    def getStats(self):
        mess = self.find_player_stats_from_html()
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
                                    if index[i+1] == '0':
                                        stats.append('0%')
                                        hasAttPass = False
                                    else:
                                        hasAttPass = True
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
                        elif index[10:19] == '"targets"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:15] == '"rec"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:21] == '"catch_pct"':
                            if index[i] == '>':
                                if index[i+5] == '0' or index[i+5] == '1' or index[i+5] == '2' or index[i+5] == '3' or index[i+5] == '4' or index[i+5] == '5' or index[i+5] == '6' or index[i+5] == '7' or index[i+5] == '8' or index[i+5] == '9':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:19] == '"rec_yds"':
                            if index[i] == '>':
                                if index[i+2] == '0' or index[i+2] == '1' or index[i+2] == '2' or index[i+2] == '3' or index[i+2] == '4' or index[i+2] == '5' or index[i+2] == '6' or index[i+2] == '7' or index[i+2] == '8' or index[i+2] == '9':
                                    if index[i+3] == '0' or index[i+3] == '1' or index[i+3] == '2' or index[i+3] == '3' or index[i+3] == '4' or index[i+3] == '5' or index[i+3] == '6' or index[i+3] == '7' or index[i+3] == '8' or index[i+3] == '9':
                                        stats.append(index[i+1]+index[i+2]+index[i+3])
                                    else:
                                        stats.append(index[i+1]+index[i+2])
                                else:
                                    stats.append(index[i+1])
                        elif index[10:27] == '"rec_yds_per_rec"':
                            if index[i] == '>':
                                if index[i+3] == '.':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:27] == '"rec_yds_per_tgt"':
                            if index[i] == '>':
                                if index[i+3] == '.':
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4]+index[i+5])
                                else:
                                    stats.append(index[i+1]+index[i+2]+index[i+3]+index[i+4])
                        elif index[10:18] == '"rec_td"':
                            if index[i] == '>':
                                stats.append(index[i+1])
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
        count = 0
        for index in stats:
            if index == '</td':
                stats.remove(index)
                stats.insert(count,'0')
                count+=1

        return stats


class Quarterback(Player):
    def set_up_dataframe(self):
        Boxscore = self.getStats()
        gameLogs = seperateGames(Boxscore,numQBStats)
        print(gameLogs)
        sched = self.get_Player_schedule()
        row = []
        val = len(gameLogs)
        for i in range(val):
            row.append(realAbbs[sched[i]._opponent_abbr])

        return gameLogs, row

    def dataframe(self):
         playerBoxscore, rows = self.set_up_dataframe()
         df = pd.DataFrame(data = playerBoxscore, index = rows, columns=['Passes Completed', 'Passes Attempted', 'Completion Percentage', 'Pass Yards', 'Pass TDs', 'Interceptions Thrown', 'Quarterback Rating', 'Fumbles', 'Pass Yds / Attempt', 'Pass Adj Yds / Attempt', 'Rush Attempts', 'Rush Yards', 'Rush Yds / Attempt', 'Rush TDs', 'Snaps Played', '% Total Snaps Played'])
         display(df)

class Receiver(Player):
    def set_up_dataframe(self):
        Boxscore = self.getStats()
        try:
           if isContained(Boxscore[8],'%') == True:
               gameLogs = seperateGames(Boxscore,numReceiverStats)
           else:
               gameLogs = seperateGames(Boxscore,numRBStats)
        except:
               print("This player has no receiving stats.")
               quit()
        sched = self.get_Player_schedule()
        row = []
        val = len(gameLogs)
        for i in range(val):
            row.append(realAbbs[sched[i]._opponent_abbr])

        return gameLogs, row

    def dataframe(self):
         playerBoxscore, rows = self.set_up_dataframe()
         if isContained(playerBoxscore[0][8],'%') == False:
             df = pd.DataFrame(data = playerBoxscore, index = rows, columns=['Targets', 'Receptions', 'Rec Yards', 'Yds/Rec','Rec TDs','Catch%', 'Yds/Target','Rush Attempts', 'Rush Yards', 'Rush Yds / Attempt', 'Rush TDs', 'Snaps Played', '% Total Snaps Played'])
         else:
             df = pd.DataFrame(data = playerBoxscore, index = rows, columns=['Targets', 'Receptions', 'Rec Yards', 'Yds/Rec','Rec TDs','Catch%', 'Yds/Target', 'Snaps Played', '% Total Snaps Played'])
         display(df)

class RunningBack(Player):
    def set_up_dataframe(self):
        Boxscore = self.getStats()
        if len(Boxscore) < numRBStats:
            print("This player has no rushing stats.")
            quit()
        gameLogs = seperateGames(Boxscore,numRBStats)
        sched = self.get_Player_schedule()
        row = []
        val = len(gameLogs)
        for i in range(val):
            row.append(realAbbs[sched[i]._opponent_abbr])

        return gameLogs, row

    def dataframe(self):
        playerBoxscore, rows = self.set_up_dataframe()
        df = pd.DataFrame(data = playerBoxscore, index = rows, columns=['Rush Attempts', 'Rush Yds', 'Rush Yds/Attempt', 'Rush TD', 'Targets', 'Receptions', 'Rec Yards', 'Yds/Rec','Rec TDs','Catch%', 'Yds/Target', 'Snaps Played', '% Total Snaps Played'])
        display(df)

### QBS and other positions may be missing a stat if they don't play. Find way to fill that with a 0.
firstName = "Jalen"
lastName = "Hurts"
team = "Eagles"
Hurts = Quarterback(firstName, lastName, team)
Hurts.dataframe()
