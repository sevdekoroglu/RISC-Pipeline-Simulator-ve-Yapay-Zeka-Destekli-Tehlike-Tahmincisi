class AIPredictor:
    def __init__(self):
        # AI'nın takip ettiği hazard geçmişi
        self.history = {
            "RAW": 0,
            "LOAD_USE": 0,
            "NONE": 0
        }
        # Performans metrikleri
        self.total_cycles = 0
        self.total_instructions = 0
        self.total_stalls = 0

    def predict_hazard_type(self, prev_inst, next_inst):
        """İki komut arasındaki bağımlılığı analiz eder."""
        if not prev_inst or not next_inst:
            return "NONE"

        p_opcode = prev_inst.get("opcode")
        p_rd = prev_inst.get("rd")
        n_rs1 = next_inst.get("rs1")
        n_rs2 = next_inst.get("rs2")

        # R0 her zaman 0'dır, hazard yaratmaz
        if p_rd is None or p_rd == 0:
            return "NONE"

        # LOAD-USE Durumu
        if p_opcode == "LOAD" and (p_rd == n_rs1 or p_rd == n_rs2):
            return "LOAD_USE"

        # Genel RAW Durumu
        if p_rd == n_rs1 or p_rd == n_rs2:
            return "RAW"

        return "NONE"

    def update_stats(self, hazard_type, is_stall, is_new_inst):
        """Her çevrimde verileri günceller."""
        self.total_cycles += 1
        if is_stall:
            self.total_stalls += 1
        if is_new_inst:
            self.total_instructions += 1
        if hazard_type in self.history:
            self.history[hazard_type] += 1

    def get_metrics(self):
        """app.py tarafından çağrılan raporlama fonksiyonu."""
        cpi = self.total_cycles / self.total_instructions if self.total_instructions > 0 else 1.0
        stall_rate = (self.total_stalls / self.total_cycles) * 100 if self.total_cycles > 0 else 0
        
        return {
            "CPI": round(cpi, 2),
            "Stall_Rate": round(stall_rate, 2),
            "Total_Cycles": self.total_cycles,
            "Total_Instructions": self.total_instructions,
            "History": self.history
        }