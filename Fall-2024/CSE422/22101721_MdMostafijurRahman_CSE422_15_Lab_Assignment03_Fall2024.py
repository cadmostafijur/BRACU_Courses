# alpha=float('-inf')
# beta=float('inf')

def alphabeta_p(level,idx,maxplayer,valu,alpha,beta):
    if level==3:
        return valu[idx]
    if maxplayer:
        m_num=float('-inf')
        chkvalue=False
        for k in range(2):
            
            num=alphabeta_p(level+1,idx*2+k,False,valu,alpha,beta)
            m_num=max(m_num,num)
            alpha=max(alpha,num)
            if beta<=alpha:
                break
        return m_num
    else:
        min_num=float('inf')
        chkvalue=True
        for j in range(2):
            
            num=alphabeta_p(level+1,idx*2+j,True,valu,alpha,beta)
            min_num=min(min_num,num)
            beta=min(beta,num)
            if beta<=alpha:
                break
        return min_num
def gamestart(ft_player):
    valuut=[-1, 1, -1, 1, -1, 1, -1, 1]
    win_in_rounds=[]
    t_round=3
    ck_curr_player=ft_player
    for i in range(t_round):
        win_in_round_valu=alphabeta_p(0,0,ck_curr_player==1,valuut,float('-inf'),float('inf'))
        if win_in_round_valu == 1 :
            win_in_round="Sub-Zero"
        else:
            win_in_round="Scorpion"
        win_in_rounds.append(win_in_round)
        if ck_curr_player == 0 :
            ck_curr_player=1 
        else:
            ck_curr_player=0
    return win_in_rounds

print("if Scorpion enter 0,else  Sub-Zero enter 1")
ft_player=int(input("Enter your Choice:"))
win_round_valu=gamestart(ft_player)
# print(win_round_valu)
win_game=win_round_valu[-1]
print(f"Game Winner: {win_game}")
print(f"Total Rounds Played: {len(win_round_valu)}")
k=1
for win in win_round_valu:
    print(f"Winner of Round {k}: {win}")
    k+=1



############## part 02

# def min_maxalgo(nidx,level,chk_turn,alpha,beta,valu):
#     if level==3:
#         return valu[nidx]
#     if chk_turn:
#         m_num = float('-inf')
#         for i in range(2):
#             num = min_maxalgo(2 * nidx + i, level + 1, False, alpha, beta, valu)
#             m_num = max(m_num, num)
#             alpha = max(alpha, num)
#             if beta <= alpha:
#                 break
#         return m_num
#     else:
#         min_num = float('inf')
#         for k in range(2):
#             num = min_maxalgo(2 * nidx + k, level + 1, True, alpha, beta, valu)
#             min_num = min(min_num, num)
#             beta = min(beta, num)
#             if beta <= alpha:
#                 break
#         return min_num
# def pacman_game(c):
#     valu = [3, 6, 2, 3, 7, 1, 2, 0]
#     minimax_valu = min_maxalgo(0, 0, True, float('-inf'), float('inf'), valu)
#     l_tree = max(valu[0], valu[1]) - c
#     r_tree = max(valu[4], valu[5]) - c

#     if l_tree > r_tree:
#         new_minimax = l_tree
#         path = "left"
#     else:
#         new_minimax = r_tree
#         path = "right"

#     if new_minimax > minimax_valu:
#         print(f"The new minimax value is {new_minimax}. Pacman goes {path} and uses dark magic.")
#     else:
#         print(f"The minimax value is {minimax_valu}. Pacman does not use dark magic.")
# c=int(input("enter valu of c:"))
# pacman_game(c)
# # comment="invalid value"
# # check=pacman_game(c) if  else
# # if c.lstrip('-').isdigit():
# #     pacman_game(c)
# # else:
# #     print(comment)





#######Part 03

# # 1)
# yes, in minimax algo first player maximize node beacause primary goal 
# to maximize the utility and assume the opponent minimize it.
# # (it depends on type of the game )
# # 2)
# no. alpha beta pruning is design for the deterministic adversarial games 
# such as tic tac toe,,chess.Its mainly two players game. ot works by 
# pruning branch on deterministic results. on the other hand stochastic  
# environment games randomness uncertaily  such as poker game where involve 
# uncertainity due to hindden cars and probalistic results.
