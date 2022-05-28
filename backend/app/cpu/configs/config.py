from cpu.scalers.FIFO import fifo
from cpu.memory.swap_algorithm.swap_fifo import swap_fifo

scalonator_translate = {
    "FIFO": fifo,
}

swap_translate = {
    "FIFO": swap_fifo
}


path = "cpu/configs"
file_name = "cicles_log.json"
turnover_file_name = "turnover.json"
