from cpu.scalers.FIFO import fifo
from cpu.scalers.SJF import sjf
from cpu.scalers.RR import rr
from cpu.scalers.EDF import edf
from cpu.memory.swap_algorithm.swap_fifo import swap_fifo

scalonator_translate = {
    "FIFO": fifo,
    "SJF": sjf,
    "RR": rr,
    "EDF": edf,
}

swap_translate = {
    "FIFO": swap_fifo
}


path = "cpu/configs"
file_name = "cicles_log.json"
turnover_file_name = "turnover.json"
