from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>TEST</title></head>
    <body style="background:red; padding:50px;">
        <h1>✅ DIRECT HTML WORKING!</h1>
        <p>If you see RED background, Flask is working.</p>
        <p>Template me problem hai.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🔧 TEST: http://localhost:7000")
    app.run(port=7000, debug=True)
    # python test_simple.py