from fontTools.ttLib.tables.ttProgram import Program, _indentRE, _unindentRE


def format_assembly(instructions: str | list[str] | bytes) -> str:
    inst: list[str] = []
    if isinstance(instructions, bytes):
        p = Program()
        p.fromBytecode(instructions)
        inst: list[str] = p.getAssembly()
    elif isinstance(instructions, str):
        inst = instructions.splitlines()
    elif isinstance(instructions, list):
        inst = instructions
    else:
        raise TypeError(f"Can't format assembly of type {type(instructions)}")

    # Apply indentation to imported binary program. Who said OCD?
    asm = "\n"
    white = "  "  # indent with two spaces
    indent = 0
    for line in inst:
        if _unindentRE.match(line):
            indent -= 1
        asm += f"{white * indent}{line}\n"
        if _indentRE.match(line):
            indent += 1
    return asm
