from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_sci_md")
except OSError:
    nlp = spacy.load("en_core_web_sm")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model": nlp.meta["name"]})

@app.route('/extract', methods=['POST'])
def extract_keywords():
    data = request.get_json()
    text = data.get('text', '')
    
    doc = nlp(text)
    # scispaCy extracts general biomedical entities without specific types
    keywords = [ent.text.strip() for ent in doc.ents if len(ent.text.strip()) > 2]
    
    return jsonify({"keywords": keywords})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)