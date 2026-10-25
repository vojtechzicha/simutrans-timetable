"""author the first structural spec of the Těšínsko/Třinecko/Frýdecko sheet (intervals and minutes 'auto', checked after).
25 Oct 2026: every line whose rows failed the Step 4 audit is set by hand with the bus schedule method v4, both directions
together; the reading, candidates, typed values and need per line are in ../method-check-2026-10-25.md."""
import os, sys, json
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, AL, rel
T = load('trips.json')
c = json.load(open(rel('config.json'), encoding='utf-8'))
c['terminus_alias'] = {"Třinec, autobusová stanice pod Kanadou": "Třinec, autobusová stanice"}
c['terminus_alias_why'] = "Třinec, autobusová stanice pod Kanadou is the bus station's other stand; trips start and end at either, so they are one terminal."
ALL = sorted({AL(nm(s)) for tr in T.values() for t in tr for s in t['stops']})
def S(sub):
    m = [s for s in ALL if s == sub] or [s for s in ALL if s.endswith(sub)] or [s for s in ALL if sub in s]
    if len(m) != 1: raise SystemExit(f'stop {sub!r}: {m[:6]}')
    return m[0]
def leg(fr, to, **kw): return dict(fr=S(fr), to=S(to), **({'at': 'auto'} if not kw.get('untimed') and 'at' not in kw and 'knot_at' not in kw else {}), **{k: (S(v) if k in ('knot', 'core_to') else [S(x) for x in v] if k in ('via', 'notvia') else v) for k, v in kw.items()})
def two(name, A, B, a=None, b=None, every='auto'):
    a = a or {}; b = b or {}
    return dict(name=name, every=every, legs=[leg(A, B, **a), leg(B, A, **b)])
def loop(name, A, every='auto', **kw): return dict(name=name, every=every, legs=[leg(A, A, **kw)])
import builtins
def oneway(name, A, B, every='auto', a=None):
    return dict(name=name, every=every, legs=[leg(A, B, **(a or {})), leg(B, A, untimed=True)])
L = {}
TAS, JAS, NZS = 'Třinec, autobusová stanice', 'Jablunkov, autobusová stanice', 'Návsí, železniční stanice'
TZS = 'Třinec, železniční stanice'; BZS = 'Bystřice, železniční stanice'
CAS, CZS = 'Český Těšín, autobusová stanice', 'Český Těšín, železniční stanice'
HAV = 'Havířov, Město, železniční stanice'
FAN, FZS, FPOL = 'Frýdek, autobusové nádraží', 'Frýdek, železniční stanice', 'Místek, poliklinika'
NR = 'Mor.Ostrava, Náměstí Republiky'
# ---------------- Jablunkovsko–Třinecko (861)
# G1 (Jablunkovsko–Třinecko) method check 25 Oct 2026: replacement entries for tfj_spec.py (only changed lines).
# Set by hand with the bus schedule method v4 (../method-check-2026-10-25.md): every row passes Step 4 per direction and keeps
# the real 13:00-18:00 rate (slots within ±1 of the real departures there).
L['764'] = dict(core=[S(TAS)], sim=[loop('764', TAS, every=180, at=['13:35', '14:20'])])
L['766'] = dict(core=[S(TAS)], sim=[loop('766', TAS, every=120, at=['15:40'])])
L['769'] = dict(core=[S(TAS), S('Vendryně, konečná')], sim=[two('769', TAS, 'Vendryně, konečná')])
L['770'] = dict(core=[S(BZS), S('Paseky, konečná')], sim=[two('770', BZS, 'Paseky, konečná', a=dict(at=['13:45', '14:51']), b=dict(at=['13:30', '15:05']), every=180)])
L['771'] = dict(core=[S(BZS), S('Nýdek, náměstí'), S('Hluchová, Setinka')],
                # the Setinka trips (Bystřice 15:10 via náměstí) are 771 Hluchová's, so the main rows leave them out
                sim=[two('771', BZS, 'Nýdek, náměstí', a=dict(at=['13:50'], notvia=['Hluchová, Setinka']), b=dict(at=['14:00'], notvia=['Hluchová, Setinka']), every=120),
                dict(name='771 Hluchová', every=480, legs=[leg(BZS, 'Hluchová, Setinka', at=['12:25']), leg('Hluchová, Setinka', BZS, at=['12:47'])])])
