"""config.lines of the Novojičínsko/Bílovecko sheet (line specs + notes from nj_notes.py); keeps the unmodelled reasons.
Intervals and minutes 'auto' are fitted by 05_schedule.py and then checked by hand (dump.py / review.py)."""
import os, sys, json
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, AL, rel
T = load('trips.json')
c = json.load(open(rel('config.json'), encoding='utf-8'))
ALL = sorted({AL(nm(s)) for tr in T.values() for t in tr for s in t['stops']})
def S(sub):
    m = [s for s in ALL if s == sub] or [s for s in ALL if s.endswith(sub)] or [s for s in ALL if sub in s]
    if len(m) != 1: raise SystemExit(f'stop {sub!r}: {m[:6]}')
    return m[0]
def leg(fr, to, **kw): return dict(fr=S(fr), to=S(to), **({'at': 'auto'} if not kw.get('untimed') and 'at' not in kw and 'knot_at' not in kw else {}), **{k: (S(v) if k in ('knot', 'core_to') else [S(x) for x in v] if k in ('via', 'notvia', 'stops_via') else v) for k, v in kw.items()})
def two(name, A, B, a=None, b=None, every='auto'):
    return dict(name=name, every=every, legs=[leg(A, B, **(a or {})), leg(B, A, **(b or {}))])
def loop(name, A, every='auto', **kw): return dict(name=name, every=every, legs=[leg(A, A, **kw)])
def oneway(name, A, B, every='auto', a=None):
    return dict(name=name, every=every, legs=[leg(A, B, **(a or {})), leg(B, A, untimed=True)])
NJ = 'Nový Jičín, autobusové nádraží'; KAN = 'Kopřivnice, autobusové nádraží'; FUS = 'Frenštát p.Radh., u škol'
SVN = 'Ostrava, Svinov, nádraží'; SVM = 'Ostrava, Svinov, mosty'; DUB = 'Ostrava, Dubina'; NR = 'Ostrava, Mor.Ostrava, Náměstí Republiky'
BB = 'Bílovec, restaurace Beseda'; BZ = 'Bílovec, železniční stanice'; ODRY = 'Odry, autobusová stanice'
L = {}
# ---------------- Bílovecko (884)
L['286'] = dict(core=[S('Hlubočec, točna'), S(SVN), S('Hradec n.Moravicí, železniční stanice')],
                sim=[two('286', 'Hlubočec, točna', SVN, a=dict(at=['14:43', '15:50']), b=dict(at=['14:59', '15:49']), every=120), two('286 Hradec', SVN, 'Hradec n.Moravicí, železniční stanice', every=240)])
L['287'] = dict(core=[S('Kyjovice, has.zbroj.'), S(SVN)], sim=[two('287', 'Kyjovice, has.zbroj.', SVN, a=dict(at=['16:42']), b=dict(at=['15:37'], notvia=['Pustá Polom, Nový Dvůr']), every=120),
                     oneway('287 Pustá Polom', SVN, 'Pustá Polom, autobusová stanice', every=480, a=dict(at=['16:47']))])
