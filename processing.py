import pandas as pd
import openpyxl as xl

#definitions
AHC = 'Associate Head Coach'
AC = 'Assistant Coach'
HC = 'Head Coach'
COL_OG = 5 # number of columns initially
COL_N = 6 # number of columns we want

#fun create df from sheet
def toDF(file:str,sheet:int):
    return pd.read_excel(file,sheet)

def filter(df:pd.DataFrame,league_name:str):

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
        
        if empty_check[0] == False: #if it is not empty
            last_team = row[0]
            isteam = False
        else:
            isteam = True
            
        if isleague==True: # look for the league
            last_league = row[0]
            continue
        else:
            team.append(last_team)
            name.append(row[2])
            phone.append(row[3])
            email.append(row[4])
            league.append(last_league)
            league_.append(league_name)

            #role change
            if empty_check[1] == True:
                None
            elif '/' in row[1]:
                list_role = row[1].split('/')
                role.append(list_role)
            else:
                role.append(row[1])
            continue
    
    newdf = pd.DataFrame(list(zip(team,role,name,phone,email,league,league_)),columns=cols)
    return newdf

def tojson(df:pd.DataFrame,filename:str):
    df.to_json(filename+'.json',orient='records')
    return

def script(file:str):
    hdr = xl.load_workbook(file)
    for i,name in enumerate(hdr.sheetnames):
        if i==0:
            df = toDF(file,i)
            fdf = filter(df,name)
        else:
            df = toDF(file,i)
            fdf = pd.concat([fdf,filter(df,name)])
        print('Done '+name)
    
    tojson(fdf,'database.json')

script('NR.xlsx')