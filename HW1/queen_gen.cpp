#include <iostream>
#include <vector>
#include <string>
#include <cmath>

using namespace std;

// Converts (row, col) to a variable ID from 1 to 64
int id(int r, int c) {
    return (r * 8) + c + 1;
}

int main() {

    vector<string> clauses;
    // 1. Row Constraint: Each row must have at least one queen
    for (int r = 0; r < 8; r++) {
        string clause = "";
        for (int c = 0; c < 8; c++) {
            clause += to_string(id(r, c)) + " ";
        }
        clauses.push_back(clause + "0");
    }
    // 2. Conflict Constraints: No two queens can attack each other
    for (int r1 = 0; r1 < 8; r1++) {
        for (int c1 = 0; c1 < 8; c1++) {
            for (int r2 = 0; r2 < 8; r2++) {
                for (int c2 = 0; c2 < 8; c2++) {
                    int u = id(r1, c1);
                    int v = id(r2, c2);

                    if (u >= v) continue; // Avoid duplicate pairs (e.g., 1-2 and 2-1)

                    // Logic: Do these two squares conflict?
                    bool sameRow = (r1 == r2);
                    bool sameCol = (c1 == c2);
                    bool sameDiag = (abs(r1 - r2) == abs(c1 - c2));

                    if (sameRow || sameCol || sameDiag) {
                        // Add clause: (NOT u OR NOT v) -> They cannot both be true
                        clauses.push_back("-" + to_string(u) + " -" + to_string(v) + " 0");
                    }
                }
            }
        }
    }
    // Output DIMACS format
    cout << "c 8-Queens CNF for MiniSat" << endl;
    cout << "p cnf 64 " << clauses.size() << endl;
    for (const string& c : clauses) {
        cout << c << endl;
    }

    return 0;
}