L['288'] = dict(core=[S('Zbyslavice, střed'), S(SVN)], sim=[two('288', 'Zbyslavice, střed', SVN, a=dict(at=['14:00']), b=dict(at=['15:04']), every=120)])
L['628'] = dict(core=[S(BZ), S('Jistebník, železniční stanice'), S(DUB)], sim=[two('628', BZ, DUB, a=dict(at=['13:43']), b=dict(at=['14:44']), every=120)])
L['671'] = dict(core=[S(SVM), S('Bílovec, Výškovice, restaurace'), S('Skřipov, U Kostela')], sim=[two('671', SVM, 'Skřipov, U Kostela', a=dict(core_to='Bílovec, Výškovice, restaurace', at=['16:10']), b=dict(knot='Bílovec, Výškovice, restaurace', knot_at=['16:24']), every=80)])
L['672'] = dict(core=[S('Slatina'), S(SVM)], sim=[two('672', 'Slatina', SVM, a=dict(at=['16:04']), b=dict(at=['14:30']), every=144)])
L['679'] = dict(core=[S('Zbyslavice, střed'), S('Klimkovice, centrum'), S(SVN)], sim=[two('679', 'Zbyslavice, střed', SVN, a=dict(at=['15:45']), b=dict(at=['16:40']), every=180)])
L['692'] = dict(core=[S(BZ)], sim=[loop('692', BZ, every=180, at=['15:44', '17:19'])])
L['693'] = dict(core=[S(BZ)], sim=[loop('693', BZ, every=120, at=['13:44', '14:49'])])
L['613'] = dict(core=[S('Fulnek, náměstí'), S('Studénka, železniční stanice')], sim=[two('613', 'Fulnek, náměstí', 'Studénka, železniční stanice', a=dict(at=['15:58']), b=dict(at=['16:11']), every=96)])
L['626'] = dict(core=[S(NJ), S(BB)], sim=[two('626', NJ, BB)])
L['629'] = dict(core=[S(NJ), S(BB)], sim=[two('629', BB, NJ, a=dict(at=['13:38']), b=dict(at=['15:35']), every=180)])
L['673'] = dict(core=[S(SVN), S('Březová, škola')], sim=[two('673', SVN, 'Březová, škola', a=dict(at=['14:37']), b=dict(at=['16:07']), every=180)])
L['691'] = dict(core=[S(BB), S('Odry, Veselí, horní konec')], sim=[two('691', BB, 'Odry, Veselí, horní konec')])
# ---------------- Novojičínsko Západ (882)
L['614'] = dict(core=[S(ODRY), S(NJ)], sim=[two('614', ODRY, NJ, a=dict(at=['14:50']), b=dict(at=['13:30']), every=120)])
L['615'] = dict(core=[S('Luboměř, Heltinov'), S(ODRY), S(NJ)], sim=[two('615', NJ, 'Luboměř, Heltinov', a=dict(at=['14:05']), b=dict(at=['13:58']), every=80)])
L['616'] = dict(core=[S(NJ), S('Jeseník n.Odrou, Blahutovice, restaurace')], sim=[two('616', NJ, 'Jeseník n.Odrou, Blahutovice, restaurace')])
L['618'] = dict(core=[S('Fulnek, železniční stanice'), S(NJ)], sim=[two('618', 'Fulnek, železniční stanice', NJ, a=dict(at=['14:10', '14:45', '15:25']), b=dict(at=['14:00', '14:35', '15:12']), every=120)])
L['620'] = dict(core=[S(NJ), S(ODRY), S('Odry, Pohoř, dolní konec')], sim=[two('620', NJ, ODRY, a=dict(notvia=['Odry, Pohoř, dolní konec'], at=['13:40', '15:10']), b=dict(notvia=['Odry, Pohoř, dolní konec'], at=['13:58', '14:33']), every=120),
                     two('620 Pohoř', NJ, 'Odry, Pohoř, dolní konec', a=dict(at=['15:15']), b=dict(at=['13:20']), every=180)])
L['621'] = dict(core=[S(NJ), S('Frýdek-Místek, Frýdek, autobusové nádraží'), S(NR)],
                sim=[two('621', NJ, 'Frýdek-Místek, Frýdek, autobusové nádraží', a=dict(at=['15:17', '15:47']), b=dict(at=['14:06', '14:36']), every=160),
                     two('621 Ostrava', NJ, NR, a=dict(at=['14:42']), b=dict(at=['15:18']), every=120)])
L['622'] = dict(core=[S('Mořkov, železniční stanice'), S(NJ)], sim=[two('622', NJ, 'Mořkov, železniční stanice', a=dict(at=['14:32', '15:20']), b=dict(at=['14:55', '16:07']), every=120)])
L['623'] = dict(core=[S(NJ), S('Studénka, Dělnický dům')], sim=[two('623', NJ, 'Studénka, Dělnický dům')])
L['625'] = dict(core=[S(NJ), S(BB), S('Tísek, obecní úřad')], sim=[two('625', NJ, BB, a=dict(at=['16:37']), b=dict(at=['17:16']), every=120),
                     two('625 Tísek', NJ, 'Tísek, obecní úřad', a=dict(stops_via=['Tísek, u kostela'], at=['15:32']), b=dict(at=['14:24']), every=240)])
