"""Opavsko/Vítkovsko/Hlučínsko sheet config beyond the line specs: pak rules, texts, areas, network state, owner checks,
reasons for the lines left out, area_home, the 204 designed-trolleybus post-step. (opa_spec.py writes config.lines; this
script never touches lines.) Idempotent."""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
c = json.load(open(P, encoding='utf-8'))
c['artifact_url'] = 'https://claude.ai/artifact/K5ZeDCY2YYqV1Sz3tQwj3j'
c['regular_not_diversion'] = {
    '902241': 'Opava, Psychiatrická léčebna not served 28 Sep – 23 Nov 2026: short works, the regular route is modelled.',
    '903241': 'Opava, Psychiatrická léčebna not served 28 Sep – 23 Nov 2026: short works, the regular route is modelled.',
    '902243': 'Opava, Psychiatrická léčebna not served 28 Sep – 23 Nov 2026: short works, the regular route is modelled.',
    '903243': 'Opava, Psychiatrická léčebna not served 28 Sep – 23 Nov 2026: short works, the regular route is modelled.',
    '902262': 'Opava, Psychiatrická léčebna not served 5 Oct – 23 Nov 2026: short works, the regular route is modelled.',
    '902253': 'Služovice, obecní úřad not served 7 Sep – 31 Oct 2026: short works, the regular route is modelled.',
    '902256': 'Dolní Benešov, Zábřeh, Mexiko not served 16–21 Oct 2026: short works, the regular route is modelled.',
    '902275': 'Dolní Benešov, Zábřeh, Mexiko not served 16–21 Oct 2026: short works, the regular route is modelled.',
    '904284': 'Dolní Benešov, Zábřeh, Mexiko not served 16–21 Oct 2026: short works, the regular route is modelled.',
}
c['area_home'] = {'233': 'vitkovsko', '240': 'vitkovsko', '241': 'vitkovsko', '242': 'vitkovsko', '243': 'vitkovsko',
                  '254': 'opavsko', '285': 'hlucinsko', '292': 'hlucinsko'}
A = {a['id']: a for a in c['areas']}
A['opavsko'].update(operator='Z-Group bus', depot='provozovna Opava', note='')
A['vitkovsko'].update(operator='Z-Group bus', depot='provozovna Opava (Vítkov buses 23-)', note='')
A['hlucinsko'].update(operator='Transdev Slezsko', depot='provozovna Ostrava', note='Some of the 24- buses are registered under Transdev Morava.')
A['mhd-opava-trol'].update(operator='Městský dopravní podnik Opava', depot='depot', note="Trolleybus lines; timetables from CIS JŘ's city-transport JDF. Trolleybuses take VZ-DPOpava-trolleybus. 201, 202 and 203 run under the wire all the way; 204 leaves it on Vrchní street (Ratibořská – Divadlo) and at Kylešovice, škola, so MDPO runs it with trolleybuses that have an auxiliary drive: the ten 32 Tr 314–323 with traction batteries, or the two 26 Tr 305 and 306 with diesel generators (each card has an Overhead wire table).")
A['mhd-opava'].update(operator='Městský dopravní podnik Opava', depot='depot', note='Town buses take VZ-DPOpava-bus.')
c['fill_designed'] = {'204': dict(carrier='MDPO', type_contains=' Tr', alt=['battery', 'diesel generator'],
                                  why='designed: an MDPO trolleybus with an auxiliary drive ({alt}) for 204’s unwired sections, not in service {w0}–{w1} (204 ran with replacement buses during the Vrchní street closure, 12–23 Oct)')}