L['772'] = dict(core=[S(TAS), S('Gora, konečná')], sim=[two('772', TAS, 'Gora, konečná')])
L['773'] = dict(core=[S(BZS), S('Nýdek, náměstí'), S('Nýdek, Střelmá')],
                sim=[dict(name='773', every=480, legs=[leg(BZS, 'Nýdek, Střelmá', knot='Nýdek, náměstí', knot_at=['12:33']), leg('Nýdek, Střelmá', BZS, at=['12:42'])])])
L['781'] = dict(core=[S(NZS), S('Šance, opevnění'), S(JAS), S('Hrčava, konečná')],
                # the Hrčava trips via Šance (Návsí 10:58, 18:58; Třinec 22:23) are 781 Hrčava's
                sim=[two('781', NZS, 'Šance, opevnění', a=dict(at=['14:03', '14:43'], notvia=['Hrčava, konečná']), b=dict(at=['14:35', '15:30'], notvia=['Hrčava, konečná']), every=120),
                     two('781 Hrčava', JAS, 'Hrčava, konečná')])
L['782'] = dict(core=[S(NZS), S('Radvanov, konec'), S(JAS)], sim=[dict(name='782', every=480, legs=[leg(NZS, 'Radvanov, konec', at=['14:55']), leg('Radvanov, konec', JAS, at=['15:05']), leg(JAS, NZS, untimed=True, rt=5)])])
L['783'] = dict(core=[S(TAS), S('Návsí, nadjezd'), S(JAS), S('Bukovec, škola'), S('točna Písečná')],
                # main rows: the trips that run through to Bukovec (via Bukovec, škola); the Ski areál and Písečná trips are their lines'
                sim=[two('783', TAS, 'Bukovec, škola', a=dict(at=['13:28', '14:15', '15:13'], core_to=JAS, via=['Bukovec, škola']),
                         b=dict(knot=JAS, knot_at=['13:52', '14:37', '15:37'], via=['Bukovec, škola']), every=180),
                     two('783 Písečná', NZS, 'točna Písečná'),
                     dict(name='783 Ski areál', every=480, legs=[leg(TAS, 'Ski areál - Kempaland', at=['14:00']), leg('Ski areál - Kempaland', TAS, untimed=True)])])
L['784'] = dict(core=[S(NZS), S('Horní Lomná, střed'), S('Horní Přelač')],
                sim=[two('784', NZS, 'Horní Přelač', a=dict(at=['14:55', '16:00'], core_to='Horní Lomná, střed'), b=dict(at=['14:30', '16:25'], knot='Horní Lomná, střed'), every=180)])
L['786'] = dict(core=[S(JAS), S('Bystřice, Na Paseky')], sim=[two('786', JAS, 'Bystřice, Na Paseky')])
L['787'] = dict(core=[S('Bystřice, Na Paseky'), S(JAS), S(TAS)],
                sim=[two('787', 'Bystřice, Na Paseky', JAS, a=dict(at=['15:58']), b=dict(at=['14:50']), every=120), two('787 Třinec', TAS, 'Bystřice, Na Paseky')])
L['788'] = dict(core=[S(JAS), S('Lísky, konečná')], sim=[two('788', JAS, 'Lísky, konečná')])
# ---------------- Českotěšínsko (871)
L['731'] = dict(core=[S(CAS), S('Albrechtice, střed')], sim=[two('731', CAS, 'Albrechtice, střed')])
L['739'] = dict(core=[S(CAS), S(FAN)], sim=[two('739', CAS, FAN)])
L['743'] = dict(core=[S('Hnojník, škola polská'), S('Řeka, konečná')], sim=[two('743', 'Hnojník, škola polská', 'Řeka, konečná')])
L['732'] = dict(core=[S(TAS), S(CAS), S(HAV)],
                sim=[two('732', TAS, HAV, a=dict(knot=CAS, knot_at=['13:45', '15:15']), b=dict(at=['13:52', '14:27'], core_to=CAS), every=180)])
