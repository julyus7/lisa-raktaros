"""Create 20 original Sokoban levels by reversible pulls, with replayable solutions."""
from pathlib import Path
import json
import random

W, H = 12, 9
DIRS = {'w': -W, 'a': -1, 's': W, 'd': 1}
REV = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
ROOT = Path(__file__).resolve().parent


def reachable(floor, start):
    seen = {start}
    todo = [start]
    while todo:
        p = todo.pop()
        for d in DIRS.values():
            q = p+d
            if q in floor and q not in seen:
                seen.add(q)
                todo.append(q)
    return seen


def make(seed, count, rounds):
    rng = random.Random(seed)
    floor = {y*W+x for y in range(1, H-1) for x in range(1, W-1)}
    # Original sparse interior walls; keep the entire walkable region connected.
    for p in rng.sample(sorted(floor), 10):
        trial = floor-{p}
        if len(reachable(trial, min(trial))) == len(trial):
            floor = trial
    available = [p for p in sorted(floor)
                 if sum(p+d in floor for d in DIRS.values()) >= 3]
    goals = set(rng.sample(available, count))
    boxes = set(goals)
    player = rng.choice(sorted(floor-boxes))
    route = []
    pulls = 0
    for _ in range(rounds):
        options = []
        for key, d in DIRS.items():
            if player+d in floor-boxes:
                options.append((key, d, player-d in boxes))
        pulling = [o for o in options if o[2]]
        choices = pulling if pulling and rng.random() < .80 else options
        if not choices:
            break
        key, d, pull = rng.choice(choices)
        if pull:
            boxes.remove(player-d)
            boxes.add(player)
            pulls += 1
        player += d
        route.append(key)
    if len(boxes-goals) < 2 or pulls < 10:
        return None
    board = ['#']*(W*H)
    for p in floor:
        board[p] = '.' if p in goals else ' '
    for p in boxes:
        board[p] = '*' if p in goals else '$'
    board[player] = '+' if player in goals else '@'
    solution = ''.join(REV[k] for k in reversed(route))
    return {'seed': seed, 'width': W, 'height': H,
            'rows': [''.join(board[y*W:(y+1)*W]) for y in range(H)],
            'solution': solution, 'solution_pushes': pulls, 'boxes': count}


def main():
    levels = []
    seed = 242001
    while len(levels) < 20:
        n = len(levels)
        level = make(seed, 3+n//7, 180+n*15)
        seed += 1
        if level:
            levels.append(level)
    (ROOT/'levels.json').write_text(json.dumps(levels, indent=2)+'\n', encoding='utf-8')
    print('Created 20 original levels with constructive solutions.')


if __name__ == '__main__':
    main()
