
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"

DATABASE = "users.db"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------- HTML TEMPLATE ----------------

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Digital Electronics Converter</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #080c14;
    --panel: #101827;
    --panel2: #141f31;
    --border: #25344b;
    --blue: #329bff;
    --blue2: #1675df;
    --text: #e8eef8;
    --muted: #91a0b6;
    --green: #32d6a0;
    --red: #ff6577;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}

button, input, select {
    font-family: inherit;
}

a {
    color: inherit;
    text-decoration: none;
}

/* AUTH PAGES */

.auth-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 25px;
    background:
        radial-gradient(ellipse at 50% 0%, #12335a 0%, transparent 50%),
        var(--bg);
}

.auth-card {
    width: 100%;
    max-width: 420px;
    padding: 38px;
    background: rgba(16, 24, 39, 0.96);
    border: 1px solid var(--border);
    border-radius: 15px;
    box-shadow: 0 20px 70px #0008;
}

.brand-icon {
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    background: #132b47;
    color: var(--blue);
    border: 1px solid #24578c;
    border-radius: 12px;
    font-size: 23px;
    margin-bottom: 22px;
}

.auth-card h1 {
    font-size: 25px;
    margin-bottom: 9px;
    letter-spacing: -0.7px;
}

.subtitle {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 28px;
}

.field {
    margin-bottom: 18px;
}

.field label {
    display: block;
    font-size: 12px;
    color: #b8c6d9;
    font-weight: 600;
    margin-bottom: 9px;
}

.field input {
    width: 100%;
    padding: 13px 14px;
    border: 1px solid var(--border);
    background: #0b1321;
    color: white;
    outline: none;
    border-radius: 8px;
    font-size: 13px;
    transition: 0.2s;
}

.field input:focus {
    border-color: var(--blue);
    box-shadow: 0 0 0 3px #329bff18;
}

.primary-btn {
    width: 100%;
    padding: 13px;
    background: var(--blue2);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
}

.primary-btn:hover {
    background: var(--blue);
    transform: translateY(-1px);
}

.auth-footer {
    text-align: center;
    margin-top: 24px;
    font-size: 12px;
    color: var(--muted);
}

.auth-footer a {
    color: var(--blue);
    font-weight: 600;
}

.flash {
    padding: 11px 13px;
    border-radius: 7px;
    margin-bottom: 16px;
    font-size: 12px;
    background: #351d29;
    color: #ff9eac;
    border: 1px solid #713143;
}

/* DASHBOARD */

.topbar {
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 6%;
    border-bottom: 1px solid var(--border);
    background: #0c1320;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 15px;
    font-weight: 700;
}

.logo-mark {
    height: 37px;
    width: 37px;
    border-radius: 9px;
    display: grid;
    place-items: center;
    background: #142e4c;
    border: 1px solid #24578c;
    color: var(--blue);
    font-size: 19px;
}

.logo small {
    display: block;
    font-size: 9px;
    color: var(--muted);
    font-weight: 500;
    letter-spacing: 1px;
    margin-top: 3px;
}

.top-right {
    display: flex;
    align-items: center;
    gap: 18px;
    font-size: 12px;
    color: var(--muted);
}

.logout {
    padding: 9px 14px;
    border: 1px solid var(--border);
    border-radius: 7px;
    color: #c5d2e4;
    transition: 0.2s;
}

.logout:hover {
    border-color: var(--blue);
    color: var(--blue);
}

.container {
    max-width: 1120px;
    margin: auto;
    padding: 48px 25px;
}

.heading {
    margin-bottom: 30px;
}

.heading .eyebrow {
    color: var(--blue);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.heading h1 {
    font-size: clamp(25px, 4vw, 34px);
    letter-spacing: -1.2px;
    margin-bottom: 10px;
}

.heading p {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.7;
}

.section-label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 32px 0 14px;
}

.cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 25px;
    min-width: 0;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 23px;
}

.card-icon {
    width: 39px;
    height: 39px;
    display: grid;
    place-items: center;
    color: var(--blue);
    background: #142c48;
    border: 1px solid #254e77;
    border-radius: 9px;
    font-size: 18px;
}

.card-header h2 {
    font-size: 15px;
    margin-bottom: 5px;
}

.card-header p {
    color: var(--muted);
    font-size: 11px;
}

.input-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 17px;
}

.input-group label {
    display: block;
    font-size: 11px;
    color: #aab9cc;
    font-weight: 600;
    margin-bottom: 9px;
}

.input-group input,
.input-group select {
    width: 100%;
    background: #0b1321;
    color: white;
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 12px;
    font-size: 14px;
    outline: none;
}

.input-group input:focus,
.input-group select:focus {
    border-color: var(--blue);
}

.action-btn {
    width: 100%;
    background: var(--blue2);
    color: white;
    border: 0;
    border-radius: 7px;
    padding: 12px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 700;
    margin-top: 5px;
    transition: 0.2s;
}

.action-btn:hover {
    background: var(--blue);
}

.result-box {
    margin-top: 20px;
    background: #0b1422;
    border: 1px solid #263d59;
    border-radius: 8px;
    padding: 17px;
    min-height: 85px;
}

