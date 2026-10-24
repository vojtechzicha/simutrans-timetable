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
  Non-DPP lines must be exactly as good as DPP ones — never DPP or other-city stand-ins. Advert wraps → the type's normal livery.
- ODIS: regional buses `VZ-ODIS-bus` (livery by real paint: 3ČSAD → `3csadbilozelena`, white → `bilazelenykruh`, Transdev
  `transdev`, Z-Group `bila`…); town lines `VZ-MHD<Town>` only (Havířov, Karviná, Orlová, Krnov, Nový Jičín, Třinec…).
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
