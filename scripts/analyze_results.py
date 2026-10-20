#!/usr/bin/env python3
"""Anonymized item-level learning evidence: standard library only. No network."""
import argparse,csv,json,html,statistics,math
from pathlib import Path
from collections import defaultdict

def read_csv(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def validate_and_analyze(results, items, cfg):
    objective_ids={o['id'] for o in cfg['objectives']}
    if not 0 <= float(cfg['threshold']) <= 1:raise ValueError('threshold outside 0..1')
    target={o['id']:float(o.get('target',cfg['threshold'])) for o in cfg['objectives']}
    if any(not 0<=t<=1 for t in target.values()):raise ValueError('objective target outside 0..1')
    valid_types={'diagnostic','quiz','test'}
    idx={}
    for x in items:
        k=x['item_id']; atype=x['assessment_type']
        if k in idx:raise ValueError('duplicate item '+k)
        if atype not in valid_types or x['objective_id'] not in objective_ids:raise ValueError('bad item type or objective '+k)
        pts=float(x['max_points'])
        if pts<=0:raise ValueError('bad max points for '+k)
        idx[k]={**x,'max_points':pts}
    seen=set(); scores=defaultdict(list); per_obj=defaultdict(lambda:[0.,0.,set()]); by_student=defaultdict(lambda:defaultdict(dict)); warnings=[]
    for r in results:
        sid=r['student_id'].strip(); typ=r['assessment_type']; key=r['item_id']
        if not sid:raise ValueError('empty pseudonymous student_id')
        if key not in idx:raise ValueError('unknown item '+key)
        if typ != idx[key]['assessment_type']:raise ValueError('type mismatch '+key)
        uid=(sid,typ,key)
        if uid in seen:raise ValueError('duplicate score record '+str(uid))
        seen.add(uid)
        try:v=float(r['points'])
        except (ValueError,TypeError):raise ValueError('invalid/missing points '+str(uid))
        mx=idx[key]['max_points']
        if not 0<=v<=mx:raise ValueError('score outside bounds '+str(uid))
        by_student[sid][typ][key]=v
        oid=idx[key]['objective_id']; rec=per_obj[(typ,oid)];rec[0]+=v;rec[1]+=mx;rec[2].add(sid)
    typs=sorted({x['assessment_type'] for x in items},key=lambda t:['diagnostic','quiz','test'].index(t))
    result={'course':cfg.get('course','unspecified'),'synthetic_or_real':'not determined by script','students':len(by_student),'assessments':{},'objectives':{},'warnings':warnings,'growth_comparable':False,'growth_note':'Not calculated: different pre/post items, constructs or scales may not be equivalent. Comparable anchor design and matched cohort validation required.'}
    for typ in typs:
        relevant={k:v for k,v in idx.items() if v['assessment_type']==typ}
        total=sum(i['max_points'] for i in relevant.values())
        complete=[]; incomplete=[]
        for sid,smap in by_student.items():
            present=smap.get(typ,{})
            if set(present)==set(relevant):complete.append((sid,sum(present.values())/total*100))
            elif present:incomplete.append(sid)
        values=[v for _,v in complete]
        result['assessments'][typ]={'n_complete':len(values),'n_partial':len(incomplete),'n_missing':len(by_student)-len(values)-len(incomplete),'possible_points_per_complete_student':total,'mean_percent':round(statistics.mean(values),2) if values else None,'median_percent':round(statistics.median(values),2) if values else None,'distribution':{'0-49':sum(v<50 for v in values),'50-69':sum(50<=v<70 for v in values),'70-84':sum(70<=v<85 for v in values),'85-100':sum(v>=85 for v in values)}}
        if incomplete: warnings.append(f'{typ}: {len(incomplete)} partial student assessment(s) excluded from overall mean; objective scores based on observed item responses only.')
    for typ in typs:
        for o in cfg['objectives']:
            oid=o['id']; a,b,sids=per_obj.get((typ,oid),[0.,0.,set()]);pct=round(100*a/b,2) if b else None
            # Per-student objective rate among students with complete coverage for that objective.
            associated={k:v for k,v in idx.items() if v['assessment_type']==typ and v['objective_id']==oid}
            flags=[]
            for sid,smap in by_student.items():
                present=smap.get(typ,{})
                if associated and set(associated).issubset(present):
                    n=sum(present[k] for k in associated); d=sum(x['max_points'] for x in associated.values());flags.append(n/d>=target[oid])
            result['objectives'].setdefault(oid,{'label':o['label'],'target_percent':target[oid]*100,'by_assessment':{}})['by_assessment'][typ]={'earned_points':round(a,2),'possible_points':round(b,2),'observed_percent':pct,'n_observed':len(sids),'n_complete_objective':len(flags),'n_meeting_target':sum(flags),'pct_students_meeting_target':round(100*sum(flags)/len(flags),2) if flags else None}
            if not b:warnings.append(f'{oid}/{typ}: no item scores; no attainment estimate')
    if not results:warnings.append('No responses found; no attainment estimates available.')
    return result

def svg_bar(title,labels,series,filename,y_label='Percent',max_val=100):
    width=900;height=max(280,140+len(labels)*65);x0=270;plot=550;line=55
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title,quote=True)}">', '<rect width="100%" height="100%" fill="white"/>', f'<text x="30" y="35" font-family="Arial" font-size="20" font-weight="bold">{html.escape(title)}</text>',f'<text x="30" y="58" font-family="Arial" font-size="12">{html.escape(y_label)} • missing values not plotted</text>']
    palette=['#277da1','#f4a261','#488a6c']
    for j,lab in enumerate(labels):
        y=100+j*65;parts.append(f'<text x="15" y="{y+15}" font-family="Arial" font-size="13">{html.escape(lab[:38])}</text>')
        for k,(name,vals) in enumerate(series):
            v=vals[j]
            if v is None:continue
            bw=max(0,min(plot,(v/max_val)*plot));by=y-3+k*15
            parts +=[f'<rect x="{x0}" y="{by}" width="{bw:.1f}" height="12" fill="{palette[k%len(palette)]}"/>',f'<text x="{x0+bw+5:.1f}" y="{by+10}" font-family="Arial" font-size="11">{v:.1f}%</text>']
    foot=height-26
    for k,(name,_) in enumerate(series):
        xx=30+k*240;parts +=[f'<rect x="{xx}" y="{foot-10}" width="12" height="12" fill="{palette[k%len(palette)]}"/>',f'<text x="{xx+18}" y="{foot}" font-family="Arial" font-size="12">{html.escape(name)}</text>']
    parts.append('</svg>');Path(filename).write_text('\n'.join(parts),encoding='utf-8')

