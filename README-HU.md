# Raktaros (Sokoban) – Apple Lisa

Magyar, ablakban futó játék Lisa Office System 3 rendszerhez, húsz saját pályával.
A feladat az összes láda kijelölt pontra tolása. Egyszerre egy láda tolható;
húzni nem lehet. A feliratok a Lisa betűkészlete miatt ékezet nélküliek.

## Letöltés és indítás

A [Releases](https://github.com/julyus7/lisa-raktaros/releases) oldalon töltsd le
a **Raktaros.dc42** fájlt. Indítsd a saját LOS 3 rendszeredet LisaEm-ben,
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
