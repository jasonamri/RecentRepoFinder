from requests import get
from datetime import datetime,timedelta
import pytz

max_time_since = timedelta(hours=24)

reposTxt = open("repos.txt","r")

for url in reposTxt:
  #with username in case we get "TOHacks2020" repos
  repo_name = url[url.find('.com/')+5:-1] 
  
  #get commits page, and pull oldest dated item
  s = get(url[:-1] + "/commits/master").content.decode("utf-8")
  pos = s.rfind("committed") + 37
  date_string = s[pos:pos+20]
  date = datetime.strptime(date_string,"%Y-%m-%dT%H:%M:%SZ")

  #difference between now and the repo's first commit
  date_difference = pytz.timezone('US/Eastern').localize(datetime.now()) - pytz.utc.localize(date)
  
  #filter
  if date_difference > max_time_since:
    print(repo_name, "was created too long ago")
    

 
  