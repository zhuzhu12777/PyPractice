# Copyright cocotb contributors
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause

DUT         ?= matrix_multiplier
TOPLEVEL    ?= $(DUT)
MODULE      ?= test_$(DUT)
# TESTCASE    ?= 

TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)

# export RANDOM_SEED := 1234567890
export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = $(PWD)/../rtl/$(DUT).sv

COCOTB_TOPLEVEL     := $(DUT)
COCOTB_TEST_MODULES := test_$(DUT)

include $(shell cocotb-config --makefiles)/Makefile.sim