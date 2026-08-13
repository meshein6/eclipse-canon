"""The single-page app. HTML is emitted with four placeholders filled by build.py."""
HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Canon of Solar Eclipses</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Newsreader:ital,opsz,wght@1,6..72,300&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#070a10;--ink2:#0d121c;--rule:#1e2836;--dim:#5d6b80;--text:#aebac9;
 --corona:#f4f1e6;--ring:#e8a33d;--hybrid:#d76b52;--penumbra:#43536b;--now:#5fd9c0;--bronze:#b58b4c}
html,body{height:100%;overflow:hidden;background:var(--ink)}
body{font-family:"IBM Plex Mono",ui-monospace,monospace;color:var(--text);
 -webkit-font-smoothing:antialiased;display:flex;flex-direction:column;touch-action:manipulation}
header{padding:11px 14px 8px;border-bottom:1px solid var(--rule);display:flex;align-items:baseline;
 gap:3px 12px;flex-wrap:wrap;background:linear-gradient(180deg,#0b1119,var(--ink))}
h1{font-family:"Newsreader",Georgia,serif;font-style:italic;font-weight:300;font-size:19px;color:var(--corona);line-height:1}
.sub{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim)}
.sub b{color:var(--text);font-weight:500}
.bar{display:flex;gap:7px;align-items:center;flex-wrap:wrap;padding:7px 14px;
 border-bottom:1px solid var(--rule);background:var(--ink2)}
.seg{display:flex;border:1px solid var(--rule);border-radius:2px;overflow:hidden}
.seg button{font:inherit;font-size:10px;letter-spacing:.08em;text-transform:uppercase;background:transparent;
 color:var(--dim);border:0;padding:6px 10px;cursor:pointer;transition:.15s;white-space:nowrap}
.seg button+button{border-left:1px solid var(--rule)}
.seg button[aria-pressed="true"]{background:#182437;color:var(--corona)}
.seg button:hover{color:var(--text)}
.seg button:focus-visible{outline:2px solid var(--now);outline-offset:-2px}
.spacer{flex:1}
.keys{display:flex;gap:9px;flex-wrap:wrap}
.key{display:flex;align-items:center;gap:4px;font-size:9.5px;background:none;border:0;
 color:var(--dim);cursor:pointer;padding:3px 1px;font-family:inherit}
.key .sw{width:8px;height:8px;border-radius:50%;flex:none}
.key[aria-pressed="false"]{opacity:.3;text-decoration:line-through}
.key:focus-visible{outline:2px solid var(--now);outline-offset:2px}
main{flex:1;min-height:0;position:relative}
.pane{position:absolute;inset:0;display:none;flex-direction:column;min-height:0}
.pane.on{display:flex}
/* canon */
.canonCol{flex:1;display:flex;flex-direction:column;min-width:0;min-height:0}
#wrap{flex:1;position:relative;min-width:0;min-height:110px}
canvas#cv{display:block;width:100%;height:100%;cursor:grab;touch-action:none}
.readout{flex:none;border-top:1px solid var(--rule);background:var(--ink2);padding:6px 10px;
 display:flex;gap:8px;align-items:center;font-size:11px;min-height:34px}
.rotext{flex:1;display:flex;gap:3px 18px;align-items:baseline;flex-wrap:wrap;min-width:0}
.zbtns{display:flex;gap:4px;align-items:center;flex:none}
.zbtns button.b{padding:4px 9px;font-size:11px;line-height:1}
button.b.arw{padding:4px 8px;font-size:14px;line-height:1;flex:none}
.lbl{color:var(--dim);font-size:9px;letter-spacing:.12em;text-transform:uppercase;margin-right:5px}
.date{font-family:"Newsreader",serif;font-style:italic;color:var(--corona)}
.hint{color:var(--dim);font-size:10px}
em{font-style:normal;color:var(--corona)}
#detail{height:0;overflow:hidden;border-top:1px solid var(--rule);background:var(--ink2);
 transition:height .26s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;flex:none}
#detail.open{height:min(58%,410px)}
#detail .inner{overflow-y:auto;flex:1;min-height:0}
#map{display:block;background:#04070c;border-bottom:1px solid var(--rule);margin:0 auto;max-width:100%}
/* globe */
.dtools{display:flex;gap:7px;align-items:center;flex-wrap:wrap;padding:6px 10px;
 border-bottom:1px solid var(--rule);background:var(--ink)}
#globeBox{position:relative;width:100%;border-bottom:1px solid var(--rule);min-height:200px}
#globe{display:block;width:100%;height:100%;background:#04070c;cursor:grab;touch-action:none}
#skyBox{position:relative;width:100%;border-bottom:1px solid var(--rule);min-height:200px;display:none}
/* the scene is drawn in WebGL underneath and the readouts in 2-D on top, which
   keeps the text crisp and leaves the pointer handlers on one element */
#sky3d{position:absolute;inset:0;width:100%;height:100%;background:#04070c;display:none}
#sky{position:absolute;inset:0;width:100%;height:100%;background:#04070c;cursor:grab;touch-action:none}
#sky.gl{background:transparent}
.obsRow{display:none;gap:8px 12px;align-items:baseline;flex-wrap:wrap;padding:6px 10px;
 border-bottom:1px solid var(--rule);background:var(--ink2);font-size:10.5px}
#obsPos{color:var(--corona);font-size:11.5px;white-space:nowrap}
/* wide enough to sit beside the buttons on a desktop, and to drop to its own
   line rather than being squeezed into a column on a phone */
#obsInfo{flex:1 1 270px;min-width:0;color:var(--text);display:flex;gap:2px 10px;flex-wrap:wrap}
.tRow{display:flex;gap:8px;align-items:center;padding:7px 10px;border-bottom:1px solid var(--rule)}
.tRow input[type=range]{flex:1;min-width:0;accent-color:var(--ring);height:16px}
#tLab{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--corona);
 white-space:nowrap;min-width:74px;text-align:right}
#tDur{font-size:10px;color:var(--ring);white-space:nowrap;min-width:96px;text-align:right}
/* desktop: canon left, selected eclipse right; full width when nothing is selected */
@media (min-width:900px){
  #paneCanon{flex-direction:row}
  #detail{height:auto!important;width:0;border-top:0;border-left:1px solid var(--rule);
   transition:width .26s cubic-bezier(.4,0,.2,1)}
  #detail.open{width:min(46%,560px)}
}
/* expanded: the eclipse viewer takes the whole pane */
#detail.expanded{position:absolute;inset:0;width:100%!important;height:100%!important;
 z-index:5;border:0;border-left:0}
/* machine */
#mScroll{flex:1;overflow-y:auto;min-height:0}
#dialBox{position:relative;width:100%;aspect-ratio:1/1;max-height:56vh}
#dial{display:block;width:100%;height:100%}
#geom{display:block;width:100%;background:var(--ink);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.blk{padding:11px 14px;border-bottom:1px solid var(--rule)}
.blk:last-child{border-bottom:0}
.note{font-size:11px;line-height:1.6;color:var(--dim)}
.note b{color:var(--text);font-weight:500}
.note+.note{margin-top:8px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px 14px;font-size:11px}
.v{color:var(--corona);font-size:13px}
/* stepper */
.foot{padding:7px 12px;border-top:1px solid var(--rule);background:var(--ink2);
 display:flex;gap:8px;align-items:center;flex:none}
button.b{font:inherit;font-size:10.5px;background:transparent;color:var(--dim);
 border:1px solid var(--rule);padding:6px 10px;cursor:pointer;border-radius:2px;transition:.15s;white-space:nowrap}
