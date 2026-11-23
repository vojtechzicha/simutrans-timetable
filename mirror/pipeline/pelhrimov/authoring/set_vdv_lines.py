"""The VDV lines of the Pelhřimov sheet (config.lines for 250 … 925 and 905), designed by hand with the bus schedule method v4
(23 Nov 2026). Stop names are found in the reading by substring, so a JDF name change shows up as an error here.
Edit and rerun: python -X utf8 authoring/set_vdv_lines.py, then scripts/run.py."""
import json, os
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(HOME, 'config.json')
c = json.load(open(P, encoding='utf-8'))
R = json.load(open(os.path.join(HOME, 'data', 'derived', 'reading.json'), encoding='utf-8'))
STOPS = sorted({s for x in R.values() for r in x['rows'] for s in r['stops']})
def S(key):
    hit = [s for s in STOPS if key in s]
    exact = [s for s in hit if s == key]
    if exact: return exact[0]
    assert len(hit) == 1, f'{key}: {hit}'
    return hit[0]
AN = S('Pelhřimov, autobusové nádraží')
L = c['lines']
def line(core, sims, note=''):
    return dict(core=core, sim=sims, note=note)
def sim(name, every, *legs, window=None):
    d = dict(name=name, every=every, legs=list(legs))
    if window: d['window'] = window
    return d
def leg(fr, to, at, **k): return dict(fr=fr, to=to, at=at, **k)

HUM = S('Humpolec, autobusové nádraží')
KUCH = S('Humpolec, Kuchařov'); MYS = S('Mysletín')
L['259'] = line([AN, HUM, KUCH, MYS], [sim('259', 240, leg(AN, HUM, ['9:37']), leg(HUM, AN, ['13:32'])),
    sim('259 Mysletín', 480, leg(MYS, KUCH, ['14:02'], notvia=[AN]), leg(KUCH, MYS, ['14:29'], notvia=[AN], stops_via=[S('Bystrá')]))])
LUK = S('Lukavec, náměstí') if any('Lukavec, náměstí' in s for s in STOPS) else S('Lukavec')
L['301'] = line([AN, LUK], [sim('301', 120, leg(AN, LUK, ['14:33'], stops_via=[S('Dubovice')]), leg(LUK, AN, ['14:23']))])
PAC = S('Pacov, autobusové nádraží'); NC = S('Nová Cerekev, náměstí')
L['305'] = line([PAC, NC], [sim('305', 120, leg(PAC, NC, ['15:18']), leg(NC, PAC, ['16:03']))])
ZL = S('Želiv, Lhotice'); ZR = S('Želiv, restaurace Na Želivce')
L['258'] = line([AN, ZR, ZL], [sim('258', 120, leg(AN, ZL, ['14:37'], core_to=ZR), leg(ZL, AN, ['15:37'], core_to=AN))])
CER = S('Černovice, náměstí')
L['280'] = line([AN, NC, CER], [
    sim('280 Černovice', 120, leg(AN, CER, ['14:38']), leg(CER, AN, ['14:37'])),
    sim('280 Nová Cerekev', 120, leg(AN, NC, ['15:38'], notvia=[CER]), leg(NC, AN, ['16:00'], notvia=[CER]))])
KAM = S('Kamenice n.Lipou, autobusové nádraží') if any('Kamenice n.Lipou, autobusové' in s for s in STOPS) else S('Kamenice nad Lipou, autobusové nádraží')
LV = S('Libkova Voda')
L['281'] = line([AN, LV, KAM], [
    sim('281 Kamenice', 240, leg(AN, KAM, ['14:57']), leg(KAM, AN, ['10:22'])),
    sim('281 Libkova Voda', 60, leg(AN, LV, ['14:40'], notvia=[KAM]), leg(LV, AN, ['15:01'], notvia=[KAM]))])
