"""Writes the hand-set parts of config.json for MHD Pelhřimov + VDV 250 (pak rules, line notes, unmodelled lines, network state,
page texts). Edit here and rerun: python -X utf8 authoring/set_texts.py"""
import json, os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
c = json.load(open(P, encoding='utf-8'))
c['pak'] = dict(repo='C:/Users/vojte/Developer/simutrans-custom-czech-pak128', package='VZ-VDV-bus', packages=['VZ-VDV-bus', 'VZ-MHDPelhrimov-bus'],
  why=('VDV regional buses (white with the green VDV chevrons) take VZ-VDV-bus, which has the Crossway LE LINE 10,8M and 14,5M; the ICOM town buses take the town '
       'package VZ-MHDPelhrimov-bus. The Crossway LE LINE 12M in VDV paint and the Isuzu Novociti Life in ICOM blue with a white fade were drawn for this sheet '
       'by the art session (simutrans-122-0-c1, pakset main 03e77e8, 23 Nov 2026) from photos of 7J0 8266; any further type goes there.'),
  types={}, paints=[], special={}, rules=[
   ['*', 'Crossway LE LINE 10,8M', 'VDV', 'VZ-VDV-Crossway_LE_Line_10_8M-vdv-Crossway_LE_Line_10_8M'],
   ['*', 'Crossway LE LINE 14,5M', 'VDV', 'VZ-VDV-Crossway_LE_Line_14_5M-vdv-Crossway_LE_Line_14_5M'],
   ['*', 'Crossway LE LINE 12M', 'VDV', 'VZ-VDV-Crossway_LE_Line_12M-vdv-Crossway_LE_Line_12M'],
   ['*', 'NOVO Citi Life', 'modrá s bílým', 'VZ-MHDPelhrimov-NovoCiti_Life-icommodra-NovoCiti_Life']])
c['lines']['1']['note'] = (
 "Pelhřimov's main town line: the silo (industrial zone, west) – bus station – Táborská / Starý Pelhřimov (housing, east), 42 trips, most of them at the shift "
 "changes (5:00–7:30, 14:00–14:45), run through the afternoon by one bus in a fixed sequence: silo 14:40 → Táborská, Táborská 15:30 → silo, silo 15:45 → Starý "
 "Pelhřimov, Starý Pelhřimov 16:15 → silo, then silo 16:35 → Táborská. That sequence is one circuit every 120 (exact at 14:40, 15:30, 15:45 and 16:15; 16:35 is "
 "5 min off its repeat), one bus; two separate Simutrans lines (Táborská, Starý Pelhřimov) would need two. The 14:00–14:45 shift extras (silo 14:00 and 14:20, "
 "Táborská 14:25, Starý Pelhřimov 14:45), the 16:15 silo → Táborská and the short Táborská – bus station trips (16:35, 16:55, 17:25) run over stops of this circuit "
 "and are off the pattern. Read at the bus station, 13:00–18:00 has 9 trips each way and the circuit passes it 5 times each way: the rest is the shift-change "
 "work of a second and third bus (14:00–14:45 at the silo) at no repeating minute (passing check: no branch, ≥ 3 each way at one minute, is hidden there).")
c['lines']['3']['note'] = (
 "A loop from the bus station run both ways: via the railway station, the hospital (nemocnice II) and Pod Dolní branou, back by Architekta Janáka and Pod Floriánem "
 "(trips reach Architekta Janáka 17–24 min out), or the other way round via Pod Floriánem first and Karlovo náměstí (8–9 min out). Each way is its own Simutrans line "
 "(one route each). Whole day via the station: 6:45, 7:15, 9:25, 10:25, 11:10, 14:05, 14:55, 16:15, 16:50, 18:25; via Pod Floriánem: 4:40, 6:00, 6:36, 7:50, 10:00, "
 "12:05, 12:57, 15:15, 15:45, 16:57, 17:30 – about every 30 min in the afternoon between the two, at no fixed minute. Step 4 (method v4: a passing pattern is used "
 "where one exists): via the station every 180 at 16:15 and 16:50 (also 13:15, 13:50, 19:15 …; 7:15 exact too), via Pod Floriánem every 240 at 15:45 and 16:57 "
 "(also 12:57, 19:45 …), 5 real departures on the minute in the afternoon. 14:05, 14:55, 15:15, 17:30 and 18:25 are off the pattern. One bus each. A single line "
 "every 60 alternating the two ways (:15 / :45) would keep the half-hourly rhythm but hits only 15:45 and 16:15. The way via the station follows the 14:05 path by "
 "Křemešnická (its slot trips run via the railway station, Modřínová and Pod Hájkem, which the other way serves), the other way the 15:15 path by Skrýšov, so every "
 "stop of the loop is on a line. The passing check reads the loop at Čajkovského, which both ways pass, so it counts every trip as one way.")
c['lines']['250']['note'] = (
 "VDV regional line Pelhřimov – Humpolec – Havlíčkův Brod, Dopravní terminál: hourly through the day, leaving Pelhřimov at :43 (13:53 and 17:48 are 10 and 5 min "
 "off) and Havlíčkův Brod at :12 (13:02 is 10 min off; 18:15 and 19:15 wait for trains), 64 min, 3 buses. Short trips Pelhřimov – Humpolec, Poliklinika: out at "
 "13:18, 15:13, 17:18 and 18:43 (and 14:10 from the silo), back at 14:07 and 18:07. Read at the Poliklinika, 5 go out and 2 come back in the afternoon: the buses "
 "sleep at the Humpolec garage (provozovna Oblast Humpolecko), so the short line runs at its inbound rate, every 240 (13:18 / 17:18 out, 14:07 / 18:07 back), and "
 "the other out trips are off the pattern (buses going home; to be confirmed by the plates on Tue 24 Nov). Kojčice, Dehtáře (with Vadčice) and Velký Rybník, obec "
 "are village stops off the main road that only a few trips serve (15:13 out; 15:12 and 13:02 in from Havlíčkův Brod); every place is served, so the short line runs "
 "through them, 6 min longer than its slot trips take.")
