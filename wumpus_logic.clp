;; --- 1. Perception Rules ---

;; Rule: Infer Stench
;; If there is a Wumpus, mark the four cardinal rooms as Stenchy.
(defrule infer-stench
   (declare (salience 10))
   (wumpus ?wx ?wy)
   =>
   (assert (stench ?wx (+ ?wy 1)))
   (assert (stench ?wx (- ?wy 1)))
   (assert (stench (+ ?wx 1) ?wy))
   (assert (stench (- ?wx 1) ?wy)))

;; Rule: Infer Breeze
;; If there is a Pit, mark the four cardinal rooms as Breezy.
(defrule infer-breeze
   (pit ?px ?py)
   =>
   (assert (breeze ?px (+ ?py 1)))
   (assert (breeze ?px (- ?py 1)))
   (assert (breeze (+ ?px 1) ?py))
   (assert (breeze (- ?px 1) ?py)))

;; --- 2. Reachability (Pathfinding) ---

;; Rule: Initialize Path
;; Marks the starting coordinates as the first reachable room.
(defrule init-path
   (start ?x ?y)
   =>
   (assert (reachable ?x ?y))
   (printout t "Starting exploration at (" ?x "," ?y ")" crlf))

;; Rule: Move Safely
;; This is the core engine. It looks for adjacent rooms and checks safety.
(defrule move-safely
   ;; 1. Take a room we can already reach
   (reachable ?x ?y)
   
   ;; 2. Pick any valid coordinates from our 'number' facts (fixes the Analysis error)
   (number ?nx)
   (number ?ny)
   
   ;; 3. Test if the new room (nx, ny) is exactly 1 step away from (x, y)
   (test (= 1 (+ (abs (- ?nx ?x)) (abs (- ?ny ?y)))))

   ;; 4. Safety Constraints
   (not (pit ?nx ?ny))      ;; No Pits allowed
   (not (wumpus ?nx ?ny))   ;; No Wumpus allowed
   (not (stench ?nx ?ny))   ;; No Stench allowed (per your requirement)
   (not (reachable ?nx ?ny)) ;; Don't walk in circles
   =>
   ;; 5. Mark this new room as reachable and keep moving
   (assert (reachable ?nx ?ny))
   (printout t "Moving to safe room: (" ?nx "," ?ny ")" crlf))

;; --- 3. Victory Condition ---

;; Rule: Victory
;; If the exit (goal) is marked as reachable, we win!
(defrule victory
   (goal ?gx ?gy)
   (reachable ?gx ?gy)
   =>
   (printout t "SUCCESS: Path to Exit (" ?gx "," ?gy ") found!" crlf)
   (halt))

(defrule game-over-trapped
   (declare (salience -100)) ;; Fires ONLY when no other rules can run
   (goal ?gx ?gy)
   (not (reachable ?gx ?gy)) ;; We haven't reached the goal
   =>
   (printout t "!!! MISSION FAILED !!!" crlf)
   (printout t "The agent is trapped! No safe path exists to (" ?gx "," ?gy ")." crlf)
   (halt))