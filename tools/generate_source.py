"""Build the native Raktaros program around the tested Amoba LOS shell."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
source = (ROOT/'templates/AmobaM.TEXT').read_text()
levels = json.loads((ROOT.parent/'tests/levels.json').read_text())
source = source.replace('program Amoba;', 'program Raktaros;')
start = source.index('   ttLeft =')
end = source.index('   nextClkPoll :')
source = source[:start]+'''   sgWidth = 12;
   sgHeight = 9;
   sgCells = 108;
   sgLeft = 16;
   sgTop = 36;
   sgCellW = 24;
   sgCellH = 20;
   sgMaxUndo = 2048;
type BOVideoPtr = ^integer;
var
   sgBoard, sgShown : array[1..sgCells] of integer;
   sgGoal, sgBox : array[1..sgCells] of boolean;
   sgHistP : array[1..sgMaxUndo] of integer;
   sgHistB : array[1..sgMaxUndo] of boolean;
   sgPerson, sgLevel, sgSteps, sgPushes, sgHead, sgCount : integer;
   sgDone, sgReady, sgPainted : boolean;
''' + source[end:]
start = source.index('function TTWinner')
end = source.index('procedure doUpdateEvent', start)
body = '''function SGInside(cell : integer) : boolean;
begin
   SGInside := (cell >= 1) and (cell <= sgCells)
end;
procedure SGCheck;
var i : integer;
begin
   sgDone := true;
   for i := 1 to sgCells do
      if sgGoal[i] and (not sgBox[i]) then sgDone := false
end;
procedure SGLoad(level : integer);
var i : integer;
    map : Str255;
    ch : char;
begin
   if level < 1 then level := 20;
   if level > 20 then level := 1;
   sgLevel := level;
   case level of
'''
for number, level in enumerate(levels, 1):
    board = ''.join(level['rows'])
    assert len(board) == 108 and "'" not in board
    body += f"      {number}: map := '{board}';\n"
body += '''   end;
   for i := 1 to sgCells do begin
      ch := map[i];
      sgBoard[i] := 0;
      if ch = '#' then sgBoard[i] := 1;
      sgGoal[i] := (ch = '.') or (ch = '*') or (ch = '+');
      sgBox[i] := (ch = '$') or (ch = '*');
      if (ch = '@') or (ch = '+') then sgPerson := i
   end;
   sgSteps := 0; sgPushes := 0; sgHead := 0; sgCount := 0;
   sgPainted := false; sgReady := true;
   SGCheck
end;
procedure SGDraw;
var i, x, y, value : integer;
    box : Rect;
    text : Str255;
begin
   if myWindow = nil then exit(SGDraw);
   SetPort(myWindow);
   ClipRect(myWindow^.portRect);
   if not sgPainted then begin
      EraseRect(myWindow^.portRect);
      MoveTo(16, 18); DrawString('RAKTAROS (SOKOBAN)');
      MoveTo(324, 104); DrawString('W A S D: MOZGAS');
      MoveTo(324, 125); DrawString('Z: VISSZAVONAS');
      MoveTo(324, 146); DrawString('N: UJRAKEZDES');
      MoveTo(324, 167); DrawString('P: ELOZO PALYA');
      MoveTo(324, 188); DrawString('K: KOVETKEZO');
      MoveTo(16, 241); DrawString('TOLD A LADAKAT A PONTOKRA! HUZNI NEM LEHET.');
      MoveTo(324, 230); DrawString('20 SAJAT PALYA')
   end;
   PenSize(1, 1);
   for i := 1 to sgCells do begin
      value := sgBoard[i];
      if sgGoal[i] then value := value+2;
      if sgBox[i] then value := value+4;
      if i = sgPerson then value := value+8;
      if (not sgPainted) or (sgShown[i] <> value) then begin
         x := sgLeft+((i-1) mod sgWidth)*sgCellW;
         y := sgTop+((i-1) div sgWidth)*sgCellH;
         SetRect(box, x, y, x+sgCellW, y+sgCellH);
         EraseRect(box);
         if sgBoard[i] = 1 then begin
            SetRect(box, x+1, y+1, x+sgCellW-1, y+sgCellH-1);
            PaintRect(box);
            PenMode(patBic);
            MoveTo(x+2,y+10); LineTo(x+sgCellW-3,y+10);
            MoveTo(x+12,y+2); LineTo(x+12,y+9);
            MoveTo(x+7,y+11); LineTo(x+7,y+sgCellH-3);
            PenMode(patCopy)
         end
         else begin
            if sgGoal[i] then begin
               SetRect(box,x+9,y+7,x+15,y+13); PaintOval(box)
            end;
            if sgBox[i] then begin
               SetRect(box,x+3,y+3,x+21,y+17);
               EraseRect(box); FrameRect(box);
               MoveTo(x+4,y+4); LineTo(x+20,y+16);
               MoveTo(x+20,y+4); LineTo(x+4,y+16);
               if sgGoal[i] then begin
                  SetRect(box,x+6,y+6,x+18,y+14); FrameRect(box)
               end
            end;
            if i = sgPerson then begin
               SetRect(box,x+8,y+2,x+16,y+8); FrameOval(box);
               MoveTo(x+12,y+8); LineTo(x+12,y+14);
               MoveTo(x+6,y+10); LineTo(x+18,y+10);
               MoveTo(x+12,y+14); LineTo(x+7,y+18);
               MoveTo(x+12,y+14); LineTo(x+17,y+18)
            end
         end;
         sgShown[i] := value
      end
   end;
   SetRect(box,320,30,498,90); EraseRect(box);
   MoveTo(324,43); NumToStr(sgLevel,text);
   DrawString(concat('PALYA: ',text,' / 20'));
   MoveTo(324,62); NumToStr(sgSteps,text);
   DrawString(concat('LEPESEK: ',text));
   MoveTo(324,81); NumToStr(sgPushes,text);
   DrawString(concat('TOLASOK: ',text));
   SetRect(box,320,195,498,216); EraseRect(box);
   MoveTo(324,210);
   if sgDone then DrawString('KESZ! K: TOVABB');
   sgPainted := true
end;
procedure SGMove(delta : integer);
var target, beyond : integer;
    pushed : boolean;
begin
   if sgDone then exit(SGMove);
   target := sgPerson+delta;
   if not SGInside(target) then exit(SGMove);
   if sgBoard[target] = 1 then exit(SGMove);
   pushed := sgBox[target];
   if pushed then begin
      beyond := target+delta;
      if not SGInside(beyond) then exit(SGMove);
      if (sgBoard[beyond] = 1) or sgBox[beyond] then exit(SGMove)
   end;
   sgHead := (sgHead mod sgMaxUndo)+1;
   sgHistP[sgHead] := sgPerson;
   sgHistB[sgHead] := pushed;
   if sgCount < sgMaxUndo then sgCount := sgCount+1;
   if pushed then begin
      sgBox[target] := false; sgBox[beyond] := true;
      if sgPushes < 30000 then sgPushes := sgPushes+1
   end;
   sgPerson := target;
   if sgSteps < 30000 then sgSteps := sgSteps+1;
   SGCheck;
   SGDraw
end;
procedure SGUndo;
var oldpos, delta : integer;
begin
   if sgCount = 0 then exit(SGUndo);
   oldpos := sgHistP[sgHead];
   delta := sgPerson-oldpos;
   if sgHistB[sgHead] then begin
      sgBox[sgPerson+delta] := false;
      sgBox[sgPerson] := true;
      if sgPushes > 0 then sgPushes := sgPushes-1
   end;
   sgPerson := oldpos;
   sgHead := sgHead-1;
   if sgHead = 0 then sgHead := sgMaxUndo;
   sgCount := sgCount-1;
   if sgSteps > 0 then sgSteps := sgSteps-1;
   SGCheck;
   SGDraw
end;
procedure SGClick;
var pt : Point;
    row, col, cell : integer;
begin
   SetPort(myWindow); GetMouse(pt);
   if (pt.h < sgLeft) or (pt.h >= sgLeft+sgWidth*sgCellW) or
      (pt.v < sgTop) or (pt.v >= sgTop+sgHeight*sgCellH) then exit(SGClick);
   col := (pt.h-sgLeft) div sgCellW;
   row := (pt.v-sgTop) div sgCellH;
   cell := row*sgWidth+col+1;
   if cell = sgPerson-sgWidth then SGMove(-sgWidth)
   else if cell = sgPerson+sgWidth then SGMove(sgWidth)
   else if cell = sgPerson-1 then SGMove(-1)
   else if cell = sgPerson+1 then SGMove(1)
end;
'''
source = source[:start]+body+source[end:]
source = source.replace('ttPainted', 'sgPainted').replace('TTDraw', 'SGDraw').replace('TTClick', 'SGClick')
source = source.replace('if not ttReady then begin\nttComputer := true;\nTTNewGame\nend;',
                        'if not sgReady then SGLoad(1);')
start = source.index("'1'..'9': begin")
end = source.index('\nend;\nfolderActivate', start)
source = source[:start]+''' 'w', 'W': SGMove(-sgWidth);
 'a', 'A': SGMove(-1);
 's', 'S': SGMove(sgWidth);
 'd', 'D': SGMove(1);
 'z', 'Z': SGUndo;
 'n', 'N', ' ': begin SGLoad(sgLevel); SGDraw end;
 'p', 'P': begin SGLoad(sgLevel-1); SGDraw end;
 'k', 'K': begin SGLoad(sgLevel+1); SGDraw end
''' + source[end:]
source = source.replace('ttReady := false;', 'sgReady := false;')
start = source.index('if (myWindow <> nil) and ttComputer and')
end = source.index('if myWindow <> nil then BlockPresent;', start)
source = source[:start]+source[end:]
assert 'ttReady' not in source and 'TTNewGame' not in source and 'ttComputer' not in source
(ROOT.parent/'src/M.TEXT').write_bytes(source.replace('\n', '\r').encode('ascii'))
print('Wrote src/M.TEXT; supporting units are already in src/.')
