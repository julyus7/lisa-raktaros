"""Replay all generated solutions and validate undo and rejected moves."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
LEVELS = json.loads((ROOT/'levels.json').read_text())
DIRS = {'w': -12, 'a': -1, 's': 12, 'd': 1}


def unpack(level):
    board = ''.join(level['rows'])
    floor = {p for p, c in enumerate(board) if c != '#'}
    goals = {p for p, c in enumerate(board) if c in '.*+'}
    boxes = {p for p, c in enumerate(board) if c in '$*'}
    player = next(p for p, c in enumerate(board) if c in '@+')
    return floor, goals, boxes, player


def step(floor, boxes, player, key):
    d = DIRS[key]
    q = player+d
    if q not in floor or (q in boxes and q+d not in floor-boxes):
        return boxes, player, False
    new = set(boxes)
    pushed = q in new
    if pushed:
        new.remove(q)
        new.add(q+d)
    return new, q, pushed


def main():
    assert len(LEVELS) == 20
    source = (ROOT.parent/'src/M.TEXT').read_text()
    maps = re.findall(r"\d+: map := '([^']*)';", source)
    assert maps == [''.join(level['rows']) for level in LEVELS]
    # Minimal fixtures independent of the generated levels.
    assert step({1,2,3}, {2}, 1, 'a') == ({2}, 1, False)
    assert step({1,2,3}, {2,3}, 1, 'd') == ({2,3}, 1, False)
    assert step({1,2}, {2}, 1, 'd') == ({2}, 1, False)
    assert step({1,2,3}, {2}, 1, 'd') == ({3}, 2, True)
    total = 0
    for number, level in enumerate(LEVELS, 1):
        assert len(level['rows']) == 9 and all(len(r) == 12 for r in level['rows'])
        floor, goals, boxes, player = unpack(level)
        assert len(boxes) == len(goals) == level['boxes']
        assert boxes != goals and player not in boxes
        start = (set(boxes), player)
        undo = []
        inverse = []
        pushes = 0
        for key in level['solution']:
            old = (set(boxes), player)
            boxes, new_player, pushed = step(floor, boxes, player, key)
            assert new_player != player
            undo.append(old)
            inverse.append((player, pushed))
            player = new_player
            pushes += pushed
            assert boxes <= floor and len(boxes) == len(goals) and player not in boxes
        assert boxes == goals and pushes == level['solution_pushes']
        while undo:
            old_player, pushed = inverse.pop()
            delta = player-old_player
            if pushed:
                boxes.remove(player+delta)
                boxes.add(player)
                pushes -= 1
            player = old_player
            assert (boxes,player) == undo.pop(), 'Native inverse undo differs from full snapshot'
        assert (boxes, player) == start
        assert pushes == 0
        for key in DIRS:
            new, p, _ = step(floor, boxes, player, key)
            if p == player:
                assert new == boxes
        total += len(level['solution'])
        print(f'PASS level {number:02}: {len(level["solution"])} moves, {level["solution_pushes"]} pushes; inverse undo restored start')
    print('PASS:', total, 'constructive solution moves; 20 levels are solvable.')


if __name__ == '__main__':
    main()
