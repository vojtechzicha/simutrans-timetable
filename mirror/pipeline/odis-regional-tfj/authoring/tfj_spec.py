"""author the first structural spec of the Těšínsko/Třinecko/Frýdecko sheet (intervals and minutes 'auto', checked after)"""
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
FAN, FZS, FPOL = 'Frýdek, autobusové nádraží', 'Frýdek, železniční stanice', 'Místek, poliklinika'
NR = 'Mor.Ostrava, Náměstí Republiky'
# ---------------- Jablunkovsko–Třinecko (861)
L['764'] = dict(core=[S(TAS)], sim=[loop('764', TAS)])
L['766'] = dict(core=[S(TAS)], sim=[loop('766', TAS)])
L['769'] = dict(core=[S(TAS), S('Vendryně, konečná')], sim=[two('769', TAS, 'Vendryně, konečná')])
L['770'] = dict(core=[S(BZS), S('Paseky, konečná')], sim=[two('770', BZS, 'Paseky, konečná')])
L['771'] = dict(core=[S(BZS), S('Nýdek, náměstí'), S('Hluchová, Setinka')], sim=[two('771', BZS, 'Nýdek, náměstí'),
                dict(name='771 Hluchová', every=480, legs=[leg(BZS, 'Hluchová, Setinka', at=['12:25']), leg('Hluchová, Setinka', BZS, at=['12:47'])])])
L['772'] = dict(core=[S(TAS), S('Gora, konečná')], sim=[two('772', TAS, 'Gora, konečná')])
L['773'] = dict(core=[S(BZS), S('Nýdek, náměstí'), S('Nýdek, Střelmá')],
                sim=[dict(name='773', every=480, legs=[leg(BZS, 'Nýdek, Střelmá', knot='Nýdek, náměstí', knot_at=['12:33']), leg('Nýdek, Střelmá', BZS, at=['12:42'])])])
L['781'] = dict(core=[S(NZS), S('Šance, opevnění'), S(JAS), S('Hrčava, konečná')],
                sim=[two('781', NZS, 'Šance, opevnění'), two('781 Hrčava', JAS, 'Hrčava, konečná')])
L['782'] = dict(core=[S(NZS), S('Radvanov, konec'), S(JAS)], sim=[dict(name='782', every=480, legs=[leg(NZS, 'Radvanov, konec', at=['14:55']), leg('Radvanov, konec', JAS, at=['15:05']), leg(JAS, NZS, untimed=True, rt=5)])])
L['783'] = dict(core=[S(TAS), S('Návsí, nadjezd'), S(JAS), S('Bukovec, škola'), S('točna Písečná')],
                sim=[two('783', TAS, 'Bukovec, škola', a=dict(core_to=JAS), b=dict(knot=JAS)),
                     two('783 Písečná', NZS, 'točna Písečná'),
                     dict(name='783 Ski areál', every=480, legs=[leg(TAS, 'Ski areál - Kempaland', at=['14:00']), leg('Ski areál - Kempaland', TAS, untimed=True)])])
L['784'] = dict(core=[S(NZS), S('Horní Lomná, střed'), S('Horní Přelač')],
                sim=[two('784', NZS, 'Horní Přelač', a=dict(core_to='Horní Lomná, střed'), b=dict(knot='Horní Lomná, střed'))])
L['786'] = dict(core=[S(JAS), S('Bystřice, Na Paseky')], sim=[two('786', JAS, 'Bystřice, Na Paseky')])
L['787'] = dict(core=[S('Bystřice, Na Paseky'), S(JAS), S(TAS)],
                sim=[two('787', 'Bystřice, Na Paseky', JAS), two('787 Třinec', TAS, 'Bystřice, Na Paseky')])
L['788'] = dict(core=[S(JAS), S('Lísky, konečná')], sim=[two('788', JAS, 'Lísky, konečná')])
# ---------------- Českotěšínsko (871)
L['731'] = dict(core=[S(CAS), S('Albrechtice, střed')], sim=[two('731', CAS, 'Albrechtice, střed')])
L['739'] = dict(core=[S(CAS), S(FAN)], sim=[two('739', CAS, FAN)])
L['743'] = dict(core=[S('Hnojník, škola polská'), S('Řeka, konečná')], sim=[two('743', 'Hnojník, škola polská', 'Řeka, konečná')])
L['732'] = dict(core=[S(TAS), S(CAS), S('Havířov, Město, železniční stanice')],
                sim=[two('732', TAS, 'Havířov, Město, železniční stanice', a=dict(knot=CAS), b=dict(core_to=CAS))])
