% initial guess equal to the Target 
sqrt(Target, FinalAnswer) :-
    Target > 0,
    Tolerance = 0.0001,
    CurrentEst = Target, 
    sqrt_helper(Target, CurrentEst, Tolerance, FinalAnswer).

% Base Case: If the square of the current estimate is close to Target.
sqrt_helper(Target, CurrentEst, Tolerance, CurrentEst) :-
    Diff is abs(Target - (CurrentEst * CurrentEst)),
    Diff =< Tolerance.

% Recursive Step: If not close enough, find better estimate
sqrt_helper(Target, CurrentEst, Tolerance, FinalAnswer) :-
    Diff is abs(Target - (CurrentEst * CurrentEst)),
    Diff > Tolerance,
    % Newton-Raphson Formula: next = (curr + target/curr) / 2
    NextEst is (CurrentEst + (Target / CurrentEst)) / 2,
    sqrt_helper(Target, NextEst, Tolerance, FinalAnswer).