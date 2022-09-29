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

# class to process the data from the database

class Processing():
    def __init__(self,file) -> None:
        self.file = file
        self.cols = ['team','role','name','phone','email','conference','league']

    def removeNull(self,df):
        """ Remove the Nulls """
        for x,row in df.iterrows():
            for y,val in row.items():
                if not isinstance(val,str):
                    continue
                if '\u00a0' in val:
                    df.at[x,y] = df.at[x,y].replace('\u00a0','')
                if '\xa0' in val:
                    df.at[x,y] = df.at[x,y].replace('\xa0','')
                if '\u00e9' in val:
                    df.at[x,y] = df.at[x,y].replace('\u00e9','e')
                if '\u00e8' in val:
                    df.at[x,y] = df.at[x,y].replace('\u00e8','e')
                if '\u2013' in val:
                    df.at[x,y] = df.at[x,y].replace('\u2013','-')
        return df

    
    def toDF(self,sheet):
        """function to create dataframe from each sheet"""
        return pd.read_excel(self.file,sheet,converters={'Conference':str,'Team':str,'Role':str,'Name':str,'Phone':str,'Email':str})


    def roleWordReplaceHelper(self,roll):
        """function to help filter and rewrite the roles"""
        words = roll.split(' ')
        for word in words: # eg VP
            newRole = ' '
            for r in LISTROLES:
                replaceFlag = False
                if word == r[0] or word.capitalize() == r[0]:
                    newRole += r[1] + ' '
                    replaceFlag = True
                    break
            if not replaceFlag:
                newRole += word
        return newRole

    def filter(self,df,league_name):
        """filter the data from the df"""

        # inits of new lists to concat for new df
        team,role,name,phone,email,conference,league = [],[],[],[],[],[],[]

        # memory vars
        teamLast = 'none'
        conferenceLast = 'none'

        for i,row in df.iterrows():

            # check the cols to see if any cells empty
            emptyCheck = pd.DataFrame.isna(row)

            # empty if no email/phone and conference
            if emptyCheck[4] == True & emptyCheck[5] == True & emptyCheck[0] == True:
                continue

            # check each column starting with 0 and 1
            else:
                # check for last conferences and teams
                if emptyCheck[0] == False:
                    conferenceLast = row[0]
                if emptyCheck[1] == False:
                    teamLast = row[1]
            
                conference.append(conferenceLast)
                team.append(teamLast)

                # checking the phone # replace digits with *
                # phoneNum = row[4]
                # for spot in phoneNum:
                #     if spot.isdigit():
                #         phoneNum.replace(spot,'*')
                # phone.append(phoneNum)

                # email/conference/league/name
                email.append(row[5])
                conference.append(conferenceLast)
                league.append(league_name)
                name.append(row[3])
                phone.append(str(row[4]).replace('tel:',''))

                # roles
                if not emptyCheck[2]:
                    if '/' in row[2]:
                        listRoles = row[2].split('/')
                        rolesToPush = []
                        for role_ in listRoles:
                            rolesToPush.append(self.roleWordReplaceHelper(role_))
                        role.append(rolesToPush)
                    else:
                        role.append([self.roleWordReplaceHelper(row[2])])
        nDF = pd.DataFrame(list(zip(team,role,name,phone,email,conference,league)),columns=self.cols)
        return nDF

    
    def toJSON(self,df,filename):
        """send to json"""
        df.to_json(filename+'.json',orient='records')
    
    
    def fullScript(self):
        """put it all together"""
        hdr = xl.load_workbook(self.file)
        for i,name in enumerate(hdr.sheetnames):
            
            df = self.toDF(i)
            df = self.removeNull(df)
            if i == 0:
                fdf = self.filter(df,name)

            else:
                ndf = self.filter(df,name)
                fdf = pd.concat([fdf,ndf])
            
            print('Finished sheet #'+str(i)+': '+str(name))
            
        self.toJSON(fdf,'databasev1')
        print('We getting somewhere')


p = Processing('NextRecruitDatabase.xlsx')
p.fullScript()