from requests import get
from datetime import datetime,timedelta
import pytz
import csv

max_time_since = timedelta(hours=24)
output_date_format = "%Y-%m-%d"
output_time_format = "%I:%M %p"


#read URLs and process dates
reposCSV = open("repos.csv","r",encoding='utf-8-sig')
repos = csv.reader(reposCSV, delimiter=',')
dates = []

for row in repos:
  url = row[0]
  
  #with username in case we get "TOHacks2020" repos
  repo_name = url[url.find('.com/')+5:] 
  
  #get commits page
  commits_url = url + "/commits/master"
  response = get(commits_url)
  if response.status_code != 200:
    print(repo_name, "is an invalid URL")
    dates.append([url,"Error Code:",str(response.status_code)])
    continue
    
  #find oldest commit
  s = response.content.decode("utf-8")
  pos0 = s.find('<button class="btn btn-outline BtnGroup-item" disabled="disabled">Older</button>')
  while pos0 < 0: #click through pages until the "older" button is disabled
    pos1 = s.find('<a rel="nofollow" class="btn btn-outline BtnGroup-item" href="')
    pos2 = s.find('https://github.com/',pos1)
    pos3 = s.find('">Older</a>',pos1)
    response = get(s[pos2:pos3])
    s = response.content.decode("utf-8")
    pos0 = s.find('<a rel="nofollow" class="btn btn-outline BtnGroup-item" href="')
  pos = s.rfind("committed") + 37

  #read, process, and timezone dates
  date_naive_string = s[pos:pos+20]
  date_naive = datetime.strptime(date_naive_string,"%Y-%m-%dT%H:%M:%SZ")
  date_aware = pytz.utc.localize(date_naive).astimezone(pytz.timezone('US/Eastern'))
  date_aware_string = date_aware.strftime(output_date_format)
  time_aware_string = date_aware.strftime(output_time_format)
  comparison_date_aware = pytz.timezone('US/Eastern').localize(datetime.now())

  #difference between now and the repo's first commit
  date_difference = comparison_date_aware - date_aware
  
  #filter
  if date_difference > max_time_since:
    print(repo_name, "was created too long ago")
    
  #save info to later write date to csv
  dates.append([url,date_aware_string,time_aware_string])
    
reposCSV.close()

#save dates back to CSV
reposCSV = open("repos.csv","w",encoding='utf-8-sig',newline='')
repos = csv.writer(reposCSV, delimiter=',')
repos.writerows(dates)
reposCSV.close()
