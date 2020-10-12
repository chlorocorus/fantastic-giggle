import sys


def gen_stream(stream) -> None:
    for pos, byte in enumerate(stream.read()):
        if pos % 26 == 25:
            print(f"{byte:02x}")
        else:
            print(f"{byte:02x}", end=' ')
    print()


print("// Autogenerated file by `genmem.py`")
print("// Due to the sparse nature of Verilog HEX files, it is recommended to")
print("// use the `genmem.py` script with a hex file to generate hex files.")
print("// === MEMFILE BELOW ===")
if len(sys.argv) == 1 or sys.argv[1] == "-":
    gen_stream(sys.stdin.buffer)
else:
    gen_stream(open(sys.argv[1], 'rb'))
print("// === MEMFILE ABOVE ===")
