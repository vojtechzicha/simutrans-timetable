"""TFJ sheet config beyond the line specs: pak rules, texts, areas' operators, network state, reasons for the lines left out.
(tfj_spec.py writes config.lines; this script never touches lines.)"""
import json
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
c = json.load(open(P, encoding='utf-8'))
c['artifact_url'] = 'https://claude.ai/artifact/2LecoKwCYb2Lmk1sRDTjrx'
c['plate_lookup'] = True
c['regular_not_diversion'] = {'871731': 'The diversion of 731 (28 Aug – 30 Nov 2026: Stonava, Důl ČSM-Jih, Důl ČSM-Sever and Bonkov rozcestí not served, Stonava, Bonkov instead) ends in six weeks, so the regular route is modelled (shared rule: short-term closures as the regular state; the same works as 582 on the Havířovsko/Karvinsko/Orlovsko sheet).'}

A = {a['id']: a for a in c['areas']}
if 'frydlantsko' not in A:      # added 21 Oct 2026 (owner: do the next sheets; Frýdlantsko joins this one)
    fr = dict(id='frydlantsko', name='Frýdlantsko', prefix='864', kind='regional', branch='Transdev Slezsko pr. Frýdek-Místek',
              depot='provozovna Frýdek-Místek', fleet=['32'], near=['32', '33', '42', '43', '73'])
    c['areas'].insert([a['id'] for a in c['areas']].index('frydecko') + 1, fr); A['frydlantsko'] = fr
A['frydecko'].update(fleet=['33'], near=['33', '32', '42', '43', '73'])
A['frydlantsko'].update(note='Frýdlant nad Ostravicí, Ostravice and the Beskydy valleys, run from the Frýdek-Místek branch (32- buses).')
# the first parts of Frýdlantsko's stops (a town JDF's stop that starts with one of them is not prefixed with the town)
c['towns'] = sorted(set(c['towns']) | {'Baška', 'Bílá', 'Čeladná', 'Frýdlant n.O.', 'Frýdlant nad Ostravicí', 'Kunčice p.O.', 'Lhotka', 'Malenovice', 'Metylovice', 'Ostravice', 'Pržno', 'Staré Hamry', 'Pstruží', 'Kozlovice', 'Raškovice'})
A['trinecko'].update(note='Jablunkovsko and Třinecko are one contract area (licences 861xxx), run from the Jablunkov branch (74-).')
A['mhd-tesin'].update(operator='ARRIVA autobusy', depot='from the Třinec garage', note="Town buses take the town pak VZ-MHDCeskyTesin-bus; Třinec town buses lent here keep their VZ-MHDTrinec-bus object.")
A['mhd-trinec'].update(operator='ARRIVA autobusy', depot='garage Třinec', note='Town buses take the town pak VZ-MHDTrinec-bus.')
A['mhd-fm'].update(note='Town buses take the town pak VZ-MHDFrydekMistek-bus; regional buses with the kraj logo lent to town lines keep their VZ-ODIS-bus object.')

