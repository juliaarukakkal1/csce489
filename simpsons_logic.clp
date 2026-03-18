;; ==========================================
;; 1. Logic & Inference Rules
;; ==========================================

;; Rule: Identify a Father
(defrule find-father
   (parentOf ?c ?p)
   (male ?p)
   =>
   (assert (father ?p ?c))
   (printout t ?p " is the father of " ?c "." crlf))

;; Rule: Identify a Mother
(defrule find-mother
   (parentOf ?c ?p)
   (female ?p)
   =>
   (assert (mother ?p ?c))
   (printout t ?p " is the mother of " ?c "." crlf))

;; Rule: Identify Siblings
(defrule find-siblings
   (parentOf ?c1 ?p)
   (parentOf ?c2 ?p)
   (test (neq ?c1 ?c2))
   =>
   (assert (sibling ?c1 ?c2))
   ;; Using 'duplicate' check or checking facts to prevent double printing is common, 
   ;; but this is the basic logic.
   (printout t ?c1 " and " ?c2 " are siblings." crlf))

;; Rule: Identify Grandparents
(defrule find-grandparent
   (parentOf ?c ?p)
   (parentOf ?p ?gp)
   =>
   (assert (grandparent ?gp ?c))
   (printout t ?gp " is the grandparent of " ?c "." crlf))

;; Rule: Identify Aunts and Uncles
(defrule find-aunt-uncle
   (parentOf ?c ?p)
   (sibling ?p ?au)
   =>
   (assert (aunt-uncle ?au ?c))
   (printout t ?au " is the aunt/uncle of " ?c "." crlf))