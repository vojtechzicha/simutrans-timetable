"""config.lines of the Bruntálsko/Krnovsko/Rýmařovsko sheet: the Simutrans lines of every modelled ODIS line, with notes
(brn_notes.py). Intervals and minutes are 'auto' where the review found the fit right, hand-set where it did not.
Idempotent: rerun after editing, then the pipeline (python -X utf8 run.py --base odis-regional-bruntalsko)."""
import os, sys, json
os.environ['ODIS_BASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, AL, rel
T = load('trips.json')
c = json.load(open(rel('config.json'), encoding='utf-8'))
c['terminus_alias'] = {}
c['terminus_alias_why'] = ''
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
def oneway(name, A, B, every='auto', a=None):
    return dict(name=name, every=every, legs=[leg(A, B, **(a or {})), leg(B, A, untimed=True)])
L = {}
KAS, KZS = 'Krnov, autobusová stanice', 'Krnov, železniční stanice'
BAS, BZS = 'Bruntál, autobusová stanice', 'Bruntál, železniční stanice'
RAS = 'Rýmařov, autobusová stanice'
HBAS = 'Horní Benešov, autobusová stanice'
MAAS = 'Město Albrechtice, autobusová stanice'
OAS = 'Osoblaha, autobusová stanice'
ZHAS = 'Zlaté Hory, autobusová stanice'
JZS = 'Jindřichov, železniční stanice'
VZS = 'Vrbno p.Prad., železniční stanice'
MBN = 'Moravský Beroun, náměstí'
# ---------------- Krnovsko (852)
L['822'] = dict(core=[S(KAS), S('Staré Purkartice, točna')], sim=[two('822', KAS, 'Staré Purkartice, točna')])
L['831'] = dict(core=[S(KAS), S(MAAS), S('Slezské Pavlovice')], sim=[two('831', KAS, 'Slezské Pavlovice')])
L['832'] = dict(core=[S(KAS), S(MAAS), S(OAS)], sim=[two('832', KAS, OAS, a=dict(at=['16:20']), b=dict(at=['15:41']), every=180)])
L['833'] = dict(core=[S(KAS), S(JZS), S(OAS)], sim=[two('833', KAS, JZS, a=dict(stops_via=[S('rozcestí Dakon')])), two('833 Osoblaha', JZS, OAS)])
L['824'] = dict(core=[S(KAS), S(MAAS), S('Vrbno p.Prad., zámeček')], sim=[two('824', KAS, 'Vrbno p.Prad., zámeček', a=dict(at=['12:05']), b=dict(at=['14:18']), every=480)])
L['913'] = dict(core=[S(KAS), S('Olomouc, autobusové nádraží')], sim=[two('913', KAS, 'Olomouc, autobusové nádraží', every=480)])
L['901'] = dict(core=[S(KAS), S(MAAS), S(ZHAS)], sim=[two('901', KAS, ZHAS)])
L['902'] = dict(core=[S(JZS), S('restaurace U hájenky'), S(ZHAS)], sim=[two('902', JZS, 'restaurace U hájenky', a=dict(at=['15:41']), b=dict(at=['16:06']), every=120), two('902 Zlaté Hory', JZS, ZHAS)])
# ---------------- Bruntálsko (853)
L['811'] = dict(core=[S(KAS), S(HBAS)], sim=[two('811', KAS, HBAS, b=dict(stops_via=[S('Dubnice, pohostinství')])), two('811 Sosnová', KAS, 'Sosnová, Obecní úřad', a=dict(at=['14:10']), b=dict(at=['14:40']), every=90)])
L['814'] = dict(core=[S(KAS), S('Čaková, konečná'), S('Zátor, točna')], sim=[two('814', KAS, 'Čaková, konečná'), oneway('814 Zátor', KAS, 'Zátor, točna', every=480, a=dict(at=['15:00']))])
L['816'] = dict(core=[S(KZS), S('Krasov, točna')], sim=[two('816', KZS, 'Krasov, točna')])
L['817'] = dict(core=[S(KAS)], sim=[loop('817', KAS)])
L['818'] = dict(core=[S(KAS), S('Úblo, točna'), S('Skrochovice, most')], sim=[two('818', KAS, 'Úblo, točna'), two('818 Skrochovice', 'Úblo, točna', 'Skrochovice, most'),
                     two('818 Neplachovice', 'Úblo, točna', 'Neplachovice, škola', a=dict(at=['12:30', '13:30']), b=dict(at=['13:05', '14:10']), every=480)])
L['819'] = dict(core=[S(KAS), S(BAS)], sim=[two('819', KAS, BAS)])
L['861'] = dict(core=[S(BZS), S('Vrbno p.Prad., zámeček')], sim=[two('861', BZS, 'Vrbno p.Prad., zámeček', a=dict(at=[40]), b=dict(at=[54]), every=60)])
L['862'] = dict(core=[S(BZS), S('Karlova Studánka, dolní parkoviště')], sim=[two('862', BZS, 'Karlova Studánka, dolní parkoviště', a=dict(at=[10]), b=dict(at=[10]), every=60)])
L['863'] = dict(core=[S(BAS), S('rozcestí Ludvíkov'), S('Karlova Studánka, Hvězda autobusová stanice')],
                sim=[two('863', BAS, 'rozcestí Ludvíkov')])
SHAS = 'Světlá Hora, autobusová stanice'
L['865'] = dict(core=[S(BZS), S('Dětřichovice, točna'), S(SHAS)],
                sim=[dict(name='865', every=480, legs=[leg(BZS, 'Dětřichovice, točna', at=['15:05']), leg('Dětřichovice, točna', SHAS, at=['15:37']),
                                                     leg(SHAS, BZS, untimed=True, lines=['866', '865'])])])
L['866'] = dict(core=[S('Světlá Hora, autobusová stanice'), S('Světlá Hora, Podlesí')],
                sim=[two('866', 'Světlá Hora, autobusová stanice', 'Světlá Hora, Podlesí', a=dict(at=['13:40', '14:20', '15:50']), b=dict(at=['13:55', '14:35']), every=480)])
L['872'] = dict(core=[S(BAS), S('Milotice n.Opavou, škola')], sim=[two('872', BAS, 'Milotice n.Opavou, škola', a=dict(at=['13:50']), b=dict(at=['14:10']), every=90)])
L['874'] = dict(core=[S(HBAS), S('Horní Životice, střed'), S('Svobodné Heřmanice, obecní úřad')],
                sim=[two('874', HBAS, 'Horní Životice, střed')])
L['885'] = dict(core=[S(BZS), S('Ovčárna točna')], sim=[two('885', BZS, 'Ovčárna točna')])
L['907'] = dict(core=[S(VZS), S(ZHAS)], sim=[two('907', VZS, ZHAS, a=dict(at=['15:15']), b=dict(at=['16:25']), every=120)])
# ---------------- Rýmařovsko (854)
L['873'] = dict(core=[S(BZS), S('Václavov, dolní')], sim=[two('873', BZS, 'Václavov, dolní')])
L['877'] = dict(core=[S(RAS), S(BZS), S('Bruntál, KARLA')], sim=[two('877', RAS, BZS), two('877 KARLA', RAS, 'Bruntál, KARLA', a=dict(at=['12:40']), b=dict(at=['14:17']), every=480)])
L['878'] = dict(core=[S(RAS), S('Karlov, garáž')], sim=[two('878', RAS, 'Karlov, garáž', a=dict(at=['15:30']), b=dict(at=['16:10']), every=90)])
L['879'] = dict(core=[S(RAS), S('Nová Ves, konečná')], sim=[two('879', RAS, 'Nová Ves, konečná')])
L['880'] = dict(core=[S(RAS), S('Anenská Huť')], sim=[two('880', RAS, 'Anenská Huť')])
L['909'] = dict(core=[S(BZS), S(MBN)], sim=[two('909', BZS, MBN, a=dict(at=['14:45']), b=dict(at=['15:10']), every=120),
                                                   two('909 Leskovec', BZS, 'rozcestí Bohdanovice', a=dict(at=['15:10']), b=dict(at=['12:50']), every=180)])
L['910'] = dict(core=[S(BZS), S(MBN), S('Moravský Beroun, železniční stanice')],
                sim=[two('910', BZS, 'Moravský Beroun, železniční stanice', a=dict(core_to=MBN), b=dict(knot=MBN))])
L['911'] = dict(core=[S(BZS), S('Granitol')], sim=[two('911', BZS, 'Granitol')])
L['912'] = dict(core=[S(RAS), S('Šternberk, Dvorská')], sim=[two('912', RAS, 'Šternberk, Dvorská')])
L['921'] = dict(core=[S(RAS), S('Olomouc, autobusové nádraží'), S('Břidličná, Kovohutě'), S('Ryžoviště, náměstí')],
                sim=[two('921', RAS, 'Olomouc, autobusové nádraží', a=dict(at=['12:25']), b=dict(at=['16:55']), every=480)])
RZS = 'Rýmařov, železniční stanice'
L['922'] = dict(core=[S(RZS), S(RAS), S('Tvrdkov, Ruda, restaurace'), S('Uničov, autobusová stanice')],
                sim=[two('922', RZS, 'Tvrdkov, Ruda, restaurace', a=dict(knot=RAS), b=dict(core_to=RAS)),
                     dict(name='922 Uničov', every=480, legs=[leg(RAS, 'Uničov, autobusová stanice', at=['12:30']), leg('Uničov, autobusová stanice', RZS, at=['15:09']),
                                                             leg(RZS, RAS, untimed=True, rt=5)])])
# ---------------- MHD Krnov (856)
NEM = 'Krnov, Nemocnice hl.brána'
L['801'] = dict(core=[S(NEM), S('Krnov, Petrův důl'), S('průmyslová zóna II, točna')],
                sim=[two('801', NEM, 'Krnov, Petrův důl'),
                     dict(name='801 PZ', every=480, legs=[leg('Krnov, Petrův důl', 'Hájnický potok', core_to='průmyslová zóna II, točna', at=['13:05', '13:30', '14:05', '14:34', '15:22', '15:52']),
                                                        leg('Hájnický potok', 'Krnov, Petrův důl', knot='průmyslová zóna II, točna', knot_at=['13:15', '13:42', '14:16', '14:43', '15:34', '16:06'])])])
L['802'] = dict(core=[S('Krnov, Aut.stanoviště'), S('Ježník, sanatorium')], sim=[two('802', 'Krnov, Aut.stanoviště', 'Ježník, sanatorium')])
L['805'] = dict(core=[S('Hlubčická Na špici'), S('Chomýž, točna')], sim=[two('805', 'Hlubčická Na špici', 'Chomýž, točna', a=dict(at=['14:40']), b=dict(at=['15:35']), every=90)])
L['806'] = dict(core=[S('Krnov, Aut.stanoviště'), S('Cvilín točna'), S('st.hranice CLO')],
                sim=[two('806', 'Krnov, Aut.stanoviště', 'Cvilín točna', a=dict(at=['14:45']), b=dict(at=['15:05']), every=90),
                     dict(name='806 CLO', every=480, legs=[leg('Krnov, Aut.stanoviště', 'st.hranice CLO', at=['17:50']), leg('st.hranice CLO', 'Cvilín točna', at=['18:04']),
                                                         leg('Cvilín točna', 'Krnov, Aut.stanoviště', untimed=True)])])
L['807'] = dict(core=[S(NEM), S('Guntramovice, točna'), S('Krnov, Aut.stanoviště')],
                sim=[dict(name='807', every=480, legs=[leg(NEM, 'Guntramovice, točna', at=['14:13']), leg('Guntramovice, točna', 'Krnov, Aut.stanoviště', at=['14:33']),
                                                     leg('Krnov, Aut.stanoviště', NEM, untimed=True, rt=7)])])
# ---------------- MHD Bruntál (855)
L['851'] = dict(core=[S(BZS), S('Bruntál, KARLA')], sim=[two('851', BZS, 'Bruntál, KARLA', a=dict(stops_via=[S('Bruntál, nový hřbitov')]))])

NF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brn_notes.py')
NOTES = {}
if os.path.exists(NF): exec(open(NF, encoding='utf-8').read())   # NOTES
for k_, n_ in NOTES.items():
    if k_ in L: L[k_]['note'] = n_
missing = sorted(set(L) - set(NOTES), key=int)
if missing: print('no note:', missing)
c['lines'] = L
other = {x for v in c['other_sheets'].values() for x in v.get('lines', [])}
c['unmodelled'] = {x: c.get('unmodelled', {}).get(x, '(pending)') for x in load('line_class.json') if x not in L and x not in other}
json.dump(c, open(rel('config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(L), 'lines;', len(c['unmodelled']), 'unmodelled; reason still missing:', sorted((k for k, v in c['unmodelled'].items() if v == '(pending)'), key=int))
