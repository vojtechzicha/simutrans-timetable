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
                sim=[two('286', 'Hlubočec, točna', SVN), two('286 Hradec', SVN, 'Hradec n.Moravicí, železniční stanice', every=240)])
L['287'] = dict(core=[S('Kyjovice, has.zbroj.'), S(SVN)], sim=[two('287', 'Kyjovice, has.zbroj.', SVN),
                     oneway('287 Pustá Polom', SVN, 'Pustá Polom, autobusová stanice', every=480, a=dict(at=['16:47']))])
L['288'] = dict(core=[S('Zbyslavice, střed'), S(SVN)], sim=[two('288', 'Zbyslavice, střed', SVN, a=dict(at=['14:00']), b=dict(at=['15:04']), every=120)])
L['628'] = dict(core=[S(BZ), S('Jistebník, železniční stanice'), S(DUB)], sim=[two('628', BZ, DUB)])
L['671'] = dict(core=[S(SVM), S('Bílovec, Výškovice, restaurace'), S('Skřipov, U Kostela')], sim=[two('671', SVM, 'Skřipov, U Kostela', a=dict(core_to='Bílovec, Výškovice, restaurace'), b=dict(knot='Bílovec, Výškovice, restaurace'))])
L['672'] = dict(core=[S('Slatina'), S(SVM)], sim=[two('672', 'Slatina', SVM)])
L['679'] = dict(core=[S('Zbyslavice, střed'), S('Klimkovice, centrum'), S(SVN)], sim=[two('679', 'Zbyslavice, střed', SVN)])
L['692'] = dict(core=[S(BZ)], sim=[loop('692', BZ)])
L['693'] = dict(core=[S(BZ)], sim=[loop('693', BZ)])
L['613'] = dict(core=[S('Fulnek, náměstí'), S('Studénka, železniční stanice')], sim=[two('613', 'Fulnek, náměstí', 'Studénka, železniční stanice')])
L['626'] = dict(core=[S(NJ), S(BB)], sim=[two('626', NJ, BB)])
L['629'] = dict(core=[S(NJ), S(BB)], sim=[two('629', BB, NJ, a=dict(at=['13:38']), b=dict(at=['15:35']), every=180)])
L['673'] = dict(core=[S(SVN), S('Březová, škola')], sim=[two('673', SVN, 'Březová, škola', a=dict(at=['14:37']), b=dict(at=['16:07']), every=180)])
L['691'] = dict(core=[S(BB), S('Odry, Veselí, horní konec')], sim=[two('691', BB, 'Odry, Veselí, horní konec')])
# ---------------- Novojičínsko Západ (882)
L['614'] = dict(core=[S(ODRY), S(NJ)], sim=[two('614', ODRY, NJ)])
L['615'] = dict(core=[S('Luboměř, Heltinov'), S(ODRY), S(NJ)], sim=[two('615', NJ, 'Luboměř, Heltinov')])
L['616'] = dict(core=[S(NJ), S('Jeseník n.Odrou, Blahutovice, restaurace')], sim=[two('616', NJ, 'Jeseník n.Odrou, Blahutovice, restaurace')])
L['618'] = dict(core=[S('Fulnek, železniční stanice'), S(NJ)], sim=[two('618', 'Fulnek, železniční stanice', NJ)])
L['620'] = dict(core=[S(NJ), S(ODRY), S('Odry, Pohoř, dolní konec')], sim=[two('620', NJ, ODRY), two('620 Pohoř', NJ, 'Odry, Pohoř, dolní konec', a=dict(at=['15:15']), b=dict(at=['16:08']), every=120)])
L['621'] = dict(core=[S(NJ), S('Frýdek-Místek, Frýdek, autobusové nádraží'), S(NR)],
                sim=[two('621', NJ, 'Frýdek-Místek, Frýdek, autobusové nádraží'), two('621 Ostrava', NJ, NR)])
