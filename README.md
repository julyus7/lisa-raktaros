# Raktaros (Sokoban) for Apple Lisa

Hungarian Sokoban for Apple Lisa Office System 3, running in a window.
Push every crate onto a marked goal. You can push one crate at a time;
you cannot pull crates. Includes **20 original, solvable levels**.
Hungarian captions use unaccented characters for the Lisa font.

![Native LOS gameplay](screenshots/gameplay.png)

## Download and run

Download **[Raktaros.dc42](https://github.com/julyus7/lisa-raktaros/releases/latest/download/Raktaros.dc42)**
from Releases, or [dist/Raktaros.dc42](dist/Raktaros.dc42) using Download raw.
The image is a tagged 400 KB Lisa floppy in Disk Copy 4.2 format:
**419,284 bytes**. It is an application floppy; boot your own LOS installation first.

1. Boot Lisa Office System 3 in LisaEm.
2. Insert `Raktaros.dc42` as the floppy.
3. Open the disk and its Raktaros tool icon.
4. To install on the hard disk, select LOS **Duplicate** and drag the duplicate
   into your Games folder. Allow the running tool to close if LOS requests it.
   Keep the floppy inserted until copying completes.

The game has its own icon, **tool ID 242**, and volume identity ending D603.
It can coexist with Minesweeper, BlockOut, Amoba and other existing tools.
LOS allows only one copy of a given tool on a disk; replace an earlier version
of Raktaros when updating it.

## Controls

| Key | Action |
| --- | --- |
| W / A / S / D | Up / left / down / right |
| Click an adjacent cell | Move or push |
| Z | Undo; up to 2048 moves |
| N / Space | Restart the current level |
| P / K | Previous / next level; wraps between 1 and 20 |

A crate on a goal has a double frame. Movement stops when every goal is filled;
Z can undo the winning push, or K advances to the next level.

## Source and validation

- [src/M.TEXT](src/M.TEXT): released Lisa Pascal game and embedded levels.
- `src/G.TEXT`, `J.TEXT`, `D.TEXT`, `I.TEXT`: supporting LOS units.
- [BUILD.md](BUILD.md): native compiler and rebuild instructions.
- [VALIDATION.md](VALIDATION.md): native gameplay, rendering and installation checks.
- [README-HU.md](README-HU.md): magyar leiras es kezeles.
- [CREDITS.md](CREDITS.md): inherited LOS framework and source provenance.

All 20 levels passed native replay under LOS 3.1: 1176 solution moves and
60 state comparisons. Installation alongside seven existing games passed,
as did a fresh hard-disk launch with no floppy inserted.

SHA-256: `10b911d0cdabcb707fbc920edf1103cc4d0cc09a7977ca936483321113b9f165`.
