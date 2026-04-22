import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 데이터 저장용 (임시)
orders = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

@app.route('/api/order', methods=['POST'])
def create_order():
    data = request.json
    order = {
        "id": len(orders) + 1,
        "item": data.get('item'),
        "price": data.get('price'),
        "status": "대기중"
    }
    orders.append(order)
    return jsonify({"status": "success", "order": order})

@app.route('/api/accept/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    for order in orders:
        if order['id'] == order_id and order['status'] == "대기중":
            order['status'] = "배차완료"
            return jsonify({"status": "success"})
    return jsonify({"status": "fail", "message": "이미 배차되었거나 없는 오더입니다."})

if __name__ == '__main__':
    app.run(debug=True)
