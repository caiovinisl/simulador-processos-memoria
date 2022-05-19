

def swap_fifo(
    memory_real
):
    old_process_name = memory_real.process_stack[-1] #pega a primeira posição
    memory_real.process_stack.rotate()
    return old_process_name