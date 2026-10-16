from runqa import run,ROOT
from concurrent.futures import ThreadPoolExecutor
cases={'plateau':dict(DIGHD_TEST_ROOM=55),'hole':dict(DIGHD_TEST_ROOM=55,DIGHD_TEST_OBJSTATE='387:1'),'nest':dict(DIGHD_TEST_ROOM=44),'spider':dict(DIGHD_TEST_ROOM=44,DIGHD_TEST_COSTUME=136,DIGHD_TEST_POS='80,100',DIGHD_TEST_CHORE_EVERY=8),'laser':dict(DIGHD_TEST_ROOM=85),'maggie':dict(DIGHD_TEST_ROOM=15,DIGHD_TEST_COSTUME=18,DIGHD_TEST_POS='160,170',DIGHD_TEST_CHORE_EVERY=12),'brink':dict(DIGHD_TEST_ROOM=15,DIGHD_TEST_COSTUME=17,DIGHD_TEST_POS='160,170',DIGHD_TEST_CHORE_EVERY=12),'boston':dict(DIGHD_TEST_ROOM=15,DIGHD_TEST_COSTUME=14,DIGHD_TEST_POS='160,170',DIGHD_TEST_CHORE_EVERY=12)}
def case(z):
 n,v=z;run('r18-native/'+n,dict(SAVE=15,DIGHD_QUIT_AT=500,**v),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r18')
with ThreadPoolExecutor(max_workers=3) as p:list(p.map(case,cases.items()))