L['733'] = dict(core=[S(CAS), S('U Stonávky')], sim=[two('733', CAS, 'U Stonávky', a=dict(at=['14:50']), b=dict(at=['15:29']), every=120)])
L['734'] = dict(core=[S(TAS), S(CAS)], sim=[two('734', TAS, CAS, a=dict(at=['14:20', '15:30']), b=dict(at=['15:05', '16:05']), every=180)])
L['735'] = dict(core=[S(CAS), S('Těrlicko, střed')], sim=[two('735', CAS, 'Těrlicko, střed', a=dict(at=['16:50']), b=dict(at=['16:52']), every=96)])
L['736'] = dict(core=[S(CAS), S('Chotěbuz, hájenka')],
                sim=[two('736', CAS, 'Chotěbuz, hájenka', a=dict(at=['13:35', '14:25']), b=dict(at=['13:55', '14:45']), every=160)])
L['738'] = dict(core=[S('Svibice, Slovenská'), S('Karviná, Fryštát, autobusové nádraží')],
                sim=[two('738', 'Svibice, Slovenská', 'Karviná, Fryštát, autobusové nádraží',
                         a=dict(at=['13:52', '14:17', '14:37', '14:57']), b=dict(at=['14:34', '14:52', '15:12', '15:39']), every=90)])
# 745: the main rows leave out the Třanovice trips (notvia), which are 745 Třanovice's own (Ex4: one line per destination)
L['745'] = dict(core=[S('Komorní Lhotka, konečná'), S('Hnojník, obch.stř.'), S('Třanovice, křižovatka')],
                sim=[two('745', 'Komorní Lhotka, konečná', 'Hnojník, obch.stř.', a=dict(at=['14:16'], notvia=['Třanovice, křižovatka']),
                         b=dict(at=['15:37'], notvia=['Třanovice, křižovatka']), every=120),
                     two('745 Třanovice', 'Komorní Lhotka, konečná', 'Třanovice, křižovatka', a=dict(at=['15:31']), b=dict(at=['16:06']), every=120)])
L['747'] = dict(core=[S(CAS), S('Střítež, Obecní úřad')], sim=[two('747', CAS, 'Střítež, Obecní úřad', a=dict(at=[45]), b=dict(at=[15]), every=60)])
L['748'] = dict(core=[S('Střítež, Obecní úřad'), S('Řeka, konečná')],
                sim=[two('748', 'Střítež, Obecní úřad', 'Řeka, konečná', a=dict(at=['16:11', '17:11']), b=dict(at=['15:40', '16:30']), every=120)])
L['750'] = dict(core=[S(TAS), S(FAN)], sim=[two('750', TAS, FAN, a=dict(at=['13:50', '14:20']), b=dict(at=['14:50', '15:40']), every=180)])
L['754'] = dict(core=[S(TAS), S(CAS)], sim=[two('754', TAS, CAS, a=dict(at=['13:45', '14:22', '15:30']), b=dict(at=['13:40', '14:20', '15:10']), every=144)])
# ---------------- MHD Český Těšín (875)
# ---------------- MHD Český Těšín (replaces L['721'] and the L['721']['sim'].append(... '721 Mosty' ...) line)
L['721'] = dict(core=[S(CZS)],
                sim=[loop('721', CZS, at=['14:15', '14:51', '15:31'], every=120),
                     dict(name='721 Mosty', every=144, legs=[leg(CZS, 'Mosty, osada Antoníček', at=['13:55', '15:00']),
                                                           leg('Mosty, osada Antoníček', 'Nová Tovární točna', at=['14:19', '15:24']),
                                                           leg('Nová Tovární točna', CZS, untimed=True, lines=['725', '721'])])])
L['722'] = dict(core=[S(CZS)], sim=[loop('722', CZS, at=['13:22', '14:01', '14:25', '14:55', '15:15'], every=180)])
L['723'] = dict(core=[S(CZS), S(CAS), S('Horní Žukov, točna')],
                sim=[two('723', CZS, 'Horní Žukov, točna', a=dict(knot=CAS, at=[37]), b=dict(core_to=CAS, at=[0]), every=60)])