button.b:hover:not(:disabled){color:var(--text);border-color:var(--dim)}
button.b:disabled{opacity:.3;cursor:default}
button.b.on{background:#182437;color:var(--corona);border-color:#2c3d52}
button.b:focus-visible{outline:2px solid var(--now);outline-offset:2px}
.lb{font-size:9px;letter-spacing:.06em;text-transform:uppercase;margin:0 3px;opacity:.85}
#stepInfo{flex:1;text-align:center;font-size:10.5px;line-height:1.35;min-width:0}
/* the masthead chip: an eclipse happening right now, or the next one along */
.chip{font:inherit;font-size:9px;letter-spacing:.1em;text-transform:uppercase;
 background:#111a26;border:1px solid var(--rule);color:var(--dim);border-radius:2px;
 padding:4px 8px;cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{color:var(--text);border-color:var(--dim)}
.chip.live{background:#3b1d1d;border-color:#8f3a33;color:#ffd9d2}
.chip .dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#e8574a;
 margin-right:6px;vertical-align:middle;animation:beat 1.6s ease-in-out infinite}
@keyframes beat{0%,100%{opacity:1}50%{opacity:.25}}
#tLive{white-space:nowrap}
#tLive.on{background:#3b1d1d;border-color:#8f3a33;color:#ffd9d2}
#stepInfo .d{font-family:"Newsreader",serif;font-style:italic;font-size:14px;color:var(--corona);display:block}
@media (max-width:520px){h1{font-size:16px}header{padding:9px 11px 6px}.bar{padding:6px 11px;gap:6px}
 .seg button{padding:6px 8px}.foot{padding:6px 9px;gap:6px}button.b{padding:6px 8px;font-size:10px}}
/* The ribbon's four full labels need about 800px on their own, so anything short
   of a wide desktop gets the short ones. Below 760 the date also moves to its own
   line rather than being crushed into a column between the buttons. */
.lbS{display:none}
@media (max-width:1024px){.lb{display:none}.lbS{display:inline}}
@media (max-width:760px){
  .foot{flex-wrap:wrap;justify-content:center;gap:5px}
  #stepInfo{flex:0 0 100%;order:-1;margin-bottom:2px}
  #gHint{display:none}
  .dtools{gap:5px}
  .tRow{gap:6px;padding:6px 8px}
  #tLab{min-width:64px}#tDur{min-width:auto}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<header><h1>Canon of Solar Eclipses</h1>
<div class="sub"><b>2000&nbsp;BCE&thinsp;&ndash;&thinsp;3000&nbsp;CE</b> &middot; <b id="nEcl">-</b> eclipses</div>
<div class="spacer"></div>
<button class="chip" id="liveChip"></button></header>
<div class="bar">
  <div class="seg" role="group" aria-label="View">
    <button id="tCanon" aria-pressed="true">Canon</button><button id="tMach" aria-pressed="false">Saros machine</button>
  </div>
  <div class="seg" id="axisSeg" role="group" aria-label="Vertical axis">
    <button id="mSaros" aria-pressed="true">Saros</button><button id="mInex" aria-pressed="false">Inex</button><button id="mGamma" aria-pressed="false">&gamma;</button>
  </div>
  <button class="b" id="szBtn" aria-pressed="false" style="font-size:10px;padding:6px 9px">&#9679; Even</button>
  <div class="spacer"></div>
  <div class="keys" role="group" aria-label="Filter by type">
    <button class="key" data-t="0" aria-pressed="true"><span class="sw" style="background:#f4f1e6"></span>Total</button>
    <button class="key" data-t="1" aria-pressed="true"><span class="sw" style="background:#e8a33d"></span>Annular</button>
    <button class="key" data-t="2" aria-pressed="true"><span class="sw" style="background:#d76b52"></span>Hybrid</button>
    <button class="key" data-t="3" aria-pressed="true"><span class="sw" style="background:#43536b"></span>Partial</button>
  </div>
</div>
<main>
  <section class="pane on" id="paneCanon">
    <div class="canonCol">
      <div id="wrap"><canvas id="cv"></canvas></div>
      <div class="readout">
        <div class="rotext" id="ro"></div>
        <div class="zbtns">
          <button class="b" id="zOut" aria-label="Zoom out">&minus;</button>
          <button class="b" id="zIn" aria-label="Zoom in">+</button>
          <button class="b" id="zRst" aria-label="Reset the view">Reset</button>
        </div>
      </div>
    </div>
    <div id="detail"><div class="inner">
      <div class="dtools">
        <button class="b arw" id="expand" aria-pressed="false" title="Expand to fill the pane">&#10530;</button>
        <div class="seg" role="group" aria-label="Projection">
          <button id="vGlobe" aria-pressed="true">Globe</button><button id="vFlat" aria-pressed="false">Flat</button>
        </div>
        <div class="zbtns">
          <button class="b" id="gOut" aria-label="Zoom out">&minus;</button>
          <button class="b" id="gIn" aria-label="Zoom in">+</button>
          <button class="b" id="gRst" aria-label="Centre on the eclipse">Fit</button>
        </div>
        <div class="spacer"></div>
        <span class="hint" id="gHint">drag to spin &middot; tap to stand there</span>
      </div>
      <div id="globeBox"><canvas id="globe"></canvas></div>
      <div id="skyBox"><canvas id="sky3d"></canvas><canvas id="sky"></canvas></div>
      <div class="tRow" id="tRow">
        <button class="b" id="tPlay" aria-label="Animate the eclipse">&#9654;</button>
        <button class="b" id="tSpeed" aria-label="Playback speed">&times;500</button>
        <button class="b" id="tLive" aria-pressed="false" aria-label="Follow the real clock">&#9679; Live</button>
        <input type="range" id="tSlide" min="0" max="1000" value="500" aria-label="Time through the eclipse">
        <span id="tLab">--:-- UT</span><span id="tDur"></span>
      </div>
      <div class="obsRow" id="obsRow">
        <span id="obsPos">nowhere yet</span>
        <button class="b" id="obsSun" title="Point the view at the Sun and zoom in">&#9788; Find the Sun</button>
        <button class="b on" id="obsTerr" aria-pressed="true" title="Fetch real elevation for this spot">&#9968; Terrain</button>
        <button class="b" id="obsClr" title="Stop standing anywhere">Clear</button>
        <span id="obsInfo"></span>
      </div>
      <canvas id="map"></canvas>
      <div class="blk"><div class="grid2" id="pStats"></div></div>
      <div class="blk"><div class="note" id="pNote"></div></div>
      <div class="blk"><div class="note" style="font-size:9.5px;opacity:.75">
        Eclipse geometry computed from lunar/solar theory. Elevation for the ground
        view is fetched as you use it from
        <a href="https://registry.opendata.aws/terrain-tiles/" style="color:var(--bronze)">AWS&nbsp;Terrain&nbsp;Tiles</a>
        (Mapzen terrarium encoding); everything else in the page is offline.
        Borders from Natural Earth
        (public domain); populated places from
        <a href="https://www.geonames.org/" style="color:var(--bronze)">GeoNames</a>,
        <a href="https://creativecommons.org/licenses/by/4.0/" style="color:var(--bronze)">CC&nbsp;BY&nbsp;4.0</a>.
      </div></div>
    </div></div>
  </section>
  <section class="pane" id="paneMach">
    <div id="mScroll">
      <div id="dialBox"><canvas id="dial"></canvas></div>
      <div class="blk"><div class="note">
        <b>The spiral is a counter, not an orbit.</b> Nothing on it is the Earth, Sun or Moon.
        Its 223 cells are 223 consecutive new moons &mdash; exactly one saros, 18&nbsp;years 11&nbsp;days.
        The pointer advances one cell per new moon and takes four turns to get round.
        Because eclipses repeat every 223 lunations, <b>every eclipse of a given saros series lands on the same cell, every time</b>.
        Saros 139 is always cell 77. This is the dial the Antikythera mechanism used.
      </div></div>
      <canvas id="geom"></canvas>
      <div class="blk"><div class="note">
        <b>These three panels are the real geometry.</b>
      </div>
      <div class="note"><b>1 &middot; Where the Moon is in its orbit.</b> Eclipses need the new moon to sit near a
        <b>node</b> &mdash; one of the two points where the Moon's tilted orbit crosses Earth's orbital plane.
        The angle <i>F</i> measures how far the Moon is from the ascending node. Only inside the shaded windows,
        within about 21&deg; of 0&deg; or 180&deg;, can a shadow reach us. <i>F</i> advances 30.67&deg; per lunation.</div>
      <div class="note"><b>2 &middot; How far away the Moon is.</b> Its orbit is an ellipse, so its apparent size
        changes. Near perigee the Moon covers the Sun completely &rarr; <b>total</b>. Near apogee it falls short
        and leaves a ring &rarr; <b>annular</b>. The angle <i>M&prime;</i> is its position around that ellipse,
        advancing 25.82&deg; per lunation.</div>
      <div class="note"><b>3 &middot; Where the shadow axis crosses Earth.</b> <i>Gamma</i> is the miss distance
        in Earth radii. Inside &plusmn;0.9972 the axis strikes the globe and someone sees a central eclipse; outside it,
        only a partial near a pole. Step through a saros series and watch gamma march from one limit to the other &mdash;
        that drift is what eventually kills the series.</div>
      </div>
      <div class="blk"><div class="note">
        <b>Why it nearly repeats.</b> Over 223 lunations <i>F</i> comes back
        <b>0.48&deg;</b> short and <i>M&prime;</i> <b>2.82&deg;</b> short of a clean return. Small enough that the next
        eclipse is almost a twin; large enough that after roughly 70 turns the series has walked off the node and ends.
        The saros is also 8 hours longer than a whole number of days, so each repeat lands about
        <b>115&deg; further west</b>.
      </div></div>
    </div>
  </section>
</main>
<div class="foot">
  <button class="b" id="prevT" aria-label="Previous eclipse chronologically">&#9664;<span class="lb">Prev chronological</span><span class="lbS">chrono</span></button>
  <button class="b" id="prev" aria-label="Previous in this saros series">&#9664;<span class="lb">Prev in saros</span><span class="lbS">saros</span></button>
  <div id="stepInfo"><span class="d">Select an eclipse</span><span class="hint" id="stepSub">tap a point on the canon</span></div>
  <button class="b" id="play" aria-label="Play through this saros series">&#9654;&#9654;</button>
  <button class="b" id="clr" aria-label="Clear selection">Clear</button>
  <button class="b" id="next" aria-label="Next in this saros series"><span class="lb">Next in saros</span><span class="lbS">saros</span>&#9654;</button>
  <button class="b" id="nextT" aria-label="Next eclipse chronologically"><span class="lb">Next chronological</span><span class="lbS">chrono</span>&#9654;</button>
</div>
<script>
const AB="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
const IX={};for(let i=0;i<64;i++)IX[AB[i]]=i;
const g2=(s,i)=>IX[s[i]]*64+IX[s[i+1]];
const g4=(s,i)=>((IX[s[i]]*64+IX[s[i+1]])*64+IX[s[i+2]])*64+IX[s[i+3]];
const gL=(s,i,lo,hi)=>lo+g2(s,i)/4095*(hi-lo);
const g3=(s,i)=>((IX[s[i]]*64+IX[s[i+1]])*64+IX[s[i+2]]);
const gL3=(s,i,lo,hi)=>lo+g3(s,i)/262143*(hi-lo);
const META="__META__",PIDX="__PIDX__",PDAT="__PDAT__";
const TYPES=["Total","Annular","Hybrid","Partial"],COL=["#f4f1e6","#e8a33d","#d76b52","#43536b"];
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const poly=t=>t.split("~").map(s=>{const o=[];
  for(let i=0;i<s.length;i+=4)o.push([gL(s,i,-180,180),gL(s,i+2,-90,90)]);return o;});
const LAND=poly("__COAST__"),BORD0=poly("__ADMIN0__"),BORD1=poly("__ADMIN1__");
/* populated places, sorted biggest first so the draw loop can stop early */
const PLC=(()=>{const d="__PLACES__",nm="__PNAMES__".split("~"),o=[];
  for(let i=0,j=0;i+7<=d.length;i+=7,j++)
    o.push([nm[j],gL3(d,i,-180,180),gL3(d,i+3,-90,90),IX[d[i+6]]]);
  return o;})();
const E=[];
for(let i=0,n=0;i<META.length;i+=31,n++){
  const c=g4(META,i),d=c%32,m=((c-d)/32)%12+1,y=Math.floor(c/384)-2000;
  const S=g2(META,i+4)-20,I=g2(META,i+9)-10;
  /* the last 16 characters of each record are the packed penumbral geometry at
     greatest eclipse. The viewer now carries its own Sun and Moon and recomputes
     that at whatever instant the clock is showing, so it reads past them. */
  E.push({i:n,y:y+((m-1)*30.6+d)/365.25,ymd:[y,m,d],S:S,I:I,t:IX[META[i+6]],
    g:gL(META,i+7,-1.6,1.6),w:g2(META,i+11),dur:g2(META,i+13),
    k:223*(I-271)+358*S+44,cell:0,p:null});
}
const MAXDUR=Math.max(...E.map(e=>e.dur));
for(const e of E)e.cell=((e.k%223)+223)%223;
for(let i=0;i<PIDX.length;i+=4){
  const at=g4(PIDX,i),b=PDAT.substr(i/4*151,151),pts=[],ws=[],ds=[],ts=[];
  for(let q=0;q<78;q+=6)pts.push([gL3(b,q,-180,180),gL3(b,q+3,-90,90)]);
  for(let q=86;q<112;q+=2)ws.push(g2(b,q));
  for(let q=112;q<138;q+=2)ds.push(g2(b,q));
  for(let q=138;q<151;q++)ts.push(IX[b[q]]);
  E[at].p={pts:pts,ut:g2(b,78),w:g2(b,80),dur:g2(b,82),span:g2(b,84),ws:ws,ds:ds,ts:ts};
}
const BY={saros:new Map(),inex:new Map()};
for(const e of E){for(const[k,v]of[["saros",e.S],["inex",e.I]]){
  if(!BY[k].has(v))BY[k].set(v,[]);BY[k].get(v).push(e);}}
for(const m of[BY.saros,BY.inex])for(const a of m.values())a.sort((p,q)=>p.y-q.y);
nEcl.textContent=E.length.toLocaleString();
const YEARS=E.map(e=>e.y);
const lo_=v=>{let a=0,b=YEARS.length;while(a<b){const m=(a+b)>>1;YEARS[m]<v?a=m+1:b=m;}return a;};
const BYK=new Map();for(const e of E)BYK.set(e.k,e);
const _n=new Date(),nowY=_n.getFullYear()+(_n.getMonth()*30.6+_n.getDate())/365.25;

let tab="canon",mode="saros",on=[true,true,true,true],hover=null,sel=null,yvOverride=null,timer=null;
let szDur=false;
function durScale(e){if(!szDur)return e.t===3?0.66:1;
  if(!e.dur)return 0.34;return Math.max(0.42,Math.min(2.5,0.40+1.25*Math.sqrt(e.dur/420)));}
let view={x0:nowY-30,x1:nowY+30,y0:0,y1:1};
const cv=document.getElementById("cv"),ctx=cv.getContext("2d"),ro=document.getElementById("ro");
let W=0,H=0;const PAD={l:52,r:12,t:14,b:42};
const baseYv=e=>mode==="saros"?e.S:mode==="inex"?e.I:e.g;
const yv=e=>yvOverride?yvOverride(e):baseYv(e);
const series=()=>mode==="gamma"?BY.saros:BY[mode];
function fitY(){if(mode==="gamma"){view.y0=-1.7;view.y1=1.7;return;}
  const a=lo_(view.x0),b=lo_(view.x1);let mn=1e9,mx=-1e9;
  for(let i=a;i<b;i++){const v=baseYv(E[i]);if(v<mn)mn=v;if(v>mx)mx=v;}
  if(mn>mx){mn=0;mx=100;}const p=Math.max(2,(mx-mn)*.06);view.y0=mn-p;view.y1=mx+p;}
fitY();
const sx=y=>PAD.l+(y-view.x0)/(view.x1-view.x0)*(W-PAD.l-PAD.r);
const sy=v=>PAD.t+(view.y1-v)/(view.y1-view.y0)*(H-PAD.t-PAD.b);
const ix=p=>view.x0+(p-PAD.l)/(W-PAD.l-PAD.r)*(view.x1-view.x0);
function resize(){const dp=Math.min(devicePixelRatio||1,2),r=cv.getBoundingClientRect();
  W=r.width;H=r.height;cv.width=Math.round(W*dp);cv.height=Math.round(H*dp);
  ctx.setTransform(dp,0,0,dp,0,0);draw();setReadout();}
new ResizeObserver(resize).observe(document.getElementById("wrap"));
const YSTEP=[2000,1000,500,200,100,50,20,10,5,2,1];
const yrLab=g=>{const y=Math.round(g);return y<=0?(1-y)+" BCE":String(y);};
function ticks(){const span=view.x1-view.x0,px=W-PAD.l-PAD.r;
  /* YSTEP descends, so every coarse step clears the spacing test; take the
     finest one that still does, otherwise labels land 2000 years apart. */
  if(span>=3){let maj=YSTEP.filter(s=>px/(span/s)>58).pop()||YSTEP[0];
    let mi=YSTEP[Math.min(YSTEP.indexOf(maj)+1,YSTEP.length-1)];
    if(px/(span/mi)<9)mi=maj;const M=[],m=[];
    for(let g=Math.ceil(view.x0/mi)*mi;g<=view.x1;g+=mi)(Math.abs(g%maj)<1e-9?M:m).push(g);
    return{maj:M,min:m,fmt:yrLab,sub:null};}
  const M=[],m=[],y0=Math.floor(view.x0),y1=Math.ceil(view.x1);
  const st=px/(span*12)>32?1:(px/(span*4)>32?3:6);
  for(let y=y0;y<=y1;y++)for(let k=0;k<12;k+=st){const g=y+(k*30.6+15)/365.25;
    if(g<view.x0||g>view.x1)continue;(k===0?M:m).push({v:g,k:k});}
  return{maj:M.map(o=>o.v),min:m.map(o=>o.v),fmt:g=>yrLab(Math.floor(g+.002)),
    sub:[...M,...m].map(o=>({v:o.v,t:MON[o.k]}))};}
const nsY=(s,t)=>{const r=s/t,p=Math.pow(10,Math.floor(Math.log10(r))),n=r/p;
  return(n<1.5?1:n<3.5?2:n<7.5?5:10)*p;};
function draw(){
  if(!W||!H)return;
  ctx.clearRect(0,0,W,H);
  const plotH=H-PAD.t-PAD.b,T=ticks(),ys=nsY(view.y1-view.y0,7);
  ctx.save();ctx.beginPath();ctx.rect(PAD.l,PAD.t,W-PAD.l-PAD.r,plotH);ctx.clip();
  ctx.lineWidth=1;ctx.strokeStyle="#101822";ctx.beginPath();
  for(const g of T.min){const X=Math.round(sx(g))+.5;ctx.moveTo(X,PAD.t);ctx.lineTo(X,H-PAD.b);}ctx.stroke();
  ctx.strokeStyle="#17222f";ctx.beginPath();
  for(const g of T.maj){const X=Math.round(sx(g))+.5;ctx.moveTo(X,PAD.t);ctx.lineTo(X,H-PAD.b);}ctx.stroke();
  ctx.strokeStyle="#141d29";ctx.beginPath();
  for(let g=Math.ceil(view.y0/ys)*ys;g<=view.y1;g+=ys){const Y=Math.round(sy(g))+.5;
    ctx.moveTo(PAD.l,Y);ctx.lineTo(W-PAD.r,Y);}ctx.stroke();
  if(mode==="gamma"||yvOverride){ctx.strokeStyle="#25344a";ctx.setLineDash([3,4]);ctx.beginPath();
    for(const v of[-0.9972,0.9972]){const Y=Math.round(sy(v))+.5;
      if(Y>PAD.t&&Y<H-PAD.b){ctx.moveTo(PAD.l,Y);ctx.lineTo(W-PAD.r,Y);}}ctx.stroke();ctx.setLineDash([]);}
  const act=sel||hover,SR=series(),key=e=>mode==="inex"?e.I:e.S,hk=act?key(act):null;
  ctx.strokeStyle=hk!==null?"rgba(26,36,50,.55)":"rgba(38,52,70,.85)";ctx.lineWidth=1;ctx.beginPath();
  for(const[k,arr]of SR){if(k===hk)continue;
    if(arr[arr.length-1].y<view.x0||arr[0].y>view.x1)continue;
    for(let i=0;i<arr.length;i++){const X=sx(arr[i].y),Y=sy(yv(arr[i]));i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}}
  ctx.stroke();
  if(hk!==null&&SR.has(hk)){const arr=SR.get(hk);ctx.strokeStyle="rgba(95,217,192,.9)";ctx.lineWidth=1.7;
    ctx.beginPath();
    for(let i=0;i<arr.length;i++){const X=sx(arr[i].y),Y=sy(yv(arr[i]));i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}
    ctx.stroke();}
  const r=Math.max(1.1,Math.min(4.4,320/Math.sqrt(view.x1-view.x0)));
  const a0=Math.max(0,lo_(view.x0)-4),a1=Math.min(E.length,lo_(view.x1)+4),sq=r<1.9;
  for(let pass=0;pass<2;pass++){
    for(let t=0;t<4;t++){if(!on[t])continue;
      ctx.globalAlpha=pass?(t===3?.7:1):(hk===null?(t===3?.7:1):.14);
      ctx.fillStyle=COL[t];ctx.beginPath();
      for(let i=a0;i<a1;i++){const e=E[i];if(e.t!==t)continue;
        const lit=key(e)===hk;if(pass?!lit:lit)continue;
        const X=sx(e.y);if(X<PAD.l-8||X>W-PAD.r+8)continue;
        const Y=sy(yv(e));if(Y<PAD.t-8||Y>H-PAD.b+8)continue;
        const rr=r*durScale(e);
        if(sq)ctx.rect(X-rr,Y-rr,rr*2,rr*2);else{ctx.moveTo(X+rr,Y);ctx.arc(X,Y,rr,0,6.2832);}}
      ctx.fill();}
    if(hk===null)break;}
  ctx.globalAlpha=1;
  if(szDur){
    const lx=W-PAD.r-14,ly=PAD.t+13;
    ctx.textAlign="right";ctx.textBaseline="middle";
    ctx.font='8.5px "IBM Plex Mono",monospace';
    let off=0;
    for(const d of [120,300,450]){
      const rr=r*Math.max(0.42,Math.min(2.5,0.40+1.25*Math.sqrt(d/420)));
      const rr2=Math.max(rr,2.2);
      ctx.fillStyle="rgba(244,241,230,.55)";
      ctx.beginPath();ctx.arc(lx-off-rr2,ly,rr2,0,6.2832);ctx.fill();
      ctx.fillStyle="#4d5c72";
      ctx.fillText(Math.round(d/60)+"m",lx-off-rr2*2-3,ly);
      off+=rr2*2+26;
    }
  }
  if(nowY>view.x0&&nowY<view.x1){const X=Math.round(sx(nowY))+.5;
    ctx.strokeStyle="rgba(95,217,192,.5)";ctx.setLineDash([2,3]);ctx.beginPath();
    ctx.moveTo(X,PAD.t);ctx.lineTo(X,H-PAD.b);ctx.stroke();ctx.setLineDash([]);
    ctx.fillStyle="#5fd9c0";ctx.font='500 9px "IBM Plex Mono",monospace';
    ctx.textAlign="left";ctx.textBaseline="top";ctx.fillText("NOW",X+4,PAD.t+2);}
  for(const e of[hover,sel]){if(!e)continue;const X=sx(e.y),Y=sy(yv(e));
    ctx.strokeStyle=e===sel?"#f4f1e6":"#5fd9c0";ctx.lineWidth=e===sel?1.4:1;
    ctx.beginPath();ctx.arc(X,Y,Math.max(r,2.5)+5,0,6.2832);ctx.stroke();}
  ctx.restore();
  ctx.strokeStyle="#1e2836";ctx.lineWidth=1;ctx.beginPath();
  ctx.moveTo(PAD.l+.5,PAD.t);ctx.lineTo(PAD.l+.5,H-PAD.b+.5);ctx.lineTo(W-PAD.r,H-PAD.b+.5);ctx.stroke();
  const yb=H-PAD.b;
  ctx.strokeStyle="#27364a";ctx.beginPath();
  for(const g of T.min){const X=Math.round(sx(g))+.5;if(X<PAD.l||X>W-PAD.r)continue;
    ctx.moveTo(X,yb+.5);ctx.lineTo(X,yb+4.5);}ctx.stroke();
  ctx.strokeStyle="#41546e";ctx.beginPath();
  for(const g of T.maj){const X=Math.round(sx(g))+.5;if(X<PAD.l||X>W-PAD.r)continue;
    ctx.moveTo(X,yb+.5);ctx.lineTo(X,yb+8.5);}ctx.stroke();
  ctx.fillStyle="#7f8fa4";ctx.font='10px "IBM Plex Mono",monospace';ctx.textAlign="center";ctx.textBaseline="top";
  for(const g of T.maj){const X=sx(g);if(X<PAD.l+22||X>W-PAD.r-22)continue;ctx.fillText(T.fmt(g),X,yb+11);}
  if(T.sub){ctx.fillStyle="#4d5c72";ctx.font='8.5px "IBM Plex Mono",monospace';
    for(const o of T.sub){const X=sx(o.v);if(X<PAD.l+10||X>W-PAD.r-10)continue;ctx.fillText(o.t,X,yb+25);}}
  const sp=view.x1-view.x0;
  ctx.fillStyle="#3f4c5e";ctx.font='9px "IBM Plex Mono",monospace';ctx.textAlign="right";
  ctx.fillText(sp>=3?("span "+(sp>=1000?(sp/1000).toFixed(1)+" kyr":Math.round(sp)+" yr")):
    ("span "+Math.round(sp*12)+" mo"),W-PAD.r,yb+(T.sub?25:11));
  ctx.fillStyle="#5d6b80";ctx.font='9.5px "IBM Plex Mono",monospace';
  ctx.textAlign="right";ctx.textBaseline="middle";
  const dc=ys<1?1:0;
  for(let g=Math.ceil(view.y0/ys)*ys;g<=view.y1;g+=ys){const Y=sy(g);
    if(Y<PAD.t+6||Y>H-PAD.b-6)continue;ctx.fillText(g.toFixed(dc),PAD.l-7,Y);}
  ctx.save();ctx.translate(11,PAD.t+plotH/2);ctx.rotate(-Math.PI/2);
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillStyle="#3f4c5e";
  ctx.font='9px "IBM Plex Mono",monospace';
  ctx.fillText(mode==="saros"?"SAROS SERIES":mode==="inex"?"INEX SERIES":"GAMMA",0,0);ctx.restore();
}
const dstr=e=>{const[y,m,d]=e.ymd;return(y<=0?(1-y)+" BCE":y)+" "+MON[m-1]+" "+String(d).padStart(2,"0");};
const utf=m=>String(Math.floor(m/60)).padStart(2,"0")+":"+String(m%60).padStart(2,"0")+" UT";
const fd=s=>Math.floor(s/60)+"m "+String(s%60).padStart(2,"0")+"s";
/* whole eclipses run for hours, so minutes stop reading past about ninety */
const fdl=s=>{const m=Math.round(s/60);
  return m>=90?Math.floor(m/60)+"h "+String(m%60).padStart(2,"0")+"m":fd(s);};
function setReadout(){
  const e=hover||sel;
  if(!e){const c=(view.x0+view.x1)/2,a=new Set();
    for(let i=lo_(c-9.02);i<lo_(c+9.02);i++)a.add(E[i].S);
    ro.innerHTML='<span><span class="lbl">In view</span><em>'+(lo_(view.x1)-lo_(view.x0)).toLocaleString()+
      '</em></span><span><span class="lbl">Saros running</span><em>'+a.size+
      '</em></span><span class="hint">'+(szDur?'dot size = central duration':'drag to pan &middot; scroll to zoom &middot; tap a point &middot; dbl-click resets')+'</span>';return;}
  ro.innerHTML='<span class="date" style="font-size:15px">'+dstr(e)+'</span>'+
    '<span><span class="lbl">Type</span><em style="color:'+COL[e.t]+'">'+TYPES[e.t]+'</em></span>'+
    '<span><span class="lbl">Saros</span><em>'+e.S+'</em></span>'+
    '<span><span class="lbl">Inex</span><em>'+e.I+'</em></span>'+
    '<span><span class="lbl">Gamma</span><em>'+e.g.toFixed(3)+'</em></span>'+
    (e.dur?'<span><span class="lbl">Central</span><em>'+fd(e.dur)+'</em></span>':'');
}
/* ---------- map ---------- */
const detail=document.getElementById("detail"),mp=document.getElementById("map"),mc=mp.getContext("2d");
function drawMap(e){
  const dp=Math.min(devicePixelRatio||1,2);
  const availW=(mp.parentElement&&mp.parentElement.clientWidth)||360;
  const availH=Math.max(110,(detail.clientHeight||380)*0.62);
  let w=availW,h=Math.round(w/2);
  const cap=Math.max(105,Math.min(availH,290));
  if(h>cap){h=Math.round(cap);w=Math.round(h*2);}
  mp.style.width=w+"px";mp.style.height=h+"px";
  mp.width=Math.round(w*dp);mp.height=Math.round(h*dp);mc.setTransform(dp,0,0,dp,0,0);
  mc.fillStyle="#04070c";mc.fillRect(0,0,w,h);
  const X=l=>(l+180)/360*w,Y=b=>(90-b)/180*h;
  mc.strokeStyle="#111a25";mc.lineWidth=1;mc.beginPath();
  for(let l=-150;l<180;l+=30){mc.moveTo(X(l),0);mc.lineTo(X(l),h);}
  for(let b=-60;b<90;b+=30){mc.moveTo(0,Y(b));mc.lineTo(w,Y(b));}mc.stroke();
  mc.strokeStyle="#26364a";mc.lineWidth=.8;mc.beginPath();
  for(const p of LAND){for(let i=0;i<p.length;i++){const x=X(p[i][0]),y=Y(p[i][1]);i?mc.lineTo(x,y):mc.moveTo(x,y);}mc.closePath();}
  mc.stroke();
  if(e&&e.p){
    const arr=BY.saros.get(e.S),i=arr.indexOf(e);
    for(const[ev,col,lw]of[[arr[i-2],"#6d5430",1.2],[arr[i-1],"#b58b4c",1.5],[e,COL[e.t],2.2]]){
      if(!ev||!ev.p)continue;
      const pts=smooth(ev.p,80),segs=[[]];
      for(let q=0;q<pts.length;q++){
        if(q&&Math.abs(pts[q][0]-pts[q-1][0])>180)segs.push([]);
        segs[segs.length-1].push(pts[q]);}
      mc.lineCap="round";mc.lineJoin="round";mc.strokeStyle=col;mc.lineWidth=lw;mc.beginPath();
      for(const g of segs){if(g.length<2)continue;
        g.forEach((p,q)=>q?mc.lineTo(X(p[0]),Y(p[1])):mc.moveTo(X(p[0]),Y(p[1])));}
      mc.stroke();
      const md=pts[pts.length>>1];
      mc.fillStyle=col;mc.beginPath();mc.arc(X(md[0]),Y(md[1]),ev===e?3.2:2,0,6.2832);mc.fill();
      if(ev!==e){mc.fillStyle="#5d6b80";mc.font='8px "IBM Plex Mono",monospace';mc.textAlign="center";
        mc.fillText(ev.ymd[0],X(md[0]),Y(md[1])-6);}}
  }else if(e){
    mc.fillStyle="#5d6b80";mc.font='10px "IBM Plex Mono",monospace';mc.textAlign="center";
    mc.fillText(e.t===3?"no central path \u2014 the axis misses Earth":"path not computed before 1000 CE",w/2,h/2);}
  mc.strokeStyle="#1e2836";mc.strokeRect(.5,.5,w-1,h-1);
}
/* ---------- globe ---------- */
const globe=document.getElementById("globe"),gb=globe.getContext("2d");
const globeBox=document.getElementById("globeBox");
const RAD=Math.PI/180;
const GZMAX=120;
let gLon=0,gLat=20,gZoom=1,detView="globe",tFrac=.5,tTimer=null,gSize=0;
const llv=(lon,lat)=>{const c=Math.cos(lat*RAD);
  return[c*Math.cos(lon*RAD),c*Math.sin(lon*RAD),Math.sin(lat*RAD)];};
/* mirrors jd_to_date in eclipses.py: Julian calendar before 1582 Oct 15 */
function jdOf(y,m,d,mins){let Y=y,M=m;if(M<=2){Y-=1;M+=12;}
  const greg=(y>1582)||(y===1582&&(m>10||(m===10&&d>=15)));
  const B=greg?(2-Math.floor(Y/100)+Math.floor(Math.floor(Y/100)/4)):0;
  return Math.floor(365.25*(Y+4716))+Math.floor(30.6001*(M+1))+d+B-1524.5+mins/1440;}
/* and back again, so a clock that runs past midnight still names the right day */
function calOf(jd){const z=Math.floor(jd+0.5),f=jd+0.5-z;
  let A=z;if(z>=2299161){const al=Math.floor((z-1867216.25)/36524.25);
    A=z+1+al-Math.floor(al/4);}
  const B=A+1524,C=Math.floor((B-122.1)/365.25),D=Math.floor(365.25*C),
        E=Math.floor((B-D)/30.6001);
  const day=B-D-Math.floor(30.6001*E),m=E<14?E-1:E-13,y=m>2?C-4716:C-4715;
  return{y:y,m:m,d:day,mins:f*1440};}

/* ---------- Sun and Moon ----------

   Enough of a real ephemeris to stand on the ground and look up. Meeus,
   Astronomical Algorithms: the solar theory of ch.25, the truncated ELP-2000/82
   lunar series of ch.47, nutation from ch.22, and Laskar's obliquity, which is
   the one term here that stays honest across five millennia. Everything comes
   out as vectors in kilometres in an equatorial-of-date frame, because the
   observer, the shadow axis and the two discs all want vectors, not angles.

   Checked against pyephem at matched terrestrial time: the Moon agrees to about
   10 arcsec over 1000-2000 CE and 25 arcsec over the rest of the canon, the Sun
   to about 25 arcsec throughout. Both are far inside the 30-arcmin discs being
   drawn. */
const sinD=x=>Math.sin(x*RAD),cosD=x=>Math.cos(x*RAD);
const clamp1=v=>Math.max(-1,Math.min(1,v));
/* ch.47 table A: D, M, M', F, then the longitude and distance coefficients */
const MLR=[0,0,1,0,6288774,-20905355,2,0,-1,0,1274027,-3699111,2,0,0,0,658314,-2955968,
0,0,2,0,213618,-569925,0,1,0,0,-185116,48888,0,0,0,2,-114332,-3149,
2,0,-2,0,58793,246158,2,-1,-1,0,57066,-152138,2,0,1,0,53322,-170733,
2,-1,0,0,45758,-204586,0,1,-1,0,-40923,-129620,1,0,0,0,-34720,108743,
0,1,1,0,-30383,104755,2,0,0,-2,15327,10321,0,0,1,2,-12528,0,
0,0,1,-2,10980,79661,4,0,-1,0,10675,-34782,0,0,3,0,10034,-23210,
4,0,-2,0,8548,-21636,2,1,-1,0,-7888,24208,2,1,0,0,-6766,30824,
1,0,-1,0,-5163,-8379,1,1,0,0,4987,-16675,2,-1,1,0,4036,-12831,
2,0,2,0,3994,-10445,4,0,0,0,3861,-11650,2,0,-3,0,3665,14403,
0,1,-2,0,-2689,-7003,2,0,-1,2,-2602,0,2,-1,-2,0,2390,10056,
1,0,1,0,-2348,6322,2,-2,0,0,2236,-9884,0,1,2,0,-2120,5751,
0,2,0,0,-2069,0,2,-2,-1,0,2048,-4950,2,0,1,-2,-1773,4130,
2,0,0,2,-1595,0,4,-1,-1,0,1215,-3958,0,0,2,2,-1110,0,
3,0,-1,0,-892,3258,2,1,1,0,-810,2616,4,-1,-2,0,759,-1897,
0,2,-1,0,-713,-2117,2,2,-1,0,-700,2354,2,1,-2,0,691,0,
2,-1,0,-2,596,0,4,0,1,0,549,-1423,0,0,4,0,537,-1117,
4,-1,0,0,520,-1571,1,0,-2,0,-487,-1739,2,1,0,-2,-399,0,
0,0,2,-2,-381,-4421,1,1,1,0,351,0,3,0,-2,0,-340,0,
4,0,-3,0,330,0,2,-1,2,0,327,0,0,2,1,0,-323,1165,
1,1,-1,0,299,0,2,0,3,0,294,0,2,0,-1,-2,0,8752];
/* table B: the same arguments, latitude only */
const MBT=[0,0,0,1,5128122,0,0,1,1,280602,0,0,1,-1,277693,2,0,0,-1,173237,
2,0,-1,1,55413,2,0,-1,-1,46271,2,0,0,1,32573,0,0,2,1,17198,
2,0,1,-1,9266,0,0,2,-1,8822,2,-1,0,-1,8216,2,0,-2,-1,4324,
2,0,1,1,4200,2,1,0,-1,-3359,2,-1,-1,1,2463,2,-1,0,1,2211,
2,-1,-1,-1,2065,0,1,-1,-1,-1870,4,0,-1,-1,1828,0,1,0,1,-1794,
0,0,0,3,-1749,0,1,-1,1,-1565,1,0,0,1,-1491,0,1,1,1,-1475,
0,1,1,-1,-1410,0,1,0,-1,-1344,1,0,0,-1,-1335,0,0,3,1,1107,
4,0,0,-1,1021,4,0,-1,1,833,0,0,1,-3,777,4,0,-2,1,671,
2,0,0,-3,607,2,0,2,-1,596,2,-1,1,-1,491,2,0,-2,1,-451,
0,0,3,-1,439,2,0,2,1,422,2,0,-3,-1,421,2,1,-1,1,-366,
2,1,0,1,-351,4,0,0,1,331,2,-1,1,1,315,2,-2,0,-1,302,
0,0,1,3,-283,2,1,1,-1,-229,1,1,0,-1,223,1,1,0,1,223,
0,1,-2,-1,-220,2,1,-1,-1,-220,1,0,1,1,-185,2,-1,-2,-1,181,
0,1,2,1,-177,4,0,-2,-1,176,4,-1,-1,-1,166,1,0,1,-1,-164,
4,0,1,-1,132,1,0,-1,-1,-119,4,-1,0,-1,115,2,-2,0,1,107];
/* Espenak & Meeus delta-T, seconds; the same branches as deltaT() in geometry.py */
function deltaT(y){let t,u;
  if(y<-500){u=(y-1820)/100;return -20+32*u*u;}
  if(y<500){u=y/100;return 10583.6-1014.41*u+33.78311*u*u-5.952053*u*u*u
    -0.1798452*Math.pow(u,4)+0.022174192*Math.pow(u,5)+0.0090316521*Math.pow(u,6);}
  if(y<1600){u=(y-1000)/100;return 1574.2-556.01*u+71.23472*u*u+0.319781*u*u*u
    -0.8503463*Math.pow(u,4)-0.005050998*Math.pow(u,5)+0.0083572073*Math.pow(u,6);}
  if(y<1700){t=y-1600;return 120-0.9808*t-0.01532*t*t+t*t*t/7129;}
  if(y<1800){t=y-1700;return 8.83+0.1603*t-0.0059285*t*t+0.00013336*t*t*t-Math.pow(t,4)/1174000;}
  if(y<1860){t=y-1800;return 13.72-0.332447*t+0.0068612*t*t+0.0041116*t*t*t
    -0.00037436*Math.pow(t,4)+0.0000121272*Math.pow(t,5)-0.0000001699*Math.pow(t,6)
    +0.000000000875*Math.pow(t,7);}
  if(y<1900){t=y-1860;return 7.62+0.5737*t-0.251754*t*t+0.01680668*t*t*t
    -0.0004473624*Math.pow(t,4)+Math.pow(t,5)/233174;}
  if(y<1920){t=y-1900;return -2.79+1.494119*t-0.0598939*t*t+0.0061966*t*t*t-0.000197*Math.pow(t,4);}
  if(y<1941){t=y-1920;return 21.20+0.84493*t-0.076100*t*t+0.0020936*t*t*t;}
  if(y<1961){t=y-1950;return 29.07+0.407*t-t*t/233+t*t*t/2547;}
  if(y<1986){t=y-1975;return 45.45+1.067*t-t*t/260-t*t*t/718;}
  if(y<2005){t=y-2000;return 63.86+0.3345*t-0.060374*t*t+0.0017275*t*t*t
    +0.000651814*Math.pow(t,4)+0.00002373599*Math.pow(t,5);}
  if(y<2050){t=y-2000;return 62.92+0.32217*t+0.005589*t*t;}
  if(y<2150)return -20+32*Math.pow((y-1820)/100,2)-0.5628*(2150-y);
  u=(y-1820)/100;return -20+32*u*u;}
const jdYear=jd=>2000+(jd-2451545.0)/365.25;
/* nutation in longitude and obliquity (arcsec), and the true obliquity */
function nut(T){const O=125.04452-1934.136261*T,L=280.4665+36000.7698*T,
        Lm=218.3165+481267.8813*T,u=T/100;
  const dp=-17.20*sinD(O)-1.32*sinD(2*L)-0.23*sinD(2*Lm)+0.21*sinD(2*O);
  const de=9.20*cosD(O)+0.57*cosD(2*L)+0.10*cosD(2*Lm)-0.09*cosD(2*O);
  /* Laskar: the textbook cubic drifts by minutes of arc at the ends of this canon */
  const e0=23.43929111-(4680.93*u+1.55*u*u-1999.25*Math.pow(u,3)+51.38*Math.pow(u,4)
    +249.67*Math.pow(u,5)+39.05*Math.pow(u,6)-7.12*Math.pow(u,7)-27.87*Math.pow(u,8)
    -5.79*Math.pow(u,9)-2.45*Math.pow(u,10))/3600;
  return{dp:dp,de:de,eps:e0+de/3600};}
/* ecliptic lon/lat/distance to an equatorial-of-date vector, km */
function eqv(lon,lat,r,eps){const cl=cosD(lat),ce=cosD(eps),se=sinD(eps);
  const x=cl*cosD(lon),y=cl*sinD(lon),z=sinD(lat);
  return[r*x,r*(y*ce-z*se),r*(y*se+z*ce)];}
const AUKM=149597870.7,RE=6378.137,EF2=0.00669437999014,RSUNKM=696000,RMOONKM=1737.4;
function sunVec(T,n){
  const L0=280.46646+36000.76983*T+0.0003032*T*T;
  const M=357.52911+35999.05029*T-0.0001537*T*T;
  const e=0.016708634-0.000042037*T-0.0000001267*T*T;
  const C=(1.914602-0.004817*T-0.000014*T*T)*sinD(M)+(0.019993-0.000101*T)*sinD(2*M)
    +0.000289*sinD(3*M);
  const R=1.000001018*(1-e*e)/(1+e*cosD(M+C));
  const lam=L0+C-0.00569-0.00478*sinD(125.04-1934.136*T);   /* aberration, nutation */
  return eqv(lam,0,R*AUKM,n.eps);}
function moonVec(T,n){
  const Lp=218.3164477+481267.88123421*T-0.0015786*T*T+T*T*T/538841-Math.pow(T,4)/65194000;
  const D=297.8501921+445267.1114034*T-0.0018819*T*T+T*T*T/545868-Math.pow(T,4)/113065000;
  const M=357.5291092+35999.0502909*T-0.0001536*T*T+T*T*T/24490000;
  const Mp=134.9633964+477198.8675055*T+0.0087414*T*T+T*T*T/69699-Math.pow(T,4)/14712000;
  const F=93.2720950+483202.0175233*T-0.0036539*T*T-T*T*T/3526000+Math.pow(T,4)/863310000;
  const E=1-0.002516*T-0.0000074*T*T;
  const A1=119.75+131.849*T,A2=53.09+479264.290*T,A3=313.45+481266.484*T;
  let sl=0,sr=0,sb=0;
  for(let i=0;i<MLR.length;i+=6){const a=MLR[i]*D+MLR[i+1]*M+MLR[i+2]*Mp+MLR[i+3]*F;
    const f=MLR[i+1]===0?1:(Math.abs(MLR[i+1])===1?E:E*E);
    sl+=MLR[i+4]*f*sinD(a);sr+=MLR[i+5]*f*cosD(a);}
  for(let i=0;i<MBT.length;i+=5){const a=MBT[i]*D+MBT[i+1]*M+MBT[i+2]*Mp+MBT[i+3]*F;
    const f=MBT[i+1]===0?1:(Math.abs(MBT[i+1])===1?E:E*E);
    sb+=MBT[i+4]*f*sinD(a);}
  sl+=3958*sinD(A1)+1962*sinD(Lp-F)+318*sinD(A2);
  sb+=-2235*sinD(Lp)+382*sinD(A3)+175*sinD(A1-F)+175*sinD(A1+F)
     +127*sinD(Lp-Mp)-115*sinD(Lp+Mp);
  return eqv(Lp+sl/1e6+n.dp/3600,sb/1e6,385000.56+sr/1000,n.eps);}
/* One evaluation per instant, cached: every caller wants the same three things.
   Positions are computed at TD, the Earth's rotation at UT — that distinction is
   the whole reason delta-T is here. */
let _skyC={jd:null};
function sky(jdUT){
  if(_skyC.jd===jdUT)return _skyC;
  const Tu=(jdUT-2451545.0)/36525;
  const T=(jdUT+deltaT(jdYear(jdUT))/86400-2451545.0)/36525,n=nut(T);
  let th=280.46061837+360.98564736629*(jdUT-2451545.0)+0.000387933*Tu*Tu-Tu*Tu*Tu/38710000;
  th=(((th+n.dp*cosD(n.eps)/3600)%360)+360)%360;
  _skyC={jd:jdUT,S:sunVec(T,n),M:moonVec(T,n),th:th};
  return _skyC;}
const vlen=a=>Math.hypot(a[0],a[1],a[2]);
const vdot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
function subsolar(jd){const s=sky(jd),S=s.S,d=vlen(S);
  return{lat:Math.asin(clamp1(S[2]/d))/RAD,
         lon:((Math.atan2(S[1],S[0])/RAD-s.th)%360+540)%360-180};}
/* The shadow axis in Earth-fixed coordinates, which is all the globe needs:
   the axis direction pointing away from the Sun, the foot of its perpendicular
   from Earth's centre, that distance in Earth radii (gamma), and the penumbral
   cone radius there. Defined whether or not the axis strikes Earth, which is
   what lets a partial eclipse draw the region that sees it. */
function axisAt(jd){const s=sky(jd);
  const u=[s.M[0]-s.S[0],s.M[1]-s.S[1],s.M[2]-s.S[2]],dsm=vlen(u);
  u[0]/=dsm;u[1]/=dsm;u[2]/=dsm;
  const t0=-vdot(s.M,u),P=[s.M[0]+t0*u[0],s.M[1]+t0*u[1],s.M[2]+t0*u[2]];
  const L1=(RMOONKM+Math.abs(t0)*(RSUNKM+RMOONKM)/dsm)/RE;
  const c=cosD(s.th),sn=sinD(s.th);
  const fx=v=>[v[0]*c+v[1]*sn,-v[0]*sn+v[1]*c,v[2]];
  const Pf=fx(P);
  return{u:fx(u),P:[Pf[0]/RE,Pf[1]/RE,Pf[2]/RE],g:vlen(P)/RE,L1:L1};}
/* Where an observer stands, and what the Sun and Moon look like from there.
   The Moon's parallax is over a degree — two of its own diameters — so the
   topocentric step is not a refinement here, it is the whole question of
   whether you see the eclipse at all. */
function local(jd,lat,lon){const s=sky(jd);
  const t=(s.th+lon)*RAD,la=lat*RAD,sl=Math.sin(la),cl=Math.cos(la);
  const N=RE/Math.sqrt(1-EF2*sl*sl),ct=Math.cos(t),st=Math.sin(t);
  const O=[N*cl*ct,N*cl*st,N*(1-EF2)*sl];
  const zen=[cl*ct,cl*st,sl],est=[-st,ct,0],nor=[-sl*ct,-sl*st,cl];
  const Sv=[s.S[0]-O[0],s.S[1]-O[1],s.S[2]-O[2]];
  const Mv=[s.M[0]-O[0],s.M[1]-O[1],s.M[2]-O[2]];
  const dS=vlen(Sv),dM=vlen(Mv);
  const uS=[Sv[0]/dS,Sv[1]/dS,Sv[2]/dS],uM=[Mv[0]/dM,Mv[1]/dM,Mv[2]/dM];
  const hz=v=>({alt:Math.asin(clamp1(vdot(v,zen)))/RAD,
                az:((Math.atan2(vdot(v,est),vdot(v,nor))/RAD)+360)%360});
  const rS=Math.asin(RSUNKM/dS)/RAD,rM=Math.asin(RMOONKM/dM)/RAD;
  const sep=Math.acos(clamp1(vdot(uS,uM)))/RAD;
  const mag=Math.max(0,(rS+rM-sep)/(2*rS));
  /* east/north/up components as well, since that is the frame the sky is drawn in */
  const toH=v=>[vdot(v,est),vdot(v,nor),vdot(v,zen)];
  return{S:hz(uS),M:hz(uM),hS:toH(uS),hM:toH(uM),toH:toH,
         zen:zen,est:est,nor:nor,
         rS:rS,rM:rM,sep:sep,mag:mag,obsc:overlap(rS,rM,sep),
         tot:sep<rM-rS,ann:sep<rS-rM};}
/* fraction of the solar disc the Moon covers: the classic two-circle lens */
function overlap(r1,r2,d){
  if(d>=r1+r2)return 0;
  if(d<=Math.abs(r1-r2))return Math.min(1,(r2*r2)/(r1*r1));
  const a=r1*r1*Math.acos(clamp1((d*d+r1*r1-r2*r2)/(2*d*r1)))
         +r2*r2*Math.acos(clamp1((d*d+r2*r2-r1*r1)/(2*d*r2)))
         -0.5*Math.sqrt(Math.max(0,(-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2)));
  return Math.min(1,a/(Math.PI*r1*r1));}
function camOf(w,h){const R=Math.min(w,h)*.46*gZoom,sl=Math.sin(gLon*RAD),cl=Math.cos(gLon*RAD);
  return{cx:w/2,cy:h/2,R:R,c:llv(gLon,gLat),e:[-sl,cl,0],
    n:[-Math.sin(gLat*RAD)*cl,-Math.sin(gLat*RAD)*sl,Math.cos(gLat*RAD)]};}
function pj(lon,lat,k){const p=llv(lon,lat);
  return{x:k.cx+k.R*(p[0]*k.e[0]+p[1]*k.e[1]+p[2]*k.e[2]),
         y:k.cy-k.R*(p[0]*k.n[0]+p[1]*k.n[1]+p[2]*k.n[2]),
         v:p[0]*k.c[0]+p[1]*k.c[1]+p[2]*k.c[2]};}
/* polyline with the far side of the sphere dropped; a null entry lifts the pen */
function arc(pts,k,cl){gb.beginPath();let up=false;
  for(const q of pts){
    if(!q){up=false;continue;}
    const s=pj(q[0],q[1],k);
    if(s.v<=0){up=false;continue;}
    up?gb.lineTo(s.x,s.y):gb.moveTo(s.x,s.y);up=true;}
  gb.strokeStyle=cl;gb.stroke();}
/* Outline of the region that sees any of the eclipse. The penumbra is a cylinder
   of radius L1 about the shadow axis; where that cylinder cuts the globe on the
   sunward side is the edge of the partial-eclipse zone. Points where the cylinder
   misses the sphere come back null, so the curve simply stops there. */
function penCurve(u,P,L1,n){
  let a=[P[0],P[1],P[2]];
  let an=Math.hypot(a[0],a[1],a[2]);
  if(an<1e-6){a=Math.abs(u[2])<.9?[-u[1],u[0],0]:[0,-u[2],u[1]];
    an=Math.hypot(a[0],a[1],a[2]);}
  a=[a[0]/an,a[1]/an,a[2]/an];
  const b=[u[1]*a[2]-u[2]*a[1],u[2]*a[0]-u[0]*a[2],u[0]*a[1]-u[1]*a[0]],out=[];
  for(let i=0;i<=n;i++){const th=i/n*6.283185307,
    ca=Math.cos(th)*L1,sb=Math.sin(th)*L1;
    const q=[P[0]+ca*a[0]+sb*b[0],P[1]+ca*a[1]+sb*b[1],P[2]+ca*a[2]+sb*b[2]];
    const q2=q[0]*q[0]+q[1]*q[1]+q[2]*q[2];
    if(q2>1){out.push(null);continue;}
    const s=-Math.sqrt(1-q2);
    const p=[q[0]+s*u[0],q[1]+s*u[1],q[2]+s*u[2]];
    out.push([Math.atan2(p[1],p[0])/RAD,
      Math.asin(Math.max(-1,Math.min(1,p[2])))/RAD]);}
  return out;}
/* night is shaded per pixel: cheap, and gives a real twilight gradient */
function shade(k,w,h,sub){const s=llv(sub.lon,sub.lat),sc=2;
  const ow=Math.max(2,Math.ceil(w/sc)),oh=Math.max(2,Math.ceil(h/sc));
  if(!shade.cv)shade.cv=document.createElement("canvas");
  const oc=shade.cv;if(oc.width!==ow||oc.height!==oh){oc.width=ow;oc.height=oh;}
  const ox=oc.getContext("2d"),img=ox.createImageData(ow,oh),D=img.data;
  for(let py=0;py<oh;py++)for(let px=0;px<ow;px++){
    const X=(px*sc+sc/2-k.cx)/k.R,Y=-(py*sc+sc/2-k.cy)/k.R,q=X*X+Y*Y;
    if(q>1)continue;
    const Z=Math.sqrt(1-q);
    const wx=X*k.e[0]+Y*k.n[0]+Z*k.c[0],wy=X*k.e[1]+Y*k.n[1]+Z*k.c[1],
          wz=X*k.e[2]+Y*k.n[2]+Z*k.c[2];
    const el=Math.asin(Math.max(-1,Math.min(1,wx*s[0]+wy*s[1]+wz*s[2])))/RAD;
    if(el>=0)continue;
    const a=el<-18?.78:.78*(-el/18),o=(py*ow+px)*4;
    D[o]=2;D[o+1]=6;D[o+2]=14;D[o+3]=Math.round(a*255);}
  ox.putImageData(img,0,0);return oc;}
/* The track is 13 samples about 15 minutes apart. Joining them with straight
   chords puts visible kinks in a curve that is actually smooth, so interpolate
   with a Catmull-Rom spline. Longitudes are unwrapped first or the spline tears
   at the antimeridian. */
function prep(p){if(p._la)return p;
  const lo=[p.pts[0][0]];
  for(let i=1;i<p.pts.length;i++)lo.push(lo[i-1]+(((p.pts[i][0]-p.pts[i-1][0]+540)%360)-180));
  p._lo=lo;p._la=p.pts.map(q=>q[1]);return p;}
const at_=(a,i)=>a[Math.max(0,Math.min(a.length-1,i))];
const cr=(a,b,c,d,t)=>{const t2=t*t,t3=t2*t;
  return .5*(2*b+(c-a)*t+(2*a-5*b+4*c-d)*t2+(3*b-3*c+d-a)*t3);};
function spl(arr,x){const i=Math.floor(x),t=x-i;
  return cr(at_(arr,i-1),at_(arr,i),at_(arr,i+1),at_(arr,i+2),t);}
const fIdx=(p,f)=>Math.max(0,Math.min(p.pts.length-1-1e-9,f*(p.pts.length-1)));
function trackAt(p,f){prep(p);const x=fIdx(p,f);
  return[((spl(p._lo,x)+540)%360)-180,Math.max(-90,Math.min(90,spl(p._la,x)))];}
function widthAt(p,f){if(!p.ws)return p.w;
  const v=spl(p.ws,fIdx(p,f));
  return Math.max(1,Math.min(v,Math.max(600,p.w*6)));}
/* ---------- the clock ----------

   Every eclipse gets a window running from first to last penumbral contact —
   the whole event, not just the umbra's crossing. That is what gives a partial
   eclipse, which has no track at all, something for its slider to run along, and
   it is also the span over which somebody standing off to one side of a total
   track sees anything happen.

   Greatest eclipse is the axis's closest approach to Earth's centre; the
   contacts are where the penumbral cone stops reaching Earth. Where a track was
   computed its stored time of greatest eclipse is kept as the anchor, so the
   umbra still sits exactly where it always did. Cached per eclipse. */
function win(e){
  if(e._w)return e._w;
  const d0=jdOf(e.ymd[0],e.ymd[1],e.ymd[2],0);
  let bj=d0,bv=1e9;
  for(let k=-24;k<=36;k++){const j=d0+k/24,v=axisAt(j).g;if(v<bv){bv=v;bj=j;}}
  let lo=bj-1/24,hi=bj+1/24;
  for(let i=0;i<34;i++){const a=lo+(hi-lo)/3,b=hi-(hi-lo)/3;
    if(axisAt(a).g<axisAt(b).g)hi=b;else lo=a;}
  let g=(lo+hi)/2;
  /* reach: how far the penumbra still touches Earth, either side of greatest */
  const miss=j=>{const x=axisAt(j);return x.g-(1+x.L1);};
  const edge=dir=>{let ok=g,bad=null;
    for(let k=1;k<=26;k++){const j=g+dir*k/96;if(miss(j)>0){bad=j;break;}ok=j;}
    if(bad===null)return dir*26/96;
    for(let i=0;i<26;i++){const m=(ok+bad)/2;miss(m)>0?bad=m:ok=m;}
    return ok-g;};
  const a=edge(-1)*1440,b=edge(1)*1440;
  if(e.p){const gs=jdOf(e.ymd[0],e.ymd[1],e.ymd[2],e.p.ut);
    /* the stored date comes from TD and the stored time from UT, so they can
       disagree by a day; take whichever whole day lands nearest */
    const gg=gs+Math.round(g-gs);
    return e._w={g:gg,a:a+(g-gg)*1440,b:b+(g-gg)*1440};}
  return e._w={g:g,a:a,b:b};}
/* minutes from greatest eclipse at the current slider position, and the Julian
   day that lands on */
const tOff=e=>{const w=win(e);return w.a+(w.b-w.a)*tFrac;};
const tJD=e=>win(e).g+tOff(e)/1440;
/* where the umbra is along its track: 0 at the sunrise end, 1 at the sunset end,
   outside [0,1] while the eclipse is still only partial anywhere on Earth */
const tUF=e=>e&&e.p?(tOff(e)+e.p.span/2)/e.p.span:0.5;
/* The partial-eclipse zone at the moment the clock is showing: where the
   penumbral cylinder cuts the globe on the sunward side. */
function penNow(e){return e?axisAt(tJD(e)):null;}
/* The region that sees any part of the eclipse: the union of the instantaneous
   penumbral zones across the whole event, which is what published eclipse maps
   draw and what actually encloses the entire track.

   The boundary is found by sweeping azimuths out from the mid-eclipse point,
   which assumes the union is star-shaped about it; that holds for the lens shape
   these regions actually take. Cached per eclipse. */
function penFrames(e){
  const w=win(e),N=26,fr=[];
  for(let i=0;i<=N;i++)fr.push(axisAt(w.g+(w.a+(w.b-w.a)*i/N)/1440));
  return fr;}
function penUnion(e){
  if(!e)return null;
  if(e._pu!==undefined)return e._pu;
  const fr=penFrames(e);
  const inside=p=>{for(const f of fr){
    const d=p[0]*f.u[0]+p[1]*f.u[1]+p[2]*f.u[2];
    if(d>=0)continue;
    const x=p[0]-d*f.u[0]-f.P[0],y=p[1]-d*f.u[1]-f.P[1],z=p[2]-d*f.u[2]-f.P[2];
    if(x*x+y*y+z*z<f.L1*f.L1)return true;}
    return false;};
  /* sweep out from the most-eclipsed spot at greatest eclipse */
  const c0=deepVec(fr[fr.length>>1]);
  if(!inside(c0))return e._pu=null;
  let e1=Math.abs(c0[2])<.9?[-c0[1],c0[0],0]:[0,-c0[2],c0[1]];
  const e2=[c0[1]*e1[2]-c0[2]*e1[1],c0[2]*e1[0]-c0[0]*e1[2],c0[0]*e1[1]-c0[1]*e1[0]];
  const at=(th,r)=>{const cr=Math.cos(r),sr=Math.sin(r),ct=Math.cos(th),st=Math.sin(th);
    return[cr*c0[0]+sr*(ct*e1[0]+st*e2[0]),cr*c0[1]+sr*(ct*e1[1]+st*e2[1]),
           cr*c0[2]+sr*(ct*e1[2]+st*e2[2])];};
  const out=[];
  for(let i=0;i<=240;i++){const th=i/240*6.283185307;
    let lo=0,hi=3.0;
    if(!inside(at(th,1e-3))){out.push(null);continue;}
    for(let b=0;b<17;b++){const mid=(lo+hi)/2;inside(at(th,mid))?lo=mid:hi=mid;}
    const p=at(th,lo);
    out.push([Math.atan2(p[1],p[0])/RAD,
      Math.asin(Math.max(-1,Math.min(1,p[2])))/RAD]);}
  e._pu=out;return out;}
/* 1 where this stretch of the track is annular, 0 where it is total */
function typeAt(p,f){if(!p.ts)return 0;
  return p.ts[Math.max(0,Math.min(p.ts.length-1,Math.round(f*(p.ts.length-1))))];}
/* central-phase length where the umbra is standing right now */
function durAt(p,f){if(!p.ds)return p.dur;
  return Math.max(0,Math.min(spl(p.ds,fIdx(p,f)),p.dur*3));}
const smooth=(p,n)=>{const o=[];for(let i=0;i<=n;i++)o.push(trackAt(p,i/n));return o;};
/* great-circle bearing and offset, for the path edges */
function bearing(a,b){const la1=a[1]*RAD,la2=b[1]*RAD,dl=(b[0]-a[0])*RAD;
  return Math.atan2(Math.sin(dl)*Math.cos(la2),
    Math.cos(la1)*Math.sin(la2)-Math.sin(la1)*Math.cos(la2)*Math.cos(dl));}
function dest(lon,lat,brg,km){const d=km/6371,la=lat*RAD;
  const la2=Math.asin(Math.sin(la)*Math.cos(d)+Math.cos(la)*Math.sin(d)*Math.cos(brg));
  const lo2=lon*RAD+Math.atan2(Math.sin(brg)*Math.sin(d)*Math.cos(la),
    Math.cos(d)-Math.sin(la)*Math.sin(la2));
  return[((lo2/RAD+540)%360)-180,la2/RAD];}
/* The two limits of the central path, offset from the centre line by half the
   local umbral width. Kept away from the extreme ends: there the axis grazes the
   surface, the width balloons past 800 km, and offsetting a sharply curving line
   by that much makes the offset curve fold back on itself. The bearing baseline
   is deliberately wide, since a short one turns coordinate noise into visible
   faceting. */
function edges(p,n){const L=[],R=[],f0=.03,f1=.97,cap=Math.max(500,p.w*2.5);
  for(let i=0;i<=n;i++){const f=f0+(f1-f0)*i/n,c=trackAt(p,f);
    const a=trackAt(p,Math.max(0,f-.012)),b=trackAt(p,Math.min(1,f+.012));
    const br=bearing(a,b),hw=Math.min(widthAt(p,f),cap)/2;
    L.push(dest(c[0],c[1],br-Math.PI/2,hw));
    R.push(dest(c[0],c[1],br+Math.PI/2,hw));}
  return[L,R];}
/* screen point back to a place on the globe, for standing somewhere */
function unpj(px,py,k){const X=(px-k.cx)/k.R,Y=-(py-k.cy)/k.R,q=X*X+Y*Y;
  if(q>1)return null;
  const Z=Math.sqrt(1-q);
  const w=[X*k.e[0]+Y*k.n[0]+Z*k.c[0],X*k.e[1]+Y*k.n[1]+Z*k.c[1],
           X*k.e[2]+Y*k.n[2]+Z*k.c[2]];
  return[Math.atan2(w[1],w[0])/RAD,Math.asin(clamp1(w[2]))/RAD];}
function sizeGlobe(){
  const w=globeBox.clientWidth||320;
  /* keep the globe inside whatever the panel actually is, or on a phone the
     drawer scrolls and half the globe hides under the stats */
  const room=detail.classList.contains("expanded")
    ?Math.max(280,(detail.clientHeight||520)-120)
    :Math.max(200,Math.min(480,(detail.clientHeight||420)-148));
  gSize=Math.max(190,Math.min(w,room));
  globeBox.style.height=gSize+"px";
  const dp=Math.min(devicePixelRatio||1,2);
  globe.width=Math.round(w*dp);globe.height=Math.round(gSize*dp);
  gb.setTransform(dp,0,0,dp,0,0);
  return{w:w,h:gSize};}
function drawGlobe(){
  if(detView!=="globe")return;
  const {w,h}=sizeGlobe();if(!w)return;
  const e=sel,k=camOf(w,h);
  gb.clearRect(0,0,w,h);
  gb.save();gb.beginPath();gb.arc(k.cx,k.cy,k.R,0,6.2832);gb.clip();
  gb.fillStyle="#071624";gb.fill();
  gb.lineWidth=1;
  const gr=gZoom>=8?5:gZoom>=3?10:30,gs=Math.min(3,gr/4);
  for(let lon=-180;lon<180;lon+=gr){const p=[];
    for(let la=-90;la<=90;la+=gs)p.push([lon,la]);arc(p,k,"#0f1e2c");}
  for(let la=-90+gr;la<90;la+=gr){const p=[];
    for(let lo=-180;lo<=180;lo+=gs)p.push([lo,la]);arc(p,k,"#0f1e2c");}
  /* borders fade in so a whole-Earth view stays readable */
  const fade=(z0,z1)=>Math.max(0,Math.min(1,(gZoom-z0)/(z1-z0)));
  const aC=fade(1.4,2.4),aP=fade(3,5);
  if(aC>.02){gb.globalAlpha=aC*.85;gb.lineWidth=.8;
    for(const b of BORD0)arc(b,k,"#4a5f7a");}
  if(aP>.02){gb.globalAlpha=aP*.6;gb.lineWidth=.7;
    for(const b of BORD1)arc(b,k,"#38495e");}
  gb.globalAlpha=1;
  gb.lineWidth=.9;
  for(const p of LAND)arc(p.concat([p[0]]),k,"#2f4a63");
  gb.restore();
  gb.save();gb.beginPath();gb.arc(k.cx,k.cy,k.R,0,6.2832);gb.clip();
  const jd=e?tJD(e):nowJD();
  const sub=subsolar(jd);
  gb.drawImage(shade(k,w,h,sub),0,0,w,h);
  /* city pins, once you are zoomed in far enough for them to mean anything */
  /* Populated places, each population tier fading in over a zoom range. PLC is
     sorted biggest first, so once a tier is invisible everything after it is too. */
  if(gZoom>=1.5){
    gb.font='9px "IBM Plex Mono",monospace';gb.textAlign="left";gb.textBaseline="middle";
    const al=[fade(1.5,2.2),fade(2.4,3.4),fade(4,5.5),fade(7,9),fade(11,14)];
    const nmFrom=[1.9,2.8,4.6,8,12];
    /* Labels are placed greedily into a coarse grid and dropped when their slot is
       taken, otherwise a dense region turns into an unreadable smear. Biggest
       places come first, so they win the contested slots. */
    const occ=new Set();let labels=0;
    for(const c of PLC){const t=c[3],a=al[t];
      if(a<=.02)break;
      const s=pj(c[1],c[2],k);if(s.v<=0.02)continue;
      if(s.x<-20||s.x>w+20||s.y<-20||s.y>h+20)continue;
      gb.globalAlpha=a;
      gb.fillStyle="#b58b4c";gb.beginPath();gb.arc(s.x,s.y,t<=1?2.1:1.6,0,6.2832);gb.fill();
      if(gZoom<nmFrom[t]||labels>=220)continue;
      const row=(s.y/13)|0,c0=(s.x/58)|0,c1=((s.x+c[0].length*5.4)/58)|0;
      let free=true;
      for(let cc=c0;cc<=c1;cc++)if(occ.has(row+":"+cc)){free=false;break;}
      if(!free)continue;
      for(let cc=c0;cc<=c1;cc++)occ.add(row+":"+cc);
      gb.strokeStyle="rgba(4,7,12,.85)";gb.lineWidth=2.6;
      gb.strokeText(c[0],s.x+4.5,s.y);
      gb.fillStyle="#c3cedb";gb.fillText(c[0],s.x+4.5,s.y);labels++;}
    gb.globalAlpha=1;}
  const ss=pj(sub.lon,sub.lat,k);
  if(ss.v>0){gb.fillStyle="rgba(244,241,230,.9)";gb.beginPath();gb.arc(ss.x,ss.y,3,0,6.2832);gb.fill();
    gb.strokeStyle="rgba(244,241,230,.35)";gb.lineWidth=1;gb.beginPath();gb.arc(ss.x,ss.y,7,0,6.2832);gb.stroke();
    gb.fillStyle="rgba(244,241,230,.6)";gb.font='8.5px "IBM Plex Mono",monospace';
    gb.textAlign="center";gb.textBaseline="top";gb.fillText("sun overhead",ss.x,ss.y+10);}
  /* the whole area that sees a partial — the only geometry a partial eclipse has */
  /* whole-event partial region where there is a track, single instant otherwise */
  const pu=penUnion(e);
  if(pu){gb.setLineDash([1.5,3.5]);gb.lineWidth=1.1;gb.globalAlpha=.9;
    arc(pu,k,"#93a6bd");gb.setLineDash([]);gb.globalAlpha=1;}
  /* and the zone at this instant inside it, which is the part actually seeing
     the eclipse right now — for a partial it is the only thing that moves */
  const pn=penNow(e);
  if(pn){gb.setLineDash([]);gb.lineWidth=1;gb.globalAlpha=pu?.55:.9;
    arc(penCurve(pn.u,pn.P,pn.L1,360),k,"#6b8099");gb.globalAlpha=1;}
  if(e&&e.p){
    const ns=Math.round(Math.max(140,Math.min(420,90*Math.sqrt(gZoom))));
    const [eL_,eR_]=edges(e.p,ns);
    gb.setLineDash([2,3]);gb.lineWidth=1;gb.globalAlpha=.75;
    arc(eL_,k,COL[e.t]);arc(eR_,k,COL[e.t]);
    gb.setLineDash([]);gb.globalAlpha=1;
    /* coloured by the local type, so a hybrid shows where it turns */
    gb.lineWidth=2;gb.lineCap="round";
    let run=[],cur=-1;
    for(let i=0;i<=ns;i++){const f=i/ns,ty=typeAt(e.p,f),pt=trackAt(e.p,f);
      if(ty!==cur){if(run.length>1)arc(run,k,COL[cur?1:0]);
        run=run.length?[run[run.length-1]]:[];cur=ty;}
      run.push(pt);}
    if(run.length>1)arc(run,k,COL[cur?1:0]);
    /* the umbra is only on Earth for the middle stretch of the event: before and
       after that the clock is running but the eclipse is partial everywhere */
    const uf=tUF(e);
    if(uf>=0&&uf<=1){
      const u=trackAt(e.p,uf),us=pj(u[0],u[1],k);
      if(us.v>0){
        const rr=Math.max(2.5,k.R*(widthAt(e.p,uf)/2)/6371);
        const uc=COL[typeAt(e.p,uf)?1:0];
        gb.fillStyle="rgba(7,10,16,.85)";gb.beginPath();gb.arc(us.x,us.y,rr,0,6.2832);gb.fill();
        gb.strokeStyle=uc;gb.lineWidth=1.6;gb.beginPath();gb.arc(us.x,us.y,rr,0,6.2832);gb.stroke();
        gb.strokeStyle=uc;gb.globalAlpha=.5;gb.lineWidth=1;
        gb.beginPath();gb.arc(us.x,us.y,rr+6,0,6.2832);gb.stroke();gb.globalAlpha=1;
        const dd=Math.round(durAt(e.p,uf));
        if(dd>0){gb.fillStyle=COL[e.t];gb.font='500 10px "IBM Plex Mono",monospace';
          gb.textAlign="left";gb.textBaseline="middle";
          gb.fillText(fd(dd),us.x+rr+9,us.y);}}}
  }
  /* where you are standing, and what the sky is doing there */
  if(obs){const os=pj(obs[0],obs[1],k);
    if(os.v>0){
      const L=e?local(jd,obs[1],obs[0]):null;
      const c=!L||L.obsc<=0?"#93a6bd":L.tot?"#f4f1e6":L.ann?"#e8a33d":"#8fd4c4";
      gb.strokeStyle="rgba(4,7,12,.9)";gb.lineWidth=3.4;
      gb.beginPath();gb.moveTo(os.x,os.y-10);gb.lineTo(os.x,os.y);gb.stroke();
      gb.strokeStyle=c;gb.lineWidth=1.6;
      gb.beginPath();gb.moveTo(os.x,os.y-10);gb.lineTo(os.x,os.y);gb.stroke();
      gb.beginPath();gb.arc(os.x,os.y-12.5,2.6,0,6.2832);
      gb.fillStyle=c;gb.fill();
      gb.beginPath();gb.arc(os.x,os.y,2,0,6.2832);gb.fillStyle=c;gb.fill();
      if(L){gb.font='500 9px "IBM Plex Mono",monospace';gb.textAlign="center";
        gb.textBaseline="bottom";
        gb.strokeStyle="rgba(4,7,12,.9)";gb.lineWidth=3;
        const s=L.obsc>0?Math.round(L.obsc*100)+"% covered":"nothing yet";
        gb.strokeText(s,os.x,os.y-17);gb.fillStyle=c;gb.fillText(s,os.x,os.y-17);}}}
  gb.restore();
  gb.strokeStyle="#2b3d52";gb.lineWidth=1;gb.beginPath();gb.arc(k.cx,k.cy,k.R,0,6.2832);gb.stroke();
  gb.fillStyle="#4d5c72";gb.font='9px "IBM Plex Mono",monospace';
  gb.textAlign="left";gb.textBaseline="top";
  gb.fillText("sub-solar "+sub.lat.toFixed(1)+"° "+sub.lon.toFixed(1)+"°",8,8);
  gb.fillText("×"+gZoom.toFixed(1)+(gZoom<2.2?"  — zoom in for cities":""),8,21);
  if(e&&!e.p){gb.textAlign="center";gb.fillStyle="#7d8ea6";
    gb.fillText(e.t===3
      ?"partial only — the axis misses Earth; solid line is who sees it right now"
      :"track not computed before 1000 CE; solid line is who sees it right now",w/2,h-16);}
  else if(e){gb.textAlign="center";gb.fillStyle="#6b7a90";
    gb.fillText(obs?"tap anywhere to move · drag the pin to walk it"
      :"dotted: everyone who sees any of it · tap the globe to stand there",w/2,h-16);}
}
/* ---------- standing on the ground ----------

   The sky in stereographic projection, which has the useful property of turning
   every circle on the sphere into a circle on screen: the Sun and the Moon stay
   round however far off-centre they drift, and the horizon is one clean curve.
   Look direction and field of view are yours to drag; everything in it comes
   from the topocentric Sun and Moon at whatever the clock says. */
const skyC=document.getElementById("sky"),sc=skyC.getContext("2d");
const skyBox=document.getElementById("skyBox");
let obs=null,vAz=180,vAlt=25,vFov=68,skySize=0,circ=null,vTrack=true;
/* the fifty-odd stars that are actually worth drawing when the sky goes out:
   right ascension (hours), declination, magnitude, J2000 */
const STARS=[[6.752,-16.716,-1.46],[6.399,-52.696,-0.72],[14.660,-60.834,-0.27],
[14.261,19.182,-0.05],[18.616,38.784,0.03],[5.278,45.998,0.08],[5.242,-8.202,0.13],
[7.655,5.225,0.34],[1.629,-57.237,0.46],[5.919,7.407,0.50],[14.064,-60.373,0.61],
[19.846,8.868,0.77],[12.443,-63.099,0.77],[4.599,16.509,0.85],[13.420,-11.161,1.04],
[16.490,-26.432,1.09],[7.755,28.026,1.14],[22.961,-29.622,1.16],[20.690,45.280,1.25],
[12.795,-59.689,1.25],[10.139,11.967,1.35],[6.977,-28.972,1.50],[7.576,31.888,1.58],
[17.560,-37.104,1.62],[12.519,-57.113,1.63],[5.418,6.350,1.64],[5.438,28.608,1.65],
[9.220,-69.717,1.67],[5.603,-1.202,1.69],[22.137,-46.961,1.74],[5.679,-1.943,1.77],
[12.900,55.960,1.77],[11.062,61.751,1.79],[3.405,49.861,1.79],[7.140,-26.393,1.83],
[18.403,-34.385,1.85],[8.375,-59.510,1.86],[13.792,49.313,1.86],[17.622,-42.998,1.87],
[5.992,44.947,1.90],[16.811,-69.028,1.91],[6.629,16.399,1.93],[20.427,-56.735,1.94],
[2.530,89.264,1.98],[6.378,-17.956,1.98],[9.460,-8.659,2.00],[2.120,23.462,2.00],
[10.333,19.841,2.08],[0.726,-17.987,2.04],[18.921,-26.297,2.05],[14.111,-36.370,2.06],
[0.140,29.091,2.06],[1.162,35.621,2.06],[5.796,-9.670,2.09],[14.845,74.156,2.08],
[17.582,12.560,2.08],[3.136,40.956,2.12],[2.065,42.330,2.10],[11.818,14.572,2.14],
[8.060,-40.003,2.21]];
/* Meeus ch.21: 5,000 years is enough precession to move Polaris out of the way */
function precess(ra,dec,T){
  const z1=(2306.2181*T+0.30188*T*T+0.017998*T*T*T)/3600;
  const z2=(2306.2181*T+1.09468*T*T+0.018203*T*T*T)/3600;
  const th=(2004.3109*T-0.42665*T*T-0.041833*T*T*T)/3600;
  const A=cosD(dec)*sinD(ra+z1),B=cosD(th)*cosD(dec)*cosD(ra+z1)-sinD(th)*sinD(dec);
  const C=sinD(th)*cosD(dec)*cosD(ra+z1)+cosD(th)*sinD(dec);
  return[Math.atan2(A,B)/RAD+z2,Math.asin(clamp1(C))/RAD];}
/* the view basis, and a point of the sky put on screen */
function skyCam(w,h){
  const f=[sinD(vAz)*cosD(vAlt),cosD(vAz)*cosD(vAlt),sinD(vAlt)];
  /* f x zenith, normalised: the horizontal "right" of the view */
  let r=[f[1],-f[0],0];const rn=Math.hypot(r[0],r[1])||1;r=[r[0]/rn,r[1]/rn,0];
  const up=[r[1]*f[2]-r[2]*f[1],r[2]*f[0]-r[0]*f[2],r[0]*f[1]-r[1]*f[0]];
  return{cx:w/2,cy:h/2,f:f,r:r,u:up,k:(h/2)/(2*Math.tan(vFov/4*RAD))};}
function pjSky(v,c){const d=vdot(v,c.f);
  /* the projection blows up at the point behind you; clamping keeps the horizon
     a drawable polygon instead of one with an infinite spike in it */
  const s=2/(1+Math.max(-0.9995,d)),cl=x=>Math.max(-1e5,Math.min(1e5,x));
  return{x:cl(c.cx+c.k*vdot(v,c.r)*s),y:cl(c.cy-c.k*vdot(v,c.u)*s),v:d};}
const altaz=(alt,az)=>[sinD(az)*cosD(alt),cosD(az)*cosD(alt),sinD(alt)];
/* and back: which bit of sky a pixel is looking at, which is what lets the sky
   be coloured by real altitude instead of by height up the canvas */
function unSky(px,py,c){const X=(px-c.cx)/c.k,Y=-(py-c.cy)/c.k,R=Math.hypot(X,Y);
  if(R<1e-9)return c.f.slice();
  const th=2*Math.atan(R/2),ct=Math.cos(th),st=Math.sin(th),ux=X/R,uy=Y/R;
  return[c.f[0]*ct+(ux*c.r[0]+uy*c.u[0])*st,
         c.f[1]*ct+(ux*c.r[1]+uy*c.u[1])*st,
         c.f[2]*ct+(ux*c.r[2]+uy*c.u[2])*st];}
function sizeSky(){
  const w=skyBox.clientWidth||320;
  const room=detail.classList.contains("expanded")
    ?Math.max(300,(detail.clientHeight||520)-150)
    :Math.max(210,Math.min(520,(detail.clientHeight||420)-176));
  skySize=Math.max(200,Math.min(Math.round(w*0.78),room));
  skyBox.style.height=skySize+"px";
  const dp=Math.min(devicePixelRatio||1,2);
  skyC.width=Math.round(w*dp);skyC.height=Math.round(skySize*dp);
  sc.setTransform(dp,0,0,dp,0,0);
  return{w:w,h:skySize};}
/* Sky colour: a ladder of zenith/horizon pairs against solar altitude, then the
   eclipse dims it. Brightness tracks the uncovered area of the disc almost all
   the way, then falls off a cliff in the last three per cent — which is exactly
   why totality is startling and 99 per cent is not. */
const SKYPAL=[[-20,[5,7,13],[9,12,19]],[-12,[7,11,20],[22,29,45]],
 [-6,[12,22,42],[66,58,76]],[-2,[24,48,86],[158,98,72]],[0,[38,72,118],[210,138,86]],
 [4,[52,100,150],[188,172,158]],[12,[48,110,178],[150,180,205]],[40,[30,95,175],[135,175,215]]];
function skyCols(alt,dim){
  let i=0;while(i<SKYPAL.length-2&&alt>SKYPAL[i+1][0])i++;
  const a=SKYPAL[i],b=SKYPAL[i+1];
  const t=Math.max(0,Math.min(1,(alt-a[0])/(b[0]-a[0])));
  const mix=(p,q)=>p.map((v,j)=>v+(q[j]-v)*t);
  let z=mix(a[1],b[1]),hz=mix(a[2],b[2]);
  /* the eye is roughly cube-root in luminance, so that is the curve the colour
     is dimmed along; the fall stays dramatic because dimOf already is */
  const nz=SKYPAL[0][1],nh=SKYPAL[0][2],f=Math.pow(dim,0.33);
  z=z.map((v,j)=>nz[j]+(v-nz[j])*f);hz=hz.map((v,j)=>nh[j]+(v-nh[j])*f);
  return{z:z,h:hz};}
/* the colour of one patch of sky, at its own altitude. Deep in an eclipse the
   horizon all the way round takes on the warm cast of the uneclipsed daylight
   a couple of hundred kilometres away, which is the 360-degree sunset people
   remember from totality. */
function skyRGB(skyAlt,cc,obsc){
  const t=Math.pow(Math.max(0,Math.min(1,skyAlt/55)),0.7);
  let col=cc.h.map((v,i)=>v+(cc.z[i]-v)*t);
  if(obsc>0.965){
    const q=Math.min(1,(obsc-0.965)/0.035)*0.85
      *(1-Math.min(1,Math.max(0,skyAlt)/26));
    const warm=[198,116,76];
    col=col.map((v,i)=>v+(warm[i]-v)*q);}
  return col;}
const rgb=c=>"rgb("+Math.round(c[0])+","+Math.round(c[1])+","+Math.round(c[2])+")";
function dimOf(o){if(o<=0)return 1;
  if(o<0.97)return 1-o;
  const x=Math.max(0,(1-o)/0.03);
  return Math.max(0.0006,0.03*Math.pow(x,2.1));}
/* a deterministic wobble, so a given eclipse's corona is always the same one */
function rnd(s){let x=Math.sin(s*127.1+311.7)*43758.5453;return x-Math.floor(x);}

/* ---------- WebGL sky ----------

   The sky, the two discs and the corona all live at infinity, so the whole scene
   is a function of the direction a pixel is looking — which makes it one
   full-screen fragment shader with no geometry and no matrices at all.

   Colour comes from Preetham's analytic daylight model: Perez's five-parameter
   sky function fitted against turbidity, giving CIE Yxy per direction, which is
   why the horizon warms and the zenith deepens on their own instead of being
   painted in by hand.

   The eclipse enters as the one physical change that matters. Obscuration cuts
   the direct beam, but the umbra is only a couple of hundred kilometres across
   and the atmosphere goes on scattering sunlight in from all round its edge —
   light that has come the long way through the lower atmosphere and arrives red.
   That second term is the 360-degree sunset at totality, and it falls out of the
   model rather than being faked.

   If any of this fails to compile or the context is refused, glOn stays false and
   the 2-D renderer below draws everything exactly as it did before. */
const sky3d=document.getElementById("sky3d");
let GL=null,glOn=false,glTried=false,glProg=null,glStar=null,glBuf=null,glStarBuf=null,glStarN=0;
const SKY_VS=`attribute vec2 aPos;void main(){gl_Position=vec4(aPos,0.0,1.0);}`;
const SKY_FS=`precision highp float;
uniform vec2 uRes;uniform float uK;
uniform vec3 uRight,uUp,uFwd,uSun,uMoon,uFlare;
uniform float uSunR,uMoonR,uObsc,uTurb,uAmb,uExp,uFlareI,uSeed,uNight;
const float PI=3.14159265359;
float perez(float cosT,float g,float A,float B,float C,float D,float E){
  return (1.0+A*exp(B/max(cosT,0.02)))*(1.0+C*exp(D*g)+E*cos(g)*cos(g));}
/* CIE Yxy straight out of Preetham, then into linear sRGB */
vec3 skyCol(vec3 dir,vec3 sun,float T,out float lum){
  float cosT=max(dir.z,0.0);
  float cosG=clamp(dot(dir,sun),-1.0,1.0);
  float g=acos(cosG);
  float tS=acos(clamp(sun.z,-1.0,1.0));
  float AY= 0.1787*T-1.4630,BY=-0.3554*T+0.4275,CY=-0.0227*T+5.3251,
        DY= 0.1206*T-2.5771,EY=-0.0670*T+0.3703;
  float Ax=-0.0193*T-0.2592,Bx=-0.0665*T+0.0008,Cx=-0.0004*T+0.2125,
        Dx=-0.0641*T-0.8989,Ex=-0.0033*T+0.0452;
  float Ay=-0.0167*T-0.2608,By=-0.0950*T+0.0092,Cy=-0.0079*T+0.2102,
        Dy=-0.0441*T-1.6537,Ey=-0.0109*T+0.0529;
  float chi=(4.0/9.0-T/120.0)*(PI-2.0*tS);
  float Yz=(4.0453*T-4.9710)*tan(chi)-0.2155*T+2.4192;
  float s1=tS,s2=s1*s1,s3=s2*s1;
  float xz=( 0.00166*s3-0.00375*s2+0.00209*s1)*T*T
          +(-0.02903*s3+0.06377*s2-0.03202*s1+0.00394)*T
          +( 0.11693*s3-0.21196*s2+0.06052*s1+0.25886);
  float yz=( 0.00275*s3-0.00610*s2+0.00317*s1)*T*T
          +(-0.04214*s3+0.08970*s2-0.04153*s1+0.00516)*T
          +( 0.15346*s3-0.26756*s2+0.06670*s1+0.26688);
  float dY=perez(cosT,g,AY,BY,CY,DY,EY)/perez(1.0,tS,AY,BY,CY,DY,EY);
  float dx=perez(cosT,g,Ax,Bx,Cx,Dx,Ex)/perez(1.0,tS,Ax,Bx,Cx,Dx,Ex);
  float dy=perez(cosT,g,Ay,By,Cy,Dy,Ey)/perez(1.0,tS,Ay,By,Cy,Dy,Ey);
  float Y=max(Yz*dY,0.0),x=xz*dx,y=max(yz*dy,1e-4);
  lum=Y;
  float X=x/y*Y,Z=(1.0-x-y)/y*Y;
  vec3 c=vec3( 3.2406*X-1.5372*Y-0.4986*Z,
              -0.9689*X+1.8758*Y+0.0415*Z,
               0.0557*X-0.2040*Y+1.0570*Z);
  return max(c,0.0);}
float hash(float n){return fract(sin(n*127.1+311.7)*43758.5453);}
void main(){
  vec2 q=(gl_FragCoord.xy-0.5*uRes)/uK;
  float r=length(q);
  float th=2.0*atan(r*0.5);
  vec3 dir=(r<1e-6)?uFwd:normalize(cos(th)*uFwd+sin(th)*((q.x/r)*uRight+(q.y/r)*uUp));
  /* Preetham has nothing to say once the Sun is down, so it is evaluated with the
     Sun held at the horizon and faded out into a night sky underneath */
  vec3 sunUp=uSun;
  sunUp.z=max(sunUp.z,0.0);
  sunUp=normalize(sunUp+vec3(0.0,0.0,1e-5));
  float lum;
  vec3 col=skyCol(dir,sunUp,uTurb,lum);
  float day=smoothstep(-0.20,0.02,uSun.z);
  col*=day;lum*=day;
  /* the eclipse: direct beam cut by obscuration, plus what the atmosphere
     scatters in from outside the umbra, which arrives reddened and along the
     horizon */
  float horiz=pow(1.0-clamp(dir.z,0.0,1.0),3.0);
  float direct=1.0-uObsc;
  /* blue-grey overhead where the light has come almost straight down through the
     umbra, orange round the rim where it has travelled a long shallow path in
     from the sunlit air outside */
  vec3 ambCol=mix(vec3(0.34,0.46,0.66),vec3(1.00,0.42,0.20),horiz);
  col=col*direct+lum*uAmb*(0.22+0.78*horiz)*ambCol;
  /* night: a cold gradient that the twilight fades down into */
  col+=vec3(0.055,0.095,0.190)*(1.0-day)*(0.35+0.65*horiz)*uNight;
  float aS=acos(clamp(dot(dir,uSun),-1.0,1.0));
  float aM=acos(clamp(dot(dir,uMoon),-1.0,1.0));
  /* corona, only worth drawing once the photosphere is gone */
  if(uObsc>0.995&&aM>uMoonR){
    float k=aM/uMoonR;
    /* streamers, on two scales, brightest round the equator of a tilted axis —
       the real corona follows the Sun's magnetic field, which is why it has
       equatorial wings and short polar brushes rather than an even halo */
    float ang=atan(dot(dir,uUp)-dot(uMoon,uUp),dot(dir,uRight)-dot(uMoon,uRight));
    float s1=0.60+0.40*sin(ang*6.0+uSeed*11.0);
    float s2=0.72+0.28*sin(ang*13.0-uSeed*7.0);
    float eq=0.45+0.55*abs(cos(ang-uSeed*3.1));
    float st=s1*s2*mix(0.55,1.0,eq);
    float f=pow(1.0/k,2.4)*st+pow(1.0/k,7.0)*0.9;
    col+=vec3(0.94,0.96,1.00)*f*5.0;
    /* chromosphere: a thin red rim for the few seconds either side of totality */
    col+=vec3(1.0,0.26,0.18)*exp(-(k-1.0)*150.0)*6.0;}
  /* The Sun, limb-darkened. Its surface is some five orders of magnitude
     brighter than the sky beside it, which is the whole reason it blows out to
     white while the sky keeps its colour. */
  if(aS<uSunR&&aM>uMoonR){
    float mu=sqrt(max(1.0-pow(aS/uSunR,2.0),0.0));
    float I=1.0-0.60*(1.0-mu)-0.19*(1.0-mu)*(1.0-mu);
    col+=vec3(1900.0,1830.0,1700.0)*I;}
  /* glare off whatever sliver of photosphere is still showing */
  float aF=acos(clamp(dot(dir,uFlare),-1.0,1.0));
  col+=vec3(1.0,0.96,0.88)*uFlareI*exp(-aF/(uSunR*7.0))*30.0;
  col+=vec3(1.0,0.97,0.90)*uFlareI*exp(-aF/(uSunR*46.0))*5.0;
  /* Exposure, then tone-mapped on luminance alone. Per-channel compression
     would wash the blue out of the sky exactly where it is strongest. */
  col*=uExp;
  float L=dot(col,vec3(0.2126,0.7152,0.0722));
  col*=(L>1e-6)?(L/(1.0+L))/L:0.0;
  gl_FragColor=vec4(pow(max(col,0.0),vec3(1.0/2.2)),1.0);}`;
const STAR_VS=`attribute vec3 aDir;attribute float aMag;
uniform vec3 uRight,uUp,uFwd;uniform float uK,uDpr;uniform vec2 uRes;
varying float vI;
void main(){
  float d=dot(aDir,uFwd);
  if(d<-0.3){gl_Position=vec4(9.0,9.0,9.0,1.0);gl_PointSize=1.0;vI=0.0;return;}
  float th=acos(clamp(d,-1.0,1.0));
  vec2 pp=vec2(dot(aDir,uRight),dot(aDir,uUp));
  float l=length(pp);
  vec2 px=((l<1e-6)?vec2(0.0):pp/l*(2.0*tan(th*0.5)))*uK;
  gl_Position=vec4(px/(0.5*uRes),0.0,1.0);
  gl_PointSize=max(1.5,(3.4-aMag*0.62))*uDpr;
  vI=clamp(1.35-aMag*0.30,0.15,1.0);}`;
const STAR_FS=`precision mediump float;varying float vI;uniform float uAlpha;
void main(){
  vec2 d=gl_PointCoord-0.5;
  float a=exp(-dot(d,d)*22.0);
  gl_FragColor=vec4(vec3(0.92,0.95,1.0)*vI,a*uAlpha*vI);}`;
function glCompile(gl,type,src){const s=gl.createShader(type);
  gl.shaderSource(s,src);gl.compileShader(s);
  if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))
    throw new Error(gl.getShaderInfoLog(s));
  return s;}
function glLink(gl,vs,fs){const p=gl.createProgram();
  gl.attachShader(p,glCompile(gl,gl.VERTEX_SHADER,vs));
  gl.attachShader(p,glCompile(gl,gl.FRAGMENT_SHADER,fs));
  gl.linkProgram(p);
  if(!gl.getProgramParameter(p,gl.LINK_STATUS))
    throw new Error(gl.getProgramInfoLog(p));
  /* uniforms and attributes looked up once and hung off the program */
  p.u={};p.a={};
  const nu=gl.getProgramParameter(p,gl.ACTIVE_UNIFORMS);
  for(let i=0;i<nu;i++){const n=gl.getActiveUniform(p,i).name;
    p.u[n]=gl.getUniformLocation(p,n);}
  const na=gl.getProgramParameter(p,gl.ACTIVE_ATTRIBUTES);
  for(let i=0;i<na;i++){const n=gl.getActiveAttrib(p,i).name;
    p.a[n]=gl.getAttribLocation(p,n);}
  return p;}
function glInit(){
  if(glTried)return glOn;
  glTried=true;
  try{
    const gl=sky3d.getContext("webgl",{antialias:true,alpha:false,depth:true,
      preserveDrawingBuffer:true})||sky3d.getContext("experimental-webgl");
    if(!gl)return false;
    GL=gl;
    glProg=glLink(gl,SKY_VS,SKY_FS);
    glStar=glLink(gl,STAR_VS,STAR_FS);
    glBuf=gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER,glBuf);
    /* one oversized triangle covers the viewport with no seam down the middle */
    gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
    glStarBuf=gl.createBuffer();
    glOn=true;
  }catch(err){GL=null;glOn=false;}
  return glOn;}
