from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Persistent volume path
PERSISTENT_STORAGE = "/Navya_PV_dir"

def read_and_validate_csv(file_path):
    """Read and validate CSV file, return data if valid"""
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames

            if not headers or "product" not in headers or "amount" not in headers:
                raise ValueError("Input file not in CSV format.")

            # Reset file pointer to read rows correctly
            csvfile.seek(0)
            next(reader)  # Skip the header row

            data = []
            for row in reader:
                try:
                    product = row["product"].strip().lower()  
                    amount = float(row["amount"].strip()) if row["amount"].strip() else 0  # Convert amount to float
                except ValueError:
                    amount = 0  # Default to 0 if conversion fails
                
                data.append({"product": product, "amount": amount})

            print(f"CSV Data Extracted: {data}") 
            return data
    except Exception:
        raise ValueError("Input file not in CSV format.")

@app.route("/compute", methods=["POST"])
def compute():
    try:
      
        data = request.get_json()

       
        if data is None:
            print("No JSON body received!")
            return jsonify({"file": None, "error": "Missing JSON body.", "sum": 0}), 400
        
        if not isinstance(data, dict) or "file" not in data or "product" not in data:
            print("Invalid JSON structure!")
            return jsonify({"file": None, "error": "Invalid JSON input.", "sum": 0}), 400

        file_name = data["file"]
        product = data["product"].strip().lower()  # Normalize product name
        file_path = os.path.join(PERSISTENT_STORAGE, file_name)

        # Check if file exists
        if not os.path.isfile(file_path):
            print(f" File Not Found: {file_path}")
            return jsonify({"file": file_name, "error": "File not found.", "sum": 0}), 404

        try:
            csv_data = read_and_validate_csv(file_path)
        except ValueError as e:
            print(f" CSV Read Error: {e}")
            return jsonify({"file": file_name, "error": str(e), "sum": 0}), 400

        
        print(f"Extracted CSV Data: {csv_data}")

        
        total = sum(row["amount"] for row in csv_data if row["product"] == product)

        print(f" Computed Sum for {product}: {total}")  #  Debug Log

        return jsonify({"file": file_name, "sum": int(total)}), 200

    except Exception as e:
        print(f"Unexpected Error: {e}")  
        return jsonify({"file": None, "error": str(e), "sum": 0}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
