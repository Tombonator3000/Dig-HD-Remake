from pathlib import Path
import os,json,subprocess,sys,concurrent.futures
Q=Path(__file__).resolve().parent;cases=json.loads((Q/'cases.json').read_text());mode=sys.argv[1];app=sys.argv[2] if len(sys.argv)>2 else None

def run(c):
 env=os.environ.copy();env['DIGHD_TEST_OBJSTATE']=c['state'];args=[sys.executable,str(Q/'run_qa.py'),mode+'-'+c['tag'],'--room',str(c['room']),'--camx',str(c['camx']),'--camy',str(c['camy']),'--frames','110','--dump','110']
 if app:args+=['--appimage',app]
 r=subprocess.run(args,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=240);print(c['tag'],r.returncode,flush=True);return {'case':c,'exit_code':r.returncode,'output':r.stdout}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,cases))
(Q/(mode+'-suite.json')).write_text(json.dumps(results,indent=2)+'\n');assert all(r['exit_code']==0 for r in results)
