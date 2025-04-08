
## Assigning values to signals
1. 赋值语法 sig.value = new_value 与 HDL 具有相同的语义：写入不会立即应用，而是延迟到下一个写入周期。用于 sig.setimmediatevalue(new_val) 立即设置新值
2. 有符号值和无符号值都可以使用 Python int 分配给信号, `-2**(Nbits - 1) <= value <= 2**Nbits - 1`, 分配超出范围的值将引发 OverflowError

## Reading values from signals
1. 对于 BinaryValue 对象，将保留任何未解析的位，并且可以使用 binstr 属性访问这些位，或者可以使用 integer 属性访问已解析的整数值
```
dut.counter.value.binstr
dut.counter.value.integer
dut.counter.value.n_bits
```

## 并发和顺序执行
1. await将运行异步协程并等待其完成。被调用的协程 “阻止” 当前协程的执行
2. 在 start() 或 start_soon() 中会并发运行协程, 从而允许当前协程继续执行

## Forcing and freezing signals
```
dut.my_signal.value = Force(12)
dut.my_signal.value = Release()
dut.my_signal.value = Freeze()
```

## Logging
`dut._log.info("Test multiplication operations")`

## Concurrent Execution 并发执行
```
cocotb.start_soon(Clock(dut.clk, 1, units='ns').start())
await cocotb.start(tb.reset_dut(dut.rstn, 20))
```

## cocotb.triggers.ClockCycles(signal, num_cycles, rising=True)
在信号从 0 到 1 的 num_cycles 次转换后触发。