L['619'] = dict(core=[S('Fulnek, železniční stanice'), S('Jeseník n.Odrou, Blahutovice, restaurace')],
                sim=[two('619', 'Fulnek, železniční stanice', 'Jeseník n.Odrou, Blahutovice, restaurace', a=dict(stops_via=['Hrabětice, točna'], at=['17:48']), b=dict(at=['15:45']), every=180)])
L['927'] = dict(core=[S(NJ), S('Hranice, autobusová stanice')], sim=[two('927', NJ, 'Hranice, autobusová stanice', a=dict(stops_via=['Hranice, Tř.1.máje'], at=['16:01']), b=dict(at=['17:00']), every=180)])
L['929'] = dict(core=[S(ODRY), S('Hranice, CTP zadní brána')], sim=[two('929', ODRY, 'Hranice, CTP zadní brána', a=dict(at=['13:12']), b=dict(at=['14:12']), every=480)])
L['665'] = dict(core=[S('Mořkov, železniční stanice'), S(NJ)], sim=[two('665', NJ, 'Mořkov, železniční stanice', a=dict(at=['16:17']), b=dict(at=['15:52']), every=120)])
L['667'] = dict(core=[S(NJ), S('Starý Jičín, Heřmanice, točna')], sim=[two('667', NJ, 'Starý Jičín, Heřmanice, točna', a=dict(at=['15:35']), b=dict(at=['16:06']), every=120)])
L['677'] = dict(core=[S(NJ), S('Studénka, železniční stanice'), S(SVN)], sim=[two('677', NJ, SVN, a=dict(at=['16:06']), b=dict(at=['15:35']), every=120)])
L['689'] = dict(core=[S('Bernartice n.Odrou, točna'), S(NJ)], sim=[two('689', NJ, 'Bernartice n.Odrou, točna', a=dict(at=['15:45']), b=dict(at=['16:10']), every=120)])
L['696'] = dict(core=[S(NJ), S(FUS)], sim=[two('696', NJ, FUS, a=dict(at=['14:38', '15:10', '15:30', '16:03']), b=dict(at=['14:20', '14:45', '15:20', '15:57']), every=120)])
L['697'] = dict(core=[S(NJ), S(KAN)], sim=[two('697', NJ, KAN, a=dict(at=['15:13']), b=dict(at=['14:38']), every=96)])
L['908'] = dict(core=[S(NJ), S('Hustopeče n.Bečvou, železniční stanice')], sim=[two('908', NJ, 'Hustopeče n.Bečvou, železniční stanice')])
L['987'] = dict(core=[S(NJ), S('Valašské Meziříčí, autobusová stanice')], sim=[two('987', NJ, 'Valašské Meziříčí, autobusová stanice', a=dict(at=['13:55', '15:20']), b=dict(at=['13:30', '15:05']), every=180)])
L['988'] = dict(core=[S(NJ), S('Valašské Meziříčí, autobusová stanice')], sim=[two('988', NJ, 'Valašské Meziříčí, autobusová stanice', a=dict(lines=['988'], at=['16:40']), b=dict(lines=['988'], at=['16:15']), every=120)])
# ---------------- Novojičínsko Východ (883)
L['379'] = dict(core=[S('Petřvald, náměstí'), S('Ostrava, Zábřeh, Kotva')], sim=[two('379', 'Petřvald, náměstí', 'Ostrava, Zábřeh, Kotva', a=dict(at=['15:38']), b=dict(at=['14:57']), every=180)])
L['632'] = dict(core=[S(KAN), S('Mošnov, Airport nádraží')], sim=[two('632', KAN, 'Mošnov, Airport nádraží', a=dict(at=['12:58'], via=['Contera Park']), b=dict(at=['14:08'], via=['Contera Park']), every=480)])
L['643'] = dict(core=[S(KAN), S('Bartošovice, rozcestí k pískovně')], sim=[dict(name='643', every=480, legs=[leg(KAN, 'Bartošovice, rozcestí k pískovně', at=['14:40']), leg('Bartošovice, rozcestí k pískovně', 'Bartošovice, obecní úřad', at=['15:46']),
                                                 leg('Bartošovice, obecní úřad', KAN, at=['16:04'])])])
