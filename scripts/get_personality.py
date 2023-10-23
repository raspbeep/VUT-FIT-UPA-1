from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://encyklopedie.brna.cz/home-mmb/?acc=profil_osobnosti&load=171'

html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, "html.parser")

content = soup.find('div', class_='content')
rows = content.find_all('div', class_='row')

for row in rows:
    title = row.find('span', class_='attr-title')
    if title is not None:
        print(title.get_text())
        txt = row.find('p', class_='full')
        if txt is not None:
            print(''.join(txt.get_text()))
        print()


