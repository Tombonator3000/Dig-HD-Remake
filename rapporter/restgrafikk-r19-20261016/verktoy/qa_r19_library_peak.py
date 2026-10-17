import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
def one(anim):
 run(f'r19-library-peak/267-{anim}',dict(SAVE=15,DIGHD_TEST_ROOM=92,DIGHD_TEST_COSTUME=267,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=0,DIGHD_TEST_POS='0,0',DIGHD_TEST_CAMX=160,DIGHD_QUIT_AT=215,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=1),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,[7,8]))
