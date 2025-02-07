import utils


_points = 'static/data/league.json'


def get_points(season: int, drops: bool=True) -> dict:
    raw = utils.read_json_file(_points)
    season = raw['Seasons'][str(season)] if str(season) in raw['Seasons'] else {}
    driver_points = {}

    if len(season) == 0:
        return driver_points

    for iracing_id, driver in season['Drivers'].items():
        points = driver['EarnedPoints']

        if drops:
            points = points - driver['DropPoints']
        
        driver_points[str(iracing_id)] = points
    
    return driver_points
