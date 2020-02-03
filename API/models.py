import mysql.connector

db = mysql.connector.connect(
    host="users.crtr8lbckqeg.us-east-2.rds.amazonaws.com",
    user="admin",
    passwd="8taUXlzixzlhQnbSPtuw",
    database="users"
)
"""
TABLES: 
listings - listing_id, listing_name, listing_desc
"""
cur = db.cursor(buffered=True)


def add_update(listing_id, listing_name, listing_desc):
    stmt = f'SELECT COUNT(listing_id) FROM ' \
           f'listings WHERE listing_id = {listing_id}'
    cur.execute(stmt)
    result = cur.fetchone()
    if result[0] == 0:
        # Add User
        stmt = f'INSERT INTO listings (listing_id, listing_name, ' \
               f'listing_desc) VALUES ("{listing_id}", "{listing_name}", ' \
               f'"{listing_desc}")'
        cur.execute(stmt)
        db.commit()
        stmt = f'SELECT * FROM listings WHERE listing_id = {listing_id}'
        cur.execute(stmt)
        return 'Successfully added user'
    else:
        stmt = "UPDATE listings SET listing_name = %s, listing_desc = %s " \
               "WHERE listing_id = %s"
        val = (listing_name, listing_desc, listing_id)
        cur.execute(stmt, val)
        db.commit()
        return 'Successfully updated user'


def get_listing(listing_id):
    stmt = f'SELECT * FROM listings WHERE listing_id = "{listing_id}"'
    cur.execute(stmt)
    if cur.rowcount != 0:
        return cur.fetchone()
    else:
        raise  Exception
        return e


class Listing:
    def __init__(self, listing_id, listing_name, listing_desc):
        self.listing_id = listing_id
        self.listing_name = listing_name
        self.listing_desc = listing_desc
