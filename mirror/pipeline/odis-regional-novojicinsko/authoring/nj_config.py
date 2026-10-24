"""Novojičínsko/Bílovecko sheet config beyond the line specs: version choices, other sheets, area_home, pak rules, texts,
network state, owner checks, reasons for the lines left out. (nj_spec.py writes config.lines; this script never touches lines.)"""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
c = json.load(open(P, encoding='utf-8'))
c['artifact_url'] = c.get('artifact_url')     # set after the first publish (see the end of this file)

# ---- versions: short diversions as the regular state (shared rule: ends well before the 12 Dec timetable change)
c['regular_not_diversion'] = {
    '882629': '629: the diversion timetable (30 Aug – 3 Dec) only moves times; the regular timetable is modelled.',
    '884629': '629: the diversion timetable (30 Aug – 3 Dec) only moves times; the regular timetable is modelled.',
    '882929': '929: the diversion timetable ends on 12 Nov; the regular timetable is modelled.',
    '883643': '643: the diversion timetable (16 – 31 Oct, via Příbor, Štramberská) ends in ten days; the regular route is modelled.'}

# ---- other sheets: 655 is modelled here (883655 holds 41 of the line's 45 trips; the Těšínsko sheet models only 863655's 4)
c['other_sheets']['tfj']['lines'] = ['351', '355', '980', '985']
c['other_sheets']['tfj']['why'] = 'These lines hold a licence here (Novojičínsko Východ, a few trips) and one in Frýdecko-Místecko, where most of their trips are; they are modelled once, with their buses, on the'

# ---- the area a two-licence line is shown under: the licence with most trips on the day
c['area_home'] = {'613': 'bilovecko', '621': 'nj-vychod', '623': 'nj-zapad', '625': 'nj-zapad', '626': 'bilovecko', '629': 'bilovecko',
                  '633': 'nj-vychod', '673': 'bilovecko', '677': 'nj-zapad', '691': 'bilovecko', '696': 'nj-zapad', '374': 'nj-vychod'}

# ---- areas: page text
A = {a['id']: a for a in c['areas']}
A['nj-vychod'].update(operator='Z-Group bus', note='Kopřivnice, Příbor, Frenštát pod Radhoštěm and the Ostrava – Brušperk – Hukvaldy corridor. The Kopřivnice town loop (station – Kolonie – Družební) runs inside licence 883653.')
A['nj-zapad'].update(operator='Transdev Morava', note='Nový Jičín, Odry, Fulnek and the roads to Valašské Meziříčí, Hranice and Frenštát.')
A['bilovecko'].update(operator='Transdev Morava', note='Bílovec, Studénka, Klimkovice and the lines into Ostrava-Svinov.')
A['mhd-nj'].update(operator='ARRIVA autobusy', depot='garage Nový Jičín', note="Town buses take the town pak VZ-MHDNovyJicin-bus. ARRIVA's three buses run all four town lines in turn (see 601–604).")
A['mhd-studenka'].update(operator='Transdev Morava', note='Town bus in the town pak VZ-MHDStudenka-bus.')

# ---- pak: VZ-ODIS-bus for regional buses, the town packages for Nový Jičín and Studénka
ODIS, NJ, ST = 'VZ-ODIS-', 'VZ-MHDNovyJicin-', 'VZ-MHDStudenka-'
def o(pre, core, liv): return f'{pre}{core}-{liv}-{core}'
c['pak'] = dict(
    repo='C:/Users/vojte/Developer/simutrans-custom-czech-pak128', package='VZ-ODIS-bus',
    packages=['VZ-ODIS-bus', 'VZ-MHDNovyJicin-bus', 'VZ-MHDStudenka-bus'],
    why="VZ-ODIS-bus holds the ODIS regional fleet; Transdev Morava's white with the red Transdev logo is transdev, Z-Group's white with the kraj logo bila, BORS Břeclav's yellow-blue borszlutomodra. The Nový Jičín and Studénka town buses take their town packages. Objects confirmed by the pak fleet desk on 21 Oct 2026; the Z-Group-livery Crossway LE Line (21 Oct) and ARRIVA's red-black SOR BN 10,5 no. 7577 (22 Oct; its layout is unverified, as no photo after the 2025 repaint exists) were drawn for this sheet.",
    types={}, paints=[], special={},
    rules=[
        ['*', 'SOR EBN 9,5', '', o(NJ, 'SOR_EBN_9_5', 'cervenametaliza')],
        ['*', 'SOR BN 10,5', '', o(NJ, 'SOR_BN_10_5', 'cervenocerna')],     # 7577 (2TT 8558), un-parked by the owner, installed 22 Oct (main 0fda6a6)
        ['*', 'SOR BN 12', '', o(ST, 'SOR_BN_12', 'transdevbila')],
        ['*', 'Setra S 415 LE business', '', o(ODIS, 'Setra_S_415_LE_business', 'bila')],
        ['*', 'SOR CN 12', 'BORS', o(ODIS, 'SOR_CN_12', 'borszlutomodra')],
        ['*', 'SOR CN 12', '', o(ODIS, 'SOR_CN_12', 'transdev')],
        ['*', 'SOR CN 9,5', '', o(ODIS, 'SOR_CN_9_5', 'transdev')],     # the kraj-logo-only one too (fleet desk, 21 Oct)
        ['*', 'Crossway LE LINE 12M', 'Z-Group', o(ODIS, 'Crossway_LE_Line_12M', 'bilazelenomodra')],   # 6Z9 6492, drawn 21 Oct (fleet desk, main d22c45e)
        ['*', 'Crossway LE LINE 12M', '', o(ODIS, 'Crossway_LE_Line_12M', 'transdev')],
        ['*', 'Crossway LE CITY 12M', '', o(ODIS, 'Crossway_LE_City_12M', 'bila')],
        ['*', 'Citywide LE 12M CNG', '', o(ODIS, 'Citywide_LE_12M_CNG', 'bila')],
        ['*', 'SOR CNG 12', 'Transdev', o(ODIS, 'SOR_CNG_12', 'transdev')],
        ['*', 'SOR CNG 12', '', o(ODIS, 'SOR_CNG_12', 'bila')],
        ['*', 'SOR CNG 10,5', 'Transdev', o(ODIS, 'SOR_CNG_10_5', 'transdev')],
        ['*', 'SOR CNG 10,5', '', o(ODIS, 'SOR_CNG_10_5', 'bila')],
        ['*', 'SOR CN 10,5', '', o(ODIS, 'SOR_CN_10_5', 'transdev')],
        ['*', 'SOR C 12', '', o(ODIS, 'SOR_C_12', 'transdev')],
    ])

