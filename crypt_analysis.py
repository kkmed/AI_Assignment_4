def solve():
    letters = ['S','E','N','D','M','O','R','Y']
    assignment = {}

    def is_valid():
        if len(assignment) == len(letters):
            S,E,N,D,M,O,R,Y = [assignment[l] for l in letters]

            if S == 0 or M == 0:
                return False

            send = 1000*S + 100*E + 10*N + D
            more = 1000*M + 100*O + 10*R + E
            money = 10000*M + 1000*O + 100*N + 10*E + Y

            return send + more == money
        return True

    def backtrack():
        if len(assignment) == len(letters):
            if is_valid():
                print("Solution:", assignment)
                return True
            return False

        unassigned = [l for l in letters if l not in assignment]
        var = unassigned[0]

        for digit in range(10):
            if digit in assignment.values():
                continue

            assignment[var] = digit

            if is_valid():
                if backtrack():
                    return True

            del assignment[var]

        return False

    backtrack()


solve()