"""Bruntálsko/Krnovsko/Rýmařovsko sheet config beyond the line specs: other sheets, pak rules, texts, areas, network state,
owner checks, reasons for the lines left out. (brn_spec.py writes config.lines; this script never touches lines.)
Also corrects bus lengths in data/derived/fleet.json: 01c_fleet.py's tlen() reads a length only from "10,5M"-style names,
so SOR "CN 10,5" / "BN 9,5" / "C 12" came out as 12 m (shared-script fix reported; until then this keeps the page right)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', 'config.json')
c = json.load(open(P, encoding='utf-8'))
c['plate_lookup'] = True
c['artifact_url'] = 'https://claude.ai/artifact/ApSB65b8skppcUGCfFHtnZ'
# 260 and 920 hold a licence here and one in Opavsko, where most of their trips are (parent's decision, 21 Oct 2026)
c['other_sheets']['opavsko'] = dict(c['other_sheets'].get('opavsko', {}), **{
    "lines": ["260", "920"], "label": "ODIS Opavsko Vítkovsko Hlučínsko", "short": "Opavsko/Vítkovsko/Hlučínsko sheet",
    "heading": "On the Opavsko/Vítkovsko/Hlučínsko sheet",
    "why": "These lines hold a licence here and one in Opavsko, where most of their trips are; they are modelled once, with their buses, on the"})
c['other_sheets']['opavsko'].setdefault('url', None)
c['regular_not_diversion'] = {
    '854876': 'The diversion of 876 (1 Sep – 23 Oct 2026) ends two days after the vehicle day, so the regular timetable is modelled (shared rule: short-term closures as the regular state).',
    '854912': 'The diversion of 912 (15 – 21 Oct 2026) ends the day after the vehicle day, so the regular timetable is modelled.',
    '854921': 'The diversion of 921 (1 Sep – 23 Oct 2026) ends two days after the vehicle day, so the regular timetable is modelled.'}

A = {a['id']: a for a in c['areas']}
A['krnovsko'].update(note='Krnovsko is the Osoblaha and Zlaté Hory side of Krnov; its buses carry 82- fleet numbers.')
A['bruntalsko'].update(note='Bruntálsko holds the Krnov – Bruntál corridor, the Krnov villages and the Jeseníky lines out of Bruntál; 83- buses.')
A['rymarovsko'].update(note='Rýmařovsko holds the Rýmařov lines and Bruntál – Moravský Beroun; 84- buses.')
A['mhd-krnov'].update(note='Town buses (81-, white with the blue-yellow Krnov wrap) take the town pak VZ-MHDKrnov-bus; regional buses lent to town lines keep their VZ-ODIS-bus object.')
A['mhd-bruntal'].update(note='On the vehicle day the two Bruntál town loops were worked by regional buses, which keep their VZ-ODIS-bus object.')

ODIS, KR = 'VZ-ODIS-', 'VZ-MHDKrnov-'
def o(pre, core, liv): return f'{pre}{core}-{liv}-{core}'
c['pak'] = dict(
    repo='C:/Users/vojte/Developer/simutrans-custom-czech-pak128', package='VZ-ODIS-bus',
    packages=['VZ-ODIS-bus', 'VZ-MHDKrnov-bus'],
    why="Regional buses take VZ-ODIS-bus; Transdev Morava's white with the red Transdev logo and the kraj logo is the transdev livery. Krnov's town buses take the town package VZ-MHDKrnov-bus (krnovbila). A regional bus lent to a town line keeps its VZ-ODIS-bus object. The pak fleet desk confirmed every object on 21 Oct 2026 (transdev is Transdev Morava's white with the red Transdev figure and the kraj ring; krnovbila is the Krnov white with blue-yellow chevrons); nothing new is needed.",
    types={}, paints=[], special={},
    rules=[
        ['*', 'Streetway 12M', 'Krnov', o(KR, 'Streetway_12M', 'krnovbila')],
        ['*', 'SOR BN 9,5', 'Krnov', o(KR, 'SOR_BN_9_5', 'krnovbila')],
        ['*', 'SOR NS 12', 'Krnov', o(KR, 'SOR_NS_12', 'krnovbila')],
        ['*', 'SOR CN 10,5', '', o(ODIS, 'SOR_CN_10_5', 'transdev')],
        ['*', 'SOR CN 12', '', o(ODIS, 'SOR_CN_12', 'transdev')],
        ['*', 'SOR CN 9,5', '', o(ODIS, 'SOR_CN_9_5', 'transdev')],
        ['*', 'SOR CNG 12', '', o(ODIS, 'SOR_CNG_12', 'transdev')],
        ['*', 'SOR CNG 10,5', '', o(ODIS, 'SOR_CNG_10_5', 'transdev')],
        ['*', 'SOR C 12', '', o(ODIS, 'SOR_C_12', 'transdev')],
        ['*', 'SOR ICNG 12', '', o(ODIS, 'SOR_ICNG_12', 'transdev')],
        ['*', 'Crossway LE LINE 12M', '', o(ODIS, 'Crossway_LE_Line_12M', 'transdev')],
    ])

c['texts'] = dict(
    eyebrow='ODIS regional and town buses · Krnovsko · Bruntálsko · Rýmařovsko · MHD Krnov · MHD Bruntál · vypravenost',
    lede_who='The ODIS bus lines of three regional contract areas around Krnov, Bruntál and Rýmařov (Krnovsko, Bruntálsko, Rýmařovsko) and the town lines of Krnov and Bruntál, all run by Transdev Morava from its Bruntál branch',
    swap_places='Krnov, Bruntál, Rýmařov and Moravský Beroun',
    scope='Transdev Morava licences with the area prefixes 852 (Krnovsko), 853 (Bruntálsko), 854 (Rýmařovsko), 856 (MHD Krnov) and 855 (MHD Bruntál)',
    scope_check='The prefixes match the live map (Transdev Morava, pr. Bruntál) and the fleet numbers: 82- buses run 852, 83- run 853, 84- run 854 and 81- are the Krnov town buses. 260 and 920 also hold Opavsko licences and are on that sheet.',
    buses_extra=' The fleet is the seznam-autobusu register of Transdev Morava (01c_fleet.py); every bus seen on these licences is in it.',
    search_example='82-2003',
    depots='Transdev Morava, branch Bruntál (with its Krnov and Rýmařov outstations). A seen bus counts at the branch the live map reports for it; a designed bus at its home branch.',
    sources_extra=', <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=7546">Transdev Morava register</a>',
    unmodelled_intro='Sparse lines whose stops other lines already serve (method Step 8: a long-interval line only where it is a place’s only service) and lines with no afternoon trips.')

c['network_state'] = [
    ['in', 'Three regional contract areas and two town networks',
     'Krnovsko (licences 852xxx), Bruntálsko (853xxx) and Rýmařovsko (854xxx), the Krnov town lines (856xxx) and the two Bruntál town loops (855xxx), all Transdev Morava, branch Bruntál. Lines running into the Olomouc region (913 and 921 to Olomouc, 922 to Uničov, 912 to Šternberk) are modelled to their ends: in this data no other line serves their stops there.'],
    ['in', 'Diversion timetables to the timetable change or beyond',
     'The CIS JŘ export has diversion versions valid on the vehicle day for 824 (to 12 Dec), 880 (20 Jul – 14 Dec), 901 and 907 (29 Sep – 19 Dec) and 861 (12 Oct – 20 Dec). They run to the end of the timetable year or past it, so they are modelled as they run.'],
    ['out', 'Short diversions of 876, 912 and 921',
     '876 (to 23 Oct), 912 (15 – 21 Oct) and 921 (to 23 Oct) ran diversion timetables on the vehicle day that end within days, so their regular timetables are modelled (shared rule: short works as the regular state). 912 regular adds Jiříkov, Těchanov; 921 regular runs its Břidličná local trips to Huzová.'],
    ['out', '260 and 920',
     '260 Opava – Horní Benešov – Bruntál and 920 Opava – Bruntál – Rýmařov hold a licence here and one in Opavsko (902260: 28 trips, 902920: 34 trips on the day, against 3 and 14 here). They are modelled once, on the Opavsko/Vítkovsko/Hlučínsko sheet.'],
    ['in', 'A new 909 timetable from 22 Oct',
     'The export already holds a new version of 909 valid from 22 Oct 2026, two days after the vehicle day; the sheet keeps the version of the vehicle day.'],
]

c['owner_checks'] = [
    ['877', 'Rýmařov – Bruntál every 60 at Rýmařov :34 and Bruntál :24, 6 and 4 min before the real :40 and :20, so two buses work it (shortest round).',
     'keep the real :40 / :20 and give the line a third bus.'],
    ['801 PZ', 'the industrial-zone trips are a Petrův důl – průmyslová zóna II shuttle every 480 at their times there (one bus), so the every-30 trunk is not doubled at the shift changes (as 302 Tesco on the Těšínsko sheet).',
     'run the zone trips from Nemocnice as they do (every 480, six slots), two Simutrans buses leaving Nemocnice together six times a shift.'],
    ['913', 'Krnov – Olomouc (one return a day) is every 480 with the Krnov departure at 12:07 instead of the real 5:55, so one bus works it.',
     'keep 5:55 (13:55, 21:55) and give it a second bus, or leave 913 out and list its three stops (Lipina, Horní Loděnice in the Olomouc region; Bílčice, bytovky).'],
    ['832', 'Krnov – Osoblaha is every 180 on the real 16:20 and 15:41 with two buses, against the default shortest round.',
     'the shortest round: one bus, every departure about an hour off the real times.'],
]

c['unmodelled'] = {
    '803': 'Krnov town line to Červený dvůr: five trips a day (4:40, 5:45, 6:35, 21:29, 22:10), none in the afternoon.',
    '815': 'Krnov – Krasov – Čaková – Zátor: three trips a day (6:10; Krasov 14:30 and Zátor, škola 15:40 back to Krnov). Its stops are on 814, 814 Zátor and 816.',
    '852': 'Bruntál town loop via U Rybníka: eight trips a day, in the afternoon only KARLA 15:12 and 18:27 to the station. Its afternoon stops are on 851 and the regional lines.',
    '876': 'Rýmařov – Břidličná – Lomnice: five trips a day, the last at 12:44; none in the afternoon. Its stops are on 877, 911 and 921.',
    '914': 'Bruntál – Šternberk – Olomouc: two trips a day (6:35, back 11:50), none in the afternoon.',
}
# ---- final cross-sheet pass (parent, 21 Oct 2026): sheets built in parallel, one bus one sheet in the order
# Ostrava > HKO town > HKO regional > TFJ > Opavsko > Novojičínsko > Bruntálsko (a later sheet excludes the earlier sheets' buses)
c['other_sheets']['opavsko'].update(derived='../odis-regional-opavsko/data/derived/roster.json', schedule='../odis-regional-opavsko/data/derived/schedule.json', url='https://claude.ai/artifact/K5ZeDCY2YYqV1Sz3tQwj3j')
c['other_sheets']['novojicinsko'] = dict(lines=[], label='ODIS Novojičínsko Bílovecko', short='Novojičínsko/Bílovecko sheet', derived='../odis-regional-novojicinsko/data/derived/roster.json', url='https://claude.ai/artifact/YFgUu62jD8YqfpuoL8FZpp')
# ---- end cross-sheet
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# bus lengths in the sheet's fleet.json (see the docstring)
FP = os.path.join(HERE, '..', 'data', 'derived', 'fleet.json')
if os.path.exists(FP):
    F = json.load(open(FP, encoding='utf-8')); n = 0
    for v in F.values():
        m = re.match(r'SOR [A-Z]+ (\d+)(?:,(\d))?$', v.get('type') or '')
        if m:
            ln = f"{m.group(1)}.{m.group(2)} m" if m.group(2) else f"{m.group(1)} m"
            if v.get('len') != ln: v['len'] = ln; n += 1
    json.dump(F, open(FP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('fleet lengths corrected:', n)
print('config updated')
