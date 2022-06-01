from collections import deque,Counter

def swap_lru(
    p_order:deque,
    counter:Counter,
    removed_p_count:int
):
    least_used = counter.most_common()[:-removed_p_count-1:-1] 

    return least_used[removed_p_count-1][0] #retorna o nome do processo menos usado


