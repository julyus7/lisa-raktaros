"""Remove repeated-state loops for efficient native replay, without changing maps."""
from pathlib import Path
import json
from test_rules import LEVELS, unpack, step

result = []
for number, level in enumerate(LEVELS, 1):
    floor, goals, boxes, player = unpack(level)
    state = (tuple(sorted(boxes)), player)
    states = [state]
    indices = {state: 0}
    moves = []
    for key in level['solution']:
        boxes, player, _ = step(floor, boxes, player, key)
        state = (tuple(sorted(boxes)), player)
        if state in indices:
            index = indices[state]
            states = states[:index+1]
            moves = moves[:index]
            indices = {s:i for i,s in enumerate(states)}
        else:
            moves.append(key)
            states.append(state)
            indices[state] = len(states)-1
        if boxes == goals:
            break
    solution = ''.join(moves)
    floor, goals, boxes, player = unpack(level)
    pushes = 0
    for key in solution:
        boxes, player, pushed = step(floor, boxes, player, key)
        pushes += pushed
    assert boxes == goals
    result.append({'level':number, 'moves':solution, 'pushes':pushes})
    print(number, 'replay moves',len(solution),'pushes',pushes)
Path(__file__).with_name('solutions-short.json').write_text(json.dumps(result,indent=2)+'\n')
