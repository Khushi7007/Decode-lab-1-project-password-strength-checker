from flask import Flask, render_template, request
import re
import math

app = Flask(__name__)


def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"\d", password):
        charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

def check_password(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    entropy = calculate_entropy(password)

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, entropy

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    entropy = None

    if request.method == "POST":
        password = request.form["password"]
        result, entropy = check_password(password)

    return render_template(
        "index.html",
        result=result,
        entropy=entropy
    )

if __name__ == "__main__":
    app.run(debug=True,port=5002)
    