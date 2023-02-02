from astroquery.vizier import Vizier

Vizier.ROW_LIMIT = -1
temperature_result = Vizier.get_catalogs("J/MNRAS/454/2863")
print(temperature_result)
temperature_table = temperature_result[0]
temperature_row = temperature_table[temperature_table['Name'] == 'Betelgeuse']
temperature = temperature_row['Teff'].data[0]
print(f"Temperature: {temperature} K")