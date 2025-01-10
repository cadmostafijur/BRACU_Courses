def min_maxalgo(nidx,level,chk_turn,alpha,beta,valu):
    if level==3:
        return valu[nidx]
    if chk_turn:
        m_num = float('-inf')
        for i in range(2):
            num = min_maxalgo(2 * nidx + i, level + 1, False, alpha, beta, valu)
            m_num = max(m_num, num)
            alpha = max(alpha, num)
            if beta <= alpha:
                break
        return m_num
    else:
        min_num = float('inf')
        for k in range(2):
            num = min_maxalgo(2 * nidx + k, level + 1, True, alpha, beta, valu)
            min_num = min(min_num, num)
            beta = min(beta, num)
            if beta <= alpha:
                break
        return min_num
def pacman_game(c):
    valu = [3, 6, 2, 3, 7, 1, 2, 0]
    minimax_valu = min_maxalgo(0, 0, True, float('-inf'), float('inf'), valu)
    l_tree = max(valu[0], valu[1]) - c
    r_tree = max(valu[4], valu[5]) - c

    if l_tree > r_tree:
        new_minimax = l_tree
        path = "left"
    else:
        new_minimax = r_tree
        path = "right"

    if new_minimax > minimax_valu:
        print(f"The new minimax value is {new_minimax}. Pacman goes {path} and uses dark magic.")
    else:
        print(f"The minimax value is {minimax_valu}. Pacman does not use dark magic.")
c=int(input("enter valu of c:"))
pacman_game(c)
# comment="invalid value"
# check=pacman_game(c) if  else
# if c.lstrip('-').isdigit():
#     pacman_game(c)
# else:
#     print(comment)

