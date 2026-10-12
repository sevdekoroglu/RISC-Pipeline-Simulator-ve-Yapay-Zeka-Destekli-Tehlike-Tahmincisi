from pipeline import PipelineCPU

# Pipeline sistemi oluştur
cpu = PipelineCPU("""
# R-tipi Mantıksal İşlem Testi
LOAD x1, 15        # x1 = 15 (Binary: 1111)
LOAD x2, 7         # x2 = 7  (Binary: 0111)
AND x3, x1, x2     # x3 = 1111 & 0111 = 7  (AND Testi)
OR  x4, x3, x0     # x4 = 0111 | 0000 = 7  (OR Testi)
XOR x5, x4, x1     # x5 = 0111 ^ 1111 = 8  (XOR Testi - Binary: 1000)
""")

# 10 clock döngüsü çalıştır ve pipeline durumunu yazdır
for cycle in range(10):
    cpu.cycle()
