# fig014_01: Boston Low, pilotark 1

Levert av Codex 2026-10-09 09:01 CEST.

Status: Kandidat til Toms visuelle godkjenning. Lokal teknisk kontroll bestod, og 28 ruter er integrert i en lokal testpakke på Toms forespørsel 2026-10-09. Ark 2 til 4 avventer godkjenning av dette arket, som angitt i ORDRE.md.

## Bildearbeid

- Verktøy: innebygd ChatGPT-bildeverktøy, image_gen. Verktøyet oppga ikke et bestemt modellnavn.
- Redigeringsgrunnlag: referanse.png. Stilanker som bilde to: stil/room009_core.png.
- Prompt: prompt.txt ordrett, inkludert avsluttende linjeskift. Ingen korrigeringsprompt eller tillegg ble brukt.
- Format: PNG, 1536 x 1024. To genereringer med samme prompt og de samme to inngangsbildene.
- Første forsøk er levert som resultat.png. Andre forsøk ble forkastet fordi costume014_029 fikk omrissoverlapp 0,798, under grensen 0,80.
- Alle 28 ruter er bevart: 8 kropper uten hode, 8 separate hoder og 12 gangbilder mot høyre. De magenta skyggemarkørene er bevart.

## Kontroll

Prosjektets eksisterende gpt-inn ble kjørt på en separat kopi av bare denne jobben, med originalrutene fra work/extract. Repoets status.csv, RAPPORT.md og retur.md er overlatt til Claude.

| Måling, valgt forsøk | Resultat |
| --- | --- |
| Lokal teknisk status | godkjent, 28 av 28 figurruter klippet ut |
| Forskyvning, originalpiksler | x 0,11, y 0,04 |
| Største lokale forskyvning | 0,77 originalpiksler |
| Kantlikhet for hele arket | 0,989 |
| Laveste omrissoverlapp per rute | 0,869, grense 0,80 |
| Laveste kantlikhet per rute | 0,875, grense 0,50 |
| Laveste dekning per rute | 0,969 |
| Flimmerkontroll | 11 nabopar, høyeste ekstra forskjell 27,3, grense 30 |

Første forsøk har svak fargevariasjon i den turkise bakgrunnen og den grå kanten. Det er dokumentert selv om den tekniske kontrollen består. Mottaket bruker originalens gjennomsiktighet og fargelås ved utklipping. Toms vurdering av ansikt, klesdetaljer og malestil gjenstår. Etterfølgende test 2026-10-09 viser pilotgrafikken i nettlesermotoren, med originalens skyggemaske. Full spillbarhet og gange ved klikk er ikke bekreftet. Se rapporten under.

## Sporing

- SHA256 resultat.png: 0dd996cb1dfb38e02842309e05bb3aece59d7ce14beae75de93818107a2e05c5
- SHA256 referanse.png: 753f0a7eab5205d03272c00f5e731447e54c60949df5a8e658b02ea8c5295b87
- SHA256 original_1x.png: 5b8caaa3817cc73829d1a5dfab8dc671151f4017c4e7a653b045e10a6d79f5f6
- SHA256 prompt.txt, faktiske filbytes: ff980fb6ff417b2e706b5ccf20828db7ffa80b2cac4b7b5f40425eeb35e43062
- SHA256 jobb.json: 04ed3d897aeb2c9cf1d6bc52ab1be1a99d2268368be5cf5150dfc3902f99fd75
- SHA256 stil/room009_core.png: fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4
- SHA256 forkastet forsøk 2: 3ada265bfd26fd061265c69a0746b4a4964896eafb2ec0abc227fd0e58e3a205

Inngangsfilene er kontrollert uendret før og etter bildearbeidet. Leveransen inneholder bare resultat.png og dette notatet.

## Integrasjon for utprøving

Tom ba om integrasjon før godkjenning. De 28 rutene er lagt til i en kopi av den eksisterende HD-pakken og lest inn i Codex-nettleseren. Kildearket er uendret. Se [spilltestrapporten](../../rapporter/fig014_01-spilltest/SPILLTEST.md) med faktiske spillbilder, kontrollresultater og testbegrensninger. Visuell godkjenning av ark 1 gjenstår.