c['texts'] = dict(
    eyebrow='ODIS regional and town buses · Novojičínsko Východ · Novojičínsko Západ · Bílovecko · MHD Nový Jičín · Studénka · vypravenost',
    lede_who='The ODIS bus lines of three regional contract areas (Novojičínsko Východ, Z-Group bus; Novojičínsko Západ and Bílovecko, Transdev Morava) and the town lines of Nový Jičín (ARRIVA autobusy) and Studénka (Transdev Morava)',
    swap_places='Nový Jičín, Kopřivnice, Frenštát, Bílovec and Ostrava-Svinov',
    scope='Licences with the area prefixes 883 (Novojičínsko Východ, Z-Group bus), 882 (Novojičínsko Západ) and 884 (Bílovecko) of Transdev Morava, 886 (MHD Nový Jičín, ARRIVA autobusy) and 887 (Studénka, Transdev Morava)',
    scope_check="The prefixes match the live map (Z-Group pr. Kopřivnice with 63- buses; Transdev Morava pr. Nový Jičín 62- and pr. Ostrava 64-; ARRIVA Nový Jičín) and the kraj's contract areas (Novojičínsko Východ, Novojičínsko Západ, Bílovecko).",
    buses_extra=" Fleet numbers and types come from the seznam-autobusu registers of Z-Group bus and Transdev Morava; ARRIVA's town buses and a few unlisted plates were looked up one by one (01b_plates.py).",
    search_example='63-1301',
    depots="Z-Group bus Kopřivnice, Transdev Morava Nový Jičín and Ostrava branches, and ARRIVA's Nový Jičín garage. A seen bus counts at the branch the live map reports for it; a designed bus at its home branch.",
    sources_extra=', <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=240">Z-Group bus register</a>, <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=7546">Transdev Morava register</a>',
    unmodelled_intro='Shift lines and sparse lines whose stops other lines already serve (method Step 8: a long-interval line only where it is a place’s only service), the Nový Jičín town lines that run as one circuit (602, 603, 604 in 601–604), and lines with no afternoon trips.')

c['network_state'] = [
    ['in', 'Three regional contract areas and two town networks',
     'Novojičínsko Východ (licences 883xxx, Z-Group bus, Kopřivnice), Novojičínsko Západ (882xxx) and Bílovecko (884xxx) of Transdev Morava; the town lines of Nový Jičín (886xxx, ARRIVA autobusy) and Studénka (887611, Transdev Morava). Lines holding licences in two areas are shown under the area with most of their trips.'],
    ['in', 'Diversion timetables to the end of the timetable year',
     'The CIS JŘ export has diversion versions valid on the vehicle day until 11–12 Dec 2026 for 286, 623, 641 (via Příbor, Štramberská), 662, 673 (Březová, škola instead of Březová, střed), 679, 692 and 693. They run until the timetable change, so they are modelled as they run.'],
    ['out', 'Short diversions: 629, 643, 929',
     '629 (to 3 Dec) and 929 (to 12 Nov) only move times; 643 (16 – 31 Oct) runs via Příbor, Štramberská. They end before the timetable change, so the regular timetables are modelled (shared rule: short works as the regular state).'],
    ['out', 'Lines on other sheets',
     '351, 355, 980 and 985 hold a few trips on Novojičínsko licences but are Frýdecko-Místecko lines, on the Těšínsko/Třinecko/Frýdecko sheet. 261, 263, 270, 285 and 678 are modelled on the Opavsko/Vítkovsko/Hlučínsko sheet, where most of their trips are. 655 is modelled here: 41 of its 45 trips are on the Novojičínsko licence.'],
]