L['670'] = dict(core=[S(NJ), S(DUB)], sim=[two('670', NJ, DUB, a=dict(at=['15:55', '17:05']), b=dict(at=['16:20', '17:20']), every=120)])
L['370'] = dict(core=[S(DUB), S('Řepiště, u kříže')], sim=[two('370', DUB, 'Řepiště, u kříže', a=dict(at=['16:19']), b=dict(at=['16:02']), every=90)])
L['371'] = dict(core=[S(DUB), S('Hukvaldy, hotel'), S('Kozlovice, střed')],
                sim=[two('371', DUB, 'Kozlovice, střed', a=dict(core_to='Hukvaldy, hotel', at=['16:58']), b=dict(knot='Hukvaldy, hotel', knot_at=['16:23']), every=120)])
L['373'] = dict(core=[S(KAN), S(DUB)], sim=[two('373', DUB, KAN, a=dict(at=['14:20', '15:20']), b=dict(at=['14:38', '15:43']), every=120)])
L['374'] = dict(core=[S(SVM), S('Trnávka, požární zbrojnice')], sim=[two('374', SVM, 'Trnávka, požární zbrojnice', a=dict(at=['14:21', '15:25']), b=dict(at=['14:35', '15:32']), every=120)])
L['376'] = dict(core=[S(DUB), S('Hukvaldy, Rychaltice, pod mostem')], sim=[two('376', DUB, 'Hukvaldy, Rychaltice, pod mostem', a=dict(at=['16:10', '17:05']), b=dict(at=['16:03', '17:03']), every=120)])
L['634'] = dict(core=[S(KAN), S(FUS)], sim=[two('634', KAN, FUS, a=dict(lines=['634'], at=['15:38']), b=dict(lines=['634'], at=['14:28']), every=90)])
L['635'] = dict(core=[S(KAN), S(FUS)], sim=[two('635', KAN, FUS, a=dict(lines=['635'], at=['14:18', '15:28']), b=dict(lines=['635'], at=['14:25', '15:55']), every=120)])
L['638'] = dict(core=[S(KAN), S('Hukvaldy, Dolní Sklenov, rozcestí')], sim=[two('638', KAN, 'Hukvaldy, Dolní Sklenov, rozcestí', a=dict(at=['15:14']), b=dict(at=['15:51']), every=180)])
L['641'] = dict(core=[S(KAN), S(DUB)], sim=[two('641', KAN, DUB, a=dict(at=[25]), b=dict(at=[0]), every=60)])
L['644'] = dict(core=[S(KAN), S('Štramberk, Libotín, koupaliště')], sim=[two('644', KAN, 'Štramberk, Libotín, koupaliště', a=dict(at=['15:45']), b=dict(at=['16:12']), every=180)])
L['646'] = dict(core=[S(KAN), S(NJ)], sim=[two('646', NJ, KAN, a=dict(lines=['646'], at=['14:00', '14:30']), b=dict(lines=['646'], at=['14:10', '14:40']), every=90)])
L['653'] = dict(core=[S(KAN), S('Kopřivnice, železniční stanice'), S(FUS)],
                sim=[dict(name='653', every=120, legs=[leg(KAN, 'Frenštát p.Radh., železniční stanice', core_to=FUS, stops_via=['Frenštát p.Radh., Continental'], at=['15:15']),
                                                leg('Frenštát p.Radh., železniční stanice', FUS, untimed=True, rt=3), leg(FUS, KAN, at=['15:55'])]),
                     loop('653 Kopřivnice', 'Kopřivnice, železniční stanice', every=30)])
