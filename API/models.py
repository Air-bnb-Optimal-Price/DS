import mysql.connector
from decouple import config

db = mysql.connector.connect(
    host=config('host'),
    user=config('user'),
    passwd=config('password'),
    database=config('database')
)
"""
TABLES: 
listings - id, prediction
"""
cur = db.cursor(buffered=True)


def add_update(id, prediction):
    stmt = f'SELECT COUNT(id) FROM listings WHERE id = {id}'
    cur.execute(stmt)
    result = cur.fetchone()
    if result[0] == 0:
        # TODO Predict then add to DB
        stmt = f'INSERT INTO listings (id, prediction)' \
               f'VALUES ("{id}", "{prediction}")'
        cur.execute(stmt)
        db.commit()
    else:
        # TODO Override previous prediction
        stmt = "UPDATE listings SET prediction = %s WHERE id = %s"
        val = (prediction, id)
        cur.execute(stmt, val)
        db.commit()


def predict(id, summary, superhost, lat, lng, prop_type, room_type, accom,
            baths, bedrooms, beds, deposit, cleaning, extra_ppl, min_nights,
            cancel, model):
    model.compile(loss='mean_squared_error',
                  optimizer='sgd',
                  metrics=['mae', 'accuracy'])
    prediction = model.predict(
        [[beds, min_nights, lat, lng, accom, baths, bedrooms, extra_ppl,
          cleaning, deposit, superhost, prop_type, room_type, cancel]])
    add_update(id, prediction[0][0])
    return get_listing(id)


def get_listing(id):
    stmt = f'SELECT * FROM listings WHERE id = "{id}"'
    cur.execute(stmt)
    if cur.rowcount != 0:
        return cur.fetchone()
    else:
        raise Exception
        return e