L['724'] = dict(core=[S(CZS), S('centrální hřbitov')], sim=[two('724', CZS, 'centrální hřbitov')])
# ---------------- MHD Třinec (866)
SOS = 'Sosna nemocnice'
L['701'] = dict(core=[S(SOS)], sim=[loop('701', SOS)])
# G3 (MHD Třinec), method check 25 Oct 2026: replacement entries for tfj_spec.py (same helpers and constants: S, leg, two,
# loop, TAS, TZS, SOS). Only the changed lines. 712 Kozinec, 713 and 701 are unchanged and are not repeated here.
L['702'] = dict(core=[S('Kanada, školy'), S(TAS)],
                sim=[two('702', 'Kanada, školy', TAS, a=dict(at=['13:05', '13:25', '13:50', '14:05']), b=dict(at=['13:05', '13:25', '13:35', '14:05']), every=90)])
# 703 is a works line (Konská, PZ): its trips are the shift changes 5:15 / 13:20 / 21:25, so every 480 (Step 8, as 709)
L['703'] = dict(core=[S('Konská, PZ konečná'), S(TAS)],
                sim=[two('703', TAS, 'Konská, PZ konečná', a=dict(at=['13:18', '13:30']), b=dict(at=['14:03', '14:08']), every=480)])
L['704'] = dict(core=[S('Podlesí konečná'), S(TAS)],
                sim=[two('704', TAS, 'Podlesí konečná', a=dict(at=['13:35', '14:45']), b=dict(at=['13:52', '15:00']), every=120)])
L['706'] = dict(core=[S(TAS), S('Kojkovice, konečná'), S('Osůvky, konečná')],
                sim=[two('706', TAS, 'Kojkovice, konečná', a=dict(at=['13:40', '14:35'], notvia=['Osůvky, konečná', 'Borek, konečná']), b=dict(at=['13:05', '13:55'], notvia=['Osůvky, konečná', 'Borek, konečná']), every=120),
                     two('706 Osůvky', TAS, 'Osůvky, konečná', a=dict(at=['13:35', '14:30'], notvia=['Kojkovice, konečná']), b=dict(at=['13:05', '14:01'], notvia=['Kojkovice, konečná']), every=120)])
L['707'] = dict(core=[S(TAS)], sim=[loop('707', TAS, stops_via=[S('Třinec, základní škola')], via=['Horní Líštná, Valovka'], at=[35], every=60)])
L['708'] = dict(core=[S('Lyžbice, Kamionka'), S(TAS)], anchor='15:40',
                sim=[two('708', TAS, 'Lyžbice, Kamionka', a=dict(at=[15]), b=dict(at=[9]), every=30)])
L['709'] = dict(core=[S(TAS), S('Konská, válcovna C')], sim=[two('709', TAS, 'Konská, válcovna C', every=480)])
L['712'] = dict(core=[S(TZS), S('Tyra, pila'), S('Tyra, hájenka')],
                sim=[two('712', TZS, 'Tyra, hájenka', a=dict(core_to='Tyra, pila', at=['14:22', '15:40']), b=dict(knot='Tyra, pila', knot_at=['15:02', '15:46']), every=120),
                     two('712 Kozinec', TAS, 'Oldřichovice, pod Kozincem')])
L['768'] = dict(core=[S(TAS), S('Vendryně, vápenka')], sim=[two('768', TAS, 'Vendryně, vápenka')])
L['713'] = dict(core=[S(TAS), S('Guty, konečná')], sim=[two('713', TAS, 'Guty, konečná')])
L['714'] = dict(core=[S(TAS), S('Oldřichovice, ves')],
                sim=[two('714', TAS, 'Oldřichovice, ves', a=dict(at=['13:37', '14:30']), b=dict(at=['13:00', '14:03']), every=120)])
L['715'] = dict(core=[S(SOS)], anchor='16:00', sim=[loop('715', SOS, at=[10, 50], every=60)])
L['716'] = dict(core=[S(TAS), S('Guty, konečná')],
                sim=[two('716', TAS, 'Guty, konečná', a=dict(at=['14:20', '15:35']), b=dict(at=['16:10', '16:55']), every=120)])
