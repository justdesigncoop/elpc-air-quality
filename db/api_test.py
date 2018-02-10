import requests

if __name__ == '__main__':
    # sessions list
    params = (
        ('page', '0'),
        ('page_size', '50'),
        ('q[measurements]', 'true'),
        ('q[time_from]', '0'),
        ('q[time_to]', '1439'),
        ('q[day_from]', '0'),
        ('q[day_to]', '355'),
        ('q[usernames]', 'HHHDenver'),
        ('q[location]', 'Denver'),
        ('q[distance]', '50'),
        ('q[sensor_name]', 'AirBeam-PM'),
        ('q[unit_symbol]', '\xB5g/m\xB3'),
    )
    response = requests.get('http://aircasting.org/api/sessions.json', params=params)
    
    # session by id
    response = requests.get('http://aircasting.org/api/sessions/9586.json')
    
    # averages
    params = (
        ('q[west]', '-105.42674388525387'),
        ('q[east]', '-104.28347911474606'),
        ('q[south]', '39.530285217883865'),
        ('q[north]', '39.99792504639966'),
        ('q[time_from]', '1320'),
        ('q[time_to]', '1319'),
        ('q[day_from]', '0'),
        ('q[day_to]', '365'),
        ('q[year_from]', '2015'),
        ('q[year_to]', '2016'),
        ('q[grid_size_x]', '46.98081264108352'),
        ('q[grid_size_y]', '25'),
        ('q[sensor_name]', 'AirBeam-PM'),
        ('q[measurement_type]', 'Particulate Matter'),
        ('q[unit_symbol]', '\xB5g/m\xB3'),
    )
    response = requests.get('http://aircasting.org/api/averages.json', params=params)
    
    # region
    params = (
        ('day_from', '0'),
        ('day_to', '365'),
        ('east', '165.44168097265174'),
        ('grid_size_x', '1'),
        ('grid_size_y', '1'),
        ('measurement_type', 'Particulate Matter'),
        ('north', '-24.217858119836414'),
        ('sensor_name', 'AirBeam-PM'),
        ('south', '-30.55369611748509'),
        ('tags', ''),
        ('time_from', '1320'),
        ('time_to', '1319'),
        ('unit_symbol', '\xB5g/m\xB3'),
        ('usernames', ''),
        ('west', '144.34793097265174'),
        ('year_from', '2015'),
        ('year_to', '2016g/m\xB3'),
    )
    response = requests.get('http://aircasting.org/api/region.json', params=params)
    
    # last session
    response = requests.get('http://aircasting.org/api/v2/data/sessions/last')