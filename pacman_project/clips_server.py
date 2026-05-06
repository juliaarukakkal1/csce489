from flask import Flask, request, jsonify
import clips
import collections

app = Flask(__name__)
env = clips.Environment()

# ==========================================================
# 1. CLIPS RULES (The Brain)
# ==========================================================
# Template for moves and our stop-tracking
env.build("(deftemplate move (slot dir) (slot score (default 0)))")
env.build("(deftemplate stop-count (slot value))")

# Rule: Ghost Danger (Only applies to moving directions)
env.build("""
(defrule ghost-danger
   (ghost-fact (dist ?d) (scared-timer ?t&:(<= ?t 5)))
   ?m <- (move (dir ?dir&~Stop) (score ?s))
   =>
   (if (= ?d 0) then (modify ?m (score (- ?s 5000000)))
    else (if (< ?d 6) then (modify ?m (score (- ?s (/ 50000 (+ ?d 1))))))))
""")

# Rule: If we've stopped too much, destroy the 'Stop' option entirely
env.build("""
(defrule ban-stopping
   (stop-count (value ?v&:(>= ?v 3)))
   ?m <- (move (dir Stop))
   =>
   (retract ?m))
""")

# Rule: Base incentive to move (Keep it simple)
env.build("""
(defrule move-incentive
   ?m <- (move (dir ?d&~Stop) (score ?s))
   =>
   (modify ?m (score (+ ?s 100))))
""")

# ==========================================================
# 2. DIJKSTRA SENSOR
# ==========================================================
def get_dijkstra_dist(start, target, walls, width, height):
    if start == target: return 0
    queue = collections.deque([(start, 0)])
    visited = {start}
    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == target: return dist
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
    return 999 

# ==========================================================
# 3. GLOBAL STATE & ROUTE
# ==========================================================
stop_streak = 0

@app.route('/decide', methods=['POST'])
def decide():
    global stop_streak
    env.reset()
    data = request.json
    
    px, py = int(data["pacman"]["x"]), int(data["pacman"]["y"])
    walls = set([(int(w['x']), int(w['y'])) for w in data.get("walls", [])])
    width, height = data.get("width", 30), data.get("height", 30)
    legal = data.get("legal", [])

    # 1. Assert current stop streak into CLIPS
    env.assert_string(f'(stop-count (value {stop_streak}))')
    
    # 2. Assert all legal moves as facts
    move_map = {"North": (0, 1), "South": (0, -1), "East": (1, 0), "West": (-1, 0), "Stop": (0, 0)}

    for m in legal:
        nx, ny = px + move_map[m][0], py + move_map[m][1]
        env.assert_string(f'(move (dir {m}) (score 0))')
        
        # Sense ghosts for this specific potential position
        for g in data.get("ghosts", []):
            d = get_dijkstra_dist((nx, ny), (int(g['x']), int(g['y'])), walls, width, height)
            # We use a simple fact assertion for the rule to catch
            env.build(f"(defrule temp-ghost-{m} => (assert (ghost-fact (dist {d}) (scared-timer {int(g.get('scared_timer', 0))}) (target-move {m}))))")

    # Note: Simplified ghost-danger for CLIPS readability. 
    # Usually you'd use a more complex multislot, but this keeps the code "less".
    env.run()

    # 3. Find the winner
    best_dir, best_score = "Stop", -float('inf')
    found_moves = False
    
    for fact in env.facts():
        if fact.template.name == 'move':
            found_moves = True
            if fact['score'] > best_score:
                best_score = fact['score']
                best_dir = fact['dir']

    # 4. Update the streak
    if best_dir == "Stop":
        stop_streak += 1
    else:
        stop_streak = 0

    print(f"[LOG] Intent: {best_dir} | Streak: {stop_streak}")
    return jsonify({"action": best_dir})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)