import bs4 as bs
import requests
import json
import lxml

def lookup(ucinetid):
  r = requests.get('https://directory.uci.edu/people/{}.txt'.format(ucinetid))
  for line in r.text.split('\n'):
    if 'Name:' in line:
      line = line[line.find(':')+2:].replace('<br/>','')
      name = line.split()
      fn = name[0]
      ln = name[-1]
      return ln + ', ' + fn[0]

# Grab your own cookies from a ucinetid login
COOKIES = {
    
}

NOTMYLINKS = [
    'Privacy',
    'Contact EEE Support',
    'Office of Information Technology',
    'EEE+ EaterEvals',
    'Faculty List',
    'Departments',
    'Logout',
    'FAQ',
    'Contact Us',
    'Return to department list',
    ''
]

BASE = 'https://eaterevals.eee.uci.edu'

# Creating sessions object with manual cookies
s = requests.Session()
[s.cookies.set(name, value) for name, value in COOKIES.items()]

#list of instructors
iids = set()
with open('depts.txt') as depts:
  for dept in depts.read().split('\n'):
    print(dept)
    dlist = bs.BeautifulSoup(s.get(BASE+'/department/'+dept).text, 'lxml')
    courses = [a['href'] for a in dlist.find_all('a') if a.text.strip() not in NOTMYLINKS]

    # all courses under this department
    for course in courses:
      clist = bs.BeautifulSoup(s.get(BASE+course).text, 'lxml')
      sections = [a['href'] for a in clist.find_all('a') if a.text.strip() == 'View results']

      # all sections for this course
      for section in sections:
        parts = section.split('/')[-1].split('-')
        iids.add(parts[2])

names = {lookup(n):n for n in iids}
with open('names.json', 'w') as out:
  out.write(json.dumps(names))
  