/* the star field in the observer's frame, rebuilt only when the sky has turned */
let starKey="";
function glStars(L,jd){
  const key=jd.toFixed(4)+":"+obs[0].toFixed(2)+":"+obs[1].toFixed(2);
  if(key===starKey)return;
  starKey=key;
  const T=(jd-2451545.0)/36525,a=[];
  for(const st of STARS){const pd=precess(st[0]*15,st[1],T);
    const v=L.toH([cosD(pd[1])*cosD(pd[0]),cosD(pd[1])*sinD(pd[0]),sinD(pd[1])]);
    if(v[2]<-0.05)continue;
    a.push(v[0],v[1],v[2],st[2]);}
  glStarN=a.length/4;
  GL.bindBuffer(GL.ARRAY_BUFFER,glStarBuf);
  GL.bufferData(GL.ARRAY_BUFFER,new Float32Array(a),GL.DYNAMIC_DRAW);}
/* How much sky glow survives once the direct beam has gone. Never zero: the
   umbra is only a couple of hundred kilometres across and the air above you is
   still lit from outside it. This is an adapted brightness, not a photometric
   one — the true ratio at totality is nearer one part in ten thousand, which on
   a screen with no dark adaptation behind it would just be black. */
function ambOf(o){
  if(o<0.94)return 0.0;
  const x=Math.min(1,(o-0.94)/0.06);
  return 0.16*x*x;}
