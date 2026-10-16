from runqa import *
from concurrent.futures import ThreadPoolExecutor
cases=[]
for a in [1,4,5,6,7,8,9,10,11,12]:cases.append(('pole%d'%a,dict(SAVE=1,DIGHD_TEST_ROOM=68,DIGHD_TEST_COSTUME=178,DIGHD_TEST_POS='460,160',DIGHD_TEST_CAMX=460,DIGHD_TEST_ANIMATION=a,DIGHD_TEST_DIRECTION=6,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_QUIT_AT=650,DIGHD_DUMP_EVERY=40)))
for cid in range(290,298):cases.append(('crystal%d'%cid,dict(SAVE=1,DIGHD_TEST_ROOM=98 if cid<294 else 99,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_POS='160,160',DIGHD_TEST_CHORE_EVERY=12,DIGHD_TEST_STATIC_SCENE=1,DIGHD_QUIT_AT=350)))
cases += [('water',dict(SAVE=1,DIGHD_TEST_ROOM=101,DIGHD_QUIT_AT=500)),('dowel',dict(SAVE=1,DIGHD_TEST_ROOM=68,DIGHD_TEST_CAMX=520,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_OBJSTATE='474:1',DIGHD_QUIT_AT=220)),('inventory10',dict(SAVE=10,DIGHD_TEST_KEYS='120:i',DIGHD_QUIT_AT=220)),('inventory15',dict(SAVE=15,DIGHD_TEST_KEYS='120:i',DIGHD_QUIT_AT=220))]
with ThreadPoolExecutor(max_workers=3) as p:list(p.map(lambda c:run('r17-final/'+c[0],c[1],binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r17'),cases))