L['655'] = dict(core=[S(FUS), S('Trojanovice, restaurace Ráztoka')], sim=[two('655', FUS, 'Trojanovice, restaurace Ráztoka', a=dict(at=['16:05', '16:55', '17:18']), b=dict(at=['15:40', '16:20', '17:10']), every=120)])
L['656'] = dict(core=[S(FUS), S('Trojanovice, Bystré, Maralův kopec')], sim=[two('656', FUS, 'Trojanovice, Bystré, Maralův kopec', a=dict(at=['13:15', '13:55', '14:49']), b=dict(stops_via=['Trojanovice, pod Dílem'], at=['13:33', '14:11', '15:05']), every=180)])
L['657'] = dict(core=[S(FUS), S('Frýdlant n.Ost., zahradnictví')], sim=[two('657', FUS, 'Frýdlant n.Ost., zahradnictví'), two('657 Kunčice', FUS, 'Kunčice p.Ondřejníkem, železniční stanice', a=dict(lines=['657', '651'], at=['14:00']), b=dict(lines=['657', '651'], stops_via=['Frenštát p.Radh., Žuchov', 'Kunčice p.Ondřejníkem, Rákovec'], at=['13:06']), every=120)])
L['661'] = dict(core=[S(FUS)], sim=[loop('661', FUS, every=480, at=['13:00', '14:20'])])
L['659'] = dict(core=[S(FUS), S('Trojanovice, točna')], sim=[two('659', FUS, 'Trojanovice, točna', a=dict(at=['13:23', '14:38']), b=dict(at=['13:36', '14:51']), every=120)])
L['660'] = dict(core=[S(FUS), S('Trojanovice, u Hutyrů')], sim=[two('660', FUS, 'Trojanovice, u Hutyrů')])
L['662'] = dict(core=[S(KAN), S('Frýdek-Místek, Frýdek, autobusové nádraží')], sim=[two('662', KAN, 'Frýdek-Místek, Frýdek, autobusové nádraží')])
L['690'] = dict(core=[S(NJ), S(KAN), S('Kopřivnice, Tymphany')], sim=[two('690', NJ, 'Kopřivnice, Tymphany', a=dict(core_to=KAN, at=['15:54']), b=dict(knot=KAN, knot_at=['16:50']), every=96)])
L['698'] = dict(core=[S(NJ), S(KAN)], sim=[two('698', NJ, KAN, a=dict(at=['13:10', '13:30', '14:20', '14:45']), b=dict(at=['13:15', '13:35', '14:15', '14:35']), every=120)])
L['699'] = dict(core=[S(NJ), S(KAN)], sim=[two('699', NJ, KAN, a=dict(lines=['699'], at=['16:25']), b=dict(lines=['699'], at=['16:55']), every=120)])
# ---------------- MHD Nový Jičín (886) and Studénka (887)
# the town lines are one observed circuit: each of ARRIVA's three buses runs 602 (:10), 601 (:50), 604 (:10) and 603 (:10 to
# Tesco, :46 back) in turn, so three buses leave the bus station at :10 every hour (live map, 20 Oct)
L['601'] = dict(core=[S(NJ), S('Šenov u N.Jičína, Tesco')],
                sim=[dict(name='601–604', every=60, legs=[leg(NJ, 'Nový Jičín, Riegrova', at=[10], lines=['602'], lay=1), leg('Nový Jičín, Riegrova', NJ, untimed=True, lines=['602']),
                                                         leg(NJ, NJ, at=[50], lines=['601'], lay=1), leg(NJ, NJ, at=[10], lines=['604']),
                                                         leg(NJ, 'Šenov u N.Jičína, Tesco', at=[10], lines=['603']), leg('Šenov u N.Jičína, Tesco', NJ, at=[46], rt=23, lines=['603'])])])
L['611'] = dict(core=[S('Studénka, Butovice, STS'), S('bílovecké nást.')], sim=[two('611', 'Studénka, Butovice, STS', 'bílovecké nást.', a=dict(at=[35]), b=dict(at=[13]), every=60)])

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nj_notes.py'), encoding='utf-8').read())   # NOTES
for k_, n_ in NOTES.items():
    if k_ in L: L[k_]['note'] = n_
missing = sorted(set(L) - set(NOTES), key=int)
if missing: print('no note:', missing)
c['lines'] = L
on_other = {x for sh in c['other_sheets'].values() for x in sh.get('lines', [])}
c['unmodelled'] = {x: c.get('unmodelled', {}).get(x, '(pending)') for x in load('line_class.json') if x not in L and x not in on_other}
json.dump(c, open(rel('config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(L), 'lines;', len(c['unmodelled']), 'unmodelled; reason still missing:', sorted((k for k, v in c['unmodelled'].items() if v == '(pending)'), key=int))