/* Preetham's zenith luminance, on the CPU, purely as a reference level */
function zenLum(T,sunAlt){
  const tS=Math.max(0,Math.min(Math.PI/2-0.02,(90-sunAlt)*RAD));
  const chi=(4/9-T/120)*(Math.PI-2*tS);
  return Math.max(0.05,(4.0453*T-4.9710)*Math.tan(chi)-0.2155*T+2.4192);}
/* Exposure. A real scene here runs from full noon to the inside of the umbra,
   some four orders of magnitude, and a fixed exposure can only get one of them
   right. This is the eye adapting — but deliberately only part of the way, since
   watching the light go is the entire point of standing here. */
function expOf(L){
  const ref=Math.max(0.05,zenLum(2.6,L.S.alt)*Math.max(1-L.obsc,ambOf(L.obsc)*0.9));
  return 0.30/Math.pow(ref,0.62);}
/* ---------- terrain ----------

   The one thing on this page that is fetched while it runs. Elevation comes from
   the AWS terrain tiles, which are open, need no key and send a permissive CORS
   header, in Mapzen's terrarium encoding: height in metres packed across the
   three colour channels as (R*256 + G + B/256) - 32768.

   The mesh is polar rather than square — rings of increasing spacing out to a
   hundred-odd kilometres, on 256 spokes. That puts the detail where the eye is,
   gives every ring a natural level of detail, and matches the shape of the
   problem, which is a horizon seen from one fixed point.

   Everything degrades: no network, an old browser, a tile that will not load,
   and you get the flat horizon back with nothing broken. */
