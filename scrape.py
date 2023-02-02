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
    x, d, l, m, t, mA, e = 0, 0, 0, 0, 0, 0, 0
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    infobox = soup.find('table', {'class': 'infobox'})
    tbody = infobox.find('tbody')
    tr_tags = tbody.find_all('tr')
    for tr in tr_tags:
        
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
            if ('Distance' in key):
                #if d == 0:
                    out.append(value)
                    print(f"{key}: {value}")
                    d+=1
                #else:
                 
                #   pass
            elif ('Luminosity (visual' in key):
                #if l ==0:
                    out.append(value)
                    print(f"{key}: {value}")
                    l+=1
                #else:
                #    pass
            elif ('Mass' in key):
                #if m == 0:
                    out.append(value)
                    print(f"{key}: {value}")
                    m+=1
                #else:
                #    pass
            elif('Temperature' in key):
                #if t == 0:
                    out.append(value)
                    print(f"{key}: {value}")
                    t+=1
                #else:
                #    pass
            elif('Magnitude' in key):
                #if mA == 0:
                    out.append(value)
                    print(f"{key}: {value}")
                    mA+=1
                #else:
                #    pass
        if (len(th_tags) >= 1 and len(td_tags) == 1):
            try:
                print(key)
                key = th_tags[x].find('a').text
                key = key.strip()
                value = td_tags[x].find('a').text
                value = re.sub(r"\[.*?\]", "", value)
                value = value.strip()
                
                if 'Evolutionary' in key: 
                    out.append(value)
                    print(f"{key}: {value}")
                    e+=1
                    #else:
                     
                     #   pass
            except:
                pass
            x+=1
    if (out[1][1]).isalpha() == False:
        out.insert(1, 'nAn')
    return out

sus = get_star('Proxima_Centauri')
print(sus)

sus2 = get_star('rigel')
print(sus2)