from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# MySQL database configuration


@app.route('/loginMed', methods=['POST'])
def loginMed():
    conn = None
    cursor = None
    try:
        data = request.get_json()
        mail = data.get('mail')
        pwd = data.get('pwd')
        
        # Corrected the variable names to match with 'mail' and 'pwd'
        if not mail or not pwd:
            return jsonify({'success': False, 'msg': 'Missing email or password'})
        
        # Establish MySQL connection
        conn = mysql.connector.connect(
            host='mysql.railway.internal',
            user='root',
            password='waNRyNtpGEtXaaqQiDPCuACUAPhsFLZS',
            database='railway',
            port=3306
        )
        cursor = conn.cursor()
        
        # Query to check if user exists and password matches
        query_all = "SELECT * FROM docteur WHERE mail = %s AND pwd = %s"
        cursor.execute(query_all, (mail, pwd))
        user = cursor.fetchone()
        
        if user:
            return jsonify({'success': True ,'msg': 'Let him in'})
        else:
            # Check if the email exists for wrong password case
            query_mail = "SELECT * FROM docteur WHERE mail = %s"
            cursor.execute(query_mail, (mail,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return jsonify({'success':False ,'msg': 'Wrong password'})
            else:
                return jsonify({'success':False ,'msg': 'User not found'})
    except mysql.connector.Error as err:
        return jsonify({'success':False ,'msg': str(err)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