let terrHost="https://s3.amazonaws.com/elevation-tiles-prod/terrarium";
const TERRAIN_URL=(z,x,y)=>terrHost+"/"+z+"/"+x+"/"+y+".png";
const TERRAIN_CREDIT="Terrain: AWS Terrain Tiles / Mapzen";
/* zoom, and how many tiles either side of the middle one to pull at that zoom */
const TZ=[[12,1],[9,1],[6,1]];
const TILES=new Map();
let terrOn=true,terrMesh=null,terrKey="",terrBusy=0,terrWant=0,terrBuf=null,terrNrm=null,
    terrIdx=null,terrHgt=null,terrN=0,glTerr=null,terrDec=null;
const tileX=(lon,z)=>(lon+180)/360*Math.pow(2,z);
const tileY=(lat,z)=>{const r=lat*RAD;
  return(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*Math.pow(2,z);};
function tileGet(z,x,y,done){
  const n=1<<z;
  x=((x%n)+n)%n;
  if(y<0||y>=n)return null;
  const k=z+"/"+x+"/"+y;
  let t=TILES.get(k);
  if(t)return t;
  t={h:null,fail:false};TILES.set(k,t);
  terrWant++;terrBusy++;
  const img=new Image();
  img.crossOrigin="anonymous";
  img.onload=()=>{
    try{
      if(!terrDec){terrDec=document.createElement("canvas");terrDec.width=terrDec.height=256;}
      const cx=terrDec.getContext("2d",{willReadFrequently:true});
      cx.clearRect(0,0,256,256);cx.drawImage(img,0,0,256,256);
      const d=cx.getImageData(0,0,256,256).data,a=new Float32Array(256*256);
      for(let i=0,j=0;i<a.length;i++,j+=4)
        a[i]=(d[j]*256+d[j+1]+d[j+2]/256)-32768;
      t.h=a;
    }catch(err){t.fail=true;}
    terrBusy--;terrDone();};
  img.onerror=()=>{t.fail=true;terrBusy--;terrDone();};
  img.src=TERRAIN_URL(z,x,y);
  return t;}
let terrTimer=null;
function terrDone(){
  /* rebuild as tiles land, so the horizon fills in rather than arriving all at
     once — but coalesced, since a rebuild costs more than a decode */
  if(terrTimer)return;
  terrTimer=setTimeout(()=>{terrTimer=null;
    if(detView==="ground"&&obs){terrMesh=null;drawSky();}
    syncObs();},180);}
/* metres above the ellipsoid at a place, from the sharpest tile that has it */
function elevAt(lon,lat){
  for(const[z]of TZ){
    const fx=tileX(lon,z),fy=tileY(lat,z);
    const n=1<<z,tx=((Math.floor(fx)%n)+n)%n,ty=Math.floor(fy);
    if(ty<0||ty>=n)continue;
    const t=TILES.get(z+"/"+tx+"/"+ty);
    if(!t||!t.h)continue;
    /* bilinear, so the mesh does not come out in steps */
    const px=(fx-Math.floor(fx))*256,py=(fy-Math.floor(fy))*256;
    const x0=Math.min(255,Math.max(0,Math.floor(px))),y0=Math.min(255,Math.max(0,Math.floor(py)));
    const x1=Math.min(255,x0+1),y1=Math.min(255,y0+1);
    const sx=px-x0,sy=py-y0,H=t.h;
    return H[y0*256+x0]*(1-sx)*(1-sy)+H[y0*256+x1]*sx*(1-sy)
          +H[y1*256+x0]*(1-sx)*sy+H[y1*256+x1]*sx*sy;}
  return null;}
function terrFetch(lon,lat){
  for(const[z,rad]of TZ){
    const cx=Math.floor(tileX(lon,z)),cy=Math.floor(tileY(lat,z));
    for(let dy=-rad;dy<=rad;dy++)for(let dx=-rad;dx<=rad;dx++)
      tileGet(z,cx+dx,cy+dy);}}
/* Rings out to 140 km, spaced so the near ground gets the vertices. Earth's
   curvature drops the far ground away by d^2/2R, using the refracted radius —
   at 100 km that is nearly 700 m, which is why distant ranges stand only partly
   above the horizon. */
const TRINGS=104,TSPOKE=256,TFAR=140000,REFR=1.15;
function buildTerrain(){
  const h0=elevAt(obs[0],obs[1]);
  if(h0===null)return null;
  const R=6371000*REFR,eye=1.7;
  const pos=new Float32Array(TSPOKE*TRINGS*3),nrm=new Float32Array(TSPOKE*TRINGS*3);
  const hs=new Float32Array(TSPOKE*TRINGS);
  const la=obs[1]*RAD,coslat=Math.cos(la);
  for(let r=0;r<TRINGS;r++){
    /* geometric spacing: a stride at your feet, kilometres at the skyline */
    const d=1.5*Math.pow(TFAR/1.5,r/(TRINGS-1));
    const drop=d*d/(2*R);
    for(let s=0;s<TSPOKE;s++){
      const az=s/TSPOKE*2*Math.PI;
      const dn=d*Math.cos(az),de=d*Math.sin(az);
      const lat2=obs[1]+dn/111320,lon2=obs[0]+de/(111320*Math.max(0.05,coslat));
      let hv=elevAt(lon2,lat2);
      if(hv===null)hv=h0;
      const i=(r*TSPOKE+s);
      hs[i]=hv;
      pos[i*3]=de;pos[i*3+1]=dn;pos[i*3+2]=hv-h0-drop-eye;}}
  /* normals by central difference on the polar grid */
  for(let r=0;r<TRINGS;r++)for(let s=0;s<TSPOKE;s++){
    const i=r*TSPOKE+s;
    const a=r>0?(r-1)*TSPOKE+s:i,b=r<TRINGS-1?(r+1)*TSPOKE+s:i;
    const c=r*TSPOKE+((s+TSPOKE-1)%TSPOKE),e=r*TSPOKE+((s+1)%TSPOKE);
    const u=[pos[b*3]-pos[a*3],pos[b*3+1]-pos[a*3+1],pos[b*3+2]-pos[a*3+2]];
    const v=[pos[e*3]-pos[c*3],pos[e*3+1]-pos[c*3+1],pos[e*3+2]-pos[c*3+2]];
    let n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
    if(n[2]<0)n=[-n[0],-n[1],-n[2]];
    const m=Math.hypot(n[0],n[1],n[2])||1;
    nrm[i*3]=n[0]/m;nrm[i*3+1]=n[1]/m;nrm[i*3+2]=n[2]/m;}
  const idx=[];
  for(let r=0;r<TRINGS-1;r++)for(let s=0;s<TSPOKE;s++){
    const s2=(s+1)%TSPOKE;
    const a=r*TSPOKE+s,b=r*TSPOKE+s2,c=(r+1)*TSPOKE+s,d2=(r+1)*TSPOKE+s2;
    idx.push(a,c,b,b,c,d2);}
  return{pos:pos,nrm:nrm,hs:hs,idx:new Uint16Array(idx),h0:h0};}
const TERR_VS=`attribute vec3 aPos;attribute vec3 aNrm;attribute float aH;
uniform vec3 uRight,uUp,uFwd;uniform float uK;uniform vec2 uRes;
varying vec3 vN;varying float vD,vH,vC;
void main(){
  float len=length(aPos);
  vec3 d=aPos/max(len,1.0);
  float c=dot(d,uFwd);
  vec2 pp=vec2(dot(d,uRight),dot(d,uUp));
  float l=length(pp);
  float th=acos(clamp(c,-1.0,1.0));
  vec2 px=((l<1e-6)?vec2(0.0):pp/l*(2.0*tan(min(th,1.54)*0.5)))*uK;
  /* depth grows with the log of distance, so near ground hides far ground */
  float z=clamp(log(max(len,1.0))/12.5,0.0,1.0);
  gl_Position=vec4(px/(0.5*uRes),z*2.0-1.0,1.0);
  vN=aNrm;vD=len;vH=aH;vC=c;}`;
const TERR_FS=`precision highp float;
varying vec3 vN;varying float vD,vH,vC;
uniform vec3 uSunDir,uHaze,uAmbC;uniform float uObsc,uExp,uAmb,uSunUp;
void main(){
  /* ground behind you would otherwise be flung right across the frame by a
     projection that only makes sense forwards */
  if(vC<0.02)discard;
  vec3 n=normalize(vN);
  float lam=max(dot(n,uSunDir),0.0);
  /* the ground goes out with the Sun: direct light cut by obscuration, then
     whatever the sky still throws down */
  float direct=(1.0-uObsc)*max(uSunUp,0.0);
  float sky=0.16+0.55*max(n.z,0.0);
  vec3 rock=(vH<0.5)?vec3(0.030,0.055,0.085):mix(vec3(0.085,0.098,0.062),
       vec3(0.30,0.30,0.31),clamp((vH-900.0)/2400.0,0.0,1.0));
  vec3 c=rock*(lam*direct*11.0+sky*(0.30+uAmb*14.0)*(0.20+0.80*direct));
  /* aerial perspective: distance mixes the ground into the sky behind it */
  float f=1.0-exp(-vD/30000.0);
  c=mix(c,uHaze,f*0.99);
  c*=uExp;
  float L=dot(c,vec3(0.2126,0.7152,0.0722));
  c*=(L>1e-6)?(L/(1.0+L))/L:0.0;
  gl_FragColor=vec4(pow(max(c,0.0),vec3(1.0/2.2)),1.0);}`;
function drawTerrain(gl,c,L,W,H,dpr){
  if(!terrOn||!obs)return false;
  const key=obs[0].toFixed(4)+":"+obs[1].toFixed(4);
  if(key!==terrKey){terrKey=key;terrMesh=null;terrFetch(obs[0],obs[1]);}
  if(!terrMesh){
    terrMesh=buildTerrain();
    if(!terrMesh)return false;
    if(!glTerr)glTerr=glLink(gl,TERR_VS,TERR_FS);
    if(!terrBuf){terrBuf=gl.createBuffer();terrNrm=gl.createBuffer();
      terrIdx=gl.createBuffer();terrHgt=gl.createBuffer();}
    gl.bindBuffer(gl.ARRAY_BUFFER,terrBuf);
    gl.bufferData(gl.ARRAY_BUFFER,terrMesh.pos,gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER,terrNrm);
    gl.bufferData(gl.ARRAY_BUFFER,terrMesh.nrm,gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER,terrHgt);
    gl.bufferData(gl.ARRAY_BUFFER,terrMesh.hs,gl.STATIC_DRAW);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,terrIdx);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,terrMesh.idx,gl.STATIC_DRAW);
    terrN=terrMesh.idx.length;}
  if(!terrN)return false;
  const p=glTerr;
  gl.useProgram(p);
  gl.bindBuffer(gl.ARRAY_BUFFER,terrBuf);
  gl.enableVertexAttribArray(p.a.aPos);gl.vertexAttribPointer(p.a.aPos,3,gl.FLOAT,false,0,0);
  gl.bindBuffer(gl.ARRAY_BUFFER,terrNrm);
  gl.enableVertexAttribArray(p.a.aNrm);gl.vertexAttribPointer(p.a.aNrm,3,gl.FLOAT,false,0,0);
  gl.bindBuffer(gl.ARRAY_BUFFER,terrHgt);
  gl.enableVertexAttribArray(p.a.aH);gl.vertexAttribPointer(p.a.aH,1,gl.FLOAT,false,0,0);
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,terrIdx);
  gl.uniform2f(p.u.uRes,W,H);gl.uniform1f(p.u.uK,c.k*dpr);
  gl.uniform3fv(p.u.uRight,c.r);gl.uniform3fv(p.u.uUp,c.u);gl.uniform3fv(p.u.uFwd,c.f);
  gl.uniform3fv(p.u.uSunDir,L.hS);
  /* the haze the far ground fades into is the sky just above the horizon */
  const dim=(1-L.obsc),amb=ambOf(L.obsc);
  const hz=[0.30+0.9*dim+amb*3.0,0.36+1.05*dim+amb*1.4,0.46+1.35*dim+amb*0.8];
  gl.uniform3fv(p.u.uHaze,new Float32Array(hz));
  gl.uniform3fv(p.u.uAmbC,new Float32Array([0.34,0.46,0.66]));
  gl.uniform1f(p.u.uObsc,L.obsc);gl.uniform1f(p.u.uExp,expOf(L));
  gl.uniform1f(p.u.uAmb,amb);
  gl.uniform1f(p.u.uSunUp,Math.max(0,Math.min(1,(L.S.alt+3)/6)));
  gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);
  gl.drawElements(gl.TRIANGLES,terrN,gl.UNSIGNED_SHORT,0);
  gl.disable(gl.DEPTH_TEST);
  return true;}
