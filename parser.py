class Parser:
    def reg(self, name):
        if not name: return None
        name = name.lower() 
        if name.startswith("x"):
            try: 
                # x10 -> 10 değerini döndürür
                return int(name[1:])
            except: 
                return None
        return None

    def parse_instruction(self, line):
        # Yorum satırlarını temizle (# sonrası)
        line = line.split("#")[0].strip()
        if not line: return None
        
        # Virgülleri temizle ve parçalara böl
        parts = line.replace(",", " ").split()
        if len(parts) < 2: return None

        opcode = parts[0].upper()

        # R-Tipi Komutlar (Aritmetik ve Mantıksal)
        if opcode in ["ADD", "SUB", "AND", "OR", "XOR"]:
            try:
                return {
                    "opcode": opcode,
                    "rd": self.reg(parts[1]),
                    "rs1": self.reg(parts[2]),
                    "rs2": self.reg(parts[3]),
                    "imm": None
                }
            except IndexError:
                return None

        # I-Tipi Komut (LOAD)
        if opcode == "LOAD":
            try:
                rd = self.reg(parts[1])
                imm_part = parts[2]
                
                # Format 1: LOAD x1, 100(x2)
                if "(" in imm_part:
                    imm_str, regpart = imm_part.split("(")
                    imm = int(imm_str)
                    rs1 = self.reg(regpart.replace(")", ""))
                # Format 2: LOAD x1, 100
                else:
                    imm = int(imm_part)
                    rs1 = None
                
                return {"opcode": "LOAD", "rd": rd, "rs1": rs1, "rs2": None, "imm": imm}
            except (IndexError, ValueError):
                return None
                
        return None

    def parse_program(self, program_text):
        instructions = []
        if not program_text: return []
        
        for line in program_text.strip().split("\n"):
            inst = self.parse_instruction(line)
            if inst: 
                instructions.append(inst)
        return instructions