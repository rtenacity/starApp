from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
import numpy as np

Simbad.add_votable_fields("fluxdata(B)","fluxdata(V)","sp", "plx")
Vizier.ROW_LIMIT = -1

star_list = ['Betelgeuse', 'Rigel', 'Antares']

for star in star_list:
    result = Simbad.query_object(star)
    b_magnitude = result['FLUX_B'][0]
    v_magnitude = result['FLUX_V'][0]
    spectral_type = result['SP_TYPE'][0]
    parallax = result['PLX_VALUE'][0] * 1e-3
    
    distance = 1 / parallax
    absolute_magnitude = v_magnitude - 5 * (np.log10(distance) - 1)
    luminosity = 10 ** ((4.83 - absolute_magnitude) / 2.5)
    
    temperature_result = Vizier.get_catalogs("J/ApJ/741/4/table1")
    print (temperature_result)
    temperature_table = temperature_result[0]
    temperature_row = temperature_table[temperature_table['Star'] == star]
    if len(temperature_row) == 0:
        print(f"{star} not found in temperature catalog")
        continue
    temperature = temperature_row['Teff'].data[0]
    
    print(f"Star: {star}")
    print(f"Absolute Magnitude: {absolute_magnitude}")
    print(f"Spectral Type: {spectral_type}")
    print(f"Temperature: {temperature} K")
    print(f"Luminosity: {luminosity}")