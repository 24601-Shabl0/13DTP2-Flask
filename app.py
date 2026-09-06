from flask import Flask, g, render_template
import sqlite3 

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.context_processor
def inject_brands():
    brands = query_db("""
        SELECT DISTINCT Name
        FROM Makers
        ORDER BY Name;
    """)
    return {"nav_brands": brands}


@app.route('/')
def home():
    #home page- just the ID, maker, model, and image URL
    sql = """
              SELECT cars.carid,Makers.Name,cars.model,cars.imageURL 
              FROM cars 
              JOIN Makers ON cars.MakerID = Makers.MakerID;"""
    results = query_db(sql)
    return render_template("home.html" ,results=results)

@app.route("/car/<int:id>")
def car(id):    
    #just one car based on the id
    sql = """ SELECT * FROM cars 
    JOIN Makers ON Makers.MakerID=cars.MakerID
    WHERE cars.carid = ?;"""
    result = query_db(sql, (id,),True)
    return render_template("car.html", car=result)

# ...existing code...

@app.route("/brands")
def brands():
    sql = """
        SELECT DISTINCT Makers.Name
        FROM Makers
        JOIN cars ON cars.MakerID = Makers.MakerID
        ORDER BY Makers.Name;
    """
    results = query_db(sql)
    return render_template("brands.html", brands=results)


@app.route("/brand/<brand_name>")
def brand_cars(brand_name):
    sql = """
        SELECT cars.carid, Makers.Name, cars.model, cars.imageURL
        FROM cars
        JOIN Makers ON cars.MakerID = Makers.MakerID
        WHERE LOWER(Makers.Name) = LOWER(?)
        ORDER BY cars.model;
    """
    results = query_db(sql, (brand_name,))
    return render_template(
        "brand_cars.html",
        results=results,
        brand=brand_name
    )

# ...existing code...

if __name__ == "__main__":
    app.run(debug=True)