ODIS, TR, CT, FM = 'VZ-ODIS-', 'VZ-MHDTrinec-', 'VZ-MHDCeskyTesin-', 'VZ-MHDFrydekMistek-'
def o(pre, core, liv): return f'{pre}{core}-{liv}-{core}'
c['pak'] = dict(
    repo='C:/Users/vojte/Developer/simutrans-custom-czech-pak128', package='VZ-ODIS-bus',
    packages=['VZ-ODIS-bus', 'VZ-MHDTrinec-bus', 'VZ-MHDCeskyTesin-bus', 'VZ-MHDFrydekMistek-bus'],
    why="Pak session f3, 20 Oct 2026: regional buses take VZ-ODIS-bus; the town buses of Třinec, Český Těšín and Frýdek-Místek take their town packages. A regional bus (kraj logo) lent to a town line keeps its VZ-ODIS-bus object. Transdev Slezsko's 3ČSAD white-green (with or without the kraj logo) is 3csadbilozelena, the red-black ODIS scheme odiscervenocerna.",
    types={}, paints=[], special={},
    # [areas ('*', 'regional', 'mhd' or a list of area ids), type substring (type + full name), paint substring, object ('~' = stand-in)]
    rules=[
        ['*', 'SOR NS 12 electric', 'zelená metalíza', o(FM, 'SOR_NS_12_electric', 'zelenametaliza')],
        ['*', 'SOR NS 12 electric', 'polep', o(FM, 'SOR_NS_12_electric', 'frydekmistekpolep')],
        ['*', 'SOR NSG 12', 'polep', o(FM, 'SOR_NSG_12', 'frydekmistekpolep')],
        ['*', 'SOR BNG 12', '', o(FM, 'SOR_BNG_12', '3csadbilozelena')],
        ['*', 'Urbanway 12M CNG', '', o(FM, 'Urbanway_12M_CNG', '3csadbilozelena')],
        ['*', 'Citywide LF 12M CNG', '', o(FM, 'Citywide_LF_12M_CNG', '3csadbilozelena')],
        ['*', 'SOR NS 12', 'bílo-zelená', o(TR, 'SOR_NS_12', 'trinecbilozelena')],
        ['*', 'Perun 26 BB HE', '', o(TR, 'Perun_26BB_HE', 'trinecbilozelena')],
        ['*', 'Iveco Urbanway 12M', 'bílo-zelená', o(TR, 'Urbanway_12M', 'trinecbilozelena')],
        ['*', 'Citywide LF 10,9M', '', o(CT, 'Citywide_LF_10_9M', 'ceskytesinbilozluta')],
        ['*', 'Crossway LE CITY 10,8M', '', o(CT, 'Crossway_LE_City_10_8M', 'ceskytesinbilozluta')],
        ['*', 'Dekstra LE 37', 'bílá', '~' + o(ODIS, 'Dekstra_LE_37_CNG', '3csadbilozelena')],
        ['*', 'Crossway LE CITY 12M', 'světle modrá', '~' + o(ODIS, 'Crossway_LE_City_12M', 'bila')],
        ['*', 'Crossway LE CITY 12M', 'bílá', o(ODIS, 'Crossway_LE_City_12M', 'bila')],
        ['mhd', 'Crossway LE CITY 12M', 'logo dopravy', o(ODIS, 'Crossway_LE_City_12M', '3csadbilozelena')],
        ['mhd', 'Crossway LE CITY 12M', '3ČSAD', o(FM, 'Crossway_LE_City_12M', '3csadbilozelena')],
        ['*', 'Crossway LE LINE 12M NP', 'ODIS', o(ODIS, 'Crossway_LE_Line_12M_NP_2025', 'odiscervenocerna')],
        ['*', 'Crossway LE LINE 12M', '3ČSAD', '~' + o(ODIS, 'Crossway_LE_City_12M', '3csadbilozelena')],
        ['*', 'Crossway LE CITY 12M', '3ČSAD', o(ODIS, 'Crossway_LE_City_12M', '3csadbilozelena')],
        ['*', 'Crossway LE 12M', '3ČSAD', '~' + o(ODIS, 'Crossway_LE_City_12M', '3csadbilozelena')],     # Irisbus Crossway LE 12M (401)
        ['*', 'Citywide Suburban LE 15M CNG', '3ČSAD', o(ODIS, 'Citywide_Suburban_LE_15M_CNG', '3csadbilozelena')],
        ['*', 'Rošero', 'ODIS', o(ODIS, 'Rosero_First_CNG', 'odiscervenocerna')],
        ['*', 'SOR CNG 10,5', '3ČSAD', o(ODIS, 'SOR_CNG_10_5', '3csadbilozelena')],
        ['*', 'SOR CNG 12', '3ČSAD', o(ODIS, 'SOR_CNG_12', '3csadbilozelena')],
        ['*', 'SOR ICNG 12,3', 'ODIS', o(ODIS, 'SOR_ICNG_12_3', 'odiscervenocerna')],
        ['*', 'SOR ICNG 12', 'bílá', '~' + o(ODIS, 'SOR_ICNG_12', 'transdev')],
        ['*', 'Setra S 415 LE business', '', o(ODIS, 'Setra_S_415_LE_business', 'bila')],     # Z-Group (980), as on the Novojičínsko sheet
    ])

