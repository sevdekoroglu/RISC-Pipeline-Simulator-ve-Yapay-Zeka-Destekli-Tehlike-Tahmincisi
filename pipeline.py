import datetime # Zaman damgası için gerekli
from parser import Parser
from hazard_unit import HazardUnit
from ai_predictor import AIPredictor

class PipelineCPU:
    def __init__(self, program):
        self.program = program
        self.pc = 0
        self.clock = 0
        # Her oturum için benzersiz bir ID oluşturur
        self.session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        self.parser = Parser()
        self.hazard = HazardUnit()
        self.ai = AIPredictor()

        # Programı listeye çevir
        self.instructions = self.parser.parse_program(program)

        # Register file (x0-x31)
        self.registers = [0] * 32

        # Pipeline registers
        self.IF_EX = {"opcode": None, "rs1": None, "rs2": None, "rd": None, "imm": None}
        self.EX_WB = {"opcode": None, "rd": None, "ALU_result": None}

        self.last_hazard_info = {
            "raw_hazard": False, "load_use_hazard": False,
            "forward_rs1": False, "forward_rs2": False,
            "stall": False, "ai_prediction": "NONE"
        }

        self.prev_inst = None
        self.stall = False
        
        # OLUŞTURULAN OTURUMU KAYDET
        clean_code = program.replace('\n', ' ').strip()
        self.log_save(f"START | {clean_code}", log_type="SESSION")

    def log_save(self, message, log_type="CYCLE_LOG"):
        """Verileri anlık olarak simulation_db.txt dosyasına yazar"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{log_type}] | {timestamp} | {self.session_id} | {message}"
        
        try:
            # 'a' moduyla ekleme yapar, flush() ile anında diske yazar
            with open("simulation_db.txt", "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
                f.flush() 
        except Exception as e:
            print(f"Veritabanı kayıt hatası: {e}")

    def execute_IF(self):
        if self.stall:
            return

        if self.pc >= len(self.instructions):
            self.IF_EX = {"opcode": None, "rs1": None, "rs2": None, "rd": None, "imm": None}
            return

        inst = self.instructions[self.pc]
        self.pc += 1
        
        self.IF_EX = {"opcode": None, "rs1": None, "rs2": None, "rd": None, "imm": None}
        self.IF_EX.update(inst)

    def execute_EX(self):
        opcode = self.IF_EX["opcode"]
        if opcode is None:
            self.EX_WB.update({"opcode": None, "rd": None, "ALU_result": None})
            return

        hazard_info = self.hazard.check_hazards(self.IF_EX, self.EX_WB)
        ai_prediction = self.ai.predict_hazard_type(self.prev_inst, self.IF_EX)
        
        if hazard_info["stall"]:
            self.stall = True
            self.pc -= 1  
            self.EX_WB.update({"opcode": None, "rd": None, "ALU_result": None})
            self.ai.update_stats(ai_prediction, is_stall=True, is_new_inst=False)
            self.last_hazard_info = hazard_info
            self.last_hazard_info["ai_prediction"] = ai_prediction
            return
        
        self.stall = False

        rs1, rs2 = self.IF_EX["rs1"], self.IF_EX["rs2"]
        val1 = self.registers[rs1] if rs1 is not None else 0
        val2 = self.registers[rs2] if rs2 is not None else 0

        if hazard_info["forward_rs1"]:
            val1 = self.EX_WB["ALU_result"]
        if hazard_info["forward_rs2"]:
            val2 = self.EX_WB["ALU_result"]

        if opcode == 'ADD': result = val1 + val2
        elif opcode == 'SUB': result = val1 - val2
        elif opcode == 'AND': result = val1 & val2
        elif opcode == 'OR':  result = val1 | val2
        elif opcode == 'XOR': result = val1 ^ val2
        elif opcode == 'LOAD': result = self.IF_EX["imm"]
        else: result = 0

        self.EX_WB.update({
            "opcode": opcode,
            "rd": self.IF_EX["rd"],
            "ALU_result": result
        })

        self.prev_inst = self.IF_EX.copy()
        self.ai.update_stats(ai_prediction, is_stall=False, is_new_inst=True)
        self.last_hazard_info = hazard_info
        self.last_hazard_info["ai_prediction"] = ai_prediction

    def execute_WB(self):
        opcode = self.EX_WB["opcode"]
        rd = self.EX_WB["rd"]
        result = self.EX_WB["ALU_result"]

        if opcode and rd is not None and rd != 0:
            self.registers[rd] = result

    def cycle(self):
        self.clock += 1
        self.execute_WB()
        self.execute_EX()
        self.execute_IF()

        # ÇEVRİM VERİLERİNİ KAYDET
        metrics = self.ai.get_metrics()
        h_type = "RAW" if self.last_hazard_info["raw_hazard"] else "LOAD_USE" if self.last_hazard_info["load_use_hazard"] else "NONE"
        
        log_msg = (f"Cycle:{self.clock} | Hazard:{h_type} | "
                   f"Pred:{self.last_hazard_info['ai_prediction']} | "
                   f"Stall:{self.last_hazard_info['stall']} | "
                   f"CPI:{metrics.get('cpi', 0)} | StallRate:%{metrics.get('stall_rate', 0)}")
        
        self.log_save(log_msg)