# ---------------- MHD Frýdek-Místek (865)
RIV = 'Místek, Riviéra'
# G4 (MHD Frýdek-Místek), method check 25 Oct 2026: replacement entries for tfj_spec.py (only changed lines).
# Uses tfj_spec.py's helpers S, leg, two, loop and constants RIV, FZS, FPOL. Typed real = (value + 61) mod every.
# 301: Marlenka runs :03 :23 :33 :43 (its :23 is the Řepiště loop bus passing), Riviéra :03 :13 :33 :43; every 60, four slots each end.
L['301'] = dict(core=[S(RIV), S('Lískovec, Marlenka')], sim=[two('301', RIV, 'Lískovec, Marlenka', a=dict(at=[3, 13, 33, 43]), b=dict(at=[3, 23, 33, 43]), every=60)])
# 302: anchor 15:30 by hand: the every-30 pattern ends inside the default window (last Riviéra departure 16:57, then 18:36).
L['302'] = dict(core=[S('Frýdecká skládka'), S(RIV), S('Místek, Tesco')], anchor='15:30',
                sim=[two('302', 'Frýdecká skládka', RIV, a=dict(at=[12]), b=dict(at=[27]), every=30),
                     dict(name='302 Tesco', every=480, legs=[leg(RIV, 'Místek, Tesco', at=['13:41', '14:11', '14:41']), leg('Místek, Tesco', RIV, at=['13:52', '14:22', '14:52'])])])
# 303: anchor 14:30 by hand: both hourly pairs run unchanged all day until 15:27 / 15:52 back; from 16:27 the back trips swap paths.
L['303'] = dict(core=[S('Dobrá, VÚHŽ parkoviště'), S('Baška, Obecní úřad'), S('Frýdek, Dobrovského'), S('Hodoňovice, Kamenec')], anchor='14:30',
                sim=[two('303', 'Dobrá, VÚHŽ parkoviště', 'Baška, Obecní úřad', a=dict(at=[35]), b=dict(at=[27]), every=60),
                     two('303 Hodoňovice', 'Frýdek, Dobrovského', 'Hodoňovice, Kamenec', a=dict(at=[59]), b=dict(at=[52]), every=60)])
L['304'] = dict(core=[S(FZS), S('Kozlovice, garáž ČSAD')], sim=[two('304', FZS, 'Kozlovice, garáž ČSAD', b=dict(stops_via=[S('Měrkovice, Jednota')]))])
# 305: every 120, out 16:08 (even hours :08) and 17:12 (odd :12), back :59 every hour.
L['305'] = dict(core=[S(FZS), S('Horní Sklenov, restaurace')], sim=[two('305', FZS, 'Horní Sklenov, restaurace', a=dict(at=['16:08', '17:12']), b=dict(at=['15:59', '16:59']), every=120)])
L['306'] = dict(core=[S('Pavlíkova točna'), S(FAN)], sim=[two('306', 'Pavlíkova točna', FAN, b=dict(stops_via=[S('Frýdek, myslivna')]))])
L['307'] = dict(core=[S('Letná, točna'), S(FPOL)], sim=[two('307', 'Letná, točna', FPOL)])
# 308: every 120 on the odd-hour round (Záhoří 15:57, poliklinika 15:28); 308 Mitrovice every 480 on the real round 13:19 / 14:01.
L['308'] = dict(core=[S('Skalice, Záhoří'), S(FPOL), S('Nová Bělá, Mitrovice')],
                sim=[two('308', 'Skalice, Záhoří', FPOL, a=dict(at=['15:57']), b=dict(at=['15:28']), every=120),
                     two('308 Mitrovice', FPOL, 'Nová Bělá, Mitrovice', a=dict(at=['13:19']), b=dict(at=['14:01']), every=480)])
