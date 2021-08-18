import requests
import json
import pandas as pd
from pandas import json_normalize
pd.options.display.max_rows = 20
pd.options.display.max_columns = 12

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': 'https://www.inc.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.inc.com/',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
}

r = requests.get('https://api.inc.com/rest/i5list/2021', headers=headers)

data = json.loads(r.text)
df = json_normalize(data['companies'])
df.dropna(axis=1, thresh=4500, inplace=True)
df.set_index('rank',inplace=True)
df.drop(['inc5000companyId', 'inc5000yearId', 'ifc_filelocation', 'ifc_ifmid',
         'ifc_business_model','ifc_ifiid', 'ifc_verified_companyflag',
         'raw_revenue', 'yrs_on_list', 'zipcode', 'article'], axis = 1, inplace=True)
         
#myIndustry accepted values
set(df.industry)

#myMetro accepted values
set(df.metrocode)

#myMetro is optional because we might want to see what remote jobs we could apply for
myMetro = None
#myIndustry is mandatory because the point of this program is to filter the 5000 company list to assist in job search
myIndustry = 'Software'

print(f'Siri, please find me the fastest growing opportunities in {myIndustry}')

def findMyNextOpportunity(myIndustry, myMetro=None):
    tearsheet = df[df['industry'] == myIndustry]
    
    if myMetro is not None:
        tearsheet = tearsheet[tearsheet['metrocode'] == myMetro]
    else:
        return tearsheet
    
    return tearsheet
    
#the following call to 'findMyNextOpportunity' function will retrieve just 20 high value employment prospects
findMyNextOpportunity('Software', myMetro = 'Chicago-Naperville-Elgin, IL-IN-WI')
