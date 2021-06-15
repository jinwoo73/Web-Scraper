import requests
from bs4 import BeautifulSoup
LIMIT=50
URL="https://www.indeed.com/jobs?as_and=Python+Developer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch"
def extract_indeed_pages():
  result=requests.get(URL) 

  soup=BeautifulSoup(result.text,"html.parser")
  pagination = soup.find("div",{"class":"pagination"})

  links = pagination.find_all('a')
  pages=[]
  for link in links[:-1]:
    pages.append(int(link.string))
  maxpage=pages[-1]
  return maxpage

def extract_indeed_jobs(last_page):
  
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping page{page}")
    result=requests.get(f"{URL}&start={0*LIMIT}")
    soup=BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
      job=extract_job(result)
      jobs.append(job)
  return jobs
def extract_job(html):
  title=html.find("h2",{"class":"title"}).find("a")["title"]
  company =html.find("span",{"class":"company"})
  company_anchor=company.find("a")
  if company_anchor:
    company=str(company_anchor.string)
  else:
    company=str(company.string)
  company = company.strip()
  location=html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"] 
  
  return {'title':title,'company':company,'location':location,"link":f"https://www.indeed.com/viewjob?jk={job_id}&tk=1f7ar1ccinpvj800&from=serp&vjs=3"}

      
  



