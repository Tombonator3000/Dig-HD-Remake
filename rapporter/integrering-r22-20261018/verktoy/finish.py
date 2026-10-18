"""Record only completed package checks and prepare reviewable release metadata."""
from pathlib import Path
import json,hashlib,shutil,gzip
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];T=R/'testing/distro-r22';G=R/'grafikk/rapporter/restgrafikk-r22-20261018'
c=json.loads((T/'kontroll-linux.json').read_text());assert c['result']=='PASS' and c['packaged_native_tests']['passed'];b=json.loads((T/'build-result.json').read_text());assert b['status']=='completed' and b['conclusion']=='success' and b['headSha']==c['code'];assert c['verified_mod_files']==45089 and c['payload_files_verified']==278
rel=json.loads((T/'release.json').read_text());src=next(x for x in rel['assets'] if x['name']=='TheDigHD-Linux-kildekode.tar.gz');assert src['digest']=='sha256:'+c['source']['source_archive_sha256'];assert src['size']==c['source']['source_archive_bytes']
for name in ['kontroll-linux.json','build-result.json','native-tests.json']:shutil.copy2(T/name,P/name)
for src,label in [(T/'smoke/log.txt','package-start.log.gz'),(T/'native/boston100/log.txt','package-boston100.log.gz')]:
 with gzip.open(P/label,'wb') as f:f.write(src.read_bytes())
for frame,label in [(210,'package-kneeling.png'),(420,'package-rising.png'),(660,'package-standing.png')]:shutil.copy2(T/'native/boston100/dumps'/f'frame_{frame:06d}_room032.png',P/label)
checks=c['packaged_native_tests']['post_startup_checks'];h=c['appimage_sha256'];n=c['appimage_bytes'];observed=len(c['packaged_native_tests']['cases'][0]['seen_target_cels'])
text=f'''The Dig HD for Linux, r22, 18. oktober 2026

Last ned TheDigHD-x86_64.AppImage fra Linux-releasen, gjør den kjørbar og start:

chmod +x TheDigHD-x86_64.AppImage
./TheDigHD-x86_64.AppImage

Pakken inneholder motor, spill, musikk, tale, HD-grafikk og alle 55 HD-filmer.
F5 åpner menyen. HD Graphics velger HD eller originalgrafikk.
Alt+Enter bytter vindu og fullskjerm.
Uten FUSE: ./TheDigHD-x86_64.AppImage --appimage-extract-and-run

R22 er integrert: alle 48 utvalgte Boston-ruter opp av vannet er nytegnet,
og 91 små gamle originalfragmenter er eksportert med riktig palett.
Tidligere rettinger og alle 55 HD-filmer er bevart.
Alle 45 089 mod-manifestfiler og 278 leveransefiler er kontrollert i nedlastingen.
Pakkens egen motor viser alle {observed} nye ruter, med {checks} fullomtegningskontroller
etter oppstart uten avvik. Standardoppstart, intro og HD/klassisk-bytte består også.
Byggets tester av oppstart, grafikkvalg og Debian 12 er grønne.
5963 ruter gjenstår i arbeidsinventaret. Alle er ikke bekreftet som synlige mangler.
Naturlig gjennomspilling og Toms visuelle godkjenning gjenstår.

Kode: {c['code']}
HD-mod: {c['hd_mod']}
AppImage: {n} byte
SHA-256: {h}

Uendrede motorkilder og byggeoppskrift ligger i TheDigHD-Linux-kildekode.tar.gz.
Ingen vanlige lagringer eller brukerinnstillinger er endret av testene.
Spillet tilhører Disney/Lucasfilm. Toms avtalte bruk og deling gjelder fortsatt.
'''
(T/'LES-MEG-LINUX.txt').write_text(text);(R/'LES-MEG-RETTINGER.txt').write_text('R22 er integrert i spillet og kontrollert som ny Linux-pakke.\nhttps://github.com/Tombonator3000/Dig-HD-Remake/releases/tag/linux\n\n'+text)
body=rel['body']+f'''\n\nR22, kontrollert 18. oktober 2026: 48 nye Boston-ruter opp av vannet og 91 palettrettede små originalfragmenter er integrert via PR68. Alle 45 089 mod-manifestfiler og 278 leveransefiler i den faktiske nedlastingen stemmer. Pakkens egen motor viser alle 48 nye ruter med {checks} fullomtegningskontroller etter oppstart uten avvik. Oppstart, intro og HD/klassisk-bytte er kontrollert. Alle 55 HD-filmer og tidligere rettinger er bevart. 5963 ruter gjenstår i arbeidsinventaret; naturlig gjennomspilling og Toms visuelle godkjenning gjenstår. Uendrede motorkilder og byggeoppskrift ligger i det separate GPL-kildearkivet.\n'''
(T/'release-notes.md').write_text(body)
p=P/'RAPPORT.md';p.write_text(p.read_text()+f'''\n## Publisert og kontrollert Linux-pakke\n\nBygg39117793203 er grønt, inkludert oppstart/grafikkvalg og Debian12. Faktisk nedlasting fra releasen: {n} byte, SHA-256 {h}. Alle45089 manifestfiler og278 leveransefiler stemmer med den integrerte modden. Alle55 HD-filmer er med. Standard AppRun, intro og HD/klassisk-bytte består550 oppdateringer og fem opptegningskontroller uten avvik. Pakkens egen motor viser alle48 nye ruter i rom32, med{checks} fullomtegningskontroller etter oppstart uten avvik. Ingen vanlige lagringer er brukt eller endret av prøvene.\n\nPakkens kontrollfil, byggresultat, native logger og faktiske skjermbilder ligger ved. Den uendrede GPL-kildepakkens kontrollsum og de fem patchene er kontrollert. Naturlig gjennomspilling og Toms visuelle godkjenning gjenstår.\n''')
f=json.loads((G/'fremdrift.json').read_text());f.update(published=True,distro=True,remaining_published_art_cels=5963);f['integration'].update(appimage_sha256=h,appimage_bytes=n,verified_package=True);(G/'fremdrift.json').write_text(json.dumps(f,indent=2)+'\n');p=G/'RAPPORT.md';p.write_text('R22 er nå integrert og publisert i kontrollert AppImage. Se ../integrering-r22-20261018/RAPPORT.md for den endelige leveransen.\n\n'+p.read_text())
print('Delivery checks complete',observed,'new cels',checks,'native checks',n,h)
