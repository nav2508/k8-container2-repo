from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Persistent volume path
PERSISTENT_STORAGE = "/Navya_PV_dir"

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    
    if "file" not in data or "product" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(PERSISTENT_STORAGE, data["file"])

    if not os.path.exists(file_path):
        return jsonify({"file": data["file"], "error": "File not found."}), 404

    try:
        total = 0
        with open(file_path, "r") as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                product, amount = line.strip().split(',')
                if product == data["product"]:
                    total += int(amount)

        return jsonify({"file": data["file"], "sum": total}), 200
    except:
        return jsonify({"file": data["file"], "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
