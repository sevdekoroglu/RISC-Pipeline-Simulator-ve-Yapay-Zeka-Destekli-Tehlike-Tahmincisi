class HazardUnit:
    def __init__(self):
        pass

    def detect_raw_hazard(self, IF_EX, EX_WB):
        """
        Read-After-Write (RAW) durumunu tespit eder.
        """
        rd = EX_WB.get("rd")
        # r0 yazmacı sabittir, hazard yaratmaz. rd None ise işlem yoktur.
        if rd is None or rd == 0:
            return False

        rs1 = IF_EX.get("rs1")
        rs2 = IF_EX.get("rs2")

        return (rs1 == rd) or (rs2 == rd)

    def forwarding_decision(self, IF_EX, EX_WB):
        """
        Verinin bir sonraki aşamaya beklemeden aktarılıp aktarılmayacağına karar verir.
        """
        forward_rs1 = False
        forward_rs2 = False

        rd = EX_WB.get("rd")
        rs1 = IF_EX.get("rs1")
        rs2 = IF_EX.get("rs2")

        # Forwarding sadece yazılacak bir register varsa ve bu x0 değilse yapılır
        if rd is not None and rd != 0:
            if rd == rs1:
                forward_rs1 = True
            if rd == rs2:
                forward_rs2 = True

        return forward_rs1, forward_rs2

    def detect_load_use_hazard(self, IF_EX, EX_WB):
        """
        LOAD komutundan hemen sonra gelen bağımlı komut için stall (kabarcık) gerekir.
        """
        # EX_WB içindeki komut LOAD mı kontrol et
        if EX_WB.get("opcode") != "LOAD" or EX_WB.get("rd") == 0:
            return False

        load_rd = EX_WB.get("rd")
        rs1 = IF_EX.get("rs1")
        rs2 = IF_EX.get("rs2")

        # Eğer LOAD'un hedefi, bir sonraki komutun kaynağı ise: STALL!
        return (load_rd is not None) and (load_rd == rs1 or load_rd == rs2)

    def check_hazards(self, IF_EX, EX_WB):
        """
        Tüm denetimleri birleştirir ve pipeline kontrol sinyallerini üretir.
        """
        raw = self.detect_raw_hazard(IF_EX, EX_WB)
        f_rs1, f_rs2 = self.forwarding_decision(IF_EX, EX_WB)
        load_use = self.detect_load_use_hazard(IF_EX, EX_WB)

        return {
            "raw_hazard": raw,
            "forward_rs1": f_rs1,
            "forward_rs2": f_rs2,
            "load_use_hazard": load_use,
            "stall": load_use  # LOAD-USE varsa pipeline 1 çevrim durur
        }