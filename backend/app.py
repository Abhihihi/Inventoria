from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS,cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password@1'
app.config['MYSQL_DB'] = 'inventoria_db'

mysql = MySQL(app)


@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        return '',204

@app.route('/api/register', methods=['POST'])
@cross_origin(supports_credentials=True)
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password)
    print("Hashed pwd is: ",hashed_password)
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User registered successfully'})
        # response= jsonify({'message': 'User registered successfully'})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # return response

    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    print("Data is: ",data)
    username = data.get('username')
    password = data.get('password')

    # print("Username is: ",username)
    # print("Pass is: ",password)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    # cursor.execute("SELECT * FROM users")
    user = cursor.fetchone()
    # print("User is",user[3])
    cursor.close()
    # print("Check password value is:",check_password_hash(user[3], password))
    if user and check_password_hash(user[3], password) :
        return jsonify({'message': 'Login successful', 'user': {'id': user[0], 'username': user[1], 'email': user[2]}}), 200
    else:
        # print("check password: ",check_password_hash(user[3],password))
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/api/dashboard')
def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM products WHERE stock = 0')
    out_of_stock = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM products WHERE stock < 10 AND stock > 0')
    low_stock = cursor.fetchone()[0]

    cursor.execute('SELECT id, name, stock, price FROM products ORDER BY stock')
    products = cursor.fetchall()
    products_list = [{'id': row[0], 'name': row[1], 'stock': row[2], 'price': row[3]} for row in products]

    cursor.close()

    return jsonify({
        'totalProducts': total_products,
        'outOfStock': out_of_stock,
        'lowStock': low_stock,
        'products': products_list
    })


@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    stock = data['stock']
    price = data['price']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO products (name, stock, price) VALUES (%s, %s, %s)', (name, stock, price))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    name = data['name']
    stock = data['stock']
    price = data['price']

    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE products SET name=%s, stock=%s, price=%s WHERE id=%s', (name, stock, price, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Product updated successfully'})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM products WHERE id=%s', (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
