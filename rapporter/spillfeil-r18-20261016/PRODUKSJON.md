# Produksjonsgrunnlag

Nye rasterbilder er laget med Codex sitt innebygde imagegen-verktøy. Ingen ekstern API/CLI er brukt. Originale genererte filer beholdes også under Codex generated_images. Python/Pillow/OpenCV brukes til mekanisk registrering, utsnitt, palettretting og sammensetting, ikke frihåndsmaling.

Promptgrunnlaget er Toms korrigeringer i BRIEF.md, riktig originalkontekst og de godkjente pilotarkene. Endelige motivspesifikasjoner:

- Plateau: samme fjell-/plantesilhuett, perspektiv og plassering som originalen, mer malte stein-/barkdetaljer, samme dempede fiolette/oransje lys. Måner holdes separate fra bakgrunnen.
- Utgravd åpning: samme plateau, ny åpning bare der originalens utgravde tilstand viser den. Lys, jord og stein møter det samme rombildet uten rektangulær lapp.
- Måner: to separate naturlige kraterdekte måner på alfa, større kjølig grå/fiolett og mindre kremgul, ingen plastkule, midtsøm eller bobler. Originale aktørrektangler og overlapping styrer importen.
- Laser: tynn rett hvit kjerne med svakt cyan lys, alfa, ingen metallstang, endestykker eller mekaniske deler. Originalens strålepiksler bestemmer retning og endepunkter.
- Edderkopp: åtte tydelig beslektede gangfaser som mørk blå/svart silhuett av stor alien-edderkopp, smal segmentert kropp og lange kantete ben, ingen museører, pels eller hale.
- Tett rist: rediger originalens åpne grotteutløp, behold hexramme, plassering og malte grottevegger. Rist tettet med brune blader, små kvister og sammenpresset organisk bøss. Fjern fallende vann i lukket tilstand. Ingen løse rør eller fotografisk metallhaug.
- Tram-gangflate: rediger obj890, med originalscene som støtte. Samme steingangflate mellom venstre kant og blå tramåpning, samme perspektiv/omriss, tydelig frontkant og smal mørk underside. Ingen ny metallrampe, rekkverk eller trapper. Original blå tram beholdes. Fargene registreres mot eksisterende scene.

Hoder bruker eksisterende atlas fra r16, avledet fra hovedark/boston.png, maggie.png og brink.png. Ingen av Toms avviste feilbilder brukes som nytt persondesign.

`register_r18_scenes.py` kjøres før `register_r18_moon_overlap.py` og `register_r18_particles.py`. Deretter bridge-skriptet. Neck-skriptet kjøres før Brink-farger og ekstra hoder; pole har eget skript. De endelige sjekksummene i OVERRIDES.json er fasit for akkurat denne leveransen.

Kjør clean_r18_head_components.py helt til slutt på ferdig registrerte hoder. Den fjerner bare små frakoblede alfaområder og beholder den største hodeflaten pixelidentisk. HEAD-CLEANUP-FILES.json lister alle895 endrede ruter fra siste opprydding.
