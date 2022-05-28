from collections import deque

def swap_fifo(
    p_order:deque
):
    old_process_name = p_order[-1] #pega a primeira posição
    p_order.rotate()
    return old_process_name
