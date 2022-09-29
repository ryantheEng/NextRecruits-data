import pandas as pd
import openpyxl as xl

#constants
AHC = 'Associate Head Coach'
AC = 'Assistant Coach'
HC = 'Head Coach'
GM = 'General Manager'
BUS = 'Business'
AGM = 'Assistant General Manager'
VP = 'Vice President'
DIR = 'Director'
OPS = 'Operations'
DEV = 'Developer'
ASS = 'Assistant'

LISTROLES = [
    ['AHC',AHC],
    ['AC',AC],
    ['HC',HC],
    ['GM',GM],
    ['BUS',BUS],
    ['AGM',AGM],
    ['VP',VP],
    ['DIR',DIR],
    ['OPS',OPS],
    ['DEV',DEV],
    ['ASS',ASS]
]

class Processing():
    #definitions
    COL_OG = 5 # number of columns initially
    COL_N = 6 # number of columns we want

    def __init__(self,file):
        self.file = file
        

    #fun create df from sheet
    def toDF(self,sheet):
        return pd.read_excel(self.file,sheet,converters={'Team':str,'Role':str,'Name':str,'Phone #':str,'Email':str})

    def filter(self,df,league_name):

        # init new lists for new df
        team = []
        role = []
        name = []
        phone = []
        email = []
        league = [] # conference
        league_ = [] # actual league

        # cols
        cols = ['team','role','name','phone','email','conference','league']

        # init memory 
        last_league = ''
        last_team = ''

        for i,row in df.iterrows():
            
            isleague = True
            empty_check = pd.DataFrame.isna(row)
            if empty_check[0] == True & empty_check[1] == True & empty_check[2] == True & empty_check[3] == True & empty_check[4] == True:
                break
            if empty_check[1] == False:
                isleague = False        
            
            if empty_check[0] == False & empty_check[3] == False & empty_check[4] == False: #if it is not empty
                last_team = row[0]
                isteam = False
            else:
                isteam = True
                
            if isleague==True: # look for the league
                last_league = row[0]
                continue
            else:
                team.append(last_team.replace("\u00A0",""))
                name.append(str(row[2]).replace("\u00A0",""))

                phone_e = str(row[3]).replace(" ",'').replace('(','').replace(')',' ').replace(' ','').replace('-','').replace("\u00A0","")
                print(phone_e)
                phone.append(phone_e)
                email.append(str(row[4]).replace("\u00A0",""))
                league.append(last_league.replace("\u00A0",""))
                league_.append(league_name.replace("\u00A0",""))

                #role change
                if empty_check[1] == True:
                    None
                elif '/' in row[1]: # there are multiple roles
                    lRoles = str(row[1]).split('/')
                    for role in lRoles:
                        new_role = []
                        n = role.split(' ') #split by white space
                        for word in n:
                            new_word = ''
                            for r in LISTROLES: # look through words and add better words
                                if word.capitalize() == r[0]:
                                    new_word = new_word + r[1] + ' '
                                else:
                                    new_word+=word
                        new_role.append(new_word) # this is my new written role
                    role.append(new_role)
                else:

                    n = str(row[1]).split(' ') #split by white space
                    for word in n:
                        new_word = ''
                        for r in LISTROLES: # look through words and add better words
                            if word.capitalize() == r[0]:
                                new_word = new_word + r[1] + ' '
                            else:
                                new_word+=word
                    new_role.append(new_word) # this is my new written role
                    role.append(new_role)
                continue
        
        newdf = pd.DataFrame(list(zip(team,role,name,phone,email,league,league_)),columns=cols)
        return newdf

    def tojson(self,df,filename):
        df.to_json(filename+'.json',orient='records')
        return

    def script(self):
        hdr = xl.load_workbook(self.file)
        for i,name in enumerate(hdr.sheetnames):
            if i==0:
                df = self.toDF(i)
                fdf = self.filter(df,name)
            else:
                df = self.toDF(i)
                ndf = self.filter(df,name)
                fdf = pd.concat([fdf,ndf])
            print('Done '+name)
        
        self.tojson(fdf,'database')

# script('NR.xlsx')