function drawGL(L,jd,w,h,dpr){
  const gl=GL;
  const W=Math.round(w*dpr),H=Math.round(h*dpr);
  if(sky3d.width!==W||sky3d.height!==H){sky3d.width=W;sky3d.height=H;}
  gl.viewport(0,0,W,H);
  gl.clearColor(0,0,0,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  const c=skyCam(w,h);
  const k=c.k*dpr;
  /* the sliver of Sun still showing, which is what the glare hangs off */
  let fl=L.hS,fi=0;
  if(L.obsc>0&&!L.tot){
    const d=[L.hS[0]-L.hM[0],L.hS[1]-L.hM[1],L.hS[2]-L.hM[2]];
    const n=Math.hypot(d[0],d[1],d[2]);
    if(n>1e-9){const s=Math.min(L.rM,L.sep)*RAD;
      fl=[L.hS[0]+d[0]/n*s*0.9,L.hS[1]+d[1]/n*s*0.9,L.hS[2]+d[2]/n*s*0.9];
      const m=Math.hypot(fl[0],fl[1],fl[2]);fl=[fl[0]/m,fl[1]/m,fl[2]/m];}
    fi=Math.pow(1-L.obsc,0.55);}
  else if(L.obsc<=0)fi=1;
  const p=glProg;
  gl.useProgram(p);
  gl.bindBuffer(gl.ARRAY_BUFFER,glBuf);
  gl.enableVertexAttribArray(p.a.aPos);
  gl.vertexAttribPointer(p.a.aPos,2,gl.FLOAT,false,0,0);
  gl.uniform2f(p.u.uRes,W,H);gl.uniform1f(p.u.uK,k);
  gl.uniform3fv(p.u.uRight,c.r);gl.uniform3fv(p.u.uUp,c.u);gl.uniform3fv(p.u.uFwd,c.f);
  gl.uniform3fv(p.u.uSun,L.hS);gl.uniform3fv(p.u.uMoon,L.hM);gl.uniform3fv(p.u.uFlare,fl);
  gl.uniform1f(p.u.uSunR,L.rS*RAD);gl.uniform1f(p.u.uMoonR,L.rM*RAD);
  gl.uniform1f(p.u.uObsc,L.obsc);gl.uniform1f(p.u.uTurb,2.6);
  gl.uniform1f(p.u.uAmb,ambOf(L.obsc));gl.uniform1f(p.u.uExp,expOf(L));
  gl.uniform1f(p.u.uFlareI,fi);gl.uniform1f(p.u.uSeed,(sel?sel.i%97:0)/97);
  gl.uniform1f(p.u.uNight,1);
  gl.disable(gl.DEPTH_TEST);gl.disable(gl.BLEND);
  gl.drawArrays(gl.TRIANGLES,0,3);
  /* stars, over the sky and under the ground */
  const dim=dimOf(L.obsc)*Math.max(0.02,Math.min(1,(L.S.alt+12)/14));
  const sa=Math.max(0,Math.min(1,(0.02-dim)/0.018));
  if(sa>0.01){
    glStars(L,jd);
    if(glStarN){
      const q=glStar;
      gl.useProgram(q);
      gl.bindBuffer(gl.ARRAY_BUFFER,glStarBuf);
      gl.enableVertexAttribArray(q.a.aDir);
      gl.vertexAttribPointer(q.a.aDir,3,gl.FLOAT,false,16,0);
      gl.enableVertexAttribArray(q.a.aMag);
      gl.vertexAttribPointer(q.a.aMag,1,gl.FLOAT,false,16,12);
      gl.uniform2f(q.u.uRes,W,H);gl.uniform1f(q.u.uK,k);gl.uniform1f(q.u.uDpr,dpr);
      gl.uniform3fv(q.u.uRight,c.r);gl.uniform3fv(q.u.uUp,c.u);gl.uniform3fv(q.u.uFwd,c.f);
      gl.uniform1f(q.u.uAlpha,sa);
      gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);
      gl.drawArrays(gl.POINTS,0,glStarN);
      gl.disable(gl.BLEND);}}
  /* the ground last, over the stars it hides */
  return drawTerrain(gl,c,L,W,H,dpr);
}
function drawSky(){
  if(detView!=="ground")return;
  const {w,h}=sizeSky();if(!w)return;
  const e=sel;
  if(!obs||!e){sky3d.style.display="none";skyC.classList.remove("gl");
    sc.fillStyle="#04070c";sc.fillRect(0,0,w,h);
    sc.fillStyle="#5d6b80";sc.font='10.5px "IBM Plex Mono",monospace';
    sc.textAlign="center";sc.textBaseline="middle";
    sc.fillText(e?"Tap the globe to stand somewhere":"Select an eclipse first",w/2,h/2);
    return;}
  const jd=tJD(e),L=local(jd,obs[1],obs[0]);
  /* The Sun crosses fifteen degrees of sky an hour, so at anything past a few
     degrees of field it would leave the frame before the Moon had taken a bite.
     The view follows it until you drag, and Find the Sun gives it back. */
  if(vTrack){vAz=L.S.az;vAlt=Math.max(-8,Math.min(80,L.S.alt));}
  const c=skyCam(w,h);
  const dim=dimOf(L.obsc),cols=skyCols(L.S.alt,dim);
  const useGL=glInit();
  let hasTerr=false;
  sky3d.style.display=useGL?"block":"none";
  skyC.classList.toggle("gl",useGL);
  if(useGL){
    hasTerr=drawGL(L,jd,w,h,Math.min(devicePixelRatio||1,2));
    sc.clearRect(0,0,w,h);
  }else{
  /* Sky, banded by the altitude each row is actually looking at rather than by
     how far down the canvas it is — so zooming in on the Sun gives one flat
     colour instead of a whole day's worth of gradient across two degrees. */
  const gsky=sc.createLinearGradient(0,0,0,h);
  for(let j=0;j<=6;j++){
    const v=unSky(w/2,j/6*h,c);
    gsky.addColorStop(j/6,rgb(skyRGB(Math.asin(clamp1(v[2]))/RAD,cols,L.obsc)));}
  sc.fillStyle=gsky;sc.fillRect(0,0,w,h);
  /* stars, once it is dark enough for them to be there at all */
  const sa=Math.max(0,Math.min(1,(0.02-dim)/0.018));
  if(sa>0.01){const T=(jd-2451545.0)/36525;
    sc.globalAlpha=sa;
    for(const st of STARS){const pd=precess(st[0]*15,st[1],T);
      /* through the same local basis the Sun and Moon went through */
      const v=L.toH([cosD(pd[1])*cosD(pd[0]),cosD(pd[1])*sinD(pd[0]),sinD(pd[1])]);
      if(v[2]<-0.02)continue;
      const p=pjSky(v,c);if(p.v<=0)continue;
      const r=Math.max(0.6,1.9-st[2]*0.42);
      sc.fillStyle="#e8eef7";sc.beginPath();sc.arc(p.x,p.y,r,0,6.2832);sc.fill();}
    sc.globalAlpha=1;}
  }
  /* faint altitude and azimuth grid, so a spin still feels anchored. Only in the
     flat renderer — over a real sky it reads as scaffolding. */
  if(!useGL){
  sc.strokeStyle="rgba(255,255,255,.07)";sc.lineWidth=1;
  for(let az=0;az<360;az+=30){sc.beginPath();let up=false;
    for(let al=0;al<=88;al+=2){const p=pjSky(altaz(al,az),c);
      if(p.v<=0.02){up=false;continue;}up?sc.lineTo(p.x,p.y):sc.moveTo(p.x,p.y);up=true;}
    sc.stroke();}
  for(const al of[30,60]){sc.beginPath();let up=false;
    for(let az=0;az<=360;az+=3){const p=pjSky(altaz(al,az),c);
      if(p.v<=0.02){up=false;continue;}up?sc.lineTo(p.x,p.y):sc.moveTo(p.x,p.y);up=true;}
    sc.stroke();}
  }
  /* Sun and Moon. The bloom is drawn first so the Moon can cut into it. */
  const sp=pjSky(L.hS,c);
  const rpx=(p,deg)=>{const q=pjSky(rot(p,deg),c);return Math.hypot(q.x-sp.x,q.y-sp.y);};
  const rS=Math.max(1.2,rpx(L.hS,L.rS)),ratio=L.rM/L.rS;
  const mp=pjSky(L.hM,c),rM=Math.max(1.2,rS*ratio);
  if(!useGL){
  if(sp.v>0){
    const vis=1-L.obsc;
    if(!L.tot){
      const bl=rS*(3.2+9*vis),g=sc.createRadialGradient(sp.x,sp.y,rS*0.7,sp.x,sp.y,bl);
      g.addColorStop(0,"rgba(255,248,224,"+(0.34*Math.pow(vis,0.5)+0.05)+")");
      g.addColorStop(1,"rgba(255,248,224,0)");
      sc.fillStyle=g;sc.beginPath();sc.arc(sp.x,sp.y,bl,0,6.2832);sc.fill();}
    sc.fillStyle="#fffdf2";sc.beginPath();sc.arc(sp.x,sp.y,rS,0,6.2832);sc.fill();}
  if(L.tot&&sp.v>0){
    /* corona: a soft halo with streamers, longest either side of the equator */
    const seed=e.i;
    const g=sc.createRadialGradient(mp.x,mp.y,rM*0.99,mp.x,mp.y,rM*3.4);
    g.addColorStop(0,"rgba(226,232,240,.62)");g.addColorStop(0.25,"rgba(200,212,228,.26)");
    g.addColorStop(1,"rgba(180,198,220,0)");
    sc.fillStyle=g;sc.beginPath();sc.arc(mp.x,mp.y,rM*3.4,0,6.2832);sc.fill();
    sc.save();sc.globalCompositeOperation="lighter";
    for(let i=0;i<120;i++){const a=i/120*6.2832+rnd(seed+i)*0.05;
      const len=rM*(1.25+2.4*Math.pow(rnd(seed*3+i),1.7)*(0.45+0.55*Math.abs(Math.cos(a))));
      const g2=sc.createLinearGradient(mp.x+Math.cos(a)*rM,mp.y+Math.sin(a)*rM,
        mp.x+Math.cos(a)*len,mp.y+Math.sin(a)*len);
      g2.addColorStop(0,"rgba(228,236,246,.30)");g2.addColorStop(1,"rgba(228,236,246,0)");
      sc.strokeStyle=g2;sc.lineWidth=Math.max(0.8,rM*0.10);
      sc.beginPath();sc.moveTo(mp.x+Math.cos(a)*rM*1.0,mp.y+Math.sin(a)*rM*1.0);
      sc.lineTo(mp.x+Math.cos(a)*len,mp.y+Math.sin(a)*len);sc.stroke();}
    sc.restore();
    /* chromosphere and a couple of prominences at the limb */
    sc.strokeStyle="rgba(226,86,74,.5)";sc.lineWidth=Math.max(1,rM*0.05);
    sc.beginPath();sc.arc(mp.x,mp.y,rM*1.012,0,6.2832);sc.stroke();
    for(let i=0;i<4;i++){const a=rnd(seed*7+i)*6.2832;
      sc.strokeStyle="rgba(232,96,80,.75)";sc.lineWidth=Math.max(1.2,rM*0.08);
      sc.beginPath();sc.arc(mp.x,mp.y,rM*1.03,a,a+0.10+rnd(seed*11+i)*0.13);sc.stroke();}}
  if(mp.v>0&&L.sep<L.rS+L.rM){
    /* The Moon in daylight is invisible: what you see is the bite it takes out
       of the Sun, so the disc is clipped to the Sun's. Under totality it is the
       other way round — the Moon is the larger disc, silhouetted on the corona. */
    sc.save();
    if(!L.tot){sc.beginPath();sc.arc(sp.x,sp.y,rS,0,6.2832);sc.clip();}
    sc.fillStyle=L.tot?"#05070c":"#080b12";
    sc.beginPath();sc.arc(mp.x,mp.y,rM,0,6.2832);sc.fill();
    sc.restore();
    /* the diamond ring: the last unblocked scrap of photosphere, just before and
       just after second and third contact */
    const gap=L.sep-Math.abs(L.rM-L.rS);
    if(!L.tot&&!L.ann&&L.mag>0.985&&gap<L.rS*0.5&&gap>0){
      const a=Math.atan2(sp.y-mp.y,sp.x-mp.x);
      const bx=mp.x+Math.cos(a)*rM,by=mp.y+Math.sin(a)*rM;
      const br=Math.max(2,rS*0.5*(1-gap/(L.rS*0.5)));
      const g=sc.createRadialGradient(bx,by,0,bx,by,br*7);
      g.addColorStop(0,"rgba(255,255,245,.95)");g.addColorStop(0.12,"rgba(255,250,225,.5)");
      g.addColorStop(1,"rgba(255,250,225,0)");
      sc.fillStyle=g;sc.beginPath();sc.arc(bx,by,br*7,0,6.2832);sc.fill();
      sc.fillStyle="#fffef8";sc.beginPath();sc.arc(bx,by,br,0,6.2832);sc.fill();}}
  }
  /* The ground. Stereographic turns the horizon into a single closed curve, and
     the ground is whichever side of it the zenith is not on — outside it when you
     are looking up, inside it when you are looking down at your feet. */
  const hp=[];
  for(let az=0;az<=360;az+=1)hp.push(pjSky(altaz(0,az),c));
  const zp=pjSky([0,0,1],c);
  let skyIn=false;
  for(let i=0,j=hp.length-1;i<hp.length;j=i++)
    if((hp[i].y>zp.y)!==(hp[j].y>zp.y)&&
       zp.x<(hp[j].x-hp[i].x)*(zp.y-hp[i].y)/(hp[j].y-hp[i].y)+hp[i].x)skyIn=!skyIn;
  /* real ground draws its own horizon, so the flat one steps aside */
  if(!hasTerr){
  sc.beginPath();
  if(skyIn)sc.rect(-1e5,-1e5,2e5,2e5);
  hp.forEach((p,i)=>i?sc.lineTo(p.x,p.y):sc.moveTo(p.x,p.y));
  sc.closePath();
  const gg=sc.createLinearGradient(0,c.cy,0,h);
  gg.addColorStop(0,"#0e1219");gg.addColorStop(1,"#05070b");
  sc.fillStyle=gg;sc.fill(skyIn?"evenodd":"nonzero");
  sc.strokeStyle="rgba(140,160,185,.35)";sc.lineWidth=1;
  sc.beginPath();{let up=false;
    for(let i=0;i<hp.length;i++){
      if(hp[i].v<=0.02){up=false;continue;}
      up?sc.lineTo(hp[i].x,hp[i].y):sc.moveTo(hp[i].x,hp[i].y);up=true;}}
  sc.stroke();
  }
  /* cardinal points on the horizon */
  sc.font='9px "IBM Plex Mono",monospace';sc.textAlign="center";sc.textBaseline="top";
  for(const[az,nm]of[[0,"N"],[45,"NE"],[90,"E"],[135,"SE"],[180,"S"],[225,"SW"],
                     [270,"W"],[315,"NW"]]){
    const p=pjSky(altaz(0,az),c);if(p.v<=0.05)continue;
    if(p.x<-10||p.x>w+10)continue;
    sc.fillStyle=az%90?"#4d5c72":"#8496ad";sc.fillText(nm,p.x,p.y+4);}
  /* readouts */
  sc.font='9px "IBM Plex Mono",monospace';sc.textAlign="left";sc.textBaseline="top";
  sc.fillStyle="#8496ad";
  const phase=L.S.alt<UPALT?"SUN BELOW THE HORIZON":
    L.tot?"TOTALITY":L.ann?"ANNULAR":L.obsc>0?"PARTIAL":
    (L.sep<8?"about to begin":"no eclipse here");
  sc.fillText(phase,8,8);
  sc.fillStyle="#5d6b80";
  sc.fillText("sun "+L.S.alt.toFixed(1)+"° alt  "+L.S.az.toFixed(0)+"° az",8,20);
  sc.fillText(L.obsc>0?"obscuration "+(L.obsc*100).toFixed(1)+"%  ·  magnitude "
    +L.mag.toFixed(3):"magnitude 0",8,32);
  if(L.S.alt<0){sc.fillStyle="#7d8ea6";sc.textAlign="center";
    sc.fillText("the Sun is below the horizon here",w/2,h-58);}
  sc.textAlign="right";sc.fillStyle="#3f4c5e";
  sc.fillText((vFov<3?vFov.toFixed(1):Math.round(vFov))+"° field"
    +(vTrack?" · tracking":""),w-8,8);
  /* if you have looked away, say which way the Sun went */
  if(!vTrack&&(sp.v<=0||sp.x<0||sp.x>w||sp.y<0||sp.y>h)){
    /* straight off the view basis, so it points the right way even when the Sun
       is behind you and the projection has given up */
    const a=Math.atan2(-vdot(L.hS,c.u),vdot(L.hS,c.r));
    const rr=Math.min(w,h)*0.36;
    const ax=w/2+Math.cos(a)*rr,ay=h/2+Math.sin(a)*rr;
    sc.fillStyle="rgba(244,241,230,.55)";sc.textAlign="center";sc.textBaseline="middle";
    sc.save();sc.translate(ax,ay);sc.rotate(a);
    sc.beginPath();sc.moveTo(9,0);sc.lineTo(-4,6);sc.lineTo(-4,-6);sc.closePath();sc.fill();
    sc.restore();
    sc.fillText("sun",ax-Math.cos(a)*15,ay-Math.sin(a)*15);}
}
/* rotate a unit vector away from another by an angle, for measuring disc radii */
function rot(v,deg){let a=Math.abs(v[2])<0.9?[-v[1],v[0],0]:[0,-v[2],v[1]];
  const n=Math.hypot(a[0],a[1],a[2]);a=[a[0]/n,a[1]/n,a[2]/n];
  const c=cosD(deg),s=sinD(deg);
  return[v[0]*c+a[0]*s,v[1]*c+a[1]*s,v[2]*c+a[2]*s];}
