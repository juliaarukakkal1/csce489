from flask import Flask, request, jsonify
import clips

app = Flask(__name__)
env = clips.Environment()

# ==========================================================
# 1. CLIPS KNOWLEDGE BASE
# ==========================================================

# Templates flattened to single lines for maximum parser stability
env.build("(deftemplate position (slot type) (slot x (type INTEGER)) (slot y (type INTEGER)))")
env.build("(deftemplate move-score (slot direction (type STRING)) (slot distance (type INTEGER)))")
env.build("(deftemplate move (slot direction (type STRING)))")
env.build("(deftemplate legal-action (slot direction (type STRING)))")

# Rule: Calculate Manhattan Distance for each legal move
env.build("""
(defrule evaluate-safety
   (position (type pacman) (x ?px) (y ?py))
   (position (type ghost) (x ?gx) (y ?gy))
   (legal-action (direction ?dir))
   =>
   (bind ?nx ?px) (bind ?ny ?py)
   (if (eq ?dir "North") then (bind ?ny (+ ?py 1)))
   (if (eq ?dir "South") then (bind ?ny (- ?py 1)))
   (if (eq ?dir "East")  then (bind ?nx (+ ?px 1)))
   (if (eq ?dir "West")  then (bind ?nx (- ?px 1)))
   (bind ?dist (+ (abs (- ?nx ?gx)) (abs (- ?ny ?gy))))
   (assert (move-score (direction ?dir) (distance ?dist))))
""")

# Rule: Pick the move that results in the HIGHEST distance to the ghost
env.build("""
(defrule choose-best-move
   (move-score (direction ?dir1) (distance ?d1))
   (not (move-score (distance ?d2&:(> ?d2 ?d1))))
   (not (move (direction ?)))
   =>
   (assert (move (direction ?dir1))))
""")

# Rule: Fallback to any legal move if ghost logic doesn't fire
env.build("""
(defrule default-move
   (declare (salience -10))
   (legal-action (direction ?dir))
   (not (move (direction ?)))
   =>
   (assert (move (direction ?dir))))
""")

# ==========================================================
# 2. THE FLASK BRIDGE
# ==========================================================
@app.route('/decide', methods=['POST'])
def decide():
    env.reset()
    data = request.json
    
    # Assert coordinates as strict integers
    env.assert_string(f'(position (type pacman) (x {int(data["pacman"]["x"])}) (y {int(data["pacman"]["y"])}))')
    
    for g in data["ghosts"]:
        env.assert_string(f'(position (type ghost) (x {int(g["x"])}) (y {int(g["y"])}))')
        
    for action in data["legal"]:
        env.assert_string(f'(legal-action (direction "{action}"))')
    
    env.run()
    
    # Extract the move fact
    chosen_move = "Stop"
    for fact in env.facts():
        if fact.template.name == 'move':
            chosen_move = fact['direction']
            
    print(f"Server Decision: {chosen_move}")
    return jsonify({"action": chosen_move})

if __name__ == '__main__':
    print("Logic Server starting on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)