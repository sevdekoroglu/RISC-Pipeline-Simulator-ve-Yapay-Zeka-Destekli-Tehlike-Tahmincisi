from flask import Flask, render_template, jsonify, request
from pipeline import PipelineCPU
import os

app = Flask(__name__)

# Global CPU nesnesi
cpu = PipelineCPU("")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/load_code", methods=['POST'])
def load_code():
    """Arayüzden gelen Assembly kodunu parse eder ve CPU'yu hazırlar."""
    global cpu
    try:
        data = request.get_json()
        user_code = data.get('code', '')
        # Yeni bir CPU instance'ı oluşturarak her şeyi sıfırlıyoruz
        cpu = PipelineCPU(user_code)
        return jsonify({"status": "success", "message": "Program yüklendi."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/next")
def next_cycle():
    """Simülasyonu bir saat çevrimi ilerletir."""
    global cpu
    try:
        cpu.cycle()
        
        # Pipeline içindeki AI modülünden verileri çekiyoruz
        # Fonksiyon isminin pipeline.py içindekiyle aynı olduğundan emin ol (get_metrics)
        metrics = cpu.ai.get_metrics()
        
        return jsonify({
            "clock": cpu.clock,
            "IF_EX": cpu.IF_EX,
            "EX_WB": cpu.EX_WB,
            "registers": cpu.registers,
            "hazard": cpu.last_hazard_info,
            "ai_prediction": cpu.last_hazard_info.get("ai_prediction", "NONE"),
            "metrics": metrics
        })
    except Exception as e:
        print(f"Cycle hatası: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/reset")
def reset():
    """Mevcut programı koruyarak işlemci durumunu sıfırlar."""
    global cpu
    try:
        # Mevcut programı saklayıp CPU'yu yeniden başlatıyoruz
        current_program = cpu.program
        cpu = PipelineCPU(current_program)
        return jsonify({"status": "success", "clock": 0})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # macOS AirPlay (5000 portu) çakışmasını önlemek için 5001 portu kullanımı
    print("\n--- RISC Pipeline Simulator Başlatıldı ---")
    print("Adres: http://127.0.0.1:5001")
    print("Durdurmak için: Ctrl+C\n")
    app.run(debug=True, port=5001)