/* First to fourth contact where you are standing, plus the deepest moment.

   An eclipse you cannot see is not an eclipse: the Sun setting mid-event is as
   real an end to it as fourth contact, and plenty of places catch only part of
   one before the Sun goes down. So every phase here is bounded by the horizon as
   well as by the discs, and the contacts say which of the two stopped them.
   Scanned on a coarse grid and bisected, cheap enough to redo on every step of
   the pin. Cached against the eclipse and the spot. */
const UPALT=-0.833;     /* refraction lifts the disc about its own width */
function circum(e,lon,lat){
  const key=e.i+":"+lon.toFixed(3)+":"+lat.toFixed(3);
  if(circ&&circ.key===key)return circ;
  const w=win(e),N=200,f=[];
  const at=t=>{const L=local(w.g+t/1440,lat,lon);
    return{t:t,out:L.sep-(L.rS+L.rM),in:L.sep-Math.abs(L.rM-L.rS),
      o:L.obsc,alt:L.S.alt,L:L};};
  for(let i=0;i<=N;i++)f.push(at(w.a+(w.b-w.a)*i/N));
  const up=s=>s.alt>UPALT;
  /* deepest sample with the Sun actually up, then one parabolic step */
  let bi=-1;
  for(let i=0;i<=N;i++)if(up(f[i])&&(bi<0||f[i].o>f[bi].o))bi=i;
  const anyBelow=f.some(s=>s.o>0);
  if(bi<0||f[bi].o<=0)
    return circ={key:key,max:0,maxO:0,alt:bi<0?-90:f[bi].alt,
      down:anyBelow,tot:false,ann:false,c1:null,c4:null,c2:null,c3:null};
  let tmax=f[bi].t;
  if(bi>0&&bi<N&&up(f[bi-1])&&up(f[bi+1])){
    const d=f[bi-1].o-2*f[bi].o+f[bi+1].o;
    if(d<0)tmax+=0.5*(f[bi-1].o-f[bi+1].o)/d*(w.b-w.a)/N;}
  const peak=at(tmax);
  /* walk out from the peak to the first sample past a contact or past sunset,
     then bisect that interval on whichever of the two it was */
  const edge=(fld,dir)=>{
    const gone=s=>s[fld]>0||!up(s);
    let a=null,b=null;
    for(let i=bi;i>=0&&i<=N;i+=dir)
      if(gone(f[i])){a=f[i].t;b=(i===bi?tmax:f[i-dir].t);break;}
    if(a===null)return{t:dir<0?w.a:w.b,hz:false,clip:true};
    for(let k=0;k<30;k++){const m=(a+b)/2;gone(at(m))?a=m:b=m;}
    const t=(a+b)/2;
    return{t:t,hz:!up(at(t+dir*1e-4)),clip:false};};
  const central=peak.L.tot||peak.L.ann;
  return circ={key:key,max:tmax,maxO:peak.o,alt:peak.alt,down:false,
    tot:peak.L.tot,ann:peak.L.ann,
    c1:edge("out",-1),c4:edge("out",1),
    c2:central?edge("in",-1):null,c3:central?edge("in",1):null};}
/* ---------- clock, live and otherwise ----------

   Playback runs at a multiple of real time rather than fitting every eclipse into
   the same number of seconds, so the numbers mean something: at 1x you are
   watching it happen, and the two and a half hours between first contact and
   fourth take two and a half hours. 500x puts a whole event in about half a
   minute, which is the pace the viewer used to run at. */
const SPEEDS=[1,5,20,60,200,500,2000];
let spIdx=5;
const spLabel=v=>v===1?"real time":"×"+v;
const nowJD=()=>Date.now()/86400000+2440587.5;
const utOf=jd=>{const c=calOf(jd);return utf(Math.round(c.mins)%1440);};
function setTLab(){const e=sel;
  if(!e){tLab.textContent="--:-- UT";tDur.textContent="";return;}
  const jd=tJD(e);
  tLab.textContent=utOf(jd);
  if(detView==="ground"&&obs){const L=local(jd,obs[1],obs[0]);
    tDur.textContent=L.obsc>0?(L.obsc*100).toFixed(1)+"% covered":"—";return;}
  const uf=tUF(e);
  const d=e.p&&uf>=0&&uf<=1?Math.round(durAt(e.p,uf)):0;
  tDur.textContent=d>0?fd(d)+" "+(e.t===1?"annular":"total"):"—";}
function repaint(){if(detView==="globe")drawGlobe();
  else if(detView==="ground")drawSky();else drawMap(sel);}
function stopT(){if(tTimer){cancelAnimationFrame(tTimer);tTimer=null;
  tPlay.classList.remove("on");tPlay.innerHTML="&#9654;";setTLab();}}
tPlay.onclick=()=>{if(tTimer){stopT();return;}
  if(!sel)return;setLive(false);
  tPlay.classList.add("on");tPlay.innerHTML="&#9646;&#9646;";
  let last=performance.now();
  const tick=now=>{if(!tTimer)return;
    const w=win(sel);
    /* advance by however much real time has actually passed, times the speed —
       so a dropped frame loses no eclipse and the rate is honest */
    const dt=Math.min(0.5,(now-last)/1000);last=now;
    let m=tOff(sel)+dt*SPEEDS[spIdx]/60;
    if(m>w.b)m=w.a;
    tFrac=Math.max(0,Math.min(1,(m-w.a)/(w.b-w.a)));
    tSlide.value=Math.round(tFrac*1000);setTLab();repaint();
    tTimer=requestAnimationFrame(tick);};
  tTimer=requestAnimationFrame(tick);};
tSpeed.onclick=()=>{spIdx=(spIdx+1)%SPEEDS.length;
  tSpeed.textContent=spLabel(SPEEDS[spIdx]);
  tSpeed.classList.toggle("on",SPEEDS[spIdx]===1);
  setTLab();};
tSlide.oninput=()=>{stopT();setLive(false);tFrac=+tSlide.value/1000;setTLab();repaint();};
/* An eclipse is "live" while the real clock sits inside its window. There is at
   most one at a time, and for about four hours every six months or so. */
function liveNow(){
  const n=nowJD();
  for(let i=Math.max(0,lo_(nowY)-3);i<Math.min(E.length,lo_(nowY)+3);i++){
    const e=E[i];
    if(Math.abs(jdOf(e.ymd[0],e.ymd[1],e.ymd[2],720)-n)>2)continue;
    const w=win(e);
    if(n>=w.g+w.a/1440&&n<=w.g+w.b/1440)return e;}
  return null;}
function nextEclipse(){const n=nowJD();
  for(let i=Math.max(0,lo_(nowY)-3);i<E.length;i++){
    const e=E[i];
    if(jdOf(e.ymd[0],e.ymd[1],e.ymd[2],1439)>n)return e;}
  return null;}
let live=false,liveTimer=null;
function setLive(on){
  if(on===live)return;
  live=on;
  tLive.classList.toggle("on",on);tLive.setAttribute("aria-pressed",String(on));
  if(liveTimer){clearInterval(liveTimer);liveTimer=null;}
  if(!on)return;
  stopT();
  const step=()=>{const e=sel;if(!e){setLive(false);return;}
    const w=win(e),n=nowJD();
    const f=((n-w.g)*1440-w.a)/(w.b-w.a);
    if(f<-0.02||f>1.02){setLive(false);syncLive();return;}
    tFrac=Math.max(0,Math.min(1,f));tSlide.value=Math.round(tFrac*1000);
    setTLab();repaint();};
  step();liveTimer=setInterval(step,1000);}
/* the chip in the masthead: an eclipse happening now, or the next one along */
function syncLive(){
  const e=liveNow();
  liveChip.classList.toggle("live",!!e);
  if(e){liveChip.innerHTML='<span class="dot"></span>Live &middot; '+TYPES[e.t].toLowerCase()
      +' eclipse in progress';
    liveChip.dataset.i=e.i;tLive.disabled=!(sel&&sel.i===e.i);}
  else{const nx=nextEclipse();
    tLive.disabled=true;if(live)setLive(false);
    if(nx){const days=Math.round(jdOf(nx.ymd[0],nx.ymd[1],nx.ymd[2],720)-nowJD());
      liveChip.textContent="Next: "+dstr(nx)+" · "+days+"d";
      liveChip.dataset.i=nx.i;}
    else{liveChip.textContent="";liveChip.dataset.i="";}}}
liveChip.onclick=()=>{const i=liveChip.dataset.i;
  if(i==="")return;
  const e=E[+i];setTab("canon");select(e);
  view.x0=e.y-1.2;view.x1=e.y+1.2;clampView();fitY();
  if(liveNow()===e){
    setLive(true);
    /* drop you under the shadow, so going live lands on the eclipse itself
       rather than on an empty horizon */
    const s=shadowPoint(nowJD());gLon=s[0];gLat=s[1];gZoom=Math.max(gZoom,2.4);
    setObs(s[0],s[1]);setDetView("ground");}
  refresh();};
tLive.onclick=()=>setLive(!live);
/* Three views, two buttons: the ground view is not somewhere you switch to, it is
   what you get by tapping a spot on the globe. Globe takes you back to pick
   another one. */
function setDetView(v){detView=v;
  vGlobe.setAttribute("aria-pressed",String(v==="globe"));
  vFlat.setAttribute("aria-pressed",String(v==="flat"));
  globeBox.style.display=v==="globe"?"block":"none";
  skyBox.style.display=v==="ground"?"block":"none";
  obsRow.style.display=v==="ground"?"flex":"none";
  tRow.style.display=v==="flat"?"none":"flex";
  mp.style.display=v==="flat"?"block":"none";
  vGlobe.textContent=v==="ground"?"‹ Globe":"Globe";
  gHint.textContent=v==="globe"?"drag to spin · tap anywhere to stand there"
    :v==="ground"?"drag to look · W A S D to walk · Globe to move":"flat overview";
  syncObs();repaint();}
vGlobe.onclick=()=>setDetView("globe");
vFlat.onclick=()=>setDetView("flat");
expand.onclick=()=>{const on=detail.classList.toggle("expanded");
  expand.setAttribute("aria-pressed",String(on));expand.classList.toggle("on",on);
  expand.innerHTML=on?"&#10529;":"&#10530;";
  expand.title=on?"Collapse back to the side panel":"Expand to fill the pane";
  requestAnimationFrame(()=>{repaint();resize();});};
/* where you are standing, in words */
const llStr=(lon,lat)=>Math.abs(lat).toFixed(2)+"°"+(lat<0?"S":"N")+" "
  +Math.abs(lon).toFixed(2)+"°"+(lon<0?"W":"E");
function syncObs(){
  if(!obs){obsPos.textContent="nowhere yet";obsInfo.textContent="";
    obsClr.disabled=true;return;}
  obsClr.disabled=false;
  /* local mean time is the only "clock time" a bare longitude can give you */
  obsPos.textContent=llStr(obs[0],obs[1]);
  if(!sel){obsInfo.textContent="";return;}
  const ci=circum(sel,obs[0],obs[1]),w=win(sel);
  const at=t=>utOf(w.g+t/1440);
  if(ci.maxO<=0){obsInfo.innerHTML='<span class="hint">'
    +(ci.down?"the eclipse happens here, but after the Sun has set"
             :"nothing of this one reaches here")+'</span>';return;}
  const bits=['<span class="lbl">Max</span><em>'+(ci.maxO*100).toFixed(1)+'%</em> at '
    +at(ci.max)];
  if(ci.c2&&ci.c3)bits.push('<span class="lbl">'+(ci.ann?"Annular":"Total")+'</span><em>'
    +fd(Math.round((ci.c3.t-ci.c2.t)*60))+'</em> from '+at(ci.c2.t));
  /* say so when it is the horizon that ends it rather than the Moon */
  const end=c=>at(c.t)+(c.hz?" (horizon)":"");
  bits.push('<span class="lbl">Visible</span>'+end(ci.c1)+"–"+end(ci.c4));
  if(terrOn){const h=elevAt(obs[0],obs[1]);
    bits.push('<span class="lbl">Ground</span>'+(h===null
      ?(terrBusy?"loading…":"—")
      :Math.round(h)+" m"+(terrBusy?" · loading…":"")));}
  obsInfo.innerHTML=bits.join(' &nbsp;·&nbsp; ');}
function setObs(lon,lat){obs=[lon,lat];circ=null;
  faceSun();syncObs();repaint();}
/* start looking at wherever the Sun is, since that is the point of standing here */
function faceSun(){vTrack=true;
  if(!obs||!sel)return;
  const L=local(tJD(sel),obs[1],obs[0]);
  vAz=L.S.az;vAlt=Math.max(-8,Math.min(80,L.S.alt));}
obsClr.onclick=()=>{obs=null;circ=null;syncObs();repaint();};
/* Terrain is the one thing here that reaches the network. It can be switched
   off, and the page falls back to a flat horizon with nothing else changed. */
obsTerr.onclick=()=>{terrOn=!terrOn;
  obsTerr.classList.toggle("on",terrOn);
  obsTerr.setAttribute("aria-pressed",String(terrOn));
  terrMesh=null;terrKey="";syncObs();repaint();};
obsSun.onclick=()=>{faceSun();vFov=Math.min(vFov,12);drawSky();};
/* spin + zoom + stand */
let gDrag=null,gPts=new Map(),gPinch=null,gMoved=false,gPin=false;
globe.addEventListener("pointerdown",ev=>{gPts.set(ev.pointerId,ev);
  if(gPts.size===1){globe.setPointerCapture(ev.pointerId);gMoved=false;
    const k=camOf(globeBox.clientWidth||320,gSize||320);
    gPin=false;
    if(obs){const s=pj(obs[0],obs[1],k);   /* grabbing the pin walks it instead */
      if(s.v>0&&Math.hypot(s.x-ev.offsetX,s.y-8-ev.offsetY)<16)gPin=true;}
    gDrag={x:ev.offsetX,y:ev.offsetY,lon:gLon,lat:gLat};
    globe.style.cursor="grabbing";}
  else gDrag=null;});
globe.addEventListener("pointermove",ev=>{
  if(gPts.has(ev.pointerId))gPts.set(ev.pointerId,ev);
  if(gPts.size===2){const[a,b]=[...gPts.values()];
    const dd=Math.hypot(a.offsetX-b.offsetX,a.offsetY-b.offsetY);
    if(gPinch&&dd>0)gZoom=Math.max(.7,Math.min(GZMAX,gZoom*dd/gPinch));
    gPinch=dd;gMoved=true;drawGlobe();return;}
  if(!gDrag)return;
  if(Math.abs(ev.offsetX-gDrag.x)+Math.abs(ev.offsetY-gDrag.y)>3)gMoved=true;
  if(gPin){const k=camOf(globeBox.clientWidth||320,gSize||320);
    const ll=unpj(ev.offsetX,ev.offsetY,k);
    if(ll){obs=ll;circ=null;syncObs();drawGlobe();}
    return;}
  gLon=gDrag.lon-(ev.offsetX-gDrag.x)*.35/gZoom;
  gLat=Math.max(-89,Math.min(89,gDrag.lat+(ev.offsetY-gDrag.y)*.35/gZoom));
  gLon=((gLon+540)%360)-180;drawGlobe();});
["pointerup","pointercancel"].forEach(t=>globe.addEventListener(t,ev=>{
  if(t==="pointerup"&&!gMoved&&gPts.size===1&&!gPin){
    const k=camOf(globeBox.clientWidth||320,gSize||320);
    const ll=unpj(ev.offsetX,ev.offsetY,k);
    /* a tap on the globe is the way into the ground view, every time */
    if(ll&&sel){setObs(ll[0],ll[1]);setDetView("ground");}}
  gPts.delete(ev.pointerId);if(gPts.size<2)gPinch=null;
  if(gPts.size===0){gDrag=null;gPin=false;globe.style.cursor="grab";}}));
globe.addEventListener("wheel",ev=>{ev.preventDefault();
  gZoom=Math.max(.7,Math.min(GZMAX,gZoom*(ev.deltaY>0?.88:1.136)));drawGlobe();},{passive:false});
const gZoomBy=f=>{gZoom=Math.max(.7,Math.min(GZMAX,gZoom*f));drawGlobe();};
gIn.onclick=()=>{detView==="ground"?fovBy(1/1.6):gZoomBy(1.6);};
gOut.onclick=()=>{detView==="ground"?fovBy(1.6):gZoomBy(1/1.6);};
gRst.onclick=()=>{if(detView==="ground"){vFov=68;faceSun();drawSky();return;}
  gZoom=1;faceEclipse();drawGlobe();};
/* The most-eclipsed spot on Earth at a given moment, as a unit vector.

   Where the axis strikes the globe, that is the umbra. Where it misses, the
   nearest point of the surface to the axis lies exactly on the terminator — which
   is why a partial-only eclipse is always seen with the Sun on the horizon. The
   small step sunward is only to keep that point on the lit side of the line. */
function deepVec(a){const k=a.g<1?Math.sqrt(1-a.g*a.g):0.03;
  const v=[a.P[0]-k*a.u[0],a.P[1]-k*a.u[1],a.P[2]-k*a.u[2]];
  const n=Math.hypot(v[0],v[1],v[2]);
  return[v[0]/n,v[1]/n,v[2]/n];}
function shadowPoint(jd){const v=deepVec(axisAt(jd));
  return[Math.atan2(v[1],v[0])/RAD,Math.asin(clamp1(v[2]))/RAD];}
function faceEclipse(){if(!sel)return;
  const c=sel.p?trackAt(sel.p,.5):shadowPoint(win(sel).g);
  gLon=c[0];gLat=c[1];}
/* look around the sky */
const fovBy=f=>{vFov=Math.max(0.35,Math.min(120,vFov*f));drawSky();};
let sDrag=null,sPts=new Map(),sPinch=null;
skyC.addEventListener("pointerdown",ev=>{sPts.set(ev.pointerId,ev);
  if(sPts.size===1){skyC.setPointerCapture(ev.pointerId);
    sDrag={x:ev.offsetX,y:ev.offsetY,az:vAz,alt:vAlt};skyC.style.cursor="grabbing";}
  else sDrag=null;});
skyC.addEventListener("pointermove",ev=>{
  if(sPts.has(ev.pointerId))sPts.set(ev.pointerId,ev);
  if(sPts.size===2){const[a,b]=[...sPts.values()];
    const dd=Math.hypot(a.offsetX-b.offsetX,a.offsetY-b.offsetY);
    if(sPinch&&dd>0)vFov=Math.max(0.35,Math.min(120,vFov*sPinch/dd));
    sPinch=dd;drawSky();return;}
  if(!sDrag)return;
  vTrack=false;                       /* looking away releases the Sun */
  const s=vFov/(skySize||300);
  vAz=((sDrag.az-(ev.offsetX-sDrag.x)*s)%360+360)%360;
  vAlt=Math.max(-25,Math.min(85,sDrag.alt+(ev.offsetY-sDrag.y)*s));
  drawSky();});
["pointerup","pointercancel"].forEach(t=>skyC.addEventListener(t,ev=>{
  sPts.delete(ev.pointerId);if(sPts.size<2)sPinch=null;
  if(sPts.size===0){sDrag=null;skyC.style.cursor="grab";}}));
skyC.addEventListener("wheel",ev=>{ev.preventDefault();
  fovBy(ev.deltaY>0?1.14:1/1.14);},{passive:false});
skyC.addEventListener("dblclick",()=>{faceSun();vFov=6;drawSky();});
/* walking: a step is a degree, which is about 111 km — the sort of distance that
   decides whether you are under the umbra or watching it go past */
function walk(dlon,dlat){if(!obs)return;
  obs=[((obs[0]+dlon+540)%360)-180,Math.max(-89.5,Math.min(89.5,obs[1]+dlat))];
  circ=null;syncObs();repaint();}
/* the panel animates open, so its final size is only known once it settles */
detail.addEventListener("transitionend",ev=>{
  if(ev.propertyName==="width"||ev.propertyName==="height")repaint();});
/* ---------- machine ---------- */
const dial=document.getElementById("dial"),dx=dial.getContext("2d");
const geom=document.getElementById("geom"),gx=geom.getContext("2d");
function elems(k){const T=k/1236.85;
  return{F:(((160.7108+390.67050284*k-0.0016118*T*T)%360)+360)%360,
         M:(((201.5643+385.81693528*k+0.0107582*T*T)%360)+360)%360};}
function spiral(t,cx,cy,R){const u=t/223,rIn=R*.40,rOut=R*.98;
  const a=-Math.PI/2+u*4*2*Math.PI,r=rIn+(rOut-rIn)*u;
  return{x:cx+r*Math.cos(a),y:cy+r*Math.sin(a),a:a};}