L['309'] = dict(core=[S(FPOL)], sim=[loop('309', FPOL)])
# 310: every 30 at :00 / :30 (the loop's afternoon peak 14:30-16:00).
L['310'] = dict(core=[S(FPOL)], sim=[loop('310', FPOL, every=30, at=[0])])
# 311: Riviéra :23 / :53, U kříže :03 / :42 (from 14:03); every 60, two slots each end.
L['311'] = dict(core=[S(RIV), S('Řepiště, U kříže')], sim=[two('311', RIV, 'Řepiště, U kříže', a=dict(at=[23, 53]), b=dict(at=[3, 42]), every=60)])
# 312: back read at poliklinika (trips from Brušperk end at Frýdek žst or at poliklinika); every 96, two slots each end.
L['312'] = dict(core=[S(FZS), S(FPOL), S('Brušperk, točna')],
                sim=[two('312', FZS, 'Brušperk, točna', a=dict(at=['14:35', '15:35']), b=dict(at=['14:47', '15:20'], core_to=FPOL), every=96)])
# 313: every 120, žst 13:31 (odd hours), Nošovice 14:10 (even hours).
L['313'] = dict(core=[S('Nošovice, střed'), S(FZS)], sim=[two('313', FZS, 'Nošovice, střed', a=dict(at=['13:31']), b=dict(at=['14:10']), every=120)])
# 314: mixed Frýdek ends (žst, poliklinika, Revoluční) and Janovice ends (konečná, škola): read at Baška, železniční stanice both ways.
# 314's afternoon trips start and end at Revoluční (or run on to the poliklinika), not the station: the town end is Revoluční,
# where its two Frýdek paths meet (25 Oct 2026 branch check: three of the four slots were Revoluční trips)
L['314'] = dict(core=[S('Frýdek, Revoluční'), S('Baška, železniční stanice'), S('Janovice, konečná')],
                sim=[two('314', 'Frýdek, Revoluční', 'Janovice, konečná',
                         a=dict(knot='Baška, železniční stanice', knot_at=['14:39', '15:10'], core_to='Janovice, škola', stops_via=[S('Frýdek, Na Veselé')]),
                         b=dict(knot='Baška, železniční stanice', knot_at=['14:36', '15:59'], core_to='Staré Město, střed', stops_via=[S('Janovice, Řezáč')]), every=120)])
# 316: the 315/316 round runs 13:12-16:15 (last out 15:42): its own model hours 14:00-16:00 (sim window); 316 Riviéra unchanged.
L['316'] = dict(core=[S('Palkovice, centrum'), S(FPOL), S('Pavlíkova točna'), S(RIV)],
                sim=[dict(name='316', every=90, window=['14:00', '16:00'], legs=[leg(FPOL, 'Palkovice, centrum', at=['15:42'], lines=['316', '315']), leg('Palkovice, centrum', FPOL, at=['16:15'])]),
                     two('316 Riviéra', 'Pavlíkova točna', RIV, a=dict(at=[21]), b=dict(at=[12]), every=60)])
# 318: every 240 on the two full-route rounds: poliklinika 13:50 / 14:58, back timed so the bus passes Raškovice, hotel Ondráš at 14:10 / 15:10
# (the Ondráš short trips 13:15 / 13:53 are a variant on the line's own stops and stay off the pattern).
L['318'] = dict(core=[S(FPOL), S('Raškovice, hotel Ondráš'), S('hotel Visalaje')],
                sim=[two('318', FPOL, 'hotel Visalaje', a=dict(at=['13:50', '14:58'], core_to='Raškovice, hotel Ondráš'), b=dict(knot='Raškovice, hotel Ondráš', knot_at=['14:10', '15:10']), every=240)])
# ---------------- Frýdecko-Místecko (863)
L['351'] = dict(core=[S(NR), S(FAN), S('Morávka, Lipové')],
                # outstation line (buses sleep at Morávka): timed both ways at the inbound rate, the Bebek trips are 351 Bebek's
                sim=[two('351', NR, 'Morávka, Lipové', a=dict(knot=FAN, knot_at=['16:25'], notvia=['Morávka, Bebek']),
                         b=dict(at=['16:26'], core_to=FZS, notvia=['Morávka, Bebek']), every=120),
                     two('351 Bebek', NR, 'Morávka, Bebek', a=dict(knot=FAN), b=dict(core_to=FAN))])
