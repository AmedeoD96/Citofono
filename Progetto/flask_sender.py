from flask import Flask, send_file, abort

app = Flask(__name__)
app.config["CLIENT_IMAGES"] = "/Dataset"
@app.route("/", methods=['GET', 'POST'])
def index():
    return "Smart Ringbell"

@app.route("/get-image/<path:image_name>")
def get_image(image_name):
    try:
        return send_file("./Dataset/sconosciuto.jpg", as_attachment=False)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
