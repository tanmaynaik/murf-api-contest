from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from murf import Murf

client = Murf(
    api_key="ap2_54e91e5e-8ac8-4d96-ab04-cdae5ff7a0f3",
)

def translate_text(text, target_lang):
    """
    Translate text using Murf API
    """
    try:
        response = client.text.translate(
            target_language=target_lang,
            texts=[text],
        )
        return response.translations[0].translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

app = Flask(__name__)
CORS(app)  # This allows your React app to communicate with Flask

# Original web interface route (keep existing)
@app.route('/')
def home_display():
    return render_template("index.html")

@app.route('/', methods=["POST"])
def submit():
    text = request.form.get('paragraph')
    locale = request.form.get('language')
    translated_text = translate_text(text, locale)
    return render_template("index.html", translated_text=translated_text)

# NEW API endpoint for your React frontend
@app.route('/api/translate', methods=["POST"])
def api_translate():
    """
    API endpoint for React frontend
    Expected JSON format: {
        "text": "Hello world",
        "targetLanguage": "es"
    }
    Returns: {
        "translatedText": "Hola mundo",
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided", "success": False}), 400
        
        text = data.get('text', '').strip()
        
        target_lang = data.get('targetLanguage', 'es')
        
        if not text:
            return jsonify({"error": "No text provided", "success": False}), 400
        
        # Map frontend language codes to Murf API language codes
        lang_mapping = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-BR',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'zh': 'zh-CN',
            'ar': 'ar-SA',
            'hi': 'hi-IN',
            'ta': 'ta-IN',
            'bn': 'bn-IN',
            'nl': 'nl-NL',
            'pl': 'pl-PL',
            'ru': 'ru-RU'
        }
        
        # Convert to Murf API format
        murf_target_lang = lang_mapping.get(target_lang, 'en-US')
        
        translated_text = translate_text(text, murf_target_lang)
        
        if translated_text:
            return jsonify({
                "translatedText": translated_text,
                "success": True,
                # "sourceLanguage": source_lang,
                "targetLanguage": target_lang
            })
        else:
            return jsonify({
                "error": "Translation service failed",
                "success": False
            }), 500
            
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

# Health check endpoint for testing connection
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Flask translation server is running",
        "version": "1.0"
    })

# Get available languages endpoint
@app.route('/api/languages', methods=['GET'])
def get_languages():
    languages = [
        {"code": "en", "name": "English", "flag": "🇺🇸"},
        {"code": "es", "name": "Spanish", "flag": "🇪🇸"},
        {"code": "fr", "name": "French", "flag": "🇫🇷"},
        {"code": "de", "name": "German", "flag": "🇩🇪"},
        {"code": "it", "name": "Italian", "flag": "🇮🇹"},
        {"code": "pt", "name": "Portuguese", "flag": "🇧🇷"},
        {"code": "ja", "name": "Japanese", "flag": "🇯🇵"},
        {"code": "ko", "name": "Korean", "flag": "🇰🇷"},
        {"code": "zh", "name": "Chinese", "flag": "🇨🇳"},
        {"code": "ar", "name": "Arabic", "flag": "🇸🇦"},
        {"code": "hi", "name": "Hindi", "flag": "🇮🇳"},
        {"code": "ta", "name": "Tamil", "flag": "🇮🇳"},
        {"code": "bn", "name": "Bengali", "flag": "🇧🇩"},
        {"code": "nl", "name": "Dutch", "flag": "🇳🇱"},
        {"code": "pl", "name": "Polish", "flag": "🇵🇱"},
        {"code": "ru", "name": "Russian", "flag": "🇷🇺"}
    ]
    return jsonify({"languages": languages})

if __name__ == "__main__":
    print("Starting Flask Translation Server...")
    print("Backend will be available at: http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/translate")
    app.run(debug=True, host='0.0.0.0', port=5000)