function drawDial(){
  const box=document.getElementById("dialBox").getBoundingClientRect();
  if(!box.width)return;
  const dp=Math.min(devicePixelRatio||1,2),Wd=box.width,Hd=box.height;
  dial.width=Math.round(Wd*dp);dial.height=Math.round(Hd*dp);dx.setTransform(dp,0,0,dp,0,0);
  dx.clearRect(0,0,Wd,Hd);
  const cx=Wd/2,cy=Hd/2,R=Math.min(Wd,Hd)*.46;
  dx.strokeStyle="#1b2635";dx.lineWidth=1;dx.beginPath();
  for(let t=0;t<=223;t+=.5){const p=spiral(t,cx,cy,R);t?dx.lineTo(p.x,p.y):dx.moveTo(p.x,p.y);}dx.stroke();
  const kc=sel?sel.k:0;
  const marks=new Map();
  for(const e of E){if(e.k<kc-223||e.k>kc+223)continue;if(!on[e.t])continue;
    if(!marks.has(e.cell))marks.set(e.cell,e);}
  for(let c=0;c<223;c++){const p=spiral(c+.5,cx,cy,R),nx=Math.cos(p.a),ny=Math.sin(p.a);
    const has=marks.has(c);
    dx.strokeStyle=has?"#3a4d66":"#16202c";dx.beginPath();
    dx.moveTo(p.x-nx*4,p.y-ny*4);dx.lineTo(p.x+nx*4,p.y+ny*4);dx.stroke();}
  for(const[c,e]of marks){const p=spiral(c+.5,cx,cy,R);
    dx.fillStyle=COL[e.t];dx.globalAlpha=e.t===3?.5:.92;
    dx.beginPath();dx.arc(p.x,p.y,e.t===3?2:3.1,0,6.2832);dx.fill();}
  dx.globalAlpha=1;
  if(sel){const p=spiral(sel.cell+.5,cx,cy,R);
    /* pointer takes the eclipse's own colour; partial's slate is lifted so it
       stays visible against the dial */
    const pc=sel.t===3?"#7d8ea6":COL[sel.t];
    dx.strokeStyle=pc;dx.lineWidth=1.5;dx.beginPath();dx.moveTo(cx,cy);dx.lineTo(p.x,p.y);dx.stroke();
    dx.fillStyle=pc;dx.beginPath();dx.arc(p.x,p.y,4.6,0,6.2832);dx.fill();
    dx.strokeStyle="rgba(7,10,16,.85)";dx.lineWidth=1.2;dx.stroke();
    dx.fillStyle=pc;dx.font='500 10px "IBM Plex Mono",monospace';dx.textAlign="center";
    dx.textBaseline="middle";
    dx.fillText("CELL "+sel.cell,cx,cy-11);
    dx.fillStyle="#5d6b80";dx.font='9px "IBM Plex Mono",monospace';
    dx.fillText("saros "+sel.S,cx,cy+3);
    dx.fillText("of 223",cx,cy+15);
  }else{dx.fillStyle="#3d4b5e";dx.font='9.5px "IBM Plex Mono",monospace';dx.textAlign="center";
    dx.fillText("223 lunations = 1 saros",cx,cy);}
}
function drawGeom(){
  const w=geom.parentElement.clientWidth||360;
  const h=Math.max(150,Math.min(w*0.42,210));
  const dp=Math.min(devicePixelRatio||1,2);
  geom.style.height=h+"px";geom.width=Math.round(w*dp);geom.height=Math.round(h*dp);
  gx.setTransform(dp,0,0,dp,0,0);gx.clearRect(0,0,w,h);
  const pw=w/3,pad=10,R=Math.min(pw*0.34,h*0.30);
  const el=sel?elems(sel.k):{F:0,M:0};
  const lab=(x,t,s)=>{gx.fillStyle="#4d5c72";gx.font='8.5px "IBM Plex Mono",monospace';
    gx.textAlign="center";gx.textBaseline="top";gx.fillText(t,x,8);
    gx.fillStyle="#7f8fa4";gx.fillText(s,x,h-16);};
  for(let i=1;i<3;i++){gx.strokeStyle="#141d29";gx.lineWidth=1;gx.beginPath();
    gx.moveTo(Math.round(i*pw)+.5,pad);gx.lineTo(Math.round(i*pw)+.5,h-pad);gx.stroke();}
  /* 1 - node geometry */
  let cx=pw*0.5,cy=h*0.52;
  gx.strokeStyle="#1b2635";gx.lineWidth=1;gx.beginPath();gx.arc(cx,cy,R,0,6.2832);gx.stroke();
  gx.strokeStyle="rgba(95,217,192,.15)";gx.lineWidth=6;
  for(const c of[0,180]){const a=c*Math.PI/180;
    gx.beginPath();gx.arc(cx,cy,R,a-21*Math.PI/180,a+21*Math.PI/180);gx.stroke();}
  gx.strokeStyle="#2b3a4d";gx.lineWidth=1;gx.setLineDash([3,3]);
  gx.beginPath();gx.moveTo(cx-R*1.25,cy);gx.lineTo(cx+R*1.25,cy);gx.stroke();gx.setLineDash([]);
  gx.fillStyle="#3d4b5e";gx.font='7.5px "IBM Plex Mono",monospace';gx.textAlign="left";
  gx.textBaseline="middle";gx.fillText("node",cx+R*1.27,cy);
  gx.fillStyle="#5d6b80";gx.beginPath();gx.arc(cx,cy,3.2,0,6.2832);gx.fill();
  const aF=el.F*Math.PI/180,mx=cx+R*Math.cos(aF),my=cy-R*Math.sin(aF);
  gx.strokeStyle="rgba(232,163,61,.5)";gx.lineWidth=1;gx.beginPath();gx.moveTo(cx,cy);gx.lineTo(mx,my);gx.stroke();
  gx.strokeStyle="#e8a33d";gx.lineWidth=1.2;gx.beginPath();
  gx.moveTo(mx+ (mx-cx)*0.42, my+(my-cy)*0.42);gx.lineTo(mx,my);gx.stroke();
  gx.fillStyle="#f4f1e6";gx.beginPath();gx.arc(mx,my,3.6,0,6.2832);gx.fill();
  const inWin=Math.abs(Math.sin(aF))<0.36;
  lab(pw*0.5,"1 \u00b7 NODE","F "+el.F.toFixed(0)+"\u00b0 "+(inWin?"\u2713 in window":"\u00d7 no eclipse"));
  /* 2 - distance */
  cx=pw*1.5;
  const ecc=0.35,ra=R*1.05,rb=ra*Math.sqrt(1-ecc*ecc),fx=cx-ra*ecc;
  gx.strokeStyle="#1b2635";gx.lineWidth=1;gx.beginPath();
  gx.ellipse(cx,cy,ra,rb,0,0,6.2832);gx.stroke();
  gx.fillStyle="#5d6b80";gx.beginPath();gx.arc(fx,cy,3.2,0,6.2832);gx.fill();
  const aM=el.M*Math.PI/180;
  const px2=cx+ra*Math.cos(aM),py2=cy-rb*Math.sin(aM);
  const rk=384399*(1-0.0549*Math.cos(aM));
  const near=rk<384399;
  gx.fillStyle=near?"#f4f1e6":"#e8a33d";
  gx.beginPath();gx.arc(px2,py2,near?4.2:3.0,0,6.2832);gx.fill();
  gx.strokeStyle="#2b3a4d";gx.setLineDash([2,3]);gx.lineWidth=1;
  gx.beginPath();gx.moveTo(fx,cy);gx.lineTo(px2,py2);gx.stroke();gx.setLineDash([]);
  gx.fillStyle="#3d4b5e";gx.font='7.5px "IBM Plex Mono",monospace';gx.textAlign="center";
  gx.textBaseline="middle";gx.fillText("perigee",fx+ra*0.62,cy+rb+9);
  lab(pw*1.5,"2 \u00b7 DISTANCE","M\u2032 "+el.M.toFixed(0)+"\u00b0 \u00b7 "+Math.round(rk/1000)+"k km");
  /* 3 - gamma */
  cx=pw*2.5;
  const Re=R*0.82;
  gx.strokeStyle="#2b3d52";gx.lineWidth=1;gx.beginPath();gx.arc(cx,cy,Re,0,6.2832);gx.stroke();
  gx.fillStyle="rgba(43,61,82,.15)";gx.fill();
  gx.strokeStyle="#25344a";gx.setLineDash([3,4]);gx.lineWidth=1;
  for(const v of[-0.9972,0.9972]){const Y=cy-v*Re;
    gx.beginPath();gx.moveTo(cx-Re*1.5,Y);gx.lineTo(cx+Re*1.5,Y);gx.stroke();}
  gx.setLineDash([]);
  const g=sel?sel.g:0,gy=cy-g*Re;
  gx.strokeStyle=sel?COL[sel.t]:"#5d6b80";gx.lineWidth=1.8;
  gx.beginPath();gx.moveTo(cx-Re*1.5,gy);gx.lineTo(cx+Re*1.5,gy);gx.stroke();
  gx.fillStyle=sel?COL[sel.t]:"#5d6b80";gx.beginPath();gx.arc(cx,gy,3.2,0,6.2832);gx.fill();
  lab(pw*2.5,"3 \u00b7 SHADOW AXIS","\u03b3 "+(sel?sel.g.toFixed(3):"\u2014")+
    (sel?(Math.abs(sel.g)<0.9972?" \u2713 hits Earth":" \u00d7 misses"):""));
}
/* ---------- selection + stepper ---------- */
function pickIn(e){const arr=BY.saros.get(e.S);return{arr:arr,i:arr.indexOf(e)};}
function select(e,openDetail){
  sel=e;
  if(openDetail!==false)detail.classList.add("open");
  /* every eclipse has a clock now, partials included */
  stopT();setLive(false);tFrac=.5;tSlide.value=500;
  tSlide.disabled=false;tPlay.disabled=false;circ=null;
  faceEclipse();setTLab();syncLive();syncObs();
  const {arr,i}=pickIn(e);
  syncNav();
  stepInfo.innerHTML='<span class="d">'+dstr(e)+'</span><span class="hint">saros '+e.S+
    ' &middot; '+(i+1)+' of '+arr.length+' &middot; '+TYPES[e.t]+'</span>';
  const c=(l,v)=>'<div><span class="lbl" style="display:block;margin-bottom:2px">'+l+'</span><span class="v">'+v+'</span></div>';
  pStats.innerHTML=c("Saros series",e.S)+c("Inex series",e.I)+c("Gamma",e.g.toFixed(3))+c("Dial cell",e.cell+" / 223")+
    (e.dur?c("Path width",e.w+" km")+c("Max duration",fd(e.dur)):"")+
    (e.p?c("Greatest eclipse",utf(e.p.ut))+
      c("At",Math.abs(e.p.pts[6][1]).toFixed(1)+"\u00b0"+(e.p.pts[6][1]<0?"S":"N")+" "+
        Math.abs(e.p.pts[6][0]).toFixed(1)+"\u00b0"+(e.p.pts[6][0]<0?"W":"E")):"");
  const w=win(e);
  pStats.innerHTML+=c("Whole event",fdl(Math.round((w.b-w.a)*60)));
  const pv=arr[i-1];
  if(pv&&pv.p&&e.p){const dl=((e.p.pts[6][0]-pv.p.pts[6][0])+540)%360-180;
    pNote.innerHTML="Saros "+e.S+" last came round in "+pv.ymd[0]+". One turn of the dial later its track has moved <em>"+
      Math.abs(dl).toFixed(0)+"\u00b0 "+(dl<0?"west":"east")+"</em> and <em>"+
      Math.abs(e.p.pts[6][1]-pv.p.pts[6][1]).toFixed(1)+"\u00b0 "+
      (e.p.pts[6][1]>pv.p.pts[6][1]?"north":"south")+"</em>. Amber and bronze show the two previous returns.";}
  else pNote.innerHTML=e.t===3?"Gamma exceeds 0.9972, so the shadow axis passes outside Earth. Only a partial eclipse, near a pole."
    :"Central paths are computed for 1000\u20133000 CE. Earlier, &Delta;T uncertainty makes the longitude meaningless.";
  refresh();
}
function step(d){if(!sel)return;const{arr,i}=pickIn(sel);const n=arr[i+d];if(n)select(n,detail.classList.contains("open"));}
/* chronological neighbour, skipping types the filters have switched off */
function nextVisible(from,d){for(let j=from+d;j>=0&&j<E.length;j+=d)if(on[E[j].t])return E[j];return null;}
const navBase=d=>sel?sel.i:(d>0?lo_((view.x0+view.x1)/2)-1:lo_((view.x0+view.x1)/2));
function stepTime(d){const n=nextVisible(navBase(d),d);
  if(n){stop();select(n,sel?detail.classList.contains("open"):true);}}
function deselect(){stop();stopT();setLive(false);sel=null;hover=null;circ=null;
  detail.classList.remove("open");detail.classList.remove("expanded");
  expand.setAttribute("aria-pressed","false");expand.classList.remove("on");
  expand.innerHTML="&#10530;";expand.title="Expand to fill the pane";
  stepInfo.innerHTML='<span class="d">Select an eclipse</span><span class="hint">tap a point on the canon</span>';
  tSlide.disabled=true;tPlay.disabled=true;tLab.textContent="--:-- UT";tDur.textContent="";
  syncLive();syncObs();syncNav();refresh();}
function syncNav(){
  if(sel){const{arr,i}=pickIn(sel);prev.disabled=i<=0;next.disabled=i>=arr.length-1;}
  else{prev.disabled=true;next.disabled=true;}
  prevT.disabled=!nextVisible(navBase(-1),-1);
  nextT.disabled=!nextVisible(navBase(1),1);
  clr.disabled=!sel;play.disabled=!sel;}
function refresh(){draw();setReadout();
  if(tab==="canon")repaint();
  else{drawDial();drawGeom();}}
prev.onclick=()=>{stop();step(-1);};
next.onclick=()=>{stop();step(1);};
prevT.onclick=()=>stepTime(-1);
nextT.onclick=()=>stepTime(1);
clr.onclick=()=>deselect();
zIn.onclick=()=>zoomAt((PAD.l+W-PAD.r)/2,.7);
zOut.onclick=()=>zoomAt((PAD.l+W-PAD.r)/2,1.43);
zRst.onclick=()=>{view.x0=nowY-30;view.x1=nowY+30;fitY();draw();setReadout();syncNav();};
function stop(){if(timer){clearInterval(timer);timer=null;play.classList.remove("on");}}
play.onclick=()=>{
  if(timer){stop();return;}
  if(!sel)return;
  play.classList.add("on");
  timer=setInterval(()=>{const{arr,i}=pickIn(sel);
    if(i>=arr.length-1){select(arr[0],detail.classList.contains("open"));}
    else step(1);},900);
};
/* ---------- tabs / filters ---------- */
function setTab(t){tab=t;
  tCanon.setAttribute("aria-pressed",String(t==="canon"));
  tMach.setAttribute("aria-pressed",String(t==="machine"));
  paneCanon.classList.toggle("on",t==="canon");
  paneMach.classList.toggle("on",t==="machine");
  axisSeg.style.display=t==="canon"?"flex":"none";
  requestAnimationFrame(()=>{if(t==="canon"){resize();repaint();}
    else{drawDial();drawGeom();}});}
tCanon.onclick=()=>setTab("canon");tMach.onclick=()=>setTab("machine");
szBtn.onclick=()=>{szDur=!szDur;szBtn.setAttribute("aria-pressed",String(szDur));
  szBtn.classList.toggle("on",szDur);
  szBtn.innerHTML=szDur?"\u25c9 Duration":"\u25cf Even";draw();setReadout();};
document.querySelectorAll(".key").forEach(b=>b.onclick=()=>{
  const t=+b.dataset.t;on[t]=!on[t];b.setAttribute("aria-pressed",String(on[t]));
  if(sel&&!on[sel.t])deselect();else{syncNav();refresh();}});
new ResizeObserver(()=>{if(tab==="canon")repaint();
  else{drawDial();drawGeom();}}).observe(document.querySelector("main"));
/* ---------- canon interaction ---------- */
function pick(px,py){let b=null,bd=17*17;
  const a0=Math.max(0,lo_(view.x0)-4),a1=Math.min(E.length,lo_(view.x1)+4);
  for(let i=a0;i<a1;i++){const e=E[i];if(!on[e.t])continue;
    const dx2=sx(e.y)-px;if(dx2<-17||dx2>17)continue;
    const dy2=sy(yv(e))-py;if(dy2<-17||dy2>17)continue;
    const d=dx2*dx2+dy2*dy2;if(d<bd){bd=d;b=e;}}return b;}
const BOUNDS=(function(){let sl=1e9,sh=-1e9,il=1e9,ih=-1e9;
  for(const e of E){if(e.S<sl)sl=e.S;if(e.S>sh)sh=e.S;if(e.I<il)il=e.I;if(e.I>ih)ih=e.I;}
  return{saros:[sl,sh],inex:[il,ih],gamma:[-1.7,1.7]};})();
function clampY(){const b=BOUNDS[mode],pad=(b[1]-b[0])*.06+1,L=b[0]-pad,U=b[1]+pad;
  const s=view.y1-view.y0;
  if(s>=U-L){view.y0=L;view.y1=U;return;}
  if(view.y0<L){view.y0=L;view.y1=L+s;}
  if(view.y1>U){view.y1=U;view.y0=U-s;}}
function clampView(){let s=Math.min(Math.max(view.x1-view.x0,.6),5050);
  const c=(view.x0+view.x1)/2;view.x0=c-s/2;view.x1=c+s/2;
  if(view.x0<-2005){view.x0=-2005;view.x1=-2005+s;}
  if(view.x1>3005){view.x1=3005;view.x0=3005-s;}}
function zoomAt(px,f){const a=ix(px);
  let s=Math.min(Math.max((view.x1-view.x0)*f,.6),5050);
  const t=(a-view.x0)/(view.x1-view.x0);view.x0=a-t*s;view.x1=view.x0+s;
  clampView();draw();setReadout();}
cv.addEventListener("wheel",ev=>{ev.preventDefault();
  if(ev.shiftKey){const c=(view.y0+view.y1)/2,s=(view.y1-view.y0)*(ev.deltaY>0?1.12:.89);
    view.y0=c-s/2;view.y1=c+s/2;clampY();draw();}else zoomAt(ev.offsetX,ev.deltaY>0?1.14:.877);},{passive:false});
let drag=null,pts=new Map(),pinch=null,moved=false;
cv.addEventListener("pointerdown",ev=>{pts.set(ev.pointerId,ev);
  if(pts.size===1){cv.setPointerCapture(ev.pointerId);moved=false;cv.style.cursor="grabbing";
    drag={x:ev.offsetX,y:ev.offsetY,vx0:view.x0,vx1:view.x1,vy0:view.y0,vy1:view.y1,lock:null};}else drag=null;});
cv.addEventListener("pointermove",ev=>{
  if(pts.has(ev.pointerId))pts.set(ev.pointerId,ev);
  if(pts.size===2){const[a,b]=[...pts.values()];
    const dd=Math.hypot(a.offsetX-b.offsetX,a.offsetY-b.offsetY),m=(a.offsetX+b.offsetX)/2;
    if(pinch&&dd>0)zoomAt(m,pinch/dd);pinch=dd;moved=true;return;}
  if(drag){const dx0=ev.offsetX-drag.x,dy0=ev.offsetY-drag.y;
    if(Math.abs(dx0)+Math.abs(dy0)>4)moved=true;
    /* soft axis lock: a mostly-sideways drag stops nudging the vertical axis */
    if(!drag.lock&&Math.abs(dx0)+Math.abs(dy0)>7)
      drag.lock=Math.abs(dx0)>2.2*Math.abs(dy0)?"x":Math.abs(dy0)>2.2*Math.abs(dx0)?"y":"xy";
    const lk=drag.lock||"xy";
    if(lk==="y"){view.x0=drag.vx0;view.x1=drag.vx1;}
    else{view.x0=drag.vx0-dx0/(W-PAD.l-PAD.r)*(drag.vx1-drag.vx0);
      view.x1=drag.vx1-dx0/(W-PAD.l-PAD.r)*(drag.vx1-drag.vx0);}
    if(lk==="x"){view.y0=drag.vy0;view.y1=drag.vy1;}
    else{view.y0=drag.vy0+dy0/(H-PAD.t-PAD.b)*(drag.vy1-drag.vy0);
      view.y1=drag.vy1+dy0/(H-PAD.t-PAD.b)*(drag.vy1-drag.vy0);}
    clampView();clampY();draw();setReadout();return;}
  const h=pick(ev.offsetX,ev.offsetY);
  if(h!==hover){hover=h;cv.style.cursor=h?"pointer":"grab";draw();setReadout();}});
["pointerup","pointercancel"].forEach(t=>cv.addEventListener(t,ev=>{
  if(t==="pointerup"&&!moved&&pts.size===1){const h=pick(ev.offsetX,ev.offsetY);
    if(h){stop();select(h);}else if(sel)deselect();}
  pts.delete(ev.pointerId);if(pts.size<2)pinch=null;
  if(pts.size===0){drag=null;cv.style.cursor="grab";}}));
/* only drop hover here: killing the drag would break panning past the canvas edge */
cv.addEventListener("pointerleave",()=>{if(pts.size===0){drag=null;pinch=null;}
  if(hover){hover=null;draw();setReadout();}});
cv.addEventListener("dblclick",()=>{view.x0=nowY-30;view.x1=nowY+30;fitY();draw();setReadout();});
/* horizontal keys walk the time axis, vertical keys walk the saros axis —
   the same two directions the canon itself is plotted on */
addEventListener("keydown",e=>{
  if(e.target&&(e.target.tagName==="INPUT"||e.target.tagName==="BUTTON"))return;
  /* in the ground view, W A S D walks you across the map: a degree a step, or a
     quarter of one with shift, which is about the width of an umbral path */
  if(detView==="ground"&&obs&&"wasdWASD".includes(e.key)){
    const s=e.shiftKey?0.25:1,k=e.key.toLowerCase();
    walk(k==="a"?-s:k==="d"?s:0,k==="w"?s:k==="s"?-s:0);e.preventDefault();return;}
  if(e.key==="ArrowLeft"){stepTime(-1);e.preventDefault();}
  else if(e.key==="ArrowRight"){stepTime(1);e.preventDefault();}
  else if(e.key==="ArrowUp"&&sel){stop();step(-1);e.preventDefault();}
  else if(e.key==="ArrowDown"&&sel){stop();step(1);e.preventDefault();}
  else if(e.key==="Escape"){deselect();}});
function setMode(m){if(m===mode)return;
  const from=new Map();for(const e of E)from.set(e,baseYv(e));
  const fy0=view.y0,fy1=view.y1;mode=m;fitY();
  const ty0=view.y0,ty1=view.y1;
  mSaros.setAttribute("aria-pressed",String(m==="saros"));
  mInex.setAttribute("aria-pressed",String(m==="inex"));
  mGamma.setAttribute("aria-pressed",String(m==="gamma"));
  if(matchMedia("(prefers-reduced-motion:reduce)").matches){draw();setReadout();return;}
  const t0=performance.now(),D=620;hover=null;
  (function s(t){const p=Math.min(1,(t-t0)/D),k=p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
    view.y0=fy0+(ty0-fy0)*k;view.y1=fy1+(ty1-fy1)*k;
    yvOverride=e=>{const a=from.get(e);return a+(baseYv(e)-a)*k;};draw();
    if(p<1)requestAnimationFrame(s);else{yvOverride=null;view.y0=ty0;view.y1=ty1;draw();setReadout();}})(t0);}
mSaros.onclick=()=>setMode("saros");mInex.onclick=()=>setMode("inex");mGamma.onclick=()=>setMode("gamma");
resize();
tSlide.disabled=true;tPlay.disabled=true;
setDetView("globe");syncNav();syncLive();
/* the chip is the only thing on the page that ages, so it is the only thing that
   needs a heartbeat when nothing is selected */
setInterval(syncLive,60000);
</script>
</body>
</html>'''