def interactive_radar(report, filename):
    """Write a self-contained, responsive objective radar with hover/focus details."""
    payload=json.dumps(report,ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')
    document='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Interactive objective attainment radar</title>
<style>
:root{color-scheme:light dark;font-family:system-ui,-apple-system,sans-serif}body{margin:0;padding:16px;background:Canvas;color:CanvasText}.wrap{max-width:900px;margin:auto}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:6px}select{font:inherit;padding:6px 10px}.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:.9rem}.key{display:inline-flex;gap:6px;align-items:center}.swatch{width:18px;height:3px;background:#2356e8}.swatch.target{background:#d97706;border-top:2px dashed #d97706}.chart{position:relative;width:100%;min-height:420px}svg{display:block;width:100%;height:auto;overflow:visible}.grid{fill:none;stroke:color-mix(in srgb,CanvasText 22%,transparent);stroke-width:1}.axis{stroke:color-mix(in srgb,CanvasText 28%,transparent);stroke-width:1}.target{fill:rgba(217,119,6,.08);stroke:#d97706;stroke-width:2;stroke-dasharray:7 5}.observed{fill:rgba(35,86,232,.28);stroke:#2356e8;stroke-width:4;stroke-linejoin:round}.dot{fill:#2356e8;stroke:Canvas;stroke-width:2;cursor:pointer}.dot:focus{outline:none;stroke:#d97706;stroke-width:5}.axis-label{font-size:14px;fill:CanvasText;text-anchor:middle}.axis-value{font-weight:750;fill:#2356e8}.tick{font-size:11px;fill:color-mix(in srgb,CanvasText 66%,transparent)}.tooltip{position:absolute;display:none;pointer-events:none;max-width:280px;padding:10px 12px;border:1px solid color-mix(in srgb,CanvasText 24%,transparent);border-radius:8px;background:Canvas;color:CanvasText;box-shadow:0 6px 24px rgba(0,0,0,.18);font-size:.9rem;line-height:1.4;z-index:2}.tooltip strong{display:block;margin-bottom:4px}.note{font-size:.85rem;opacity:.75;margin-top:4px}@media(max-width:600px){body{padding:8px}.axis-label{font-size:12px}.chart{min-height:340px}}
</style></head><body><main class="wrap"><div class="controls"><label>Assessment <select id="assessment"></select></label><div class="legend"><span class="key"><i class="swatch"></i>Observed</span><span class="key"><i class="swatch target"></i>Teacher target</span></div></div><div class="chart" id="chart"><svg viewBox="0 0 760 620" role="img" aria-labelledby="title desc"><title id="title">Objective attainment radar</title><desc id="desc">Use the assessment selector. Focus or hover a point for exact objective evidence.</desc></svg><div class="tooltip" id="tip" role="status"></div></div><p class="note">Percentages are observed performance on sampled items. Teacher targets are local planning indicators, not provincial grade boundaries.</p></main>
<script>
const report=__REPORT__;const objectives=Object.entries(report.objectives);const types=Object.keys(report.assessments);const svg=document.querySelector('svg'),sel=document.querySelector('#assessment'),tip=document.querySelector('#tip'),chart=document.querySelector('#chart');
const NS='http://www.w3.org/2000/svg',cx=380,cy=295,R=190;for(const t of types){const o=document.createElement('option');o.value=t;o.textContent=t[0].toUpperCase()+t.slice(1);sel.append(o)}sel.value=types.at(-1)||'';
function node(tag,attrs={},text=''){const n=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);if(text)n.textContent=text;return n}function polar(i,value){const a=-Math.PI/2+i*2*Math.PI/objectives.length;return[cx+Math.cos(a)*R*value/100,cy+Math.sin(a)*R*value/100]}function polygon(values){return values.map((v,i)=>polar(i,v).join(',')).join(' ')}function pct(v){return v==null?'N/A':Number(v).toFixed(1)+'%'}
function render(){svg.querySelectorAll('g').forEach(n=>n.remove());if(!objectives.length){svg.append(node('g',{},'No objective data'));return}const typ=sel.value,g=node('g');svg.append(g);for(const level of [20,40,60,80,100]){g.append(node('polygon',{points:polygon(objectives.map(()=>level)),class:'grid'}));g.append(node('text',{x:cx+5,y:cy-R*level/100+12,class:'tick'},level+'%'))}objectives.forEach(([id,obj],i)=>{const [x,y]=polar(i,100);g.append(node('line',{x1:cx,y1:cy,x2:x,y2:y,class:'axis'}));const [lx,ly]=polar(i,122);const label=node('text',{x:lx,y:ly,class:'axis-label'});label.append(node('tspan',{x:lx,dy:'0'},id+': '+(obj.label.length>24?obj.label.slice(0,23)+'…':obj.label)));const value=obj.by_assessment[typ]?.observed_percent;label.append(node('tspan',{x:lx,dy:'18',class:'axis-value'},pct(value)));g.append(label)});const values=objectives.map(([,o])=>o.by_assessment[typ]?.observed_percent??0);g.append(node('polygon',{points:polygon(values),class:'observed'}));const targets=objectives.map(([,o])=>o.target_percent);g.append(node('polygon',{points:polygon(targets),class:'target'}));objectives.forEach(([id,obj],i)=>{const rec=obj.by_assessment[typ]||{};const [x,y]=polar(i,rec.observed_percent??0);const dot=node('circle',{cx:x,cy:y,r:7,class:'dot',tabindex:0,'aria-label':id+' '+obj.label+', '+pct(rec.observed_percent)});const show=e=>{tip.innerHTML='';const title=document.createElement('strong');title.textContent=id+': '+obj.label;tip.append(title);const lines=[['Assessment',typ],['Observed',pct(rec.observed_percent)],['Points',(rec.earned_points??'N/A')+' / '+(rec.possible_points??'N/A')],['Meeting target',(rec.n_meeting_target??0)+' / '+(rec.n_complete_objective??0)],['Local target',pct(obj.target_percent)],['Students observed',String(rec.n_observed??0)]];for(const [a,b] of lines){const d=document.createElement('div');d.textContent=a+': '+b;tip.append(d)}tip.style.display='block';const box=chart.getBoundingClientRect();const source=e.touches?.[0]||e;tip.style.left=Math.min(box.width-290,Math.max(4,(source.clientX||box.left+x*box.width/760)-box.left+12))+'px';tip.style.top=Math.max(4,(source.clientY||box.top+y*box.width/760)-box.top-20)+'px'};dot.addEventListener('mouseenter',show);dot.addEventListener('mousemove',show);dot.addEventListener('focus',show);dot.addEventListener('mouseleave',()=>tip.style.display='none');dot.addEventListener('blur',()=>tip.style.display='none');g.append(dot)})}
sel.addEventListener('change',render);render();
</script></body></html>'''.replace('__REPORT__',payload)
    Path(filename).write_text(document,encoding='utf-8')

def svg_radar(report, filename, assessment=None):
    """Write the portable static counterpart of the interactive radar."""
    objectives=list(report['objectives'].items());types=list(report['assessments']);typ=assessment or (types[-1] if types else '')
    width=760;height=620;cx=380;cy=295;radius=190
    def fmt_pct(value):return 'N/A' if value is None else f'{value:.1f}%'
    def point(i,value,scale=1):
        angle=-math.pi/2+i*2*math.pi/len(objectives);r=radius*value/100*scale
        return cx+math.cos(angle)*r,cy+math.sin(angle)*r
    def points(values):return ' '.join(f'{point(i,v)[0]:.1f},{point(i,v)[1]:.1f}' for i,v in enumerate(values))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Objective attainment radar for {html.escape(typ,quote=True)}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="24" y="32" font-family="Arial" font-size="20" font-weight="bold">Objective attainment radar — {html.escape(typ.title())}</text>']
    if len(objectives)<3:
        parts += ['<text x="24" y="70" font-family="Arial" font-size="14">Radar chart requires at least three objectives; use the objective table or bar chart.</text>','</svg>'];Path(filename).write_text('\n'.join(parts),encoding='utf-8');return
    for level in [20,40,60,80,100]:
        parts.append(f'<polygon points="{points([level]*len(objectives))}" fill="none" stroke="#d1d5db" stroke-width="1"/>')
        parts.append(f'<text x="{cx+5}" y="{cy-radius*level/100+12:.1f}" font-family="Arial" font-size="11" fill="#6b7280">{level}%</text>')
    for i,(oid,obj) in enumerate(objectives):
        x,y=point(i,100);lx,ly=point(i,122)
        parts +=[f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#9ca3af"/>',f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Arial" font-size="13">{html.escape(oid)}: {html.escape(obj["label"][:22])}</text>',f'<text x="{lx:.1f}" y="{ly+17:.1f}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="bold" fill="#2356e8">{fmt_pct(obj["by_assessment"].get(typ,{}).get("observed_percent"))}</text>']
    values=[o['by_assessment'].get(typ,{}).get('observed_percent') or 0 for _,o in objectives]
    parts.append(f'<polygon points="{points(values)}" fill="#2356e8" fill-opacity=".28" stroke="#2356e8" stroke-width="4" stroke-linejoin="round"/>')
    parts.append(f'<polygon points="{points([o["target_percent"] for _,o in objectives])}" fill="none" stroke="#d97706" stroke-width="3" stroke-dasharray="7 5"/>')
    for i,(oid,obj) in enumerate(objectives):
        rec=obj['by_assessment'].get(typ,{});x,y=point(i,rec.get('observed_percent') or 0);detail=f'{oid}: {obj["label"]}; {typ}; observed {fmt_pct(rec.get("observed_percent"))}; points {rec.get("earned_points")}/{rec.get("possible_points")}; meeting target {rec.get("n_meeting_target")}/{rec.get("n_complete_objective")}; target {fmt_pct(obj["target_percent"])}'
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#2356e8" stroke="white" stroke-width="2"><title>{html.escape(detail)}</title></circle>')
    parts +=['<line x1="24" y1="586" x2="48" y2="586" stroke="#2356e8" stroke-width="4"/><text x="56" y="591" font-family="Arial" font-size="12">Observed</text>','<line x1="150" y1="586" x2="174" y2="586" stroke="#d97706" stroke-width="2" stroke-dasharray="7 5"/><text x="182" y="591" font-family="Arial" font-size="12">Teacher target</text>','</svg>']
    Path(filename).write_text('\n'.join(parts),encoding='utf-8')

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--items',required=True);p.add_argument('--objectives',required=True);p.add_argument('--out',required=True);a=p.parse_args(argv)
    cfg=json.loads(Path(a.objectives).read_text(encoding='utf-8'));report=validate_and_analyze(read_csv(a.input),read_csv(a.items),cfg)
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    typs=list(report['assessments']);labels=[t.title() for t in typs]
    svg_bar('Mean score among complete responses',labels,[('Mean percent',[report['assessments'][t]['mean_percent'] for t in typs])],out/'mean_scores.svg')
    oid=list(report['objectives']);series=[]
    for typ in typs:series.append((typ.title(),[report['objectives'][o]['by_assessment'][typ]['observed_percent'] for o in oid]))
    svg_bar('Objective-level observed points earned / possible', [f'{o}: {report["objectives"][o]["label"]}' for o in oid],series,out/'objective_attainment.svg')
    svg_radar(report,out/'objective_radar.svg')
    interactive_radar(report,out/'objective_radar.html')
    md=['# Teaching objective attainment (anonymized)','',f'Course: {report["course"]}. Students represented: {report["students"]}.','','## Assessment summary','| Type | Complete n | Partial n | Missing n | Mean % of complete |','|---|---:|---:|---:|---:|']
    for typ,v in report['assessments'].items():md.append(f'| {typ} | {v["n_complete"]} | {v["n_partial"]} | {v["n_missing"]} | {v["mean_percent"] if v["mean_percent"] is not None else "N/A"} |')
    md+=['','![Mean scores](mean_scores.svg)','','## Objective evidence','| Objective | Assessment | Earned / Possible | Observed % | Students meeting local target |','|---|---|---:|---:|---:|']
    for id,obj in report['objectives'].items():
        for typ,v in obj['by_assessment'].items():md.append(f'| {id}: {obj["label"]} | {typ} | {v["earned_points"]}/{v["possible_points"]} | {v["observed_percent"] if v["observed_percent"] is not None else "N/A"} | {v["n_meeting_target"]}/{v["n_complete_objective"]} |')
    md+=['','![Objective attainment](objective_attainment.svg)','','![Objective radar](objective_radar.svg)','','[Open the interactive objective radar](objective_radar.html) — choose an assessment and hover or focus each point for exact evidence.','','**Pre/post growth: NOT COMPARABLE.** '+report['growth_note'],'','Thresholds shown are teacher-defined planning indicators, not BC provincial letter-grade cutoffs. Diagnostic questions sample prerequisites; post-tests sample taught objectives; raw percentages are not equivalent constructs.','','## Teaching interpretation','Review lower-attainment objectives, inspect item distractors and student work, reteach prerequisite misconceptions and collect new aligned evidence. Do not infer causation from these scores alone.','']
    if report['warnings']:md+=['## Data warnings']+['- '+x for x in report['warnings']]
    (out/'summary.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print('Created:',*(str(out/x) for x in ['report.json','summary.md','mean_scores.svg','objective_attainment.svg','objective_radar.svg','objective_radar.html']),sep='\n - ')
if __name__=='__main__':main()
