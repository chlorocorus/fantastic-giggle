# fantastic-giggle
This is a design for low power draw applications.

## Boot ROM generation
### Generate a blank BootROM
```shell
$ dd if=/dev/zero of=./rtl_memory16/bootrom.hex bs=4k count=1
```
Edit this in a hex editor to get what you want. This is how we generate 4kB BootROM blanks in house.
### Convert the BootROM to a Verilog hex file
```shell
$ python3 ./utilities/genmem.py ./rtl_memory/bootrom.hex > ./rtl_memory/bootrom.mem
```
This can be put into a Verilog Vivado project as a valid hex file for our memory's `$readmemh`. To include the notice for posterity:
```c
// Autogenerated file by `genmem.py`
// Due to the sparse nature of Verilog HEX files, it is recommended to
// use the `genmem.py` script with a hex file to generate hex files.
// . . .
```
## Shader ISA
### Pipelining
Each shader has 4 stages.
### Addressing Modes
#### Immediate
Load two 8-bit immediate values, store into register. Due to the very nature of this shader architecture this will take two cycles.
```
Clk[0] => fetch/decode opcode
Clk[1] => fetch imm[1]
Clk[2] => fetch imm[0]
Clk[3] => execution of sequential unit(s) BEGIN

Clk[4] => STALL
Clk[5] => STALL
Clk[6] => execution of sequential unit(s) END
Clk[7] => write INTO ONLY register, possibly checking flags
```
#### Indirect
Load a 16-bit address for two 8-bit values to store into/from a register.
```
Clk[0] => fetch/decode opcode
Clk[1] => fetch addr[1]
Clk[2] => fetch addr[0]
Clk[3] => write INTO OR FROM register, possibly checking flags
```
### The flags
- 0: ALU Always
- 1: ALU Carry
- 2: ALU Zero
- 3: ALU Sign
- 4: LOD0 Bit0
- 5: LOD0 Bit1
- 6: LOD0 Hot
- 7: HBlank
- 8: LOD1 Bit0
- 9: LOD1 Bit1
- A: LOD1 Hot
- B: VBlank
- C: Never 
- D: 0
- E: 0
- F: 0 
### Opcodes
- ALU: No op, Add, Subtract, And, Or, Xor, Select Left, Select Right, set appropriate flags
- LOD: Check Nybbles 0, 1, 2, 3, set appropriate flags
- Barrel Shifter: shift left/right by a scalar
- Register File: Probably 8 16-bit registers
#### `00h` - Barrel Shift
#### `20h` - ALU Add/Subtract
#### `40h` - ALU And
#### `60h` - ALU Or
#### `80h` - ALU Xor
#### `A0h` - ALU Select Input 0
#### `C0h` - ALU Select Input 1
#### `E0h` - Intercept Control Codes
- `E0h` - JI: Store program counter into `pc` immediately
- `E1h` - JI: Store program counter into `pc` immediately
- `E2h` - JI: Store program counter into `pc` immediately
- `E3h` - JI: Store program counter into `pc` immediately
- `E4h` - JI: Store program counter into `pc` immediately
- `E5h` - JI: Store program counter into `pc` immediately
- `E6h` - JI: Store program counter into `pc` immediately
- `E7h` - JI: Store program counter into `pc` immediately
- `E8h` - JI: Store program counter into `pc` immediately
- `E9h` - JI: Store program counter into `pc` immediately
- `EAh` - JI: Store program counter into `pc` immediately
- `EBh` - JI: Store program counter into `pc` immediately
- `ECh` - NOP
- `EDh` - Barrel Shift Direction Left
- `EEh` - Barrel Shift Direction Right
- `EFh` - Barrel Shift Magnitude Set
- `F0h` - JD: Store program counter into `pc` indirectly
- `F1h` - JD: Store program counter into `pc` indirectly
- `F2h` - JD: Store program counter into `pc` indirectly
- `F3h` - JD: Store program counter into `pc` indirectly
- `F4h` - JD: Store program counter into `pc` indirectly
- `F5h` - JD: Store program counter into `pc` indirectly
- `F6h` - JD: Store program counter into `pc` indirectly
- `F7h` - JD: Store program counter into `pc` indirectly
- `F8h` - JD: Store program counter into `pc` indirectly
- `F9h` - JD: Store program counter into `pc` indirectly
- `FAh` - JD: Store program counter into `pc` indirectly
- `FBh` - JD: Store program counter into `pc` indirectly
- `FCh` - NOP
- `FDh` - STP: Store indirectly into `port`
- `FEh` - LDP: Load indirectly from `port`
- `FFh` - BRK: Breakpoint
#### Suffixes (add these to a non-control code to manipulate the operation)
- `10h`: indirect (can be added to some control opcodes)

If checking the flags then you will skip operations if the criteria aren't
satisfied.
- `08h`: check flag register bit 3 before execution
- `04h`: check flag register bit 2 before execution
- `02h`: check flag register bit 1 before execution
- `01h`: check flag register bit 0 before execution