import constants as const
import utils

_points = const.POINTS_FILE


def get_points(drops: bool=True) -> dict:
    season = utils.read_json_file(_points)
    driver_points = {}

    if len(season) == 0:
        return driver_points

    for iracing_id, driver in season['Drivers'].items():
        points = driver['EarnedPoints']

        if drops:
            points = points - driver['DropPoints']
        
        driver_points[str(iracing_id)] = points
    
    return driver_points
