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
.readout{flex:none;border-top:1px solid var(--rule);background:var(--ink2);padding:7px 12px;
 display:flex;gap:3px 18px;align-items:baseline;flex-wrap:wrap;font-size:11px;min-height:32px}
.lbl{color:var(--dim);font-size:9px;letter-spacing:.12em;text-transform:uppercase;margin-right:5px}
.date{font-family:"Newsreader",serif;font-style:italic;color:var(--corona)}
.hint{color:var(--dim);font-size:10px}
em{font-style:normal;color:var(--corona)}
#detail{height:0;overflow:hidden;border-top:1px solid var(--rule);background:var(--ink2);
 transition:height .26s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;flex:none}
#detail.open{height:min(58%,410px)}
#detail .inner{overflow-y:auto;flex:1;min-height:0}
#map{display:block;background:#04070c;border-bottom:1px solid var(--rule);margin:0 auto;max-width:100%}
/* desktop: canon left, selected eclipse right; full width when nothing is selected */
@media (min-width:900px){
  #paneCanon{flex-direction:row}
  #detail{height:auto!important;width:0;border-top:0;border-left:1px solid var(--rule);
   transition:width .26s cubic-bezier(.4,0,.2,1)}
  #detail.open{width:min(46%,560px)}
}
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
#stepInfo{flex:1;text-align:center;font-size:10.5px;line-height:1.35;min-width:0}
#stepInfo .d{font-family:"Newsreader",serif;font-style:italic;font-size:14px;color:var(--corona);display:block}
@media (max-width:520px){h1{font-size:16px}header{padding:9px 11px 6px}.bar{padding:6px 11px;gap:6px}
 .seg button{padding:6px 8px}.foot{padding:6px 9px;gap:6px}button.b{padding:6px 8px;font-size:10px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<header><h1>Canon of Solar Eclipses</h1>
<div class="sub"><b>2000&nbsp;BCE&thinsp;&ndash;&thinsp;3000&nbsp;CE</b> &middot; <b id="nEcl">-</b> eclipses</div></header>
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
      <div class="readout" id="ro"></div>
    </div>
    <div id="detail"><div class="inner">
      <canvas id="map"></canvas>
      <div class="blk"><div class="grid2" id="pStats"></div></div>
      <div class="blk"><div class="note" id="pNote"></div></div>
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
  <button class="b" id="prev" aria-label="Previous in series">&#9664;</button>
  <div id="stepInfo"><span class="d">Select an eclipse</span><span class="hint" id="stepSub">tap a point on the canon</span></div>
  <button class="b" id="play" aria-label="Play through series">&#9654;&#9654;</button>
  <button class="b" id="next" aria-label="Next in series">&#9654;</button>
</div>
<script>
const AB="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
const IX={};for(let i=0;i<64;i++)IX[AB[i]]=i;
const g2=(s,i)=>IX[s[i]]*64+IX[s[i+1]];
const g4=(s,i)=>((IX[s[i]]*64+IX[s[i+1]])*64+IX[s[i+2]])*64+IX[s[i+3]];
const gL=(s,i,lo,hi)=>lo+g2(s,i)/4095*(hi-lo);
const META="__META__",PIDX="__PIDX__",PDAT="__PDAT__";
const TYPES=["Total","Annular","Hybrid","Partial"],COL=["#f4f1e6","#e8a33d","#d76b52","#43536b"];
const MON=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const LAND="__COAST__".split("~").map(s=>{const o=[];
  for(let i=0;i<s.length;i+=4)o.push([gL(s,i,-180,180),gL(s,i+2,-90,90)]);return o;});
const E=[];
for(let i=0,n=0;i<META.length;i+=15,n++){
  const c=g4(META,i),d=c%32,m=((c-d)/32)%12+1,y=Math.floor(c/384)-2000;
  const S=g2(META,i+4)-20,I=g2(META,i+9)-10;
  E.push({i:n,y:y+((m-1)*30.6+d)/365.25,ymd:[y,m,d],S:S,I:I,t:IX[META[i+6]],
    g:gL(META,i+7,-1.6,1.6),w:g2(META,i+11),dur:g2(META,i+13),
    k:223*(I-271)+358*S+44,cell:0,p:null});
}
const MAXDUR=Math.max(...E.map(e=>e.dur));
for(const e of E)e.cell=((e.k%223)+223)%223;
for(let i=0;i<PIDX.length;i+=4){
  const at=g4(PIDX,i),b=PDAT.substr(i/4*58,58),pts=[];
  for(let q=0;q<52;q+=4)pts.push([gL(b,q,-180,180),gL(b,q+2,-90,90)]);
  E[at].p={pts:pts,ut:g2(b,52),w:g2(b,54),dur:g2(b,56)};
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
      const pts=ev.p.pts,segs=[[]];
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
/* the panel animates open, so its final size is only known once it settles */
detail.addEventListener("transitionend",ev=>{
  if(ev.propertyName==="width"||ev.propertyName==="height")drawMap(sel);});
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
    dx.strokeStyle="#b58b4c";dx.lineWidth=1.5;dx.beginPath();dx.moveTo(cx,cy);dx.lineTo(p.x,p.y);dx.stroke();
    dx.fillStyle="#b58b4c";dx.beginPath();dx.arc(p.x,p.y,4.6,0,6.2832);dx.fill();
    dx.strokeStyle="rgba(7,10,16,.85)";dx.lineWidth=1.2;dx.stroke();
    dx.fillStyle="#b58b4c";dx.font='500 10px "IBM Plex Mono",monospace';dx.textAlign="center";
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
  const {arr,i}=pickIn(e);
  prev.disabled=i<=0;next.disabled=i>=arr.length-1;
  stepInfo.innerHTML='<span class="d">'+dstr(e)+'</span><span class="hint">saros '+e.S+
    ' &middot; '+(i+1)+' of '+arr.length+' &middot; '+TYPES[e.t]+'</span>';
  const c=(l,v)=>'<div><span class="lbl" style="display:block;margin-bottom:2px">'+l+'</span><span class="v">'+v+'</span></div>';
  pStats.innerHTML=c("Saros series",e.S)+c("Inex series",e.I)+c("Gamma",e.g.toFixed(3))+c("Dial cell",e.cell+" / 223")+
    (e.dur?c("Path width",e.w+" km")+c("Max duration",fd(e.dur)):"")+
    (e.p?c("Greatest eclipse",utf(e.p.ut))+
      c("At",Math.abs(e.p.pts[6][1]).toFixed(1)+"\u00b0"+(e.p.pts[6][1]<0?"S":"N")+" "+
        Math.abs(e.p.pts[6][0]).toFixed(1)+"\u00b0"+(e.p.pts[6][0]<0?"W":"E")):"");
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
function refresh(){draw();setReadout();if(tab==="canon")drawMap(sel);else{drawDial();drawGeom();}}
prev.onclick=()=>{stop();step(-1);};
next.onclick=()=>{stop();step(1);};
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
  requestAnimationFrame(()=>{if(t==="canon"){resize();drawMap(sel);}else{drawDial();drawGeom();}});}
tCanon.onclick=()=>setTab("canon");tMach.onclick=()=>setTab("machine");
szBtn.onclick=()=>{szDur=!szDur;szBtn.setAttribute("aria-pressed",String(szDur));
  szBtn.classList.toggle("on",szDur);
  szBtn.innerHTML=szDur?"\u25c9 Duration":"\u25cf Even";draw();setReadout();};
document.querySelectorAll(".key").forEach(b=>b.onclick=()=>{
  const t=+b.dataset.t;on[t]=!on[t];b.setAttribute("aria-pressed",String(on[t]));
  if(sel&&!on[sel.t]){}refresh();});
new ResizeObserver(()=>{if(tab==="canon")drawMap(sel);else{drawDial();drawGeom();}})
  .observe(document.querySelector("main"));
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
    if(h){stop();select(h);}else if(sel){detail.classList.remove("open");
      setTimeout(()=>drawMap(sel),300);}}
  pts.delete(ev.pointerId);if(pts.size<2)pinch=null;
  if(pts.size===0){drag=null;cv.style.cursor="grab";}}));
/* only drop hover here: killing the drag would break panning past the canvas edge */
cv.addEventListener("pointerleave",()=>{if(pts.size===0){drag=null;pinch=null;}
  if(hover){hover=null;draw();setReadout();}});
cv.addEventListener("dblclick",()=>{view.x0=nowY-30;view.x1=nowY+30;fitY();draw();setReadout();});
addEventListener("keydown",e=>{
  if(e.key==="ArrowLeft"&&sel){step(-1);e.preventDefault();}
  else if(e.key==="ArrowRight"&&sel){step(1);e.preventDefault();}
  else if(e.key==="Escape"){stop();detail.classList.remove("open");}});
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
</script>
</body>
</html>'''