c['texts'] = dict(
    eyebrow='ODIS regional and town buses · Českotěšínsko · Frýdecko-Místecko · Frýdlantsko · Jablunkovsko–Třinecko · MHD Český Těšín · Frýdek-Místek · Třinec · vypravenost',
    lede_who='The ODIS bus lines of four regional contract areas (Českotěšínsko, Frýdecko-Místecko, Frýdlantsko and Jablunkovsko–Třinecko, Transdev Slezsko) and of the town networks of Český Těšín and Třinec (ARRIVA autobusy) and Frýdek-Místek (Transdev Slezsko)',
    swap_places='Třinec, Český Těšín, Jablunkov, Frýdek-Místek and Frýdlant',
    scope='Licences with the area prefixes 871 (Českotěšínsko), 863 (Frýdecko-Místecko), 864 (Frýdlantsko), 861 (Jablunkovsko–Třinecko) of Transdev Slezsko, 865 (MHD Frýdek-Místek) of Transdev Slezsko and 875 (MHD Český Těšín) and 866 (MHD Třinec) of ARRIVA autobusy',
    scope_check='The prefixes match the live map (provozovna Český Těšín, Frýdek-Místek (which runs Frýdecko-Místecko and Frýdlantsko), Jablunkov; ARRIVA Třinec) and the kraj’s list of contract areas.',
    buses_extra=' ARRIVA’s town buses and Z-Group’s buses on 980 and 985 are not in the Transdev register: their plates were looked up on seznam-autobusu.cz vehicle pages (01b_plates.py). The two Český Těšín buses with vanity plates, TESIN 001 and TESIN 004, are in the register as “001 TESIN” and “004 TESIN”: Scania Citywide LF 10,9M of 2018 in the town’s white-yellow livery.',
    search_example='73-1104',
    unmodelled_intro='Shift lines and sparse lines whose stops other lines already serve (method Step 8: a long-interval line only where it is a place’s only service), a line whose afternoon trips are part of another line’s round (315, in 316), and lines with no trips on the day.',
    depots='Transdev Slezsko branches (provozovny) and ARRIVA’s Třinec garage, which runs both the Třinec and the Český Těšín town lines. A seen bus counts at the branch the live map reports for it; a designed bus at its home branch.',
    sources_extra=', <a href="https://seznam-autobusu.cz/">seznam-autobusu.cz vehicle pages</a> (ARRIVA)')

c['other_sheets']['hko_regional'].update(
    heading='On the Havířovsko/Karvinsko/Orlovsko regional sheet',
    why='365 Havířov – Frýdek-Místek holds a licence in Havířovsko (912365) and one here in Frýdecko-Místecko (863365). It is one line, modelled once with its buses on the')

c['other_sheets']['novojicinsko'] = dict(lines=['655'], label='ODIS Novojičínsko Bílovecko', short='Novojičínsko/Bílovecko sheet',
    heading='On the Novojičínsko/Bílovecko sheet', why='655 Frenštát – Trojanovice holds a licence here (863655, 4 trips) and one in Novojičínsko Východ (883655, 41 trips); it is modelled once, with its buses, on the',
    url='https://claude.ai/artifact/YFgUu62jD8YqfpuoL8FZpp', schedule='../odis-regional-novojicinsko/data/derived/schedule.json')
