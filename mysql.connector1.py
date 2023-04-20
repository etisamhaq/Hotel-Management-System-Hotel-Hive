from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)


conn = mysql.connector.connect(host="localhost", user="root", password="", database="hotel")

@app.route("/")
def dbms():
    return render_template("dbms.html")

@app.route("/rooms")
def rooms():
    # Read all rooms from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    

    # Render the room.html template with the rooms data
    return render_template("room.html", rooms=rooms)

@app.route("/employees") 
def employees():
    return render_template("employees.html")

@app.route("/payments")
def payments():
    return render_template("payments.html")

@app.route("/bookings")
def bookings():
    return render_template("bookings.html")

@app.route("/rooms_to_dbms")
def rooms_to_dbms():
    return redirect(url_for("dbms"))

@app.route("/rooms_to_employees")
def rooms_to_employees():
    return redirect(url_for("employees"))  

@app.route("/rooms_to_payments")
def rooms_to_payments():
    return redirect(url_for("payments"))    

@app.route("/rooms_to_bookings")
def rooms_to_bookings():
    return redirect(url_for("bookings"))
    

@app.route("/create", methods=["POST"])
def create():
    # Get the room details from the request
    id=request.form["id"]
    room_type = request.form["room_type"]
    room_number = request.form["room_number"]
    max_occupancy = request.form["max_occupancy"]
    price_per_night = request.form["price_per_night"]

    # Insert the new room into the database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rooms (id,room_type, room_number, max_occupancy, price_per_night) VALUES (%s,%s, %s, %s, %s)", (id,room_type, room_number, max_occupancy, price_per_night))
    conn.commit()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    
    # Render the room.html template with the rooms data and message
    output = "Room created successfully!<br><br>"
    for room in rooms:
        output += f"Room ID: {room[0]} Room Type: {room[1]} Room Number: {room[2]} Max Occupancy: {room[3]} Price Per Night: {room[4]}<br>"
    
    return output
    # return "Room created successfully!"

@app.route("/update", methods=["POST"])
def update():
    # Get the room details from the request
    room_id = request.form["update_id"]
    room_type = request.form["new_room_type"]
    room_number = request.form["new_room_number"]
    max_occupancy = request.form["new_max_occupancy"]
    price_per_night = request.form["new_price_per_night"]

    # Update the room in the database
    cursor = conn.cursor()
    cursor.execute("UPDATE rooms SET room_type=%s, room_number=%s, max_occupancy=%s, price_per_night=%s WHERE id=%s", (room_type, room_number, max_occupancy, price_per_night, room_id))
    conn.commit()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    
    # Render the room.html template with the rooms data and message
    output = "Room updated successfully!<br><br>"
    for room in rooms:
        output += f"Room ID: {room[0]} Room Type: {room[1]} Room Number: {room[2]} Max Occupancy: {room[3]} Price Per Night: {room[4]}<br>"
    
    return output

    # return "Room updated successfully!"

@app.route("/delete", methods=["POST"])
def delete():
    # Get the room ID from the request
    room_id = request.form["delete_id"]

    # Delete the room from the database
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE id=%s", (room_id,))
    conn.commit()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    
    # Render the room.html template with the rooms data and message
    output = "Room deleted successfully!<br><br>"
    for room in rooms:
        output += f"Room ID: {room[0]} Room Type: {room[1]} Room Number: {room[2]} Max Occupancy: {room[3]} Price Per Night: {room[4]}<br>"
    
    return output

    # return "Room deleted successfully!"


if __name__ == "__main__":
    app.run(debug=True)
