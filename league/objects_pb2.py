# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: objects.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\robjects.proto\x12\x16\x61merican_muscle_series\"j\n\rGroupRuleData\x12\x14\n\x0cMinCarNumber\x18\x01 \x01(\x05\x12\x14\n\x0cMaxCarNumber\x18\x02 \x01(\x05\x12-\n\x05Group\x18\x03 \x01(\x0e\x32\x1e.american_muscle_series.eGroup\"J\n\x0eGroupRulesData\x12\x38\n\tGroupRule\x18\x01 \x03(\x0b\x32%.american_muscle_series.GroupRuleData\".\n\x0eSeasonRaceData\x12\x0e\n\x06Season\x18\x01 \x01(\x05\x12\x0c\n\x04Race\x18\x02 \x01(\x05\"n\n\x0fTimePenaltyData\x12:\n\nSeasonRace\x18\x01 \x01(\x0b\x32&.american_muscle_series.SeasonRaceData\x12\x0e\n\x06\x44river\x18\x02 \x01(\x05\x12\x0f\n\x07Seconds\x18\x03 \x01(\x05\"\x86\x03\n\x12LeagueResourceData\x12\x11\n\tiRacingID\x18\x01 \x01(\x05\x12\x10\n\x08NumDrops\x18\x02 \x01(\x05\x12\x12\n\nNonDrivers\x18\x03 \x03(\x05\x12<\n\x0cPracticeRace\x18\x04 \x03(\x0b\x32&.american_muscle_series.SeasonRaceData\x12Z\n\x10SeasonGroupRules\x18\x05 \x03(\x0b\x32@.american_muscle_series.LeagueResourceData.SeasonGroupRulesEntry\x12<\n\x0bTimePenalty\x18\x06 \x03(\x0b\x32\'.american_muscle_series.TimePenaltyData\x1a_\n\x15SeasonGroupRulesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32&.american_muscle_series.GroupRulesData:\x02\x38\x01\"\xb8\x02\n\nLeagueData\x12@\n\x07Members\x18\x01 \x03(\x0b\x32/.american_muscle_series.LeagueData.MembersEntry\x12@\n\x07Seasons\x18\x02 \x03(\x0b\x32/.american_muscle_series.LeagueData.SeasonsEntry\x1aR\n\x0cMembersEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".american_muscle_series.MemberData:\x02\x38\x01\x1aR\n\x0cSeasonsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".american_muscle_series.SeasonData:\x02\x38\x01\",\n\nMemberData\x12\x0c\n\x04Name\x18\x01 \x01(\t\x12\x10\n\x08Nickname\x18\x02 \x01(\t\"\xb0\x02\n\nSeasonData\x12@\n\x07\x44rivers\x18\x01 \x03(\x0b\x32/.american_muscle_series.SeasonData.DriversEntry\x12<\n\x05Races\x18\x02 \x03(\x0b\x32-.american_muscle_series.SeasonData.RacesEntry\x1aR\n\x0c\x44riversEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".american_muscle_series.DriverData:\x02\x38\x01\x1aN\n\nRacesEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12/\n\x05value\x18\x02 \x01(\x0b\x32 .american_muscle_series.RaceData:\x02\x38\x01\"\xf2\x01\n\nDriverData\x12\x11\n\tCarNumber\x18\x01 \x01(\x05\x12-\n\x05Group\x18\x02 \x01(\x0e\x32\x1e.american_muscle_series.eGroup\x12\x0e\n\x06Points\x18\x03 \x01(\x05\x12\x18\n\x10TotalFastestLaps\x18\x04 \x01(\x05\x12\x16\n\x0eTotalIncidents\x18\x05 \x01(\x05\x12\x19\n\x11TotalLapsComplete\x18\x06 \x01(\x05\x12\x15\n\rTotalLapsLead\x18\x07 \x01(\x05\x12\x1a\n\x12TotalPolePositions\x18\x08 \x01(\x05\x12\x12\n\nTotalRaces\x18\t \x01(\x05\"b\n\x0eGroupStatsData\x12-\n\x05Group\x18\x01 \x01(\x0e\x32\x1e.american_muscle_series.eGroup\x12\r\n\x05\x43ount\x18\x02 \x01(\x05\x12\x12\n\nFastestLap\x18\x03 \x01(\x05\"\xee\x01\n\x08RaceData\x12\x0c\n\x04\x44\x61te\x18\x01 \x01(\t\x12\r\n\x05Track\x18\x02 \x01(\t\x12\x38\n\x04Grid\x18\x03 \x03(\x0b\x32*.american_muscle_series.RaceData.GridEntry\x12:\n\nGroupStats\x18\x04 \x03(\x0b\x32&.american_muscle_series.GroupStatsData\x1aO\n\tGridEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".american_muscle_series.ResultData:\x02\x38\x01\"\xc3\x01\n\nResultData\x12\x14\n\x0cPolePosition\x18\x01 \x01(\x08\x12\x12\n\nFastestLap\x18\x02 \x01(\x08\x12\x15\n\rStartPosition\x18\x03 \x01(\x05\x12\x16\n\x0e\x46inishPosition\x18\x04 \x01(\x05\x12\x0e\n\x06Points\x18\x05 \x01(\x05\x12\x10\n\x08Interval\x18\x06 \x01(\x02\x12\x11\n\tIncidents\x18\x07 \x01(\x05\x12\x15\n\rLapsCompleted\x18\x08 \x01(\x05\x12\x10\n\x08LapsLead\x18\t \x01(\x05*&\n\x06\x65Group\x12\x0b\n\x07Unknown\x10\x00\x12\x07\n\x03Pro\x10\x01\x12\x06\n\x02\x41m\x10\x02\x42\x02H\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'objects_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\001'
  _LEAGUERESOURCEDATA_SEASONGROUPRULESENTRY._options = None
  _LEAGUERESOURCEDATA_SEASONGROUPRULESENTRY._serialized_options = b'8\001'
  _LEAGUEDATA_MEMBERSENTRY._options = None
  _LEAGUEDATA_MEMBERSENTRY._serialized_options = b'8\001'
  _LEAGUEDATA_SEASONSENTRY._options = None
  _LEAGUEDATA_SEASONSENTRY._serialized_options = b'8\001'
  _SEASONDATA_DRIVERSENTRY._options = None
  _SEASONDATA_DRIVERSENTRY._serialized_options = b'8\001'
  _SEASONDATA_RACESENTRY._options = None
  _SEASONDATA_RACESENTRY._serialized_options = b'8\001'
  _RACEDATA_GRIDENTRY._options = None
  _RACEDATA_GRIDENTRY._serialized_options = b'8\001'
  _globals['_EGROUP']._serialized_start=2230
  _globals['_EGROUP']._serialized_end=2268
  _globals['_GROUPRULEDATA']._serialized_start=41
  _globals['_GROUPRULEDATA']._serialized_end=147
  _globals['_GROUPRULESDATA']._serialized_start=149
  _globals['_GROUPRULESDATA']._serialized_end=223
  _globals['_SEASONRACEDATA']._serialized_start=225
  _globals['_SEASONRACEDATA']._serialized_end=271
  _globals['_TIMEPENALTYDATA']._serialized_start=273
  _globals['_TIMEPENALTYDATA']._serialized_end=383
  _globals['_LEAGUERESOURCEDATA']._serialized_start=386
  _globals['_LEAGUERESOURCEDATA']._serialized_end=776
  _globals['_LEAGUERESOURCEDATA_SEASONGROUPRULESENTRY']._serialized_start=681
  _globals['_LEAGUERESOURCEDATA_SEASONGROUPRULESENTRY']._serialized_end=776
  _globals['_LEAGUEDATA']._serialized_start=779
  _globals['_LEAGUEDATA']._serialized_end=1091
  _globals['_LEAGUEDATA_MEMBERSENTRY']._serialized_start=925
  _globals['_LEAGUEDATA_MEMBERSENTRY']._serialized_end=1007
  _globals['_LEAGUEDATA_SEASONSENTRY']._serialized_start=1009
  _globals['_LEAGUEDATA_SEASONSENTRY']._serialized_end=1091
  _globals['_MEMBERDATA']._serialized_start=1093
  _globals['_MEMBERDATA']._serialized_end=1137
  _globals['_SEASONDATA']._serialized_start=1140
  _globals['_SEASONDATA']._serialized_end=1444
  _globals['_SEASONDATA_DRIVERSENTRY']._serialized_start=1282
  _globals['_SEASONDATA_DRIVERSENTRY']._serialized_end=1364
  _globals['_SEASONDATA_RACESENTRY']._serialized_start=1366
  _globals['_SEASONDATA_RACESENTRY']._serialized_end=1444
  _globals['_DRIVERDATA']._serialized_start=1447
  _globals['_DRIVERDATA']._serialized_end=1689
  _globals['_GROUPSTATSDATA']._serialized_start=1691
  _globals['_GROUPSTATSDATA']._serialized_end=1789
  _globals['_RACEDATA']._serialized_start=1792
  _globals['_RACEDATA']._serialized_end=2030
  _globals['_RACEDATA_GRIDENTRY']._serialized_start=1951
  _globals['_RACEDATA_GRIDENTRY']._serialized_end=2030
  _globals['_RESULTDATA']._serialized_start=2033
  _globals['_RESULTDATA']._serialized_end=2228
# @@protoc_insertion_point(module_scope)
