"""The Simutrans lines of the Opavsko/Vítkovsko/Hlučínsko sheet -> config.lines (+ notes from opa_notes.py).
Intervals and slots 'auto' where the builder's fit is right; hand-set after the review where it was not. Idempotent: run
it, then the pipeline (python -X utf8 run.py --base odis-regional-opavsko from ../odis-regional-hko/scripts)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ['ODIS_BASE'] = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'odis-regional-hko', 'scripts'))
from lib import load, nm, AL, rel
T = load('trips.json')
c = json.load(open(rel('config.json'), encoding='utf-8'))
c['terminus_alias'] = {'Opava, Jaktař škola': 'Opava, Jaktař, škola'}
c['terminus_alias_why'] = 'The Opava town JDF writes Opava, Jaktař škola, the regional JDFs Opava, Jaktař, škola: one stop.'
ALL = sorted({AL(nm(s)) for tr in T.values() for t in tr for s in t['stops']})
def S(sub):
    m = [s for s in ALL if s == sub] or [s for s in ALL if s.endswith(sub)] or [s for s in ALL if sub in s]
    if len(m) != 1: raise SystemExit(f'stop {sub!r}: {m[:6]}')
    return m[0]
def leg(fr, to, **kw): return dict(fr=S(fr), to=S(to), **({'at': 'auto'} if not kw.get('untimed') and 'at' not in kw and 'knot_at' not in kw else {}), **{k: (S(v) if k in ('knot', 'core_to') else [S(x) for x in v] if k in ('via', 'notvia', 'stops_via') else v) for k, v in kw.items()})
def two(name, A, B, a=None, b=None, every='auto'):
    a = a or {}; b = b or {}
    return dict(name=name, every=every, legs=[leg(A, B, **a), leg(B, A, **b)])
def loop(name, A, every='auto', **kw): return dict(name=name, every=every, legs=[leg(A, A, **kw)])
def oneway(name, A, B, every='auto', a=None, rt=None):
    return dict(name=name, every=every, legs=[leg(A, B, **(a or {})), leg(B, A, untimed=True, **({'rt': rt} if rt else {}))])
L = {}
OPA, TQM, PRA, DIV, DNA = 'Opava, Bílovecká TQM', 'Opava, Bílovecká TQM', 'Opava, Praskova', 'Opava, Divadlo', 'Opava, Dolní náměstí'
VIT, BUD, ODRY = 'Vítkov, autobusová stanice', 'Budišov n.Bud., autobusová stanice', 'Odry, autobusová stanice'
HLU, PRV, MUG = 'Hlučín, autobusové nádraží', 'Ostrava, Přívoz, sad B.Němcové', 'Ostrava, Mor.Ostrava, Muglinovská'
SVI = 'Ostrava, Svinov, nádraží'
# ---------------- MHD Opava, trolleybuses (city-transport JDF)
L['201'] = dict(core=[S('Opava, Kylešovice, Bílovecká'), S(PRA), S('Opava, Městský hřbitov')], sim=[two('201', 'Opava, Kylešovice, Bílovecká', 'Opava, Městský hřbitov')])
L['202'] = dict(core=[S('Opava, Kateřinky'), S(DIV), S('Opava, Albert hypermarket')], sim=[two('202', 'Opava, Kateřinky', 'Opava, Albert hypermarket')])
L['203'] = dict(core=[S('Opava, Globus'), S(DIV), S('Opava, Jaktař')], sim=[two('203', 'Opava, Globus', 'Opava, Jaktař')])
L['204'] = dict(core=[S('Opava, Kylešovice, škola'), S(PRA), S('Opava, Englišova')], sim=[two('204', 'Opava, Kylešovice, škola', 'Opava, Englišova', a=dict(at=[0, 24, 36]), b=dict(at=[9, 33, 57]), every=60)])
# ---------------- MHD Opava, buses
L['211'] = dict(core=[S(PRA), S('Opava, Podvihov Na Nové')], sim=[two('211', PRA, 'Opava, Podvihov Na Nové')])
L['212'] = dict(core=[S(DIV), S('Opava, Milostovice'), S('Opava, Vlaštovičky')],
                sim=[two('212', DIV, 'Opava, Vlaštovičky', a=dict(core_to='Opava, Milostovice'), b=dict(knot='Opava, Milostovice'))])
L['213'] = dict(core=[S('Opava, Kylešovice, SÚS'), S(DIV), S('Opava, Vávrovice, Karlovec')], sim=[two('213', 'Opava, Kylešovice, SÚS', 'Opava, Vávrovice, Karlovec')])
L['215'] = dict(core=[S('Opava, Liliová'), S('Opava, Kylešovice, škola'), S('Opava, Globus')],
                sim=[two('215', 'Opava, Liliová', 'Opava, Globus', a=dict(core_to='Opava, Kylešovice, škola'), b=dict(knot='Opava, Kylešovice, škola'))])
L['216'] = dict(core=[S(DNA), S('Opava, Vávrovice, Držkovice')], sim=[two('216', DNA, 'Opava, Vávrovice, Držkovice', a=dict(stops_via=['Opava, Vávrovice, OPAVIA']))])
L['217'] = dict(core=[S('Opava, Koupaliště'), S(DIV), S('Slavkov')],
                sim=[two('217', 'Opava, Koupaliště', 'Slavkov', a=dict(at=[4], stops_via=['Otice, Slavkovská'], rt=20), b=dict(at=[25]), every=60)])
L['218'] = dict(core=[S('Opava, Koupaliště'), S(DNA), S('Chvalíkovice')], sim=[two('218', 'Opava, Koupaliště', 'Chvalíkovice')])
L['219'] = dict(core=[S('Opava, Malé Hoštice'), S(PRA), S('Otice, kaple')], sim=[two('219', 'Opava, Malé Hoštice', 'Otice, kaple')])
L['220'] = dict(core=[S(PRA), S('Opava, Suché Lazce, Přerovec')], sim=[two('220', PRA, 'Opava, Suché Lazce, Přerovec')])
L['222'] = dict(core=[S('Raduň, škola'), S('Opava, Podvihov Na Nové')], sim=[two('222', 'Raduň, škola', 'Opava, Podvihov Na Nové', every=480)])
L['223'] = dict(core=[S(PRA), S('Opava, Komárov, TEVA 2')], sim=[two('223', PRA, 'Opava, Komárov, TEVA 2', every=480)])
# ---------------- Vítkovsko
L['232'] = dict(core=[S(VIT), S('Fulnek, železniční stanice'), S(ODRY)], sim=[two('232', ODRY, VIT, a=dict(stops_via=['Odry, Hvězdová']), b=dict(core_to='Fulnek, železniční stanice'), every=480)])
L['233'] = dict(core=[S(VIT), S('Melč, střed')], sim=[two('233', VIT, 'Melč, střed')])
L['234'] = dict(core=[S(VIT), S('Březová, škola')], sim=[dict(name='234', every='auto', legs=[leg(VIT, 'Březová, Leskovec, škola', core_to='Březová, škola'), leg('Březová, Leskovec, škola', VIT, knot='Březová, škola')])])
L['235'] = dict(core=[S(VIT)], sim=[loop('235', VIT)])
L['236'] = dict(core=[S(VIT), S(BUD)], sim=[two('236', VIT, BUD), two('236 Podlesí', BUD, 'Budišov n.Bud., Podlesí, točna', every=480)])
L['237'] = dict(core=[S(BUD), S('Budišov n.Bud., St.Oldřůvky, točna'), S('Dvorce, náměstí')],
                sim=[two('237', BUD, 'Budišov n.Bud., St.Oldřůvky, točna'), two('237 Dvorce', BUD, 'Dvorce, náměstí')])
L['238'] = dict(core=[S(VIT), S(ODRY)], sim=[two('238', VIT, ODRY, a=dict(stops_via=['Odry, Loučky, škola']))])
L['678'] = dict(core=[S(SVI), S('Fulnek, náměstí'), S(VIT)], sim=[two('678', SVI, VIT, b=dict(stops_via=['Bravantice, Lidl']))])
# ---------------- Opavsko
L['240'] = dict(core=[S(TQM), S('Hradec n.Moravicí, železniční stanice'), S('Melč, střed'), S(VIT)], sim=[two('240', TQM, VIT)])
L['241'] = dict(core=[S(TQM), S('Melč, střed'), S(VIT)], sim=[two('241', TQM, VIT, b=dict(stops_via=['Vítkov, Zálužné'])),
                     two('241 Lipina', TQM, 'Štáblovice, Lipina, střed', a=dict(at=['14:28']), b=dict(at=['15:01']), every=480)])
L['242'] = dict(core=[S(TQM), S(VIT)], sim=[two('242', TQM, VIT)])
L['243'] = dict(core=[S(TQM), S(BUD)], sim=[two('243', TQM, BUD, every=480)])
L['245'] = dict(core=[S(TQM), S('Hradec n.Moravicí, Benkovice, střed')], sim=[two('245', TQM, 'Hradec n.Moravicí, Benkovice, střed'),
                     two('245 zámek', 'Hradec n.Moravicí, Benkovice, střed', 'Hradec n.Moravicí, zámek', a=dict(at=['13:15']), b=dict(at=['13:52']), every=480)])
L['244'] = dict(core=[S('Hradec n.Moravicí, škola'), S('Opava, Východní nádraží')], sim=[oneway('244', 'Hradec n.Moravicí, škola', 'Opava, Východní nádraží', every=480, a=dict(at=['14:20']))])
L['246'] = dict(core=[S(TQM), S('Dolní Životice, hor.konec'), S('Jakartovice, Hoř.Kunčice, točna')],
                sim=[two('246', TQM, 'Jakartovice, Hoř.Kunčice, točna', a=dict(core_to='Dolní Životice, hor.konec'), b=dict(knot='Dolní Životice, hor.konec'))])
L['247'] = dict(core=[S(TQM), S('Moravice, střed')], sim=[two('247', TQM, 'Moravice, střed', a=dict(at=['15:00']), b=dict(at=['17:00']), every=480)])
L['248'] = dict(core=[S(TQM), S('Svobodné Heřmanice, rozcestí')], sim=[two('248', TQM, 'Svobodné Heřmanice, rozcestí', a=dict(at=[53]), b=dict(at=[45]), every=60)])
L['249'] = dict(core=[S(TQM), S('Velké Heraltice, autobusová stanice')], sim=[two('249', TQM, 'Velké Heraltice, autobusová stanice'),
                     two('249 Tábor', 'Velké Heraltice, škola', 'Velké Heraltice, Tábor, střed', a=dict(at=['13:28']), b=dict(at=['13:35']), every=480)])
L['250'] = dict(core=[S(TQM), S('Brumovice, Úblo, točna'), S('Krnov, autobusová stanice')],
                sim=[two('250', TQM, 'Brumovice, Úblo, točna', every=480), two('250 Krnov', TQM, 'Krnov, autobusová stanice', every=480),
                     two('250 Holasovice', TQM, 'Holasovice, mateřská škola', a=dict(at=['14:53']), b=dict(at=['15:38']), every=480)])
L['251'] = dict(core=[S(TQM), S('Chlebičov, točna')], sim=[two('251', TQM, 'Chlebičov, točna')])
L['252'] = dict(core=[S(TQM), S('Kravaře, Nádražní'), S('Kobeřice, autobusová stanice')], sim=[two('252', TQM, 'Kobeřice, autobusová stanice', a=dict(stops_via=['Štěpánkovice, Albertovec']))])
L['253'] = dict(core=[S(TQM), S('Služovice, škola'), S('Kobeřice, autobusová stanice'), S('Služovice, Vrbka, točna')],
                sim=[two('253', TQM, 'Kobeřice, autobusová stanice'), two('253 Vrbka', TQM, 'Služovice, Vrbka, točna')])
L['254'] = dict(core=[S(TQM), S('Kravaře, Nádražní'), S('Chuchelná, rehabilitační ústav')], sim=[two('254', TQM, 'Chuchelná, rehabilitační ústav')])
L['255'] = dict(core=[S('Kobeřice, autobusová stanice'), S('Chuchelná, rehabilitační ústav')], sim=[two('255', 'Kobeřice, autobusová stanice', 'Chuchelná, rehabilitační ústav')])
L['257'] = dict(core=[S('Opava, Suché Lazce, střed'), S('Kravaře, Kouty, Olšinky')], sim=[two('257', 'Opava, Suché Lazce, střed', 'Kravaře, Kouty, Olšinky', every=480)])
L['259'] = dict(core=[S('Litultovice, kostel'), S('Jakartovice, Hoř.Kunčice, točna')], sim=[oneway('259', 'Jakartovice, Hoř.Kunčice, točna', 'Litultovice, kostel', every=480)])
L['260'] = dict(core=[S(TQM), S('Velké Heraltice, autobusová stanice'), S('Horní Benešov, autobusová stanice'), S('Bruntál, autobusová stanice')],
                sim=[two('260', TQM, 'Bruntál, autobusová stanice', a=dict(core_to='Horní Benešov, autobusová stanice'), b=dict(knot='Horní Benešov, autobusová stanice')),
                     two('260 Heřmanice', 'Velké Heraltice, autobusová stanice', 'Svobodné Heřmanice, rozcestí', a=dict(stops_via=['Velké Heraltice, Košetice, náves']), every=480)])
L['261'] = dict(core=[S(TQM), S('Fulnek, železniční stanice'), S('Nový Jičín, autobusové nádraží')], sim=[two('261', TQM, 'Nový Jičín, autobusové nádraží', a=dict(at=['14:22'], stops_via=['Hladké Životice, železniční stanice']), b=dict(at=['14:35'], stops_via=['Březová, Gručovice, střed']), every=120)])
L['262'] = dict(core=[S(TQM), S('Hradec n.Moravicí, železniční stanice'), S('Bílovec, železniční stanice')], sim=[two('262', TQM, 'Bílovec, železniční stanice', a=dict(stops_via=['Slatina'])),
                     two('262 Skřipov', TQM, 'Skřipov, Hrabství, točna', a=dict(stops_via=['Otice, Rybníčky'], notvia=['Bílovec, železniční stanice']), b=dict(notvia=['Bílovec, železniční stanice']), every=480)])
L['263'] = dict(core=[S(TQM), S('Pustá Polom, autobusová stanice'), S('Těškovice, střed')],
                sim=[two('263', TQM, 'Těškovice, střed', a=dict(core_to='Pustá Polom, autobusová stanice'), b=dict(knot='Pustá Polom, autobusová stanice'))])
L['264'] = dict(core=[S(TQM), S('Těškovice, střed')], sim=[two('264', TQM, 'Těškovice, střed')])
L['267'] = dict(core=[S(TQM), S('Nové Lublice, střed')], sim=[two('267', TQM, 'Nové Lublice, střed', b=dict(stops_via=['Jezdkovice, rozcestí']), every=480)])
L['270'] = dict(core=[S(TQM), S(SVI)], sim=[two('270', TQM, SVI)])
L['920'] = dict(core=[S(SVI), S(TQM), S('Bruntál, autobusová stanice'), S('Rýmařov, autobusová stanice'), S('Šumperk, autobusová stanice')],
                sim=[two('920', SVI, 'Šumperk, autobusová stanice', a=dict(at=['14:17']), b=dict(at=['14:35']), every=120),
                     two('920 Rýmařov', SVI, 'Rýmařov, autobusová stanice', a=dict(at=['13:17'], notvia=['Šumperk, autobusová stanice']), b=dict(at=['17:32'], notvia=['Šumperk, autobusová stanice']), every=120),
                     two('920 Opava', TQM, 'Rýmařov, autobusová stanice', a=dict(at=['13:24'], stops_via=['Rýmařov, Jamartice, hřbitov']), b=dict(at=['15:02']), every=480)])
L['923'] = dict(core=[S(TQM), S('Olomouc, autobusové nádraží')], sim=[two('923', TQM, 'Olomouc, autobusové nádraží', every=480)])
# ---------------- Hlučínsko
L['075'] = dict(core=[S('Hlučín, sídliště OKD'), S('Ostrava, Poruba, Studentská')], sim=[two('075', 'Hlučín, sídliště OKD', 'Ostrava, Poruba, Studentská')])
# Hlučínsko lines at sad B. Němcové (281, 282, 290, 292): set by hand on 25 Oct 2026 with the bus schedule method, steps 1-11
# (../method-check-2026-10-25.md; owner: "I want you to check"). The buses sleep at the far ends (Hať garage, Třebom,
# Strahovice, Chuchelná, Píšť), so the afternoon peak sends more buses out of Ostrava than come back (live map, 20 Oct): each
# line is timed both ways at the inbound rate, and the extra peak departures are off the pattern. No B lines with empty
# returns for frequency (owner, 25 Oct 2026: "Unless those empty runs add something really needed and specific, don't add
# them just for frequency"); they ran the same stops as the core lines.
L['281'] = dict(core=[S('Třebom, náměstí'), S('Kobeřice, autobusová stanice'), S(HLU), S(PRV)], sim=[
    two('281', 'Třebom, náměstí', PRV, a=dict(knot='Kobeřice, autobusová stanice', knot_at=[13]), b=dict(at=[18], core_to='Kobeřice, autobusová stanice'), every=60)])
L['282'] = dict(core=[S('Píšť, kostel'), S(HLU), S(PRV)], anchor='16:00',
                sim=[two('282', 'Píšť, kostel', PRV, a=dict(at=['15:55'], core_to=HLU), b=dict(at=['16:53']), every=120)])
L['284'] = dict(core=[S(HLU), S('Štěpánkovice, Svoboda')], sim=[two('284', HLU, 'Štěpánkovice, Svoboda')])
L['285'] = dict(core=[S('Ostrava, Poruba, Dílny DP Ostrava'), S('Štítina, škola'), S('Dobroslavice')],
                sim=[two('285', 'Ostrava, Poruba, Dílny DP Ostrava', 'Štítina, škola'), two('285 Dobroslavice', 'Ostrava, Poruba, Dílny DP Ostrava', 'Dobroslavice')])
L['290'] = dict(core=[S('Hať, točna'), S(HLU), S(PRV)], sim=[
    two('290', 'Hať, točna', PRV, a=dict(at=['14:47', '15:31', '16:07', '16:37']), b=dict(at=['14:44', '14:59', '15:24', '15:49']), every=120)])
L['292'] = dict(core=[S(PRV), S(HLU), S('Píšť, Mýto'), S('Chuchelná, železniční stanice')], sim=[
    two('292', PRV, 'Chuchelná, železniční stanice', a=dict(at=['14:33'], core_to='Píšť, Mýto'), b=dict(knot=HLU, knot_at=['14:59']), every=80)])
L['293'] = dict(core=[S(HLU), S('Bohumín, Nový Bohumín, autobusová stanice')], sim=[two('293', HLU, 'Bohumín, Nový Bohumín, autobusová stanice'), two('293 ŽD', HLU, 'Bohumín, Nový Bohumín, ŽD vrát.III', a=dict(at=['13:05']), b=dict(at=['14:13']), every=480)])
L['555'] = dict(core=[S('Bohumín, Starý Bohumín, náměstíSvobody'), S('Ostrava, Mor.Ostrava, Náměstí Republiky')],
                sim=[two('555', 'Bohumín, Starý Bohumín, náměstíSvobody', 'Ostrava, Mor.Ostrava, Náměstí Republiky')])
NOTES = {}
nf = os.path.join(HERE, 'opa_notes.py')
if os.path.exists(nf): exec(open(nf, encoding='utf-8').read())
for k_, n_ in NOTES.items():
    if k_ in L: L[k_]['note'] = n_
c['lines'] = L
modelled = set(L)
other = {x for sh in c['other_sheets'].values() for x in sh.get('lines', [])}
c['unmodelled'] = {x: c.get('unmodelled', {}).get(x, '(pending)') for x in load('line_class.json') if x not in modelled and x not in other}
json.dump(c, open(rel('config.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(L), 'lines;', len(c['unmodelled']), 'unmodelled; reason missing:', sorted((k for k, v in c['unmodelled'].items() if v == '(pending)'), key=int),
      '; no note:', sorted(set(L) - set(NOTES), key=int)[:80])