.result-title {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 12px;
}

.result-value {
    color: var(--green);
    font-size: 23px;
    font-weight: 700;
    letter-spacing: 2px;
    overflow-wrap: anywhere;
}

.result-detail {
    color: var(--muted);
    font-size: 11px;
    margin-top: 9px;
    line-height: 1.6;
}

.status {
    color: var(--blue);
    font-size: 10px;
    font-weight: 600;
    margin-top: 13px;
}

.operations {
    margin-bottom: 17px;
}

.operations label {
    display: block;
    font-size: 11px;
    color: #aab9cc;
    margin-bottom: 9px;
    font-weight: 600;
}

.operations select {
    width: 100%;
    background: #0b1321;
    color: white;
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 12px;
    outline: none;
}

.info-strip {
    margin-top: 24px;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 16px 19px;
    background: #0d1624;
    color: var(--muted);
    font-size: 11px;
    line-height: 1.8;
}

.info-strip strong {
    color: #d9e5f4;
}

.footer {
    text-align: center;
    padding: 25px;
    border-top: 1px solid var(--border);
    color: #718198;
    font-size: 10px;
    letter-spacing: 0.5px;
}

@media(max-width: 700px) {
    .cards {
        grid-template-columns: 1fr;
    }

    .topbar {
        padding: 0 18px;
    }

    .top-right {
        gap: 8px;
    }

    .top-right span {
        display: none;
    }

    .container {
        padding: 35px 17px;
    }

    .card {
        padding: 20px;
    }

    .auth-card {
        padding: 27px;
    }
}
</style>
</head>

<body>

{% if page == 'auth' %}

<div class="auth-page">
    <div class="auth-card">

        <div class="brand-icon">⌘</div>

        <h1>{{ 'Create your account' if mode == 'register' else 'Welcome back' }}</h1>

        <p class="subtitle">
            Digital Electronics Converter<br>
            {{ 'Register to access digital logic tools.' if mode == 'register' else 'Sign in to continue to your workspace.' }}
        </p>

        {% with messages = get_flashed_messages() %}
        {% for message in messages %}
            <div class="flash">{{ message }}</div>
        {% endfor %}
        {% endwith %}

        <form method="POST">

            <div class="field">
                <label>Email Address</label>
                <input type="email" name="email" placeholder="Enter your email" required>
            </div>

            <div class="field">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter your password" required minlength="6">
            </div>

            <button class="primary-btn" type="submit">
                {{ 'Create Account' if mode == 'register' else 'Sign In' }}
            </button>

        </form>

        <div class="auth-footer">
            {% if mode == 'register' %}
                Already have an account?
                <a href="{{ url_for('login') }}">Sign in</a>
            {% else %}
                Don't have an account?
                <a href="{{ url_for('register') }}">Create account</a>
            {% endif %}
        </div>

    </div>
</div>

{% else %}

<header class="topbar">
    <div class="logo">
        <div class="logo-mark">⌘</div>
        <div>
            Digital Electronics Converter
            <small>DIGITAL LOGIC WORKSPACE</small>
        </div>
    </div>

    <div class="top-right">
        <span>{{ user }}</span>
        <a class="logout" href="{{ url_for('logout') }}">Sign Out</a>
    </div>
</header>

<main class="container">

    <section class="heading">
        <div class="eyebrow">ENGINEERING TOOLS / DIGITAL ELECTRONICS</div>
        <h1>Digital Logic Workspace</h1>
        <p>
            Perform binary arithmetic, logic operations and Gray code conversion
            using a simple digital electronics interface.
        </p>
    </section>

    <div class="section-label">AVAILABLE CONVERSION TOOLS</div>

    <section class="cards">

        <!-- BINARY CALCULATOR -->

        <div class="card">

            <div class="card-header">
                <div class="card-icon">01</div>
                <div>
                    <h2>4-Bit Binary Calculator</h2>
                    <p>Arithmetic and bitwise operations</p>
                </div>
            </div>

            <div class="input-grid">
                <div class="input-group">
                    <label>Binary Input A</label>
                    <input type="text" id="binA" maxlength="4"
                           placeholder="e.g. 1010">
                </div>

                <div class="input-group">
                    <label>Binary Input B</label>
                    <input type="text" id="binB" maxlength="4"
                           placeholder="e.g. 0011">
                </div>
            </div>

            <div class="operations">
                <label>Select Operation</label>
                <select id="operation">
                    <option value="add">Addition (A + B)</option>
                    <option value="sub">Subtraction (A - B)</option>
                    <option value="and">AND (A AND B)</option>
                    <option value="or">OR (A OR B)</option>
                    <option value="xor">XOR (A XOR B)</option>
                    <option value="notA">NOT A</option>
                    <option value="notB">NOT B</option>
                </select>
            </div>

            <button class="action-btn" onclick="calculate()">
                Calculate Result
            </button>

            <div class="result-box">
                <div class="result-title">BINARY OUTPUT</div>
                <div class="result-value" id="calcResult">----</div>
                <div class="result-detail" id="calcDetail">
                    Your result will appear here.
                </div>
            </div>

            <div class="status" id="calcStatus">READY FOR INPUT</div>

        </div>

        <!-- GRAY CODE CONVERTER -->

        <div class="card">

            <div class="card-header">
                <div class="card-icon">02</div>
                <div>
                    <h2>Binary to Gray Code</h2>
                    <p>Convert 4-bit binary into Gray code</p>
                </div>
            </div>

            <div class="input-group" style="margin-bottom:17px;">
                <label>4-Bit Binary Input</label>
                <input type="text" id="grayInput" maxlength="4"
                       placeholder="Enter binary e.g. 1011">
            </div>

            <button class="action-btn" onclick="convertGray()">
                Convert to Gray Code
            </button>

            <div class="result-box">
                <div class="result-title">GRAY CODE OUTPUT</div>
                <div class="result-value" id="grayResult">----</div>
                <div class="result-detail" id="grayDetail">
                    Converted Gray code will appear here.
                </div>
            </div>

            <div class="status" id="grayStatus">READY FOR INPUT</div>

        </div>

    </section>

    <div class="section-label">ABOUT THIS WORKSPACE</div>

    <div class="info-strip">
        <strong>Binary Calculator:</strong> Supports addition, subtraction,
        AND, OR, XOR and NOT operations on 4-bit binary inputs.
        <br>
        <strong>Gray Code Converter:</strong> Converts binary input into Gray
        code using XOR between adjacent binary bits.
        <br>
        <strong>Note:</strong> Calculator logic uses 4-bit output.
        Addition carry and subtraction borrow are displayed separately.
    </div>

