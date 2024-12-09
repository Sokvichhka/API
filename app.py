from flask import Flask, jsonify, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database_st2_6.db'


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


@app.route('/products', methods=['GET'])
def get_products():
    # Query the product data
    products = query_db('SELECT * FROM product')

    # Structure data to include videos for each product
    product_list = []
    for product in products:
        product_id, title, author, video_count, image_url = product

        # Query videos for the current product
        videos = query_db('SELECT title, duration, videoUrl FROM video WHERE product_id = ?', [product_id])

        # Add product and its videos to the list
        product_list.append({
            "id": product_id,
            "title": title,
            "author": author,
            "videoCount": video_count,
            "imageUrl": image_url,
            "videos": [{"title": video[0], "duration": video[1], "videoUrl": video[2]} for video in videos]
        })

    return jsonify(product_list)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
