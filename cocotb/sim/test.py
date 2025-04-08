import math
import os
import sys
from pathlib import Path
from random import getrandbits
from typing import Any, Dict, List

import cocotb
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.triggers import RisingEdge, Timer
from cocotb.types import LogicArray, Range
from cocotb.runner import get_runner
from cocotb.result import TestSuccess, TestFailure

async def reset_dut(rstn: SimHandleBase, duration: int) -> None:
    """Reset the DUT for a given duration"""
    rstn.value = 0
    await Timer(duration, units='ns')
    rstn.value = 1

@cocotb.test()
async def test(dut):
    dut.valid_i._log.info("Valid input signal")
    dut.valid_i.value = 1

@cocotb.test()
async def test_act_during_reset(dut):
    """While reset is active, toggle signals"""
    # "Clock" is a built in class for toggling a clock signal
    cocotb.start_soon(Clock(dut.clk_i, 1, units='ns').start())
    # reset_dut is a function -
    # part of the user-generated "uart_tb" class
    # run reset_dut immediately before continuing
    await cocotb.start(reset_dut(dut.reset_i, 20))

    await Timer(10, units='ns')
    print("Reset is still active: %d" % dut.reset_i)
    await Timer(15, units='ns')
    print("Reset has gone inactive: %d" % dut.reset_i)

def test_runner():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    build_args = []
    extra_args = []
    wave_args = 0

    sources = [proj_path / "rtl" / "matrix_multiplier.sv"]

    parameters = {
        "DATA_WIDTH": "32",
        "A_ROWS": 10,
        "B_COLUMNS": 4,
        "A_COLUMNS_B_ROWS": 6,
    }

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "sim"))

    runner = get_runner(sim)

    runner.build(
        hdl_toplevel="matrix_multiplier",
        sources=sources,
        build_args=build_args + extra_args,
        parameters=parameters,
        always=True,
        waves=wave_args,
    )

    runner.test(
        hdl_toplevel="matrix_multiplier",
        hdl_toplevel_lang=hdl_toplevel_lang,
        test_module="test",
        test_args=extra_args,
        waves=wave_args,
    )


if __name__ == "__main__":
    test_runner()

