#!/usr/bin/env python3
"""Anonymized item-level learning evidence: standard library only. No network."""
import argparse,csv,json,html,statistics
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
    md=['# Teaching objective attainment (anonymized)','',f'Course: {report["course"]}. Students represented: {report["students"]}.','','## Assessment summary','| Type | Complete n | Partial n | Missing n | Mean % of complete |','|---|---:|---:|---:|---:|']
    for typ,v in report['assessments'].items():md.append(f'| {typ} | {v["n_complete"]} | {v["n_partial"]} | {v["n_missing"]} | {v["mean_percent"] if v["mean_percent"] is not None else "N/A"} |')
    md+=['','![Mean scores](mean_scores.svg)','','## Objective evidence','| Objective | Assessment | Earned / Possible | Observed % | Students meeting local target |','|---|---|---:|---:|---:|']
    for id,obj in report['objectives'].items():
        for typ,v in obj['by_assessment'].items():md.append(f'| {id}: {obj["label"]} | {typ} | {v["earned_points"]}/{v["possible_points"]} | {v["observed_percent"] if v["observed_percent"] is not None else "N/A"} | {v["n_meeting_target"]}/{v["n_complete_objective"]} |')
    md+=['','![Objective attainment](objective_attainment.svg)','','**Pre/post growth: NOT COMPARABLE.** '+report['growth_note'],'','Thresholds shown are teacher-defined planning indicators, not BC provincial letter-grade cutoffs. Diagnostic questions sample prerequisites; post-tests sample taught objectives; raw percentages are not equivalent constructs.','','## Teaching interpretation','Review lower-attainment objectives, inspect item distractors and student work, reteach prerequisite misconceptions and collect new aligned evidence. Do not infer causation from these scores alone.','']
    if report['warnings']:md+=['## Data warnings']+['- '+x for x in report['warnings']]
    (out/'summary.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print('Created:',*(str(out/x) for x in ['report.json','summary.md','mean_scores.svg','objective_attainment.svg']),sep='\n - ')
if __name__=='__main__':main()
