# Building the native Lisa program

The release was compiled by **Lisa Pascal V3.26 (10-Jul-84)** in Workshop 3,
using its **MC68000 Code Generator V3.16 (12-Jul-84)**, and linked with
**M68000 Object Code Linker 3.0 (June 1, 1984)**.
Python prepares sources and images; Pascal compilation runs on the Lisa.

## Requirements

- Real Apple Lisa 2 (2/5 or 2/10), or LisaEm with your own ROM, Workshop 3 and LOS 3 environment.
- Workshop LOS interface objects and runtime libraries required by the `uses`
  clauses, including `IOSPASLIB.OBJ`, `SYS1LIB.OBJ` and `PRLIB.OBJ`.
- Python 3.10+ for the included tools (standard library only).

ROMs, operating systems, SDK libraries and prepared developer disks are not
included. Use a separate copy of your development disk.

## Transfer and compile

Transfer the five Pascal files `G`, `J`, `D`, `I`, `M` in `src/` as Lisa TEXT
files. They retain classic CR line endings. The serial transfer utility and
Workshop receiver in [LOS Minesweeper](https://github.com/alexthecat123/los_minesweeper)
are one way to import them. Set your Workshop working prefix to the source folder
and make the LOS interface objects available.

Compile G, J, D, I, then M. For each, press `P`, enter its source name,
accept the default listing and `.OBJ` output. For the released build, the four
supporting objects already existed in the verified development environment;
M was freshly compiled. The automatic code generator reported 8152 machine-code bytes.

Delete any stale B.OBJ, press `L`, then enter these inputs one per prompt:

```text
M.OBJ
G.OBJ
J.OBJ
D.OBJ
I.OBJ
IOSPASLIB.OBJ
SYS1LIB.OBJ
PRLIB.OBJ
```

End with Return, accept the default listing and enter B.OBJ as output.
Require zero errors and an executable program file. The released B.OBJ is
11264 bytes. `src/C.TEXT` and `src/L.TEXT` contain equivalent Workshop EXEC
answers; EXEC invocation uses `R`, then `<C` or `<L`.

## Package the compiled executable

Shut down LisaEm cleanly before reading the Workshop disk. The included tool
uses the released Raktaros floppy as a filesystem template and replaces its
executable while preserving tool ID 242, phrase resources, icons and Sony tags:

```sh
python tools/package.py /path/to/closed-workshop.dc42 Raktaros-new.dc42
python tools/inspect_image.py Raktaros-new.dc42
```

The replacement must fit the template's existing allocation. This packager
does not allocate a larger file or change phrase resources.

## Optional source generation and host checks

```sh
python tools/generate_source.py
python tests/test_rules.py
python tests/shorten_solutions.py
```

The generator uses the included Amoba shell template and `tests/levels.json`.
`tests/generate_levels.py` recreates the original deterministic level set.
The checked-in src/M.TEXT is the exact source used for the release.

The local release build ran LisaEm in an Alpine Linux VM under Windows QEMU
8.2.90. This environment is not required: compatible Lisa hardware or a separate
LisaEm Workshop installation can compile the source.
