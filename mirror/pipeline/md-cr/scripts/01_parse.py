"""Parse every CZPTT train in the CIS JR rail zip into data/derived/trains.json.

One record per train file: identifiers, calendar, header foreign ends and every location with
times (minutes after midnight of the start day), activities, carrier, category and number.
"""
import json, os, sys, zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
_Y = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))['service_day'][:4]
ZIP = os.path.join(ROOT, 'data', 'raw', 'jr' + _Y, 'JR' + _Y + '.zip')
OUT = os.path.join(ROOT, 'data', 'derived', 'trains.json')


def tmin(timing):
    t = timing.findtext('Time')
    off = int(timing.findtext('Offset') or 0)
    h, m, s = t[:8].split(':')
    return off * 1440 + int(h) * 60 + int(m) + int(s) / 60


def nsp(el):
    return {p.findtext('Name'): p.findtext('Value') for p in el.findall('NetworkSpecificParameter')}


def parse(data):
    r = ET.fromstring(data)
    ids = {}
    for p in r.find('Identifiers').findall('PlannedTransportIdentifiers'):
        ids[p.findtext('ObjectType')] = p.findtext('Core') + '/' + p.findtext('Variant')
    hdr = r.find('CZPTTHeader')
    foreign = {}
    if hdr is not None:
        for tag in ('CZForeignOriginLocation', 'CZForeignDestinationLocation'):
            e = hdr.find(tag)
            if e is not None:
                foreign[tag] = e.findtext('PrimaryLocationName') or e.findtext('.//PrimaryLocationName')
    info = r.find('CZPTTInformation')
    locs = []
    for L in info.findall('CZPTTLocation'):
        loc = L.find('Location')
        rec = {'name': loc.findtext('PrimaryLocationName'), 'code': loc.findtext('LocationPrimaryCode'),
               'cc': loc.findtext('CountryCodeISO')}
        for tm in L.findall('TimingAtLocation/Timing'):
            q = tm.get('TimingQualifierCode')
            rec['arr' if q == 'ALA' else 'dep'] = tmin(tm)
        rec['act'] = [a.findtext('TrainActivityType') for a in L.findall('TrainActivity')]
        rec['ru'] = L.findtext('ResponsibleRU')
        rec['ctt'] = L.findtext('CommercialTrafficType')
        rec['tt'] = L.findtext('TrainType')
        rec['num'] = L.findtext('OperationalTrainNumber')
        p = nsp(L)
        rec['svc'] = p.get('CZPassengerServiceNumber')
        rec['order'] = p.get('CZPassengerPublicTransportOrderingCoName')
        rec['tname'] = p.get('CZTrainName')
        rec['alt'] = p.get('CZAlternativeTransport')
        locs.append(rec)
    cal = info.find('PlannedCalendar')
    return {'ids': ids, 'foreign': foreign, 'locs': locs,
            'bitmap': cal.findtext('BitmapDays'),
            'start': cal.findtext('ValidityPeriod/StartDateTime')[:10],
            'end': cal.findtext('ValidityPeriod/EndDateTime')[:10],
            'notes': [v for k, v in nsp(r).items()]}


def main():
    out = []
    with zipfile.ZipFile(ZIP) as z:
        for n in z.namelist():
            if not n.endswith('.xml'):
                continue
            rec = parse(z.read(n))
            rec['file'] = n
            out.append(rec)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print(len(out), 'trains ->', OUT)


if __name__ == '__main__':
    main()