POC = S('Počátky, autobusové nádraží'); ZIR = S('Žirovnice, náměstí')
L['290'] = line([AN, ZIR, POC], [sim('290', 120, leg(AN, POC, ['14:34'], core_to=ZIR), leg(POC, AN, ['14:31']))])
JI = S('Jihlava, autobusové nádraží')
L['300'] = line([JI, AN, PAC], [
    sim('300 Jihlava', 60, leg(JI, AN, ['15:40'], core_to=AN), leg(AN, JI, ['15:34'])),
    sim('300 Pacov', 60, leg(AN, PAC, ['15:31']), leg(PAC, AN, ['15:50'], stops_via=[S('Dobrá Voda u Pacova')]))])
c['coverage_exceptions'] = {S('Vyskytná, rozcestí'): ("A roadside stop of Vyskytná (whose village stop is on 300 and 321), served in the afternoon only by "
    "300's Jihlava :10 extras (13:10, 14:10, 15:10; one back, 14:04), which are off the pattern: three one way and one back is no branch.")}
ROH = S('Rohozná')
L['320'] = line([AN, ROH], [sim('320', 120, leg(AN, ROH, ['14:35'], stops_via=[S('Nový Rychnov, Losy samota')]), leg(ROH, AN, ['15:25']))])
NR = S('Nový Rychnov')
VYS = S('Vyskytná')
L['321'] = line([AN, NR, VYS], [sim('321', 120, leg(AN, NR, ['15:35']), leg(NR, AN, ['14:55'])),
    sim('321 Jankov', 480, leg(NR, S('Jankov, obec'), ['14:24'], notvia=[AN]), dict(fr=S('Jankov, obec'), to=NR, untimed=True, rt=17))])
HCZ = S('Horní Cerekev, železniční stanice'); HCN = S('Horní Cerekev, náměstí')
L['324'] = line([AN, HCN, HCZ], [sim('324', 120, leg(AN, HCZ, ['14:40'], core_to=HCN), leg(HCZ, AN, ['15:32']))])
L['325'] = line([AN, HCN], [sim('325', 60, leg(AN, HCN, ['15:38'], notvia=[HCZ], stops_via=[S('Vokov'), S('Dobrá Voda, obec')]), leg(HCN, AN, ['15:59'], notvia=[HCZ]))])
ZIRV = S('Žirov')
L['326'] = line([AN, ZIRV], [sim('326', 480, leg(AN, ZIRV, ['14:42']), leg(ZIRV, AN, ['15:15']))])
STO = S('Stojčín, železniční stanice'); POP = S('Popelín')
L['925'] = line([AN, POC, ZIR, STO, POP], [
    sim('925', 60, leg(AN, POC, ['14:35']), leg(POC, AN, ['14:50'])),
    sim('925 Stojčín', 120, leg(POC, STO, ['15:00'], notvia=[POP]), leg(STO, POC, ['15:30'], notvia=[POP])),
    sim('925 Popelín', 120, leg(POC, POP, ['14:10']), leg(POP, POC, ['14:36']))])
JH = S('Jindřichův Hradec, Pravdova')
NV = S('Nová Včelnice, náměstí')
L['905'] = line([AN, KAM, NV, JH], [sim('905', 120, leg(AN, JH, ['16:34', '15:49'], stops_via=[S('Myslotín')]), leg(JH, AN, ['14:12', '15:07'], stops_via=[S('Jindřichův Hradec, Průmyslová')])),
    sim('905 Nová Včelnice', 120, leg(JH, NV, ['13:27', '14:32'], notvia=[AN], core_to=S('Jarošov n.Než., rozcestí'), stops_via=[S('Jarošov n.Než., Lovětín')]), leg(NV, JH, ['13:02', '14:02'], notvia=[AN]))])
L['302'] = line([AN], [sim('302', 480, leg(AN, AN, ['14:02']))])
# model hour set by hand where the line's pattern ends inside the default window (method v4: 'Model hour set by hand')
for k, an in {'305': '14:30', '324': '14:30', '325': '15:00', '281': '15:00'}.items(): L[k]['anchor'] = an
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('VDV lines set:', ', '.join(k for k in L if k not in ('1', '2', '3', '4')))