L['622'] = dict(core=[S('Mořkov, železniční stanice'), S(NJ)], sim=[two('622', NJ, 'Mořkov, železniční stanice')])
L['623'] = dict(core=[S(NJ), S('Studénka, Dělnický dům')], sim=[two('623', NJ, 'Studénka, Dělnický dům')])
L['625'] = dict(core=[S(NJ), S(BB), S('Tísek, obecní úřad')], sim=[two('625', NJ, BB), two('625 Tísek', NJ, 'Tísek, obecní úřad', a=dict(stops_via=['Tísek, u kostela']))])
L['619'] = dict(core=[S('Fulnek, železniční stanice'), S('Jeseník n.Odrou, Blahutovice, restaurace')],
                sim=[two('619', 'Fulnek, železniční stanice', 'Jeseník n.Odrou, Blahutovice, restaurace', a=dict(stops_via=['Hrabětice, točna']))])
L['927'] = dict(core=[S(NJ), S('Hranice, autobusová stanice')], sim=[two('927', NJ, 'Hranice, autobusová stanice', a=dict(stops_via=['Hranice, Tř.1.máje']))])
L['929'] = dict(core=[S(ODRY), S('Hranice, CTP zadní brána')], sim=[two('929', ODRY, 'Hranice, CTP zadní brána', a=dict(at=['13:12']), b=dict(at=['14:12']), every=480)])
L['665'] = dict(core=[S('Mořkov, železniční stanice'), S(NJ)], sim=[two('665', NJ, 'Mořkov, železniční stanice')])
L['667'] = dict(core=[S(NJ), S('Starý Jičín, Heřmanice, točna')], sim=[two('667', NJ, 'Starý Jičín, Heřmanice, točna')])
L['677'] = dict(core=[S(NJ), S('Studénka, železniční stanice'), S(SVN)], sim=[two('677', NJ, SVN)])
L['689'] = dict(core=[S('Bernartice n.Odrou, točna'), S(NJ)], sim=[two('689', NJ, 'Bernartice n.Odrou, točna', a=dict(at=[45]), b=dict(at=[10]), every=60)])
L['696'] = dict(core=[S(NJ), S(FUS)], sim=[two('696', NJ, FUS)])
L['697'] = dict(core=[S(NJ), S(KAN)], sim=[two('697', NJ, KAN)])
L['908'] = dict(core=[S(NJ), S('Hustopeče n.Bečvou, železniční stanice')], sim=[two('908', NJ, 'Hustopeče n.Bečvou, železniční stanice')])
L['987'] = dict(core=[S(NJ), S('Valašské Meziříčí, autobusová stanice')], sim=[two('987', NJ, 'Valašské Meziříčí, autobusová stanice')])
L['988'] = dict(core=[S(NJ), S('Valašské Meziříčí, autobusová stanice')], sim=[two('988', NJ, 'Valašské Meziříčí, autobusová stanice', a=dict(lines=['988']), b=dict(lines=['988']))])
# ---------------- Novojičínsko Východ (883)
L['379'] = dict(core=[S('Petřvald, náměstí'), S('Ostrava, Zábřeh, Kotva')], sim=[two('379', 'Petřvald, náměstí', 'Ostrava, Zábřeh, Kotva')])
L['632'] = dict(core=[S(KAN), S('Mošnov, Airport nádraží')], sim=[two('632', KAN, 'Mošnov, Airport nádraží', a=dict(at=['12:58'], via=['Contera Park']), b=dict(at=['14:08'], via=['Contera Park']), every=480)])
L['643'] = dict(core=[S(KAN), S('Bartošovice, rozcestí k pískovně')], sim=[dict(name='643', every=480, legs=[leg(KAN, 'Bartošovice, rozcestí k pískovně', at=['14:40']), leg('Bartošovice, rozcestí k pískovně', 'Bartošovice, obecní úřad', at=['15:46']),
                                                 leg('Bartošovice, obecní úřad', KAN, at=['16:04'])])])
L['670'] = dict(core=[S(NJ), S(DUB)], sim=[two('670', NJ, DUB)])
L['370'] = dict(core=[S(DUB), S('Řepiště, u kříže')], sim=[two('370', DUB, 'Řepiště, u kříže')])
L['371'] = dict(core=[S(DUB), S('Hukvaldy, hotel'), S('Kozlovice, střed')],
                sim=[two('371', DUB, 'Kozlovice, střed', a=dict(core_to='Hukvaldy, hotel'), b=dict(knot='Hukvaldy, hotel'))])
