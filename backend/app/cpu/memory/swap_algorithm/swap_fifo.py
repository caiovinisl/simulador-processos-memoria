from collections import deque, Counter

def swap_fifo(
    p_order:deque,
    counter:Counter,
    removed_p_count:int
):
    old_process_name = p_order[-1] #pega a primeira posição
    p_order.rotate()
    return old_process_name
