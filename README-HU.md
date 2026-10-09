# Raktaros (Sokoban) – Apple Lisa 2

**Natív játék valódi Apple Lisa 2 számítógéphez (Lisa 2/5 és Lisa 2/10),
Lisa Office System 3 alatt.** Ugyanez a kiadás LisaEm-ben is használható.

## Indítás valódi Lisa 2 gépen

1. Indítsd el a Lisa Office System 3 rendszert a Lisa 2 gépen.
2. A `Raktaros.dc42` lemezképet írd ki Lisa-formátumú, 400 KB-os, 3,5 hüvelykes
   floppyra megfelelő lemezképíró programmal és meghajtóval. A DC42-ben lévő
   natív Lisa szektorcímkéket is meg kell őrizni. Lisa-lemezképeket támogató
   floppyhelyettesítő is használható.
3. Helyezd be a lemezt, nyisd meg a lemez ablakát, jelöld ki a játék ikonját,
   és válaszd a File/Print → Open műveletet.
4. Merevlemezre telepítéshez használd a LOS Duplikálás műveletét, majd húzd a
   másolatot a Games mappába. A másolás végéig maradjon bent a floppy.

A DC42 fájl teljes lemezkép; lemezképként kell kiírni, a fájl egyszerű
floppyra másolása nem készít Lisa-játéklemezt. LisaEm-ben közvetlenül
behelyezhető a letöltött DC42.

Az eddigi kiadási tesztek LisaEm-ben történtek; fizikai Lisa 2 gépen végzett
próba még nincs dokumentálva. Részletek: [VALIDATION.md](VALIDATION.md).

Magyar, ablakban futó játék Lisa Office System 3 rendszerhez, húsz saját pályával.
A feladat az összes láda kijelölt pontra tolása. Egyszerre egy láda tolható;
húzni nem lehet. A feliratok a Lisa betűkészlete miatt ékezet nélküliek.

## Letöltés és indítás

A [Releases](https://github.com/julyus7/lisa-raktaros/releases) oldalon töltsd le
a **Raktaros.dc42** fájlt. Indítsd a LOS 3 rendszert a valódi Lisa 2 gépeden vagy LisaEm-ben,
helyezd be a lemezképet, majd nyisd meg a Raktaros ikont.
A LOS Duplikálás műveletével a merevlemez Games mappájába is átmásolható.
A másolás befejezéséig maradjon behelyezve a floppy.

- WASD: mozgás; közvetlenül szomszédos mezőre kattintva is léphetsz.
- Z: visszavonás, legfeljebb 2048 lépésnyi előzmény.
- N vagy szóköz: újrakezdés.
- P/K: előző/következő pálya.

Saját ikon és 242-es eszközazonosító biztosítja, hogy a korábbi játékok mellett
telepíthető legyen. Mind a húsz pálya natív tesztje sikeres volt.
A merevlemezre telepített példány floppy nélkül is elindult.

A fő forrás: `src/M.TEXT`. Újrafordítás: [BUILD.md](BUILD.md).
Részletes ellenőrzések: [VALIDATION.md](VALIDATION.md).