L['733'] = dict(core=[S(CAS), S('U Stonávky')], sim=[two('733', CAS, 'U Stonávky')])
L['734'] = dict(core=[S(TAS), S(CAS)], sim=[two('734', TAS, CAS)])
L['735'] = dict(core=[S(CAS), S('Těrlicko, střed')], sim=[two('735', CAS, 'Těrlicko, střed')])
L['736'] = dict(core=[S(CAS), S('Chotěbuz, hájenka')], sim=[two('736', CAS, 'Chotěbuz, hájenka')])
L['738'] = dict(core=[S('Svibice, Slovenská'), S('Karviná, Fryštát, autobusové nádraží')], sim=[two('738', 'Svibice, Slovenská', 'Karviná, Fryštát, autobusové nádraží')])
L['745'] = dict(core=[S('Komorní Lhotka, konečná'), S('Hnojník, obch.stř.'), S('Třanovice, křižovatka')],
                sim=[two('745', 'Komorní Lhotka, konečná', 'Hnojník, obch.stř.'), two('745 Třanovice', 'Komorní Lhotka, konečná', 'Třanovice, křižovatka')])
L['747'] = dict(core=[S(CAS), S('Střítež, Obecní úřad')], sim=[two('747', CAS, 'Střítež, Obecní úřad')])
L['748'] = dict(core=[S('Střítež, Obecní úřad'), S('Řeka, konečná')], sim=[two('748', 'Střítež, Obecní úřad', 'Řeka, konečná')])
L['750'] = dict(core=[S(TAS), S(FAN)], sim=[two('750', TAS, FAN)])
L['754'] = dict(core=[S(TAS), S(CAS)], sim=[two('754', TAS, CAS, a=dict(via=['Ropice']), b=dict(via=['Ropice']))]) if False else \
           dict(core=[S(TAS), S(CAS)], sim=[two('754', TAS, CAS)])
# ---------------- MHD Český Těšín (875)
L['721'] = dict(core=[S(CZS)], sim=[loop('721', CZS, every=40)])
L['722'] = dict(core=[S(CZS)], sim=[loop('722', CZS)])
L['723'] = dict(core=[S(CZS), S(CAS), S('Horní Žukov, točna')],
                sim=[two('723', CZS, 'Horní Žukov, točna', a=dict(knot=CAS), b=dict(core_to=CAS))])
L['721']['sim'].append(dict(name='721 Mosty', every=60, legs=[leg(CZS, 'Mosty, osada Antoníček', at=[55]), leg('Mosty, osada Antoníček', 'Nová Tovární točna', at=[19]), leg('Nová Tovární točna', CZS, untimed=True, lines=['725', '721'])]))
L['724'] = dict(core=[S(CZS), S('centrální hřbitov')], sim=[two('724', CZS, 'centrální hřbitov')])
# ---------------- MHD Třinec (866)
SOS = 'Sosna nemocnice'
L['701'] = dict(core=[S(SOS)], sim=[loop('701', SOS)])
L['702'] = dict(core=[S('Kanada, školy'), S(TAS)], sim=[two('702', 'Kanada, školy', TAS)])
L['703'] = dict(core=[S('Konská, PZ konečná'), S(TAS)], sim=[two('703', TAS, 'Konská, PZ konečná')])
L['704'] = dict(core=[S('Podlesí konečná'), S(TAS)], sim=[two('704', TAS, 'Podlesí konečná')])
L['706'] = dict(core=[S(TAS), S('Kojkovice, konečná'), S('Osůvky, konečná')],
                sim=[two('706', TAS, 'Kojkovice, konečná'), two('706 Osůvky', TAS, 'Osůvky, konečná')])
L['707'] = dict(core=[S(TAS)], sim=[loop('707', TAS, stops_via=[S('Třinec, základní škola')])])
L['708'] = dict(core=[S('Lyžbice, Kamionka'), S(TAS)], sim=[two('708', TAS, 'Lyžbice, Kamionka')])
L['709'] = dict(core=[S(TAS), S('Konská, válcovna C')], sim=[two('709', TAS, 'Konská, válcovna C', every=480)])
L['712'] = dict(core=[S(TZS), S('Tyra, pila'), S('Tyra, hájenka')],
                sim=[two('712', TZS, 'Tyra, hájenka', a=dict(core_to='Tyra, pila'), b=dict(knot='Tyra, pila')), two('712 Kozinec', TAS, 'Oldřichovice, pod Kozincem')])
