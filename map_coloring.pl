:- use_module(library(clpfd)).

% Mainland Australia Map Coloring
mainland_australia(Vars) :-
    % 1. Variables for the 6 mainland states
    Vars = [WA, NT, SA, QLD, NSW, VIC],
    
    % 2. 1=Red, 2=Green, 3=Blue
    Vars ins 1..3,

    % 3. The Borders
    % Western Australia borders
    WA #\= NT,
    WA #\= SA,

    % Northern Territory borders
    NT #\= SA,
    NT #\= QLD,

    % South Australia borders
    SA #\= QLD,
    SA #\= NSW,
    SA #\= VIC,

    % Queensland borders
    QLD #\= NSW,

    % New South Wales borders
    NSW #\= VIC,

    label(Vars).