ODIS, DPB, DPT, HAV = 'VZ-ODIS-', 'VZ-DPOpava-', 'VZ-DPOpava-', 'VZ-MHDHavirov-'
def o(pre, core, liv): return f'{pre}{core}-{liv}-{core}'
c['pak'] = dict(
    repo=c['pak']['repo'], package='VZ-ODIS-bus',
    packages=['VZ-ODIS-bus', 'VZ-DPOpava-bus', 'VZ-DPOpava-trolleybus', 'VZ-MHDHavirov-bus'],
    why="Fleet desk (pak session simutrans-custom-czech-pak128-35), 21 Oct 2026: regional buses take VZ-ODIS-bus; Z-Group's white with the kraj logo is bila, Transdev Slezsko's Hlučínsko scheme is the red ring (bilacervenykruh) or the red Transdev logo (transdev); MDPO's buses take VZ-DPOpava-bus and its trolleybuses VZ-DPOpava-trolleybus (advertising wraps run in the plain livery, final). 22 Oct: the battery 32 Tr (314–323) take 32Tr_battery and the diesel-generator 26 Tr (305–306) 26TrDG, which can leave the wire (204's Vrchní street and Kylešovice škola).",
    types={}, paints=[], special={},
    rules=[
        # 22 Oct (fleet desk, main 684fc09): the off-wire variants, for the register's "alternativní pohon" (authoring/alt_drive.py)
        ['*', '32 Tr battery', '', 'VZ-DPOpava-32Tr-mdpobilocervena-32Tr_battery'],          # 314-323, battery
        ['*', '26 Tr diesel generator', '', 'VZ-DPOpava-26Tr-mdpobilocervena-26TrDG'],         # 305-306, diesel generator
        ['*', '26 Tr', '', o(DPT, '26Tr', 'mdpobilocervena')],
        ['*', '32 Tr', '', o(DPT, '32Tr', 'mdpobilocervena')],         # the three advertising wraps: plain livery, final (desk)
        ['*', '36 Tr', '', o(DPT, '36Tr', 'mdpobilocervena')],
        ['*', 'Citelis 12M', '', o(DPB, 'Citelis_12M', 'mdpobilocervena')],
        ['*', 'Urbanway 10,5M', 'městské', o(DPB, 'Urbanway_10_5M', 'mdpobilocervena')],
        ['*', 'Urbanway 12M', 'městské', o(DPB, 'Urbanway_12M', 'mdpobilocervena')],
        ['*', 'SOR NSG 12', 'MDPO', o(DPB, 'SOR_NSG_12', 'mdpobilocervena')],
        ['*', 'SOR NS 12 electric', 'elektrobus', o(DPB, 'SOR_NS_12_electric', 'mdpobilagrafika')],
        ['*', 'SOR CNG 12', 'Transdev', o(ODIS, 'SOR_CNG_12', 'transdev')],
        ['*', 'SOR CNG 12', '3ČSAD', o(ODIS, 'SOR_CNG_12', '3csadbilozelena')],
        ['*', 'SOR CNG 12', 'bílá & logo dopravy', o(ODIS, 'SOR_CNG_12', 'bila')],
        ['*', 'SOR CNG 12', 'logo dopravy', '~' + o(ODIS, 'SOR_CNG_12', 'bilazelenykruh')],   # red-ring object promised by the desk
        ['*', 'SOR CNG 10,5', 'logo dopravy', o(ODIS, 'SOR_CNG_10_5', 'bila')],
        ['*', 'SOR BNG 10,5', '', '~' + o(HAV, 'SOR_BNG_10_5', 'havirovmodra')],          # odd loan: permanent stand-in (desk)
        ['*', 'Crossway LE LINE 12M', 'logo dopravy', o(ODIS, 'Crossway_LE_Line_12M_NP', 'bilacervenykruh')],
        ['*', 'Citywide LE 13,7M', '', o(ODIS, 'Citywide_LE_13_7M_CNG', 'bilacervenykruh')],
        ['*', 'Citywide Suburban LE 12,6M', '', o(ODIS, 'Citywide_Suburban_LE_12_6M_CNG', 'bila')],
        ['*', 'Citywide LE 12M', '', o(ODIS, 'Citywide_LE_12M_CNG', 'bila')],
        ['*', 'Lion', '', o(ODIS, 'Lions_City_U_CNG', 'bila')],
    ])

