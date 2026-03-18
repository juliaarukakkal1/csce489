:- use_module(library(clpfd)).

% 1. Winning Lines (Rows, Cols, Diagonals)
line(1, 2, 3). line(4, 5, 6). line(7, 8, 9). % Rows
line(1, 4, 7). line(2, 5, 8). line(3, 6, 9). % Cols
line(1, 5, 9). line(3, 5, 7).                % Diagonals

% 2. Check for Win
win(Board, Player) :-
    line(A, B, C),
    nth1(A, Board, Player),
    nth1(B, Board, Player),
    nth1(C, Board, Player).

% 3. Move Logic
move(Board, Index, Player, NewBoard) :-
    nth1(Index, Board, b),
    replace(Board, Index, Player, NewBoard).

replace([_|T], 1, X, [X|T]).
replace([H|T], I, X, [H|R]) :- I > 1, NI is I - 1, replace(T, NI, X, R).


% 4. Alpha-Beta Pruning Logic

% Defining Scoring
alphabeta(Board, _, _, _, 1) :- win(Board, o), !.
alphabeta(Board, _, _, _, -1) :- win(Board, x), !.
alphabeta(Board, _, _, _, 0) :- \+ member(b, Board), !.

% Maximizing (AI - 'o')
alphabeta(Board, o, Alpha, Beta, Score) :-
    findall(NextB, move(Board, _, o, NextB), Neighbors),
    bounded_max(Neighbors, Alpha, Beta, -2, Score).

% Minimizing (Human - 'x')
alphabeta(Board, x, Alpha, Beta, Score) :-
    findall(NextB, move(Board, _, x, NextB), Neighbors),
    bounded_min(Neighbors, Alpha, Beta, 2, Score).

% Pruning Helpers
bounded_max([B|Bs], Alpha, Beta, CurrentMax, Score) :-
    alphabeta(B, x, Alpha, Beta, S),
    NewMax is max(CurrentMax, S),
    NewAlpha is max(Alpha, NewMax),
    ( NewAlpha >= Beta -> Score = NewMax ; bounded_max(Bs, NewAlpha, Beta, NewMax, Score) ).
bounded_max([], _, _, Score, Score).

bounded_min([B|Bs], Alpha, Beta, CurrentMin, Score) :-
    alphabeta(B, o, Alpha, Beta, S),
    NewMin is min(CurrentMin, S),
    NewBeta is min(Beta, NewMin),
    ( Alpha >= NewBeta -> Score = NewMin ; bounded_min(Bs, Alpha, NewBeta, NewMin, Score) ).
bounded_min([], _, _, Score, Score).

% 5. Best Move Selection
best_move(Board, BestMove) :-
    findall(Score-M, (move(Board, M, o, NextB), alphabeta(NextB, x, -2, 2, Score)), Pairs),
    keysort(Pairs, Sorted),
    last(Sorted, _-BestMove).

% 6. Game Loop & UI
play :- 
    Board = [b,b,b, b,b,b, b,b,b],
    display_board(Board),
    game_loop(Board, x).

game_loop(Board, _) :- win(Board, o), write('AI wins! Try harder next time.'), !.
game_loop(Board, _) :- win(Board, x), write('You won? This should be impossible!'), !.
game_loop(Board, _) :- \+ member(b, Board), write('It is a draw.'), !.

game_loop(Board, x) :-
    write('Your move (1-9): '), read(Move),
    (move(Board, Move, x, NewBoard) -> display_board(NewBoard), game_loop(NewBoard, o) ;
    write('Invalid move!'), nl, game_loop(Board, x)).

game_loop(Board, o) :-
    write("AI's Move"), nl,
    best_move(Board, Move),
    move(Board, Move, o, NewBoard),
    display_board(NewBoard),
    game_loop(NewBoard, x).

display_board([A,B,C,D,E,F,G,H,I]) :-
    format('~w|~w|~w~n-+-+-~n~w|~w|~w~n-+-+-~n~w|~w|~w~n~n', [A,B,C,D,E,F,G,H,I]).