L['354'] = dict(core=[S(FAN), S(NR)], sim=[two('354', FAN, NR, every=480)])
L['355'] = dict(core=[S(FAN), S('Mošnov, Airport nádraží')], sim=[two('355', FAN, 'Mošnov, Airport nádraží', every=480)])
# 655 is on the Novojičínsko sheet (licence 883655 holds 41 of its 45 trips; 863655 here has 4)
L['357'] = dict(core=[S(FAN), S('Vojkovice, křižovatka k Dobraticím')], sim=[two('357', FAN, 'Vojkovice, křižovatka k Dobraticím')])
L['358'] = dict(core=[S('Místek, Krytý bazén'), S('Nošovice, PZ Hyundai - hlavní brána'), S(RIV), S('Nošovice, PZ Hyundai Steel')],
                # shift line every 480 (Step 8: shift lines repeat every 480): Krytý bazén 5:03 / 13:03 / 21:03, Hyundai 6:25 / 14:25 / 22:25;
                # the Steel trips (Riviéra 12:53, IZS 14:17) are 358 Steel's and are not read into the main row
                sim=[two('358', 'Místek, Krytý bazén', 'Nošovice, PZ Hyundai - hlavní brána', a=dict(at=['13:03'], notvia=['Nošovice, PZ Hyundai Steel']),
                         b=dict(at=['14:25'], notvia=['Nošovice, PZ Hyundai Steel']), every=480),
                     dict(name='358 Steel', every=480, legs=[leg(RIV, 'Nošovice, PZ Hyundai Steel', at=['12:53']), leg('Nošovice, PZ IZS', RIV, at=['14:17'])])])
L['980'] = dict(core=[S(NR), S('Frenštát p.Radh., u škol'), S('Rožnov p.Radh., autobusová stanice')],
                # 25 Oct: the back row is read at Rožnov (all its trips pass Frenštát, u škol 22 min later); the Frenštát starts
                # (13:32, 14:17 Z-Group, 15:42, 17:27) are short trips off the pattern. Out of Ostrava approximate (13:53 slot, real 13:40)
                sim=[two('980', NR, 'Rožnov p.Radh., autobusová stanice', a=dict(core_to='Frenštát p.Radh., u škol', at=[23]),
                         b=dict(at=[5], stops_via=[S('Rožnov p.Radh., Na Kopově')]), every=30)])
RAS = 'Rožnov p.Radh., autobusová stanice'      # 985's short legs leave out the Rožnov trips (they are 985 Rožnov's)
L['985'] = dict(core=[S(NR), S('Frenštát p.Radh., u škol'), S('Rožnov p.Radh., autobusová stanice')],
                # 22 Oct: with Z-Group's 883985 trips the Frenštát short trips are an afternoon shift burst; the live map shows the
                # in-then-out rounds (32-1002: Frenštát 12:47 in, Ostrava 14:33 out; 63-1011: 14:42 in, 16:03 out) and two buses that
                # came in on other trips and go out at 15:03 (33-1015) and 15:33 (63-1005, in on 980 at 14:17): 985 + 985B (out only)
                # 25 Oct: 985 Rožnov every 180 on the real trips (Ostrava 13:53 / 16:53, Rožnov 16:35 / 19:35)
                sim=[two('985', 'Frenštát p.Radh., u škol', NR, a=dict(at=['12:47', '14:42'], notvia=[RAS]), b=dict(at=['14:33', '16:03'], notvia=[RAS]), every=480),
                     oneway('985B', NR, 'Frenštát p.Radh., u škol', every=480, a=dict(at=['15:03', '15:33'], notvia=[RAS])),
                     two('985 Rožnov', NR, 'Rožnov p.Radh., autobusová stanice', a=dict(at=['16:53']), b=dict(at=['16:35']), every=180)])
# ---------------- Frýdlantsko (864), added 21 Oct 2026
FZ, FZA = 'Frýdlant n.Ost., železniční stanice', 'Frýdlant n.Ost., zahradnictví'
L['340'] = dict(core=[S(FZ), S('Frýdek, Revoluční'), S(NR)],
                sim=[dict(name='340', every=480, legs=[leg(FZ, NR, at=['12:06']), leg(NR, FZ, at=['14:12'], core_to='Frýdek, Revoluční', stops_via=[S('Kunčice, nádraží Kunčice')])])])