c['texts'] = dict(
    eyebrow='ODIS regional buses and Opava town buses and trolleybuses · Opavsko · Vítkovsko · Hlučínsko · MHD Opava · vypravenost',
    lede_who='The ODIS bus lines of three regional contract areas (Opavsko and Vítkovsko of Z-Group bus, Hlučínsko of Transdev Slezsko) and the Opava town network of Městský dopravní podnik Opava, buses and trolleybuses',
    swap_places='Opava, Vítkov and Hlučín',
    scope="Licences with the area prefixes 902 (Opavsko) and 903 (Vítkovsko) of Z-Group bus, 904 (Hlučínsko) of Transdev Slezsko and 905 (MHD Opava) of Městský dopravní podnik Opava; the trolleybus lines 201–204 (905201–905204) from CIS JŘ's city-transport JDF (draha/mestske, downloaded 21 Oct 2026), the rest",
    scope_check='The prefixes match the live map (Z-Group, pr. Opava; Transdev Slezsko pr. Ostrava; MDPO) and the fleet numbers (22-, 23-, 24-). A line holding a second licence on the Bruntálsko or Novojičínsko sheet is modelled on the sheet with most of its trips.',
    buses_extra=" MDPO's vehicles appear on the live map as MDPO<fleet number> and are joined to the MDPO register by number. Trolleybus 204 ran with replacement buses on the day (Vrchní street closure, 12–23 Oct); it is modelled as the regular trolleybus line, and its trolleybuses are designed: MDPO trolleybuses not in service that afternoon, with an auxiliary drive for its unwired sections. A trolleybus with an auxiliary drive shows it after its type (+ battery, + diesel generator), from its register page.",
    search_example='22-1016',
    depots="Z-Group bus's Opava branch (22- Opavsko, 23- Vítkov), Transdev Slezsko pr. Ostrava (Hlučínsko's 24- buses) and MDPO's Opava depot (buses and trolleybuses). A seen bus counts at the branch the live map reports for it; a designed one at its home branch.",
    sources_extra=', <a href="https://portal.cisjr.cz/pub/draha/mestske/JDF.zip">CIS JŘ city-transport JDF</a> (Opava trolleybuses), <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=240">Z-Group bus</a>, <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=338">MDPO</a> and <a href="https://seznam-autobusu.cz/seznam?prov=1&amp;trakce=autobus&amp;iddopravce=7546">Transdev Morava</a> registers, <a href="https://www.mdpo.cz/pro-cestujici/aktuality-doprava/omezeni-provozu-mhd-na-ul-vrchni-v-opave">MDPO notice on the Vrchní closure</a>, overhead wire and trolleybus routes from <a href="https://www.openstreetmap.org/relation/1295057">OpenStreetMap</a> (Overpass, 22 Oct 2026), checked against <a href="https://cs.wikipedia.org/wiki/Trolejbusov%C3%A1_doprava_v_Opav%C4%9B">Wikipedia</a>’s partial-trolleybus stops; battery and diesel-generator trolleybuses from their <a href="https://seznam-autobusu.cz/vuz/78818">register pages</a> (“alternativní pohon”)',
)

