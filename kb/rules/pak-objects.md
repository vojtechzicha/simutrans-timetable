# Pak128 vehicle objects (the owner's custom Czech pak)

Every vehicle on a fleet sheet maps to an object in the owner's custom pak (`C:\Users\vojte\Developer\simutrans-custom-czech-pak128`,
built objects readable under `build/VZ-<City>-<mode>/`). Owner, 28 Sep 2026: "Ask the pak128 custom set which trams it has from each
city and show me clearly which."

## Naming
- `VZ-<Operator/City>-<type>-<livery>-<core>`, e.g. `VZ-DPBrno-EVO2-dpmbbilocervena-EVO2`.
- **Pak core** = last segment after the prefix (`EVO2`; a pair → `T6A5 + T6A5b`). Multi-section trams: first core only.
- Append the livery to the core only where the pak has more than one livery object for that type.
- Meaningless core (e.g. `A`) → show the family name instead.
- Stand-ins (nearest or other-city object) are written `≈ core`, with the reason once in the pak table.
- Prague: DPP cars `VZ-DPPraha-…`; every other operator shares `VZ-Praha-…` (no operator in the name); ferries `VZ-Praha-water`.
  PID suburban/regional contracts (lines 300+ run by other operators) are `VZ-PID-…` in `VZ-PID-bus` (66 objects on 30 Oct;
  tokens differ: `Setra_S_515_LE`, `SOR_ICN_10_5`). Regional PID lines use the `VZ-Praha-bus` and `VZ-DPPraha-bus` objects as they are; `VZ-PID-bus` holds only the type ×
  livery combinations those two lack (fleet desk, 2 Nov 2026, after the PID regional sheets asked for 20 types that already existed
  there). Look a type up in all three packs (DPP's own buses in `VZ-DPPraha` first) before requesting it (fleet desk, 30 Oct: all
  five "missing" objects already existed in `VZ-PID-bus`). `name=` is `<basename>-<vehicle id>`, articulated `-A` + `-B`.
  Non-DPP lines must be exactly as good as DPP ones — never DPP or other-city stand-ins. Advert wraps → the type's normal livery.
- Neighbouring regions' own paints (owner via the fleet desk, 2 Nov 2026): `VZ-DUK-bus` (Ústecký kraj: DSÚK, Platil…), `VZ-IDOL-bus`
  (Liberecký: ČSAD Liberec, BusLine LK, ČSAD Česká Lípa…), `VZ-JIKORD-bus` (Jihočeský: ČSAD AUTOBUSY České Budějovice…), as
  `VZ-ODIS` / `VZ-IREDO`; `VZ-<agency>-<Type>-<livery>`. A plain white bus uses the existing white object (IREDO / DPPraha).
- ODIS: regional buses `VZ-ODIS-bus` (livery by real paint: 3ČSAD → `3csadbilozelena`, white → `bilazelenykruh`, Transdev
  `transdev`, Z-Group `bila`…); town lines `VZ-MHD<Town>` for the town's own paint (a town-line bus in PID paint uses the PID object; fleet desk, 2 Nov 2026) (Havířov, Karviná, Orlová, Krnov, Nový Jičín, Třinec…).
- Trolleybuses `VZ-<City>-trolleybus` (waytype road, electric engine — wire is information only). Battery/diesel-generator variants
  exist where the real car has auxiliary drive (Opava 32Tr_battery 314–323, 26TrDG 305–306).
- Trams: Praha/Brno/Ostrava trams are VZ objects only (native pak trams uninstalled 28 Sep).

## Who to ask
- **Fleet desk session** (announced 21 Oct as `simutrans-custom-czech-pak128-35`; names change — find the current one with
  ListAgents): which objects exist, and requests for missing vehicles/liveries. **Never message a drawing session directly.**
  Send one inventory per sheet: type × paint × area kind × count, with operator and where it runs.
- Each pipeline keeps its open requests in `pak_request.md` (type × livery × car numbers); `pak_objects.json` files are read from
  the pak build so "requested" marks clear by themselves.
- Impossible sets (missing objects, couplings that don't work) are the pak's job to fix: ask, don't work around.
- Renames of objects that the save uses go through the save-migration flow on the pak side; renames of save objects (stops, lines)
  go through the engine's rename service (see [../related-projects.md](../related-projects.md)).
