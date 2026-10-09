# Recorded validation of Raktaros 1.0.0

These are the completed release checks, not a claim that GitHub runs a Lisa emulator.

| Check | Recorded result |
| --- | --- |
| Native compilation and link | Executable B.OBJ; zero linker errors |
| Host rules and inverse undo | 20 levels, 5747 constructive solution moves |
| Native LOS 3.1 replay | 20 levels solved, 1176 moves, 60 state comparisons |
| Native input | WASD, uppercase, mouse, restart, undo, win freeze and level wrapping |
| Rendering samples | 16 frames during 20 A/D inputs; static board cells unchanged |
| Native LOS Duplicate / hard-disk installation | 67 executable/icon/phrase files matched |
| Existing tools | All 17 prior tools, including 7 games, preserved |
| Fresh emulator launch with no floppy | Installed game starts; movement and undo pass |
| Release image | DC42 checksums valid, 800 Sony tags preserved, own ID/icon/UID |

Native input was sent through the emulated COPS hardware queue. State comparisons
only read guest RAM; they did not write game state. The rendering test sampled
frames rather than recording continuous video. The Linux LisaEm display sometimes
retained an old desktop frame after closing the game; installation screenshots
were refreshed using a host repaint request, without changing guest RAM.

The JSON reports and host log in `validation/` retain the detailed results.
`screenshots/` contains native gameplay, installation and compiler evidence.
The installed copy was tested on a separate ProFile disk containing Minesweeper,
BlockOut, Amoba, Tetris, Puzzle, Reversi and LisaFileMover. Lisa was shut down
normally before rereading the final test disk and repeating the file comparison.

The release floppy has 419284 bytes, with a 11264-byte executable:
`a3b40497a84ec622d6d76833304033aa0edadea9c375fd3afce6a29a3b979f2d` (SHA-256).
Image SHA-256 is in `dist/SHA256SUMS`.

Raw RAM dumps, developer disk images, ROMs, credentials and SDK files are not
part of this repository. The reports refer to the local development setup;
their historical emulator PID and guest paths are not needed to run the game.