L['768'] = dict(core=[S(TAS), S('Vendryně, vápenka')], sim=[two('768', TAS, 'Vendryně, vápenka')])
L['713'] = dict(core=[S(TAS), S('Guty, konečná')], sim=[two('713', TAS, 'Guty, konečná')])
L['714'] = dict(core=[S(TAS), S('Oldřichovice, ves')], sim=[two('714', TAS, 'Oldřichovice, ves')])
L['715'] = dict(core=[S(SOS)], sim=[loop('715', SOS)])
L['716'] = dict(core=[S(TAS), S('Guty, konečná')], sim=[two('716', TAS, 'Guty, konečná')])
# ---------------- MHD Frýdek-Místek (865)
RIV = 'Místek, Riviéra'
L['301'] = dict(core=[S(RIV), S('Lískovec, Marlenka')], sim=[two('301', RIV, 'Lískovec, Marlenka', a=dict(at=[3, 13]), b=dict(at=[3, 13]), every=30)])
L['302'] = dict(core=[S('Frýdecká skládka'), S(RIV), S('Místek, Tesco')],
                sim=[two('302', 'Frýdecká skládka', RIV),
                     dict(name='302 Tesco', every=480, legs=[leg(RIV, 'Místek, Tesco', at=['13:41', '14:11', '14:41']), leg('Místek, Tesco', RIV, at=['13:52', '14:22', '14:52'])])])
L['303'] = dict(core=[S('Dobrá, VÚHŽ parkoviště'), S('Baška, Obecní úřad'), S('Frýdek, Dobrovského'), S('Hodoňovice, Kamenec')],
                sim=[two('303', 'Dobrá, VÚHŽ parkoviště', 'Baška, Obecní úřad'), two('303 Hodoňovice', 'Frýdek, Dobrovského', 'Hodoňovice, Kamenec')])
L['304'] = dict(core=[S(FZS), S('Kozlovice, garáž ČSAD')], sim=[two('304', FZS, 'Kozlovice, garáž ČSAD', b=dict(stops_via=[S('Měrkovice, Jednota')]))])
L['305'] = dict(core=[S(FZS), S('Horní Sklenov, restaurace')], sim=[two('305', FZS, 'Horní Sklenov, restaurace')])
L['306'] = dict(core=[S('Pavlíkova točna'), S(FAN)], sim=[two('306', 'Pavlíkova točna', FAN, b=dict(stops_via=[S('Frýdek, myslivna')]))])
L['307'] = dict(core=[S('Letná, točna'), S(FPOL)], sim=[two('307', 'Letná, točna', FPOL)])
L['308'] = dict(core=[S('Skalice, Záhoří'), S(FPOL), S('Nová Bělá, Mitrovice')], sim=[two('308', 'Skalice, Záhoří', FPOL), two('308 Mitrovice', FPOL, 'Nová Bělá, Mitrovice')])
L['309'] = dict(core=[S(FPOL)], sim=[loop('309', FPOL)])
L['310'] = dict(core=[S(FPOL)], sim=[loop('310', FPOL)])
L['311'] = dict(core=[S(RIV), S('Řepiště, U kříže')], sim=[two('311', RIV, 'Řepiště, U kříže')])
L['312'] = dict(core=[S(FZS), S('Brušperk, točna')], sim=[two('312', FZS, 'Brušperk, točna')])
L['313'] = dict(core=[S('Nošovice, střed'), S(FZS)], sim=[two('313', FZS, 'Nošovice, střed')])
L['314'] = dict(core=[S(FZS), S('Janovice, konečná')], sim=[two('314', FZS, 'Janovice, konečná')])
L['316'] = dict(core=[S('Palkovice, centrum'), S(FPOL), S('Pavlíkova točna'), S(RIV)],
                sim=[dict(name='316', every=90, legs=[leg(FPOL, 'Palkovice, centrum', at=['15:42'], lines=['316', '315']), leg('Palkovice, centrum', FPOL, at=['16:15'])]),
                     two('316 Riviéra', 'Pavlíkova točna', RIV, a=dict(at=[21]), b=dict(at=[12]), every=60)])
L['318'] = dict(core=[S(FPOL), S('Raškovice, hotel Ondráš'), S('hotel Visalaje')],
                sim=[two('318', FPOL, 'hotel Visalaje', a=dict(core_to='Raškovice, hotel Ondráš'), b=dict(knot='Raškovice, hotel Ondráš'))])
# ---------------- Frýdecko-Místecko (863)
L['351'] = dict(core=[S(NR), S(FAN), S('Morávka, Lipové')],
                sim=[two('351', NR, 'Morávka, Lipové', a=dict(knot=FAN), b=dict(core_to=FAN))])
L['351']['sim'].append(two('351 Bebek', NR, 'Morávka, Bebek', a=dict(knot=FAN), b=dict(core_to=FAN)))
L['354'] = dict(core=[S(FAN), S(NR)], sim=[two('354', FAN, NR, every=480)])
L['355'] = dict(core=[S(FAN), S('Mošnov, Airport nádraží')], sim=[two('355', FAN, 'Mošnov, Airport nádraží', every=480)])
# 655 is on the Novojičínsko sheet (licence 883655 holds 41 of its 45 trips; 863655 here has 4)
L['357'] = dict(core=[S(FAN), S('Vojkovice, křižovatka k Dobraticím')], sim=[two('357', FAN, 'Vojkovice, křižovatka k Dobraticím')])
L['358'] = dict(core=[S('Místek, Krytý bazén'), S('Nošovice, PZ Hyundai - hlavní brána'), S(RIV), S('Nošovice, PZ Hyundai Steel')],
                sim=[two('358', 'Místek, Krytý bazén', 'Nošovice, PZ Hyundai - hlavní brána'),
                     dict(name='358 Steel', every=480, legs=[leg(RIV, 'Nošovice, PZ Hyundai Steel', at=['12:53']), leg('Nošovice, PZ IZS', RIV, at=['14:17'])])])