c['network_state'] = [
    ['in', 'Four regional contract areas and three town networks',
     'Českotěšínsko (licences 871xxx), Frýdecko-Místecko (863xxx), Frýdlantsko (864xxx, added 21 Oct) and Jablunkovsko–Třinecko (861xxx, one area) of Transdev Slezsko; the town lines of Frýdek-Místek (865xxx, Transdev Slezsko), Český Těšín (875xxx) and Třinec (866xxx), both ARRIVA autobusy. Each has its own section below.'],
    ['in', 'Diversion timetables to the end of the timetable year',
     'The CIS JŘ export has diversion versions valid on the vehicle day until 12 Dec 2026 for 770, 786, 787 (Třinec – Bystřice – Jablunkov), 315 and 316 (Palkovice: 315 skips Adámek, Podhůří and u Kožuchů), 704 and 716 (Třinec town lines; 716 runs 21 trips instead of 7, via Guty, škola and Kanada) and 721 and 722 (Český Těšín, via Nová Tovární, Walmark, točna and Tovární u trati). They run until the end of the timetable year, so they are modelled as they run.'],
    ['out', 'Line 731: Stonava mines diversion (28 Aug – 30 Nov)',
     'The diversion skips Stonava, Důl ČSM-Jih, Důl ČSM-Sever and Bonkov rozcestí. It ends in six weeks, so the regular route is modelled (shared rule: short works as the regular state), as for 582 on the Havířovsko/Karvinsko/Orlovsko sheet.'],
    ['out', '383, 387, 365 and 655',
     '383 and 387 (Frýdecko-Místecko licences) stop at Ostrava, Hranečník and are on the Ostrava sheet (section All lines at Hranečník). 365 Havířov – Frýdek-Místek is on the Havířovsko/Karvinsko/Orlovsko regional sheet. 655 Frenštát – Trojanovice is on the Novojičínsko/Bílovecko sheet, where its main licence (883655, 41 of 45 trips) is. Their buses stay there.'],
]

