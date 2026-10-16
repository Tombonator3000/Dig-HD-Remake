import os
from pathlib import Path
import hashlib,json
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';M=R/'kandidat-r19';B=R/'hd-leveranse';overrides={r['path']:r for r in json.loads((P/'OVERRIDES.json').read_text())} if (P/'OVERRIDES.json').exists() else {};unexpected=[];replaced=[];count=0
for line in (B/'SHA256SUMS').read_text().splitlines():
 expected,path=line.split(None,1);path=path.lstrip('*');f=M/path;actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None;count+=1
 if actual==expected:continue
 if path in overrides and expected==overrides[path]['base_sha256'] and actual==overrides[path]['sha256']:replaced.append(path)
 else:unexpected.append(dict(path=path,expected=expected,actual=actual))
report=dict(base_sha='4a0ab61efae8ead2f30eeb057d3a02d468ae98bc',files_checked=count,documented_replacements=replaced,changed_or_missing=unexpected)
(P/'base-preservation.json').write_text(json.dumps(report,indent=2)+'\n');print(count,'checked;',len(replaced),'documented replacements;',len(unexpected),'unexpected changes');assert not unexpected
