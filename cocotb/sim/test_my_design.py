# test_my_design.py (extended)

import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.clock import Clock


async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")


@cocotb.test()
async def my_second_test(dut):
    """Try accessing the design."""

    #await cocotb.start(generate_clock(dut))  # run the clock "in the background"
    cocotb.start_soon(Clock(dut.clk, 5, units="ns").start())  # start the clock

    await Timer(5, units="ns")  # wait a bit
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    dut._log.info("my_signal_1 is %s", dut.my_signal_1.value)
    print("my_signal_1 is %s", dut.my_signal_1.value)
    assert dut.my_signal_2.value[0] == 0, "my_signal_2[0] is not 0!"