L['373'] = dict(core=[S(KAN), S(DUB)], sim=[two('373', DUB, KAN)])
L['374'] = dict(core=[S(SVM), S('Trnávka, požární zbrojnice')], sim=[two('374', SVM, 'Trnávka, požární zbrojnice')])
L['376'] = dict(core=[S(DUB), S('Hukvaldy, Rychaltice, pod mostem')], sim=[two('376', DUB, 'Hukvaldy, Rychaltice, pod mostem')])
L['634'] = dict(core=[S(KAN), S(FUS)], sim=[two('634', KAN, FUS, a=dict(lines=['634']), b=dict(lines=['634']))])
L['635'] = dict(core=[S(KAN), S(FUS)], sim=[two('635', KAN, FUS, a=dict(lines=['635']), b=dict(lines=['635']))])
L['638'] = dict(core=[S(KAN), S('Hukvaldy, Dolní Sklenov, rozcestí')], sim=[two('638', KAN, 'Hukvaldy, Dolní Sklenov, rozcestí')])
L['641'] = dict(core=[S(KAN), S(DUB)], sim=[two('641', KAN, DUB)])
L['644'] = dict(core=[S(KAN), S('Štramberk, Libotín, koupaliště')], sim=[two('644', KAN, 'Štramberk, Libotín, koupaliště')])
L['646'] = dict(core=[S(KAN), S(NJ)], sim=[two('646', NJ, KAN, a=dict(lines=['646']), b=dict(lines=['646']))])
L['653'] = dict(core=[S(KAN), S('Kopřivnice, železniční stanice'), S(FUS)],
                sim=[dict(name='653', every='auto', legs=[leg(KAN, 'Frenštát p.Radh., železniční stanice', core_to=FUS, stops_via=['Frenštát p.Radh., Continental']),
                                                leg('Frenštát p.Radh., železniční stanice', FUS, untimed=True, rt=3), leg(FUS, KAN)]),
                     loop('653 Kopřivnice', 'Kopřivnice, železniční stanice', every=30)])
L['655'] = dict(core=[S(FUS), S('Trojanovice, restaurace Ráztoka')], sim=[two('655', FUS, 'Trojanovice, restaurace Ráztoka')])
L['656'] = dict(core=[S(FUS), S('Trojanovice, Bystré, Maralův kopec')], sim=[two('656', FUS, 'Trojanovice, Bystré, Maralův kopec', b=dict(stops_via=['Trojanovice, pod Dílem']))])
L['657'] = dict(core=[S(FUS), S('Frýdlant n.Ost., zahradnictví')], sim=[two('657', FUS, 'Frýdlant n.Ost., zahradnictví'), two('657 Kunčice', FUS, 'Kunčice p.Ondřejníkem, železniční stanice', a=dict(lines=['657', '651']), b=dict(lines=['657', '651'], stops_via=['Frenštát p.Radh., Žuchov', 'Kunčice p.Ondřejníkem, Rákovec']))])
L['661'] = dict(core=[S(FUS)], sim=[loop('661', FUS, every=480, at=['13:00', '14:20'])])
L['659'] = dict(core=[S(FUS), S('Trojanovice, točna')], sim=[two('659', FUS, 'Trojanovice, točna', a=dict(at=['13:23', '14:38']), b=dict(at=['13:36', '14:51']), every=120)])
L['660'] = dict(core=[S(FUS), S('Trojanovice, u Hutyrů')], sim=[two('660', FUS, 'Trojanovice, u Hutyrů')])
L['662'] = dict(core=[S(KAN), S('Frýdek-Místek, Frýdek, autobusové nádraží')], sim=[two('662', KAN, 'Frýdek-Místek, Frýdek, autobusové nádraží')])
L['690'] = dict(core=[S(NJ), S(KAN), S('Kopřivnice, Tymphany')], sim=[two('690', NJ, 'Kopřivnice, Tymphany', a=dict(core_to=KAN), b=dict(knot=KAN))])
L['698'] = dict(core=[S(NJ), S(KAN)], sim=[two('698', NJ, KAN, a=dict(at=[10, 30]), b=dict(at=[15, 35]), every=60)])
L['699'] = dict(core=[S(NJ), S(KAN)], sim=[two('699', NJ, KAN, a=dict(lines=['699']), b=dict(lines=['699']))])
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