c['owner_checks'] = [
    ['601', 'the Nový Jičín town lines are one Simutrans line, 601–604, with three buses running 602, 601, 604 and 603 in turn, as ARRIVA ran them on 20 Oct (three buses leave the bus station at :10 every hour).',
     'four separate town lines, one bus each (a fourth bus, which ARRIVA does not run).'],
    ['655', 'modelled on this sheet (883655: 41 trips) although the Těšínsko/Třinecko/Frýdecko sheet also carries it as a 4-trip Frýdecko-Místecko line.',
     'leave 655 on the Těšínsko sheet only (every 240, one bus) and drop it here.'],
    ['698', 'every 60 with two slots each way (Nový Jičín :10 and :30, Kopřivnice :15 and :35), the busiest hours 13:10–15:30 around the Tatra shift change; four buses, as four were seen.',
     'one slot each way (every 60), two buses.'],
    ['653', '653 Kopřivnice is the Kopřivnice town loop (station – Kolonie – Družební – station) every 30, which runs inside licence 883653.',
     'leave the loop out (its stops are on other Kopřivnice lines only in part).'],
]

c['unmodelled'] = {
    '265': 'Opava – Hradec – Skřipov – Bílovec: three trips each way a day (13:32, 15:32 from Opava; 14:20 from Bílovec). Skřipov is on 671, the Opava end on the Opavsko lines.',
    '331': 'Shift line Ostrava, Přívoz – Mošnov, Airport (4:50, 12:50, 20:55; back 6:10, 14:10, 22:08). Its stops are on 632 and the Ostrava lines.',
    '372': 'Shift trips Brušperk – Ostrava, Náměstí Republiky (4:40, 5:10, 12:40, 20:37; back 6:32, 14:35, 22:42). Its stops are on 371, 374 and 376.',
    '602': 'Part of the 601–604 town circuit (602 at :10).',
    '603': 'Part of the 601–604 town circuit (603 to Tesco at :10, back at :46).',
    '604': 'Part of the 601–604 town circuit (604 at :10).',
    '633': 'Kopřivnice – Veřovice – Bordovice – Frenštát: 8 trips, 3 in the afternoon at irregular times. Its stops are on 634, 690 and 696.',
    '636': 'Two trips a day (Kopřivnice – Tichá – Kozlovice). Its stops are on 637 and 653.',
    '637': 'Kopřivnice – Tichá – Kozlovice – Lhotka: 10 trips a day at irregular times (13:13, 15:03, 16:32, 17:13 in the afternoon). Its stops are on 653, 371 and the Frýdecko lines.',
    '639': 'One morning trip (7:05).',
    '645': 'Ženklava – Štramberk: 7 trips, two in the afternoon (12:53, 14:28). Its stops are on 644 and 646.',
    '649': 'Bílovec – Studénka – Příbor – Kopřivnice: 12 trips at irregular times. Its stops are on 626, 643 and 699.',
    '651': 'Frenštát – Kunčice pod Ondřejníkem: its trips are on 657 Kunčice (the Simutrans line takes both lines\' trips to Kunčice station, via Žuchov and Rákovec).',
    '664': 'Four trips a day (Frenštát – Kopřivnice – Příbor – Mošnov – Ostrava). Its stops are on 653, 641 and 670.',
    '666': 'Three trips a day, none in the afternoon (Nový Jičín – Starý Jičín, Heřmanice). Heřmanice is on 667.',
    '674': 'Zbyslavice / Hlubočec – Klimkovice – Ostrava: 11 trips, mostly in the morning (back 13:24, 13:44, 15:04, 15:54). Its stops are on 679, 286 and 288.',
    '675': 'Shift line Skřipov – Těškovice – Klimkovice – Ostrava, Vítkovice (4:07, 12:10, 20:10; back 6:38, 14:30, 22:37). Its stops are on 671 and the Ostrava lines.',
    '695': 'Two morning trips (6:35, 6:46).',
}
c['artifact_url'] = 'https://claude.ai/artifact/YFgUu62jD8YqfpuoL8FZpp'
# ---- final cross-sheet pass (parent, 21 Oct 2026): sheets built in parallel, one bus one sheet in the order
# Ostrava > HKO town > HKO regional > TFJ > Opavsko > Novojičínsko > Bruntálsko (a later sheet excludes the earlier sheets' buses)
c['other_sheets']['opavsko'].update(derived='../odis-regional-opavsko/data/derived/roster.json', schedule='../odis-regional-opavsko/data/derived/schedule.json', url='https://claude.ai/artifact/K5ZeDCY2YYqV1Sz3tQwj3j')
# ---- end cross-sheet
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('config updated')