L['980'] = dict(core=[S(NR), S('Frenštát p.Radh., u škol'), S('Rožnov p.Radh., autobusová stanice')],
                sim=[two('980', NR, 'Rožnov p.Radh., autobusová stanice', a=dict(core_to='Frenštát p.Radh., u škol'), b=dict(knot='Frenštát p.Radh., u škol', stops_via=[S('Rožnov p.Radh., Na Kopově')]))])
RAS = 'Rožnov p.Radh., autobusová stanice'      # 985's short legs leave out the Rožnov trips (they are 985 Rožnov's)
L['985'] = dict(core=[S(NR), S('Frenštát p.Radh., u škol'), S('Rožnov p.Radh., autobusová stanice')],
                # 22 Oct: with Z-Group's 883985 trips the Frenštát short trips are an afternoon shift burst; the live map shows the
                # in-then-out rounds (32-1002: Frenštát 12:47 in, Ostrava 14:33 out; 63-1011: 14:42 in, 16:03 out) and two buses that
                # came in on other trips and go out at 15:03 (33-1015) and 15:33 (63-1005, in on 980 at 14:17): 985 + 985B (out only)
                sim=[two('985', 'Frenštát p.Radh., u škol', NR, a=dict(at=['12:47', '14:42'], notvia=[RAS]), b=dict(at=['14:33', '16:03'], notvia=[RAS]), every=480),
                     oneway('985B', NR, 'Frenštát p.Radh., u škol', every=480, a=dict(at=['15:03', '15:33'], notvia=[RAS])),
                     two('985 Rožnov', NR, 'Rožnov p.Radh., autobusová stanice')])
# ---------------- Frýdlantsko (864), added 21 Oct 2026
FZ, FZA = 'Frýdlant n.Ost., železniční stanice', 'Frýdlant n.Ost., zahradnictví'
L['340'] = dict(core=[S(FZ), S('Frýdek, Revoluční'), S(NR)],
                sim=[dict(name='340', every=480, legs=[leg(FZ, NR, at=['12:06']), leg(NR, FZ, at=['14:12'], core_to='Frýdek, Revoluční')])])
L['341'] = dict(core=[S(FZ), S('Janovice, konečná')],
                sim=[dict(name='341', every=90, legs=[leg(FZ, 'Janovice, konečná', at=['16:34']), leg('Janovice, konečná', FZ, at=['17:00'])])])
L['342'] = dict(core=[S(FZ), S('Kozlovice, střed')], sim=[two('342', FZ, 'Kozlovice, střed')])
L['343'] = dict(core=[S(FZ), S('Čeladná, restaurace Kněhyně'), S('Čeladná, Podolánky, Plucnarka')],
                sim=[two('343', FZ, 'Čeladná, restaurace Kněhyně'),
                     dict(name='343 Podolánky', every=480, legs=[leg(FZ, 'Čeladná, Podolánky, Plucnarka', at=['15:00']), leg('Čeladná, Podolánky, Plucnarka', FZ, at=['15:35'])])])
L['344'] = dict(core=[S(FZ), S('Raškovice, hotel Ondráš')], sim=[two('344', FZ, 'Raškovice, hotel Ondráš')])
L['345'] = dict(core=[S(FZ), S('Malenovice, parkoviště'), S('Malenovice, Hutě')],
                sim=[two('345', FZ, 'Malenovice, parkoviště', a=dict(at=[55]), b=dict(at=[25]), every=60),
                     dict(name='345 Hutě', every=480, legs=[leg(FZ, 'Malenovice, Hutě', at=['15:00']), leg('Malenovice, Hutě', FZ, at=['15:22'])])])
L['346'] = dict(core=[S(FZ)], sim=[loop('346', FZ)])
L['347'] = dict(core=[S(FZ), S('Palkovice, transformátor'), S('Palkovice, Tomis parkoviště')],
                sim=[two('347', FZ, 'Palkovice, transformátor', a=dict(at=[30]), b=dict(knot='Palkovice, Tomis parkoviště', at=[57]), every=60)])
L['348'] = dict(core=[S(FZ), S('Ostravice, autobusová stanice'), S('Bílá, zámeček')], sim=[two('348', FZ, 'Bílá, zámeček', a=dict(at=[53]), b=dict(at=[16]), every=60)])
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
