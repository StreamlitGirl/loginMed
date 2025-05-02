from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)



@app.route('/add_Medecin', methods=['POST'])
def add_medecin():
    conn = None
    cursor = None
    try:
        # Get JSON data from Flutter request
        data = request.get_json()
        mail = data.get('mail')
        pwd = data.get('pwd')
        localisation = data.get('localisation')
        name = data.get('name')
        spc = data.get('specialite')

        if not mail or not pwd:
            return jsonify({'error': 'Missing mail or pwd'}), 400
            
        if not localisation :
            return jsonify({'error': 'Missing location'}), 400
                    
        if not spc :
              return jsonify({'error': 'Missing speciality'}), 400
        if not name :
            return jsonify({'error': 'Missing name'}), 400
                                  




        # Connect to the database
        conn = mysql.connector.connect(
    host='gondola.proxy.rlwy.net',
    user='root',
    password='waNRyNtpGEtXaaqQiDPCuACUAPhsFLZS
',
    database='railway',
    port=22663
)
        cursor = conn.cursor()

        # Check if the user already exists
        query_check = "SELECT * FROM docteur WHERE mail = %s"
        cursor.execute(query_check, (mail,))
        existing_user = cursor.fetchone()  # Fetch one row

        if existing_user:
            return jsonify({'message' : 'User already exists'}), 400
            

        else:
            
            query_insert = "INSERT INTO docteur (mail, pwd, location, name, speciality) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(query_insert, (mail, pwd, localisation, name, spc))
            conn.commit()

        
        return jsonify({'message': 'User added successfully'}), 201
        

     
        

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
