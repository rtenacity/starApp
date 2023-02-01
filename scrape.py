import requests
from bs4 import BeautifulSoup
import re

def remove_non_numeric(string):
  for i, char in enumerate(string):
    if not char.isdigit() and char != '.' and char != ',':
        return string[:i]
    if char == ',':
        return string[:i] + '' + string[i+1:]
  return string

def get_star(star):
    out = []
    url = f'https://en.wikipedia.org/wiki/{star}'
    out.append(star)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    infobox = soup.find('table', {'class': 'infobox'})
    tbody = infobox.find('tbody')
    tr_tags = tbody.find_all('tr')
    for tr in tr_tags:
        x = 0
        td_tags = tr.find_all('td')
        th_tags = tr.find_all('th')
        if len(td_tags) == 2:
            key = td_tags[0].text
            key = re.sub(r"\[.*?\]", "", key)
            value = td_tags[1].text
            value = re.sub(r"\[.*?\]", "", value)
            value = re.sub(r"\s*±\s*\d+.*", "", value)
            value = remove_non_numeric(value)
            value = remove_non_numeric(value)
            if ('Distance' in key) or ('Luminosity (visual' in key) or ('Mass' in key) or ('Temperature' in key) or ('Parallax' in key) or ('agnitude' in key):
                out.append(value)
                print(f"{key}: {value}")
        if (len(th_tags) >= 1 and len(td_tags) == 1):
            try:
                key = th_tags[x].find('a').text
                key = key.strip()
                value = td_tags[x].find('a').text
                value = re.sub(r"\[.*?\]", "", value)
                value = value.strip()
                if 'Evolutionary' in key: 
                    print(f"{key}: {value}")
                    out.append(value)
                if 'bsolute' in key:
                    print(f"{key}: {value}")
                    out.append(value)
            except:
                pass
            x+=1
    if out[1].isalpha() == False:
        out.insert(1, 'nAn')
    return out

sus = get_star('Proxima_Centauri')
print(sus)

sus2 = get_star('alpha_Centauri')
print(sus2)