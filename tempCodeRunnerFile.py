# parser.py (FINAL VERSION)

class Parser:

    # Register isimlerini integer index'e çevirme
    def reg(self, name):
        if name.startswith("x"):
            return int(name[1:])
        return None

    # Tek satır komutu RISC formatında ayrıştırma
    def parse_instruction(self, line):

        line = line.split("#")[0].strip()  # yorum temizle
        if not line:
            return None

        parts = line.replace(",", "").split()

        opcode = parts[0].upper()

        # --------------------- ADD rd, rs1, rs2 ----------------------
        if opcode in ["ADD", "SUB"]:
            rd = self.reg(parts[1])
            rs1 = self.reg(parts[2])
            rs2 = self.reg(parts[3])

            return {
                "opcode": opcode,
                "rd": rd,
                "rs1": rs1,
                "rs2": rs2,
                "imm": None
            }

        # --------------------- LOAD rd, imm(rs1) ----------------------
        if opcode == "LOAD":
            rd = self.reg(parts[1])

            # imm(rs1) formatını çöz
            imm_part = parts[2]
            imm, regpart = imm_part.split("(")
            imm = int(imm)
            rs1 = self.reg(regpart.replace(")", ""))

            return {
                "opcode": "LOAD",
                "rd": rd,
                "rs1": rs1,
                "rs2": None,
                "imm": imm
            }

        raise ValueError(f"Unsupported instruction: {line}")

    # Programdaki tüm satırları ayrıştırır
    def parse_program(self, program_text):
        instructions = []
        for line in program_text.split("\n"):
            inst = self.parse_instruction(line)
            if inst:
                instructions.append(inst)
        return instructions


# Test (isteğe bağlı)
if __name__ == "__main__":
    parser = Parser()
    prog = """
    ADD x1, x0, x0
    LOAD x2, 100(x1)
    SUB x3, x2, x1
    """
    out = parser.parse_program(prog)
    print(out)
