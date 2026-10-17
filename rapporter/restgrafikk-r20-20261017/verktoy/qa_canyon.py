"""Physical pose coverage and redraw QA, with an explicit observed-cel gate."""
from pathlib import Path
import os,sys,re,json
from concurrent.futures import ThreadPoolExecutor
R=Path(os.environ.get('DIGHD_WORKSPACE',Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r20-20261017';sys.path.insert(0,str(R));from runqa import run
targets={int(r['file'].split('_')[1]) for r in json.loads((P/'canyon-registration.json').read_text())}
def one(anim):
    name=f'r20-canyon/{anim}'
    # Room 23 and source room 15 have byte-identical colours for every used
    # costume34 AKPL code. The palette equality proof is stored separately.
    run(name,dict(SAVE=15,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=34,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='160,180',DIGHD_TEST_CAMX=160,DIGHD_TEST_CAMY=100,DIGHD_TEST_PALETTE=0,DIGHD_QUIT_AT=1800,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=40),binary=R/'motor/scummvm',mod=R/'kandidat-r20')
    log=(R/'testing'/name/'log.txt').read_text();checks=[(int(f),int(n)) for f,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen={int(v) for v in re.findall(r'soft cel (\d+) costume 34 ',log)};errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
    return dict(animation=anim,checks=checks,seen_hd_cells=sorted(seen),seen_new_cells=sorted(seen&targets),errors=errors,passed=bool(checks) and not any(n for f,n in checks if f>=100) and not errors,has_new_art=bool(seen&targets))
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,[6,7,8,9]))
seen=set().union(*(set(r['seen_new_cells']) for r in results));report=dict(cases=results,seen_new_cells=sorted(seen),unseen_new_cells=sorted(targets-seen),passed=all(r['passed'] for r in results) and seen==targets)
(P/'qa-canyon.json').write_text(json.dumps(report,indent=2)+'\n');print([(r['animation'],len(r['seen_new_cells']),r['passed']) for r in results]);print('Coverage',len(seen),'/',len(targets),report['passed'])
