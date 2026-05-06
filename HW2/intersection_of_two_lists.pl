% Base Case: intersection of empty list is empty list
intersect([], _, []).

% Case 1: member is in the list 
intersect([H|T], List2, [H|Res]) :-
    member(H, List2),
    intersect(T, List2, Res).

% Case 2: member is not in the list
intersect([H|T], List2, Res) :-
    \+ member(H, List2),
    intersect(T, List2, Res).