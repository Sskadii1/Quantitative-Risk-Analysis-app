from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Hàm kết nối và lấy dữ liệu từ database SQLite
def get_db_connection():
    conn = sqlite3.connect('assets_risks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input', methods=['POST'])
def input_data():
    # Nhận dữ liệu từ form
    asset = request.form['asset']
    risk = request.form['risk']
    asset_value = float(request.form['asset_value'])
    ef = float(request.form['ef'])
    sle = float(request.form['sle'])
    aro = float(request.form['aro'])
    loss_value = float(request.form['loss_value'])
    safeguard = request.form['safeguard']
    safeguard_cost = float(request.form['safeguard_cost'])
    ef_after_safeguard = float(request.form['ef_after_safeguard'])

    # Lưu dữ liệu vào database
    conn = get_db_connection()
    conn.execute('INSERT INTO assets (asset, risk, asset_value, ef, sle, aro, loss_value, safeguard, safeguard_cost, ef_after_safeguard) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (asset, risk, asset_value, ef, sle, aro, loss_value, safeguard, safeguard_cost, ef_after_safeguard))
    conn.commit()
    conn.close()

    return "Data submitted successfully!"

@app.route('/show')
def show_data():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM assets').fetchall()
    conn.close()
    return render_template('show.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
