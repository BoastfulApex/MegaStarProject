import psycopg2
import os 

from dotenv import load_dotenv

from .get_data import categories


load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME' , None)
DB_PASS     = os.getenv('DB_PASS'     , None)
DB_HOST     = os.getenv('DB_HOST'     , None)
DB_PORT     = os.getenv('DB_PORT'     , None)
DB_NAME     = os.getenv('DB_NAME'     , None)



def get_category_by_number(number):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main_category WHERE number = %s", (f'{number}',))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row[0]


def get_subcategory_by_code(code):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main_subcategory WHERE code = %s", (f'{code}',))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row[0]


def get_manufacturer_by_code(code):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main_manufacturer WHERE code = %s", (f'{code}',))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row[0]


def get_user_by_cardcode(code):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, is_sale, sale_cashback, sale_cashback_summa, all_cashback FROM authentication_megauser WHERE card_code = '{code}';")
    row = cursor.fetchone()
    if row is not None:
        return row
    else:
        print("User None")
        return None


def get_order_by_docentry(docentry):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )
    print(docentry)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM main_order WHERE doc_entry = %s", (f'{docentry}',))
    row = cursor.fetchone()
    if row is not None:
        return row[0]
    else:
        return None


def get_item_by_itemcode(itemcode):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT id FROM main_product WHERE itemcode = %s", (f'{itemcode}', ))
    row = cursor.fetchone()
    if row is not None:
        return row[0]
    else:
        return None
