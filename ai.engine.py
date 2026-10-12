class AIPerformancePredictor:
    def __init__(self):
        # AI'nın "öğrendiği" ağırlıklar (Weights)
        self.stall_weight = 1.15  # Load-use dependency gecikme katsayısı
        self.base_cpi = 1.0       # İdeal Pipeline CPI değeri
        
    def analyze_instructions(self, instructions):
        """
        Gelen assembly kodunu tarar ve daha çalışmadan 
        oluşacak Stall ve CPI değerini tahmin eder.
        """
        predicted_stalls = 0
        total_instructions = len(instructions)
        
        for i in range(len(instructions) - 1):
            current_instr = instructions[i].lower()
            next_instr = instructions[i+1].lower()
            
            # Pattern Recognition: LOAD sonrası bağımlılık var mı?
            # Örnek: LOAD R1, [100] -> ADD R2, R1 (R1 bağımlılığı)
            if "load" in current_instr:
                # Basit bir string analizi ile register bağımlılığı kontrolü
                target_reg = current_instr.split()[1].replace(",", "")
                if target_reg in next_instr:
                    predicted_stalls += 1 
        
        # CPI Tahmini = (Toplam Çevrim / Toplam Komut)
        # 3-Stage Pipeline'da: Toplam Çevrim = Komut Sayısı + 2 (Dolma) + Stall Sayısı
        predicted_cycles = total_instructions + 2 + predicted_stalls
        predicted_cpi = predicted_cycles / total_instructions
        
        return {
            "predicted_cpi": round(predicted_cpi, 2),
            "predicted_stalls": predicted_stalls,
            "confidence_score": "%95" # Modelin kendine güveni
        }

# --- KULLANIM ÖRNEĞİ ---
# codes = ["LOAD R1, 10", "ADD R2, R1", "SUB R3, R4"]
# ai = AIPerformancePredictor()
# print(ai.analyze_instructions(codes))