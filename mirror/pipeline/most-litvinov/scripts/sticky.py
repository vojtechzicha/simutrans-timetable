"""Sticky header bar shared by the fleet sheets (the Prague tram sheet's "controls" bar, 29 Sep 2026, user request).

One bar under the page header that stays on screen: line badges, depot links with counts, section links,
and a vehicle search that highlights every element with data-v="<number>[+<number>...]".
The same file is copied into brno, plzen, ostrava and most-litvinov scripts/; keep the copies identical.
Needs the page tokens --bg --surface --surface2 --ink --ink2 --muted --rule --rule2 --accent and the fonts
--font-display / --font-body (fallbacks are given).
"""
import html

E = lambda s: html.escape(str(s), quote=True)

CSS = '''<style>
.controls{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding-block:10px;border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center}
.controls .nav{position:static;padding:0;border:0;background:none;display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.controls .lab{font:600 12px var(--font-display,sans-serif);text-transform:uppercase;letter-spacing:.1em;color:var(--muted);padding-inline:2px 6px}
.controls .lnk{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:24px;padding-inline:5px;border-radius:4px;background:var(--accent);color:var(--accent-ink,#fff);font:700 15px var(--font-display,sans-serif);text-decoration:none;font-variant-numeric:tabular-nums}
.controls .dnav a{font:600 14px var(--font-display,sans-serif);text-decoration:none;color:var(--ink2);background:var(--surface2);padding:3px 8px;border-radius:4px}
.controls .dnav a b{color:var(--accent)}
.controls input[type=search]{font:14px var(--font-body,sans-serif);padding:6px 10px;border:1px solid var(--rule2);border-radius:6px;background:var(--surface);color:var(--ink);width:min(100%,230px)}
.controls a:focus-visible,.controls input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.controls #hits{font-size:13px;color:var(--muted)}
[id]{scroll-margin-top:var(--stick,110px)}
[data-v].hit{background:color-mix(in srgb,var(--accent) 22%,transparent);outline:2px solid var(--accent);border-radius:3px}
</style>'''

def controls(lines, depots, sections, example, depot_word='Depots'):
    """lines: [(href, label)]; depots: [(key, label, count)] (link goes to the visible element with data-depot=key,
    falling back to #d-<key>); sections: [(href, label)]."""
    ln = ''.join(f'<a class="lnk" href="{E(h)}">{E(t)}</a>' for h, t in lines)
    dp = ''.join(f'<a href="#d-{E(k)}" data-dep="{E(k)}">{E(t)} <b>{n}</b></a>' for k, t, n in depots)
    sc = ''.join(f'<a href="{E(h)}">{E(t)}</a>' for h, t in sections)
    return (f'<div class="controls"><nav class="nav" aria-label="Lines"><span class="lab">Lines</span>{ln}</nav>'
            f'<nav class="nav dnav" aria-label="{E(depot_word)} and sections"><span class="lab">{E(depot_word)}</span>{dp}{sc}</nav>'
            f'<input type="search" id="q" placeholder="Find vehicle, e.g. {E(example)}" aria-label="Find vehicle number" inputmode="numeric">'
            f'<span id="hits" aria-live="polite"></span></div>')

SCRIPT = '''<script>
(function(){
  var c=document.querySelector('.controls'); if(!c) return;
  function h(){ document.documentElement.style.setProperty('--stick',(c.offsetHeight+8)+'px'); }
  h(); window.addEventListener('resize',h);
  var q=document.getElementById('q'), hits=document.getElementById('hits');
  var all=[].slice.call(document.querySelectorAll('[data-v]'));
  q.addEventListener('input',function(){
    var s=q.value.trim(), first=null, n=0;
    all.forEach(function(el){
      var on=s.length>=3 && el.offsetParent!==null && el.getAttribute('data-v').split('+').some(function(x){return x.indexOf(s)===0;});
      el.classList.toggle('hit',on);
      if(on){ n++; if(!first) first=el; }
    });
    hits.textContent = s.length>=3 ? (n ? n+' found' : 'not found') : '';
    if(first) first.scrollIntoView({block:'center'});
  });
  [].forEach.call(c.querySelectorAll('a[data-dep]'),function(a){
    a.addEventListener('click',function(e){
      var t=[].slice.call(document.querySelectorAll('[data-depot="'+a.getAttribute('data-dep')+'"]')).filter(function(x){return x.offsetParent!==null;})[0];
      if(t){ e.preventDefault(); t.scrollIntoView({block:'start'}); }
    });
  });
})();
</script>'''