# MHD 2 and 4 (owner, 23 Nov 2026: "i meant the mhd lines 2 and 4"): modelled, though every stop is on 1 and 3
AN, SILO, TAB = 'Pelhřimov, autobusové nádraží', 'Pelhřimov, silo', 'Pelhřimov, Táborská'
OSV = 'Pelhřimov, Osvobození I'
c['lines']['2'] = dict(core=[SILO, AN, 'Pelhřimov, nem.II', TAB], sim=[dict(name='2', every=240, legs=[
    dict(fr=SILO, to=TAB, via=['Pelhřimov, nem.II'], at=['14:15']),
    dict(fr=TAB, to=SILO, core_to=AN, at=['14:45'])])],
  note=("Shift and school line silo – bus station – hospital (nemocnice II) – Táborská, 20 trips: silo → Táborská 5:45, 8:30, 10:40, 13:00, 14:15; back "
        "5:27, 6:05, 8:05, 9:58 to the silo and 9:00, 11:00, 14:45 to the bus station (read there). Its afternoon is one bus: bus station 12:45 → silo, "
        "13:00 → Táborská, …, silo 14:15 → Táborská, Táborská 14:45 → bus station (direct, 5 min). Every 240 at 14:15 / 14:45, exact; 13:00 is off the pattern (the "
        "same bus an hour earlier). Every stop is also on 1 or 3."))
c['lines']['4'] = dict(core=[AN, SILO, OSV], sim=[dict(name='4', every=480, legs=[
    dict(fr=AN, to=SILO, at=['14:31']), dict(fr=SILO, to=OSV, at=['14:40']), dict(fr=OSV, to=AN, at=['15:04'])])],
  note=("Shift line for the silo (industrial zone): 5:03–6:51 in the morning, then one afternoon run, bus station 14:31 → silo, silo 14:40 → bus station "
        "→ Architekta Janáka → Osvobození I, Osvobození I 15:04 → bus station, and 22:45 from Starý Pelhřimov. One circuit every 480 (shift lines repeat "
        "every 8 h, method v4) at the afternoon run's real minutes, one bus; the morning trips are off the pattern."))
c['unmodelled'] = {}
c['network_state'] = [
 ['in', 'MHD Pelhřimov, regular timetable', c['regular_not_diversion']['355003'].replace('of MHD 3', 'of MHD 3 and 4')],
 ['in', 'VDV 250, timetable valid 28 Sep – 12 Dec 2026', 'The version of 28 Sep 2026 (CIS JŘ export of 23 Nov).'],
 ['out', 'Timetable change 13 Dec 2026', 'The export holds no versions from 13 Dec yet (every version here ends on 12 Dec); refresh the sheet when the JR2027 timetables are published.']]
c['texts'] = dict(
 eyebrow='MHD Pelhřimov · VDV lines from Pelhřimov · vypravenost',
 lede_who=('The town buses of Pelhřimov (MHD lines 1–4, ICOM transport) and every VDV regional line serving Pelhřimov (ČSAD AUTOBUSY České Budějovice: '
           '250, 259, 280, 281, 290, 300, 301, 302, 305, 320, 321, 324, 325, 326, 905, 925)'),
 lede_buses='Buses are the ones seen on each line on the VDV live map on Tuesday 24 Nov 2026.',
 swap_places='the Pelhřimov bus station, Počátky and Humpolec',
 scope=('MHD Pelhřimov licences 355001–355004 (ICOM transport a.s., provozovna Pelhřimov) and every regional licence of ČSAD AUTOBUSY České Budějovice with a '
        'stop in Pelhřimov (VDV areas Humpolecko 357xxx and Pelhřimovsko 358xxx, and the Jindřichův Hradec line 340905, numbered 905 here). Not here: 401 '
        '(358401, a PID line, on the PID Benešovsko sheet) and the long-distance lines to Praha (350410, 350804; 4 trips a day each), which are not regional'),
 buses=("The VDV live map (mapavdv.kr-vysocina.cz, Kraj Vysočina) polled every minute on Tuesday 24 Nov 2026 gives every bus's licence and trip number (the JDF "
        "trip) and its VDV vehicle number; the ČSAD buses also show their number plate, which joins them to the seznam-autobusu.cz register (read on 23 Nov 2026 in "
        "the owner's browser). The register lists no fleet numbers for ICOM or ČSAD, so a bus is named by its VDV vehicle number with its plate; a town bus the map "
        "shows without a plate keeps its VDV number and its type stays unknown. A bus fills one Simutrans line it ran in that line's window, by matching."),
 depots=('ICOM transport, provozovna Pelhřimov (the town buses; its four Isuzu Novociti Life run MHD Pelhřimov) and ČSAD AUTOBUSY České Budějovice, provozovny '
         'Oblast Pelhřimovsko and Oblast Humpolecko (the VDV lines; the register files their buses at Pelhřimov and Humpolec).'),
 search_example='64-10021',
 status_html=('<p class="sub"><b>Version 3, 23 Nov 2026: MHD 2 and 4 and every VDV line from Pelhřimov added; the buses come in version 4.</b> The VDV live map keeps no '
              'history, so it is polled all day on Tuesday 24 Nov; version 4 names the real bus on every Simutrans line. The lines, typed values and bus counts '
              'here stand unless that day shows buses pairing lines in a way the timetable hides.</p>'))
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('config texts written')
