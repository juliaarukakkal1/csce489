% Facts
% Calorie Data
calories(water, 0).
calories(hamburger, 354).
calories(carrot, 25).
calories(salad, 100).
calories(banana, 105).
calories(apple, 95).
calories(peanuts, 828).
calories(chicken_soup, 87).
calories(lasagna, 166).
calories(apple_pie, 67).
calories(beans, 41).
calories(peas, 118).
calories(milk, 8).
calories(orange_juice, 39).
calories(coke, 140).
calories(cookie, 132).
calories(naan, 78).
calories(potato_soup, 149).

% Food Categories
meat(hamburger).
meat(lasagna).

legume(peas).
legume(beans).
legume(peanuts).

vegetable(carrot).
vegetable(salad).

fruit(apple).
fruit(banana).
fruit(orange_juice).
fruit(apple_pie).

drink(water).
drink(coke).
drink(milk).
drink(orange_juice).

% Rules
fruit_or_vegetable(X) :- fruit(X) ; vegetable(X).
protein(X) :- meat(X) ; legume(X) ; X = milk.

% Check if meal contains at least one Fruit/Veg
contains_fruit_or_vegetable(M) :-
    member(X, M),
    fruit_or_vegetable(X).

% Check if meal contains at least one Protein
contains_protein(M) :-
    member(X, M),
    protein(X).

% Nutritious: Fruit/Veg AND Protein
nutritious(M) :-
    contains_fruit_or_vegetable(M),
    contains_protein(M).

% Vegetarian: Does NOT contain meat
vegetarian_meal(M) :-
    \+ (member(X, M), meat(X)).

% total(+Meal, -Cals): Recursive calorie counter
total([], 0).
total([H|T], Cals) :-
    calories(H, C),
    total(T, Rest),
    Cals is C + Rest.

% Good Meal: Nutritious and Calories between 400 and 600
good_meal(M) :-
    nutritious(M),
    total(M, Cals),
    Cals >= 400,
    Cals =< 600.