L['341'] = dict(core=[S(FZ), S('Janovice, konečná')],
                sim=[dict(name='341', every=120, legs=[leg(FZ, 'Janovice, konečná', at=['14:19']), leg('Janovice, konečná', FZ, at=['15:00'])])])
L['342'] = dict(core=[S(FZ), S('Kozlovice, střed')], sim=[two('342', FZ, 'Kozlovice, střed')])
L['343'] = dict(core=[S(FZ), S('Čeladná, restaurace Kněhyně'), S('Čeladná, Podolánky, Plucnarka')], anchor='14:00',
                # model hour by hand: after 16:06 only the 16:50 outstation run (the bus stays in Čeladná for the žst shorts)
                sim=[two('343', FZ, 'Čeladná, restaurace Kněhyně', a=dict(at=['14:10'], notvia=['Čeladná, Podolánky, Plucnarka']),
                         b=dict(at=['14:35'], notvia=['Čeladná, Podolánky, Plucnarka']), every=80),
                     dict(name='343 Podolánky', every=480, legs=[leg(FZ, 'Čeladná, Podolánky, Plucnarka', at=['15:00']), leg('Čeladná, Podolánky, Plucnarka', FZ, at=['15:35'])])])
L['344'] = dict(core=[S(FZ), S('Raškovice, hotel Ondráš')],
                # the Hyundai shift trips (12:35 out, 14:25 back via Ondráš 14:50) are not the line's pattern
                sim=[two('344', FZ, 'Raškovice, hotel Ondráš', a=dict(at=['14:30', '15:10'], notvia=['Nošovice, PZ Hyundai - hlavní brána']),
                         b=dict(at=['13:20', '14:10'], notvia=['Nošovice, PZ Hyundai - hlavní brána']), every=120)])
L['345'] = dict(core=[S(FZ), S('Malenovice, parkoviště'), S('Malenovice, Hutě')], anchor='16:00',
                # model hour by hand: line_anchor moved to 14:00 only for the 14:05 zahradnictví – station hop and the Hutě trips
                sim=[two('345', FZ, 'Malenovice, parkoviště', a=dict(at=[55], notvia=['Malenovice, Hutě']), b=dict(at=[25], notvia=['Malenovice, Hutě']), every=60),
                     dict(name='345 Hutě', every=480, legs=[leg(FZ, 'Malenovice, Hutě', at=['15:00']), leg('Malenovice, Hutě', FZ, at=['15:22'])])])
L['346'] = dict(core=[S(FZ)], sim=[loop('346', FZ, at=['13:54', '14:22'], every=90)])
L['347'] = dict(core=[S(FZ), S('Palkovice, transformátor'), S('Palkovice, Tomis parkoviště')],
                sim=[two('347', FZ, 'Palkovice, transformátor', a=dict(at=['14:25', '15:30']), b=dict(knot='Palkovice, Tomis parkoviště', at=['14:57', '15:57']), every=120)])
L['348'] = dict(core=[S(FZ), S('Ostravice, autobusová stanice'), S('Bílá, zámeček')],
                sim=[two('348', FZ, 'Bílá, zámeček', a=dict(at=['13:53', '14:53']), b=dict(at=['14:31', '15:16']), every=120)])
L['349'] = dict(core=[S('Bílá, zámeček'), S('Bílá, Konečná, st.hr.')], sim=[two('349', 'Bílá, zámeček', 'Bílá, Konečná, st.hr.')])
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tfj_notes.py'), encoding='utf-8').read())   # NOTES
for k_, n_ in NOTES.items(): L[k_]['note'] = n_
missing = sorted(set(L) - set(NOTES), key=int)
if missing: print('no note:', missing)
for k_ in missing: L[k_].setdefault('note', '')
c['lines'] = L
modelled = set(L)
c['unmodelled'] = {x: c.get('unmodelled', {}).get(x, '(pending)') for x in load('line_class.json') if x not in modelled and x not in {l for v in c['other_sheets'].values() for l in v.get('lines', [])}}
json.dump(c, open(rel('config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(L), 'lines;', len(c['unmodelled']), 'unmodelled; reason still missing:', sorted((k for k, v in c['unmodelled'].items() if v == '(pending)'), key=int))