# ---- card notes (the reading behind each design; 23 Nov 2026)
NOTES = {
 '259': ("Humpolec – Zachotín – Pelhřimov, a few trips a day: Pelhřimov → Humpolec 5:37, 9:37, 12:30, 14:38, 17:37; back 6:34, 9:32, 13:29, 15:32 (read at "
         "Humpolec, autobusové nádraží; some trips start or end at Humpolec, Kuchařov). Every 240: out 9:37 / 13:37 / 17:37 (5:37, 9:37 and 17:37 exact), back "
         "13:32 (9:32 exact, 13:29 3 min). 12:30 and 14:38 are off the pattern. 259 Mysletín is the Humpolec end's own run through Bystrá (Mysletín 14:02 → "
         "Humpolec, Kuchařov, back 14:29), every 480, the only service of Bystrá and Bystrá, Březina."),
 '301': ("Pelhřimov – Červená Řečice – Hořepník – Lukavec, every 120 both ways all day: Pelhřimov at :33 in even hours (10:33, 14:30, 16:33, 18:33), Lukavec at "
         ":23 (4:23 … 16:23). Out via Dubovice, as the 14:30 runs (the only trips into the village)."),
 '305': ("Pacov – Leskovice – Nová Cerekev: Pacov 13:18 and 15:18, Nová Cerekev 14:03 and 16:03 (and 6:22 / 7:03 in the morning). Every 120, one bus; modelled "
         "at 14:30, where the pattern runs (it ends with the 16:03; 17:33 to Litohošť is a bus going home)."),
 '258': ("Pelhřimov – Svépravice – Želiv: out at :37 in even hours (12:37, 14:37 to Lhotice; 16:37, 18:37 end at Želiv, restaurace), back from Lhotice at :37 "
         "in odd hours (13:37, 15:37; 17:55 from the restaurant). Every 120, read at Želiv, restaurace so the short trips count."),
 '280': ("Pelhřimov – Nová Cerekev – Černovice, hourly from Pelhřimov at :38: even hours to Černovice (12:38, 14:38, 16:38, 18:38), odd hours to Nová Cerekev "
         "(13:38, 15:38). Back from Černovice at :37 (even hours) and from Nová Cerekev at :00 (14:00, 16:00). Ex4: two Simutrans lines every 120, all slots exact."),
 '281': ("Pelhřimov – Božejov – Kamenice nad Lipou: Kamenice trips are few (out 10:57, 14:57, 16:57; back 4:37, 6:22, 10:22): every 240 (10:57 / 14:57 out, "
         "6:22 / 10:22 back); 16:57 is a bus going to Kamenice for the night. Afternoon shuttles to Libkova Voda at :40 (13:40, 14:40, 15:40), back at :01: 281 "
         "Libkova Voda every 60, modelled at 15:00 inside its run."),
 '290': ("Pelhřimov – Mezná – Častrov – Žirovnice – Počátky: Pelhřimov at :34 in even hours (12:34, 14:34 to Počátky; 16:34, 18:34 to Žirovnice, read there), "
         "Počátky at :31 (12:31, 14:31, 16:31). Every 120."),
 '300': ("Jihlava – Vyskytná – Pelhřimov – Pacov. Jihlava → Pacov runs through hourly (Jihlava :40, Pelhřimov :31, Pacov :10); the other way not every bus runs "
         "through (Pacov :50 → Pelhřimov, some ending there; Pelhřimov :34 → Jihlava, some starting there), so the line is split at Pelhřimov: 300 Jihlava every 60 "
         "(Jihlava :40, Pelhřimov :34; 16 and 11 exact) and 300 Pacov every 60 (Pelhřimov :31, Pacov :50; 14:36 is 5 min late, the one slot off). The Jihlava "
         ":10 extras (13:10, 14:10, 15:10, via Vyskytná, rozcestí and Opatov) have one trip back (14:04): buses going to the Pelhřimov garage, off the pattern. "
         "Back from Pacov via Dobrá Voda u Pacova, as the 15:47 runs (its only afternoon trip)."),
 '302': ("Pelhřimov – Krasíkovice – Hodějovice – Pelhřimov, a loop run twice a day (7:22, 14:02): the only service of Hodějovice, so its own line every 480 at 14:02."),
 '320': ("Pelhřimov – Nový Rychnov – Rohozná, every 120 all afternoon: Pelhřimov :35 in even hours, Rohozná :25 in odd hours, all exact. Out via Losy samota, as "
         "the 14:35 runs (its only trip)."),
 '321': ("Pelhřimov – Vyskytná – Nový Rychnov: Pelhřimov :35 in odd hours (13:35, 15:35, 17:35), Nový Rychnov :55 in even hours (12:55, 14:55). Every 120. "
         "321 Jankov is the Nový Rychnov bus's loop by Opatov and Jankov (14:24, back to Nový Rychnov 14:54), every 480, the only service of Jankov, obec."),
 '324': ("Pelhřimov – Pavlov – Černov – Horní Cerekev: out 12:40 and 17:40 (to the square), 14:40 (to the station); back from the station 13:32 and 15:32. "
         "Every 120 (Pelhřimov :40 even hours, read at the square; station :32 odd hours), modelled at 14:30; 17:40 is a bus going to Horní Cerekev for the night."),
 '325': ("Pelhřimov – Rynárec – Horní Cerekev: out hourly at :38 (13:38–16:38), back at 14:57 and 15:59 (and Horní Ves 12:50). Read at Horní Cerekev, 4 out and "
         "2 back: buses sleep at Horní Cerekev / Horní Ves. Every 60 at the inbound rate, modelled at 15:00 (14:38, 15:38 out; 14:59, 15:59 back); 13:38 and "
         "16:38 are off the pattern. Out through Vokov and Dobrá Voda, as the 15:38 runs (the villages' only afternoon trip); the 14:38 goes by the road past "
         "Rynárecká and ACHP, which the town lines serve."),
 '326': ("Pelhřimov – Střítež pod Křemešníkem – Žirov: out 6:17, 14:42, 16:32; back 4:50, 6:50, 15:15. Every 480 (14:42 / 15:15), one bus; 16:32 is the bus "
         "going to Žirov for the night."),
 '925': ("Pelhřimov – Počátky – Žirovnice – Stojčín / Popelín. Pelhřimov → Počátky hourly at :35 (even hours end at Počátky, odd hours go on), and every bus "
         "back passes Počátky at :50: 925 every 60, exact both ways. Beyond Počátky, Ex4 lines: 925 Stojčín (Počátky :00 in odd hours to Stojčín, the railway "
         "station; back :30) every 120, and 925 Popelín (on from the odd-hour Pelhřimov trips, Počátky :10; back from Popelín :36) every 120. 14:10 to Žirovnice "
         "is off the pattern."),
 '905': ("Jindřichův Hradec – Nová Včelnice – Kamenice nad Lipou – Pelhřimov (Jihočeský licence, ČSAD AUTOBUSY ČB). Hourly: Pelhřimov at :49 in odd hours and "
         ":34 in even hours in the late afternoon (12:39, 14:39 earlier: the afternoon wins), Jindřichův Hradec at :07 / :12. Every 120 with two slots each way. "
         "The :34 trips run through Ondřejov and Myslotín, the :49 ones by the Ondřejov bypass: the line follows the village path (Myslotín's only service). "
         "Back via Jindřichův Hradec, Průmyslová, as the 14:12 runs. 905 Nová Včelnice is the hourly Jindřichův Hradec – Nová Včelnice shuttle (13:27, 14:32 … "
         "back :02), every 120 with two slots, through Jarošov, Lovětín as the 13:27 and 15:27 run."),
}
for k, v in NOTES.items(): L[k]['note'] = v
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('notes written')