c['network_state'] = [
    ['in', 'Three regional contract areas and the Opava town network',
     'Opavsko (licences 902xxx) and Vítkovsko (903xxx) of Z-Group bus, Hlučínsko (904xxx) of Transdev Slezsko, and the town lines of Opava (905xxx) of Městský dopravní podnik Opava. Each has its own section below; the trolleybuses are a section of their own.'],
    ['in', 'Opava trolleybuses 201–204',
     "Their timetables are in CIS JŘ's city-transport JDF (traction T), not in the bus export; they are read the same way and modelled as trolleybus lines (the owner asked for them)."],
    ['in', 'Overhead wire',
     "Each trolleybus route (OpenStreetMap route relations) was checked against the wire mapped in OpenStreetMap, every 10 m, 25 m tolerance. 201, 202 and 203 are under the wire all the way. 204 has two unwired stretches: Ratibořská – Vrchní – U Cukrovaru – Pekařská – Divadlo (about 2.0 km without wire) and Kylešovice, Bílovecká – Hlavní – škola (0.6 km in a straight line between the stops, about 1 km by the timetable; the OSM relation stops at Bílovecká, so this end was added from the timetable's stops, which have no wire within 100 m). Wikipedia marks the same stops as partial-trolleybus stops. 202's single daily trip to Malé Hoštice also leaves the wire; it is not modelled."],
    ['out', 'Trolleybus 204: Vrchní street closure (12–23 Oct)',
     'Road repairs on Vrchní street in Kateřinky: one-way 12–20 Oct, full closure 21–23 Oct. On the vehicle day 204 ran with replacement buses via Partyzánská (trips 40xx on the live map, MDPO Citelis 150–157). The closure ends this week, so 204 is modelled as the regular trolleybus line with designed trolleybuses (owner check).'],
    ['out', 'Short diversions: the regular routes are modelled',
     '241 and 243 (Opava, Psychiatrická léčebna not served, 28 Sep – 23 Nov), 262 (the same stop, 5 Oct – 23 Nov), 253 (Služovice, obecní úřad, 7 Sep – 31 Oct) and 284 (Dolní Benešov, Zábřeh, Mexiko, 16–21 Oct; also 256 and 275, which are listed). Short works are modelled as the regular state.'],
    ['in', 'Diversions to the end of the timetable year',
     '234, 242 and 261 skip Březová, střed until 11 Dec; 263 and 264 run diversion versions with the same stops until 12 Dec. They are modelled as they run.'],
    ['out', 'Lines shared with other sheets',
     '615, 620, 691, 692 and 693 (minor Vítkovsko/Opavsko licences) are on the Novojičínsko/Bílovecko sheet. This sheet models 260 and 920 (also Bruntálsko/Rýmařovsko licences), 261, 263, 270, 285 and 678 (also Novojičínsko/Bílovecko licences) and 555 (the Havířovsko/Karvinsko/Orlovsko sheet lists it as Hlučínsko\'s).'],
]
c['keep_roster'] = 'data/published/roster_v8.json'
c['keep_roster_why'] = 'The owner may have the sheet in the game (published v8). A rebuild keeps each published bus on its Simutrans line wherever it is still evidence for that line (shared 04_roster step 6); v9 (25 Oct 2026) changes only 292.'
c['owner_checks'] = [
    ['204', 'modelled as the regular trolleybus line (Kylešovice, škola – Englišova, every 60 with three slots :00 / :24 / :36), with designed MDPO trolleybuses that have an auxiliary drive, battery or diesel generator (about 2.6 km of the 10 km route has no wire); on the vehicle day it ran with replacement buses during the Vrchní street closure (to 23 Oct).',
     'model it as it ran: buses via Partyzánská (Citelis 150–157 were seen), skipping U Cukrovaru, Vrchní and Ratibořská.'],
    ['217', 'the hourly Koupaliště – Slavkov pattern (:04 / :25) is the line; the early-afternoon trips Divadlo – Slavkov (about every 32 min, 14:12–16:10) are off the pattern.',
     'add 217 Divadlo every 480 with four slots (Divadlo 14:35, 15:07, 15:40, 16:10; Slavkov 14:12, 14:50, 15:22, 15:55), one more bus.'],
    ['241', 'the regular routes of 241, 243 and 262, via Opava, Psychiatrická léčebna, not their diversions to 23 Nov.',
     'model the diversions as they run until 23 Nov (the stop not served).'],
    ['920', 'three Simutrans lines: Svinov – Šumperk and Svinov – Rýmařov every 120 each (together hourly at :17 from Svinov) and Opava – Rýmařov every 480 (13:24 / 15:02); the Bruntál short trips (11:17, 12:17; back 13:03, 14:43) are off the pattern.',
     'one Svinov – Bruntál trunk every 60 with the Rýmařov and Šumperk ends as variants.'],
    # Hlučínsko lines at sad B. Němcové, set by hand on 25 Oct 2026 (../method-check-2026-10-25.md)
    ['290', 'every 120 with four slots each way (Ostrava 14:44, 14:59, 15:24, 15:49; Hať 14:47, 15:31, 16:07, 16:37), exact in the model hours, 4 buses.',
     'every 40 with one slot each way (Ostrava :19, Hať :07): fewer typed values and 3 buses, but only three of the five Ostrava departures, and the 15:39 and 15:27 slots have no real trip.'],
]
c['unmodelled'] = {
    '214': 'Shift trips Dobrovského → Komárov, TEVA 2 (5:03, 5:30, 6:30, 13:03; one back at 6:15). Its stops are on other town lines (211, 220, 203, 213); TEVA 2 is on 223.',
    '228': 'Night line (Divadlo – Kylešovice, 23:20 – 0:57); no afternoon trips.',
    '229': 'Night line (23:33 – 3:15); no afternoon trips.',
    '256': 'Opava – Dolní Benešov – Píšť / Kravaře, Kouty: 10 trips a day, in the afternoon 14:02 and 14:11 out, 14:30 and 15:10 back. Its stops are on 282, 254, 252, 253 and 257.',
    '275': 'Opava – Dolní Benešov – Hlučín: 13 trips, mostly before 8:00; in the afternoon 14:33 and 15:21 out, 14:47 back. Its stops are on 254, 252, 253, 284 and 281.',
    '283': 'Two trips a day (Kobeřice 18:48 → Ostrava, Ostrava 21:05 → Kobeřice). Its stops are on 252, 284 and 281.',
}
# area intro wording (shared 06 keys, 21 Oct): 'Licences 905201-905204', 'At 16:00 MDPO had ...'
A['mhd-opava-trol'].update(licences='Licences 905201–905204 (trolleybus lines 201–204)', operator_short='MDPO')
A['mhd-opava'].update(operator_short='MDPO')
# ---- final cross-sheet pass (parent, 21 Oct 2026): sheets built in parallel, one bus one sheet in the order
# Ostrava > HKO town > HKO regional > TFJ > Opavsko > Novojičínsko > Bruntálsko (a later sheet excludes the earlier sheets' buses)
c['other_sheets']['novojicinsko']['url'] = 'https://claude.ai/artifact/YFgUu62jD8YqfpuoL8FZpp'
c['post_roster'] = ['authoring/offwire.py', 'authoring/alt_drive.py', 'authoring/fill_designed.py']      # run.py runs them after 04_roster (wire check; battery/diesel marks; 204's designed trolleybuses)
# ---- end cross-sheet
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('config updated')
