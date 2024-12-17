from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os
import re

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    try:
        # Save the uploaded image
        image_path = os.path.join('/tmp', image_file.filename)
        image_file.save(image_path)

        # Process with Tesseract
        text = pytesseract.image_to_string(Image.open(image_path))

        # Clean up
        os.remove(image_path)

        if "CARTE D'ETUDIANT" not in text:
            return {"error": "This is not a valid student card."}
        
        lines = text.split("\n")

        annee = None
        nom_etudiant = None
        niveau = None

        for i,line in enumerate(lines):
            line = line.strip() 
            year_match = re.search(r"(\d{4}-\d{4})", line)
            if year_match:
                annee = year_match.group(1)
            if re.match(r"\b(?!CARTE\b(\sD'ETUDIANT\b)?)[A-Z]{4,15}\b(?:\s[A-Z]{4,15}\b){1}$", line):
                nom_etudiant = line.strip()
            if re.search(r"\d+eme\s[A-Za-zéÉ]+", line):
                niveau = line.strip()
            else:
                if(re.search(r"(\d+){1}$", line)):
                    niveau = line.strip()


        return {
            "is_student_card": True,
            "annee_unv": annee,
            "nom_etudiant": nom_etudiant,
            "niveau": niveau,
            "text":text
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