c['owner_checks'] = [
    ['731', 'the regular route is modelled; on the vehicle day 731 ran a diversion (28 Aug – 30 Nov) that skips the Stonava mines, as 582 on the Havířovsko/Karvinsko/Orlovsko sheet.',
     'model the diversion as it ran (Stonava, Bonkov instead of Bonkov rozcestí and the two mines) until 30 Nov.'],
    ['784', 'the back slot from Horní Přelač is :19, 6 min before the real :25, so the line needs two buses (two were seen).',
     'keep the real :25 and give the line a third bus.'],
    ['302 Tesco', 'the Tesco extension is a Riviéra – Tesco shuttle every 480 (one bus), so the every-30 trunk is not doubled at the shift changes.',
     'run the Tesco trips from Frýdecká skládka as they do (every 480 at 13:12, 13:42, 14:12), two Simutrans buses leaving skládka together three times a shift.'],
    ['706', 'Kojkovice and Osůvky are two hourly lines, as they run until 15:00; from 15:35 one trip an hour serves both.',
     'model the later shape: one line every 60 via Borek and Osůvky to Kojkovice (one bus instead of two).'],
    ['985', 'the Frenštát short trips are the afternoon burst as the buses ran it: 985 every 480 (Frenštát 12:47, 14:42; Ostrava 14:33, 16:03; two buses) and 985B out only (Ostrava 15:03, 15:33; two buses, empty return), with Z-Group’s 883985 trips read in.',
     'one two-way line every 90 as before (two buses), the burst trips off the pattern.'],
]
c['unmodelled'] = {
    '763': 'Třinec – Vendryně, Záolší: 5 trips a day (Třinec 12:37 and 13:37 out, school trips in the morning and at 15:06). Its stops are on 769 and the Třinec lines.',
    '776': 'Shift line Jablunkov – Třinec – Nošovice, Hyundai (Jablunkov 4:20, 12:20, 20:20; back 6:25, 14:25, 22:25). Its stops are all on other lines.',
    '352': 'Ostrava – Frýdek-Místek – Morávka: 8 trips a day at irregular times (13:28, 14:58, 17:22, 18:17 in the afternoon). Its stops are on 351, the Frýdek-Místek town lines and the Ostrava DPO lines (Řepiště, u školy on DPO 81).',
    '385': 'Shift line Ostrava, Náměstí Republiky – Nošovice, Hyundai (4:54, 12:54, 20:54; back 6:18, 14:15, 22:18, each in two buses). Its stops are all on other lines.',
    '386': 'Shift line Ostrava, Svinov – Nošovice, Hyundai (4:40, 12:40, 20:40; back 6:23, 14:19, 22:23). Its stops are on other lines; the Ostrava ones on DPO lines.',
    '315': 'Its afternoon trips (poliklinika 13:12, 14:13, 15:42 → Palkovice, centrum, via Chlebovice) are the way out of the bus that comes back as 316 (centrum 13:43, 14:45, 16:15): they are the out leg of the 316 Simutrans line, with their stops. Nothing runs back on 315 after 11:17.',
    '317': 'Early-morning and late-evening trips (4:18–7:05, 20:35, 22:07) plus one at 14:05. Its stops are on other town lines.',
    '319': 'Three trips a day (7:00, 7:38, 23:01), none in the afternoon.',
    '320': 'No trips on Tuesdays.',
    '705': 'Třinec town loop every 15 min 8:00–12:30 (shopping hours), in the afternoon only 15:52, 17:28 and 19:45. Its stops are on other Třinec lines.',
    '710': 'Třinec works shift trips (4:58–7:05 and 14:08–14:13). Its stops are on other Třinec lines.',
    '711': 'Třinec, Sosna nemocnice shift trips (3:50–7:35 and 14:17). Its stops are on 701, 715 and other Třinec lines.',
    '741': 'Shift line Karviná – Český Těšín – Nošovice, Hyundai (Karviná 4:34, 12:34, 20:34; back 6:25, 14:25, 22:25). Its stops are all on other lines.',
    '751': 'Třinec – Hnojník – Třanovice – Dobrá – Frýdek-Místek: 2 trips each way in 13:00–19:00 (Třinec 14:27, 15:35; Frýdek 13:20, 14:30), at irregular times. Its stops are on 750, 745 and the Frýdek-Místek lines.',
    '752': 'Třinec – Frýdek-Místek express: 3 morning trips out, 12:20 and 14:15 back. Its stops are on 750 and the Frýdek-Místek lines.',
    '740': 'Shift line Karviná – Český Těšín – Nošovice, Hyundai, every 8 h (Karviná 4:28, 12:28, 20:28; back 6:27, 14:27, 22:27), as 741 by another road. Its stops are all on other lines (738, 358 and the Karviná lines).',
    '398': 'No trips on Tuesday 20 Oct (Frýdlant – Ostravice – Staré Hamry, a licence with no weekday service).',
    '725': 'Český Těšín shift trips to Nová Tovární (5:41, 6:05, 13:52, 14:07). Nová Tovární is on 721 Mosty and 721/722 (diversion via Nová Tovární).',
}
# 22 Oct: 980 and 985 also run trips on Z-Group's Novojičínsko licences (883980, 883985: Ostrava – Frenštát short trips);
# the Novojičínsko sheet lists both lines as modelled here, so their trips are read here too
c['jdf']['extra_lics'] = {'883980': 'frydecko', '883985': 'frydecko'}
c['live']['carriers'] = ['Transdev Slezsko', 'ARRIVA', 'Z-Group']      # Z-Group's buses on those trips (63-1005, 63-1011, 63-1308)
c.pop('plate_guess', None)      # TESIN 001 / 004 found in the register (number-first plates), 22 Oct
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('config updated; areas', [(a['id'], a.get('operator'), a['depot']) for a in c['areas']])
