from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
import numpy as np
import re
import requests
from bs4 import BeautifulSoup

Simbad.add_votable_fields("fluxdata(B)","fluxdata(V)","sp", "plx")
Vizier.ROW_LIMIT = -1

def remove_non_numeric(string):
  for i, char in enumerate(string):
    if not char.isdigit() and char != '.' and char != ',' and char != '-':
        return string[:i]
    if char == ',':
        return string[:i] + '' + string[i+1:]
  return string
def remove_bracketed(string):
    # Use a regular expression to match and capture items enclosed in brackets or parentheses
    pattern = r'\[[^\]]*\]|\([^\)]*\)'
    return re.sub(pattern, '', string)
star_list = ['Betelgeuse', 'Rigel', 'Antares']

def get_star(star):
    out = []
    url = f'https://en.wikipedia.org/wiki/{star}'
    out.append(star)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x, d, l, m, t, mA, e = 0, 0, 0, 0, 0, 0, 0
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
            raw = td_tags[1].text
            value = re.sub(r"\[.*?\]", "", raw)
            value = re.sub(r"\s*±\s*\d+.*", "", value)
            value = remove_non_numeric(value)
            value = remove_non_numeric(value)
            if ('Distance' in key):
                if d == 0:
                    out.append(value)
                    print(f"{key}: {value}")
                    d+=1
                else:
                    pass
            elif('Temperature' in key):
                if t == 0:
                    out.append(value)
                    temperature = value
                    print(f"{key}: {value}")
                    t+=1
                else:
                   pass
        if (len(th_tags) >= 1 and len(td_tags) == 1):
            try:
                key = th_tags[x].find('a').text
                key = key.strip()
                value = td_tags[x].find('a').text
                value = re.sub(r"\[.*?\]", "", value)
                value = value.strip()
                if 'Evolutionary' in key: 
                    if e == 0:
                        out.append(value)
                        evol = value
                        print(f"{key}: {value}")
                        e+=1
                    else:
                        pass
            except:
                pass
            x+=1
    result = Simbad.query_object(star)
    b_magnitude = result['FLUX_B'][0]
    v_magnitude = result['FLUX_V'][0]
    spectral_type = result['SP_TYPE'][0]
    parallax = result['PLX_VALUE'][0] * 1e-3  # convert from milliarcseconds to arcseconds
    
    distance = 1 / parallax
    absolute_magnitude = v_magnitude - 5 * (np.log10(distance) - 1)
    luminosity = 10 ** ((4.83 - absolute_magnitude) / 2.5)
    
    print(f"Star: {star}")
    print(f"Absolute Magnitude: {absolute_magnitude}")
    print(f"Spectral Type: {spectral_type}")
    print(f"Luminosity: {luminosity}")

    return [star, absolute_magnitude, spectral_type, luminosity, temperature, evol]

print(get_star('Betelgeuse'))