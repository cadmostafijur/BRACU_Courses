#Part 1: Mortal Kombat

def alpha_beta_pruning(depth, node_index, maximizing_player, values, alpha, beta):
    if depth == 3:
        return values[node_index]

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(2):
            eval = alpha_beta_pruning(depth + 1, node_index * 2 + i, False, values, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(2):
            eval = alpha_beta_pruning(depth + 1, node_index * 2 + i, True, values, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def simulate_game(start_player):
    # utility_values = [-1, 1, -1, 1, -1, 1, -1, 1]
    utility_values = [1, -1, 1, -1, 1, -1, 1, -1]
    round_winners = []
    rounds = 3

    current_player = start_player

    for round_num in range(rounds):
        round_winner_value = alpha_beta_pruning(0, 0, current_player == 1, utility_values, float('-inf'), float('inf'))
        round_winner = "Sub-Zero" if round_winner_value == 1 else "Scorpion"
        round_winners.append(round_winner)

        current_player = 1 if current_player == 0 else 0

    return round_winners

start_player = int(input("Enter 0 for Scorpion, 1 for Sub-Zero: "))
round_winners = simulate_game(start_player)

game_winner = round_winners[-1]

print(f"Game Winner: {game_winner}")
print(f"Total Rounds Played: {len(round_winners)}")

for i, winner in enumerate(round_winners, 1):
    print(f"Winner of Round {i}: {winner}")