</main>

<footer class="footer">
    DIGITAL ELECTRONICS CONVERTER &nbsp; | &nbsp; BINARY COMPUTATION SYSTEM
</footer>

<script>

function validBinary(value) {
    return /^[01]{4}$/.test(value);
}

function calculate() {

    let a = document.getElementById("binA").value.trim();
    let b = document.getElementById("binB").value.trim();
    let op = document.getElementById("operation").value;

    let result = document.getElementById("calcResult");
    let detail = document.getElementById("calcDetail");
    let status = document.getElementById("calcStatus");

    if (!validBinary(a)) {
        result.textContent = "ERROR";
        detail.textContent = "Input A must contain exactly 4 binary digits (0 or 1).";
        status.textContent = "INVALID INPUT";
        return;
    }

    if (op !== "notA" && op !== "notB" && !validBinary(b)) {
        result.textContent = "ERROR";
        detail.textContent = "Input B must contain exactly 4 binary digits (0 or 1).";
        status.textContent = "INVALID INPUT";
        return;
    }

    let A = parseInt(a, 2);
    let B = parseInt(b || "0000", 2);

    let output = 0;
    let extra = "";

    switch(op) {

        case "add":
            let sum = A + B;
            output = sum & 15;
            extra = "Carry: " + (sum > 15 ? "1" : "0");
            break;

        case "sub":
            let difference = A - B;
            output = (difference + 16) & 15;
            extra = "Borrow: " + (difference < 0 ? "1" : "0");
            break;

        case "and":
            output = A & B;
            break;

        case "or":
            output = A | B;
            break;

        case "xor":
            output = A ^ B;
            break;

        case "notA":
            output = (~A) & 15;
            break;

        case "notB":
            output = (~B) & 15;
            break;
    }

    let binaryOutput = output.toString(2).padStart(4, "0");
    let decimalOutput = output.toString();

    result.textContent = binaryOutput;

    detail.textContent =
        "Decimal Output: " + decimalOutput +
        (extra ? " | " + extra : "");

    status.textContent = "CALCULATION COMPLETED";
}

function convertGray() {

    let binary = document.getElementById("grayInput").value.trim();

    let result = document.getElementById("grayResult");
    let detail = document.getElementById("grayDetail");
    let status = document.getElementById("grayStatus");

    if (!validBinary(binary)) {
        result.textContent = "ERROR";
        detail.textContent =
            "Enter exactly 4 binary digits containing only 0 and 1.";
        status.textContent = "INVALID INPUT";
        return;
    }

    let gray = binary[0];

    for (let i = 1; i < binary.length; i++) {
        let bit = Number(binary[i - 1]) ^ Number(binary[i]);
        gray += bit.toString();
    }

    result.textContent = gray;

    detail.textContent =
        "Binary Input: " + binary +
        " | Decimal Value: " + parseInt(binary, 2);

    status.textContent = "CONVERSION COMPLETED";
}

</script>

{% endif %}

</body>
</html>
"""


# ---------------- AUTHENTICATION ----------------

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        HTML,
        page="dashboard",
        user=session["user"]
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter email and password.")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must contain at least 6 characters.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )
            conn.commit()
            conn.close()

            flash("Account created successfully. Please sign in.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            conn.close()
            flash("This email is already registered.")
            return redirect(url_for("register"))

    return render_template_string(
        HTML,
        page="auth",
        mode="register"
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user"] = user["email"]

            return redirect(url_for("home"))

        flash("Incorrect email or password.")
        return redirect(url_for("login"))

    return render_template_string(
        HTML,
        page="auth",
        mode="login"
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)
