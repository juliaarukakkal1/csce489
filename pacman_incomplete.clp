;; --- 1. Scoring and State ---

(defrule init-score
   (not (score ?))
   =>
   (assert (score 0)))

;; --- 2. Pac-Man's Turn ---

;; Priority 1: Eat a Pellet if it's right next to us
(defrule pacman-moves-to-eat
   (declare (salience 10))
   ?t <- (turn pacman)
   ?p <- (pacman ?x ?y)
   (number ?nx) (number ?ny)
   (pellet ?nx ?ny) ;; Target is a pellet
   (test (= 1 (+ (abs (- ?nx ?x)) (abs (- ?ny ?y))))) ;; Cardinal move
   (not (wall ?nx ?ny))
   =>
   (retract ?p ?t)
   (assert (pacman ?nx ?ny))
   (assert (turn ghost)) ;; Pass turn
   (printout t "Pac-Man moves to (" ?nx "," ?ny ") to eat!" crlf))

;; Priority 2: Wander safely if no pellet is adjacent
(defrule pacman-wanders
   (declare (salience 5))
   ?t <- (turn pacman)
   ?p <- (pacman ?x ?y)
   (number ?nx) (number ?ny)
   (test (= 1 (+ (abs (- ?nx ?x)) (abs (- ?ny ?y)))))
   (not (wall ?nx ?ny))
   (not (ghost ?nx ?ny)) ;; Avoid moving directly into a ghost
   =>
   (retract ?p ?t)
   (assert (pacman ?nx ?ny))
   (assert (turn ghost))
   (printout t "Pac-Man wanders to (" ?nx "," ?ny ")." crlf))

;; --- 3. Ghost's Turn ---

;; The Ghost calculates which neighbor is mathematically closer to Pac-Man
(defrule ghost-hunts
   ?t <- (turn ghost)
   ?g <- (ghost ?gx ?gy)
   (pacman ?px ?py)
   (number ?nx) (number ?ny)
   
   ;; Pick a neighbor
   (test (= 1 (+ (abs (- ?nx ?gx)) (abs (- ?ny ?gy)))))
   (not (wall ?nx ?ny))
   
   ;; Heuristic: Is the new distance smaller than the current distance?
   (test (< (+ (abs (- ?nx ?px)) (abs (- ?ny ?py))) 
            (+ (abs (- ?gx ?px)) (abs (- ?gy ?py)))))
   =>
   (retract ?g ?t)
   (assert (ghost ?nx ?ny))
   (assert (turn pacman)) ;; Pass turn back
   (printout t "Ghost stalks toward (" ?nx "," ?ny ")..." crlf))

;; --- 4. Game Rules (Automatic) ---

;; Rule: Eat the Pellet
(defrule consume-pellet
   (pacman ?x ?y)
   ?pellet <- (pellet ?x ?y)
   ?s <- (score ?old)
   =>
   (retract ?pellet ?s)
   (assert (score (+ ?old 10)))
   (printout t "NOM NOM! Score: " (+ ?old 10) crlf))

;; Rule: Death Condition
(defrule game-over-loss
   (declare (salience 100))
   (pacman ?x ?y)
   (ghost ?x ?y)
   =>
   (printout t "GAME OVER: Caught by the ghost at (" ?x "," ?y ")!" crlf)
   (halt))

;; Rule: Victory Condition
(defrule game-over-win
   (not (pellet ? ?)) ;; No pellets left on the board
   =>
   (printout t "VICTORY: All pellets cleared!" crlf)
   (halt))