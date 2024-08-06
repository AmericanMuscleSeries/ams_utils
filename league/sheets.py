# Distributed under the Apache License, Version 2.0.
# See accompanying NOTICE file for details.

import json
import logging
import gspread
import argparse
from operator import itemgetter

from league.objects import League, Group, SortBy

_ams_logger = logging.getLogger('ams')


class GDrive:
    __slots__ = ["_gc",
                 "_results_key", "_results_xls", "_result_sheets",
                 "_driver_key", "_drivers_xls", "_driver_sheets"]

    def __init__(self, credentials_filename: str):
        self._gc = None
        self._results_key = None
        self._results_xls = None
        self._result_sheets = dict()
        self._driver_key = None
        self._drivers_xls = None
        self._driver_sheets = dict()
        self._gc = gspread.oauth(
            credentials_filename=credentials_filename)

    def connect_to_results(self, key: str, sheets: dict) -> None:
        self._results_key = key
        self._results_xls = self._gc.open_by_key(self._results_key)
        for group, sheet in sheets.items():
            self._result_sheets[group] = self._results_xls.worksheet(sheet)

    def push_results(self, lg: League, season: int, groups: list, sort_by: SortBy, handicap: bool) -> int:
        count = 0  # Keeping track of sheet update calls, you only get 60/min with free projects
        # gsheets takes a list(list())
        season_values = list()

        dates = list()
        date_values = list()
        tracks = list()
        track_values = list()

        # How many cells of data for each race are we pushing?
        num_race_cells = 12
        if handicap:
            num_race_cells = 13

        season = lg.get_season(season)
        for race_number in range(len(season.races)):
            race = season.get_race(race_number + 1)
            track_name = race.track
            if track_name.count(' ') > 2:
                split_at = track_name.find(' ', track_name.find(' ') + 1)
                track_name = race.track[:split_at] + '\n' + race.track[split_at:]
            for i in range(num_race_cells):
                tracks.append(track_name)
                dates.append(race.date)
        date_values.append(dates)
        track_values.append(tracks)

        for group in groups:
            season_values.clear()
            # Push Race Dates and Tracks
            self._result_sheets[group].update(range_name="R2", values=date_values)
            self._result_sheets[group].update(range_name="R3", values=track_values)
            count += 2

            for cust_id, driver in season.drivers.items():
                if driver.group != group:
                    continue
                row = list()  # Make a list per driver row
                row.append(driver.name)
                row.append(driver.car_number)
                row.append(driver.earned_points)
                if handicap:
                    row.append(driver.handicap_points)
                else:
                    row.append(driver.earned_points-driver.drop_points)
                row.append(driver.clean_driver_points)
                row.append(driver.total_incidents)
                row.append(driver.total_wins)
                row.append(driver.total_races)
                row.append("{:.1f}".format(driver.average_finish))
                row.append(driver.race_finish_points)
                row.append(driver.pole_position_points)
                row.append(driver.laps_lead_points)
                row.append(driver.most_laps_lead_points)
                row.append(driver.fastest_lap_points)
                row.append("{:.2f}".format(driver.mu))
                row.append("{:.2f}".format(driver.sigma))

                for race_number in range(len(season.races)):
                    result = season.get_race(race_number+1).get_result(cust_id)
                    if result is None:
                        for i in range(num_race_cells):
                            row.append("")
                    else:
                        row.append(result.start_position)
                        row.append(result.finish_position)
                        row.append(result.points)
                        row.append("Y" if result.pole_position else "")
                        row.append("Y" if result.laps_lead > 0 else "")
                        row.append("Y" if result.fastest_lap else "")
                        if handicap:
                            row.append(result.handicap_points)  # HCP
                        row.append(result.incidents)
                        row.append(result.clean_driver_points)
                        row.append(result.laps_completed)
                        row.append(result.laps_lead)
                        row.append("{:.2f}".format(result.mu))
                        row.append("{:.2f}".format(result.sigma))
                season_values.append(row)

            sort_idx = 2 if sort_by == SortBy.Earned else 3
            season_values = sorted(season_values, key=itemgetter(sort_idx), reverse=True)
            # Pad the rest with blanks
            max_racers = 35
            if len(season_values) < max_racers:
                for extra_rows in range(max_racers - len(season_values)):
                    row = list()
                    for i in range(33):
                        row.append("")
                    season_values.append(row)
            # Push to the sheets
            self._result_sheets[group].update(range_name="B5", values=season_values)
            count += 1
        return count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.getLogger('ams').setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Pull league results and rack and stack them for presentation")
    parser.add_argument(
        "league",
        type=str,
        help="League json file."
    )
    # opts = parser.parse_args()

    # TODO properly utilize arguments

    gdrive = GDrive("./credentials.json")
    gdrive.connect_to_results("1SZSIvtBNU4n94vmcQFFTNErxr6uUVKz9lHVfySHWxFI-8axQGeE2G7pODwCLvA",
                              {Group.Pro: "Pro Drivers", Group.Ch: "Ch Drivers", Group.Am: "Am Drivers"})

    r = open("./league.json")
    d = json.load(r)
    league = League.from_dict(d)
    gdrive.push_results(league, 7, [Group.Pro, Group.Ch, Group.Am])
