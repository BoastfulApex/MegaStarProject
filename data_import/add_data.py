import psycopg2
import requests
import uuid
import datetime
import calendar
import random
import json
from datetime import timedelta

from .get_data import categories, sub_categories, manufacturers, clients, items, invoices, get_session_id, get_objects
from .db_get_id import *

load_dotenv()


def generateOTP():
    return random.randint(111111, 999999)


DB_USERNAME = os.getenv('DB_USERNAME', None)
DB_PASS = os.getenv('DB_PASS', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)


def check_user_sale(user_id):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    # Retrieve all active sales for the user
    cur = conn.cursor()
    cur.execute("SELECT s.id, s.name, s.product_id, s.expiration_date, s.required_quantity, s.gift_product_id, "
                "s.gift_quantity, s.active, s.orders, us.order_quantity, us.is_full FROM main_sale s "
                "JOIN main_usersale us ON s.id = us.sale_id WHERE us.user_id = %s AND s.active = True", (user_id,))
    rows = cur.fetchall()

    # Add 1 to the order_quantity of each active sale for the user
    for row in rows:
        sale_id = row[0]
        order_quantity = row[9]
        cur.execute("UPDATE main_usersale SET order_quantity = %s WHERE user_id = %s AND sale_id = %s",
                    (order_quantity + 1, user_id, sale_id))

    conn.commit()
    cur.close()
    conn.close()


def add_cashback_to_user(order_id, conn, CardCode):
    cur = conn.cursor()
    user = get_user_by_cardcode(CardCode)

    cur.execute("SELECT summa, created_date FROM main_order WHERE id=%s", (order_id,))
    order = cur.fetchone()
    order_amount = order[0]
    order_datetime = order[1]
    cur.execute("SELECT * FROM main_usercashback WHERE user_id = %s AND expiration_date > %s AND active=True",
                (user[0], order_datetime,))
    user_cashbacks = cur.fetchall()

    if user[2] is not None and user[2] != 0:
        sale_cashback = user[2]
        sale_cashback_summa = user[3]
        new_sale_cashback_summa = sale_cashback_summa + order_amount * sale_cashback / 100
        cur.execute("UPDATE authentication_megauser SET sale_cashback_summa=%s WHERE id=%s",
                    (new_sale_cashback_summa,
                     user[0]))

    for user_cashback in user_cashbacks:
        user_cashback_id = user_cashback[0]
        user_cashback_summa = user_cashback[3]
        guid = str(uuid.uuid4())
        created_date = datetime.datetime.now()
        new_user_cashback_summa = user_cashback_summa + (order_amount * 0.01)
        cur.execute("UPDATE main_usercashback SET summa=%s WHERE id=%s", (new_user_cashback_summa, user_cashback_id))

        # add 1% of the order amount to the user's all_cashback field
        user_id = user[0]
        all_cashback = user[4]

        cashback_summa = order_amount * 0.01
        new_cashback_summa = all_cashback + cashback_summa
        cur.execute("UPDATE authentication_megauser SET all_cashback=%s WHERE id=%s", (new_cashback_summa,
                                                                                       user_id))
        cur.execute(
            "INSERT INTO main_usercashbackhistory (guid, user_id, created_date, summa) VALUES (%s, %s, %s) RETURNING id",
            [guid, user_id, created_date, cashback_summa])
    conn.commit()


def add_category(conn, groupname, number):
    cursor = conn.cursor()
    guid = str(uuid.uuid4())
    created_date = datetime.datetime.now()
    try:
        cursor.execute("SELECT * FROM main_category WHERE number = %s AND groupname = %s LIMIT 1", [number, groupname])
        row = cursor.fetchone()
    except:
        row = None
    if row is not None:
        return row
    else:
        cursor.execute(
            "INSERT INTO main_category (guid, number, groupname, created_date) VALUES (%s, %s, %s, %s) RETURNING id",
            [guid, number, groupname, created_date])
        new_row = cursor.fetchone()
        return new_row


def add_subcategory(conn, code, name, u_group):
    cursor = conn.cursor()
    guid = str(uuid.uuid4())
    created_date = datetime.datetime.now()
    cursor.execute("SELECT * FROM main_subcategory WHERE code = %s AND name = %s LIMIT 1", [code, name])
    row = cursor.fetchone()

    if row:
        return row
    else:
        cursor.execute(
            "INSERT INTO main_subcategory (guid, code, name, created_date, category_id) VALUES (%s, %s, %s, %s, "
            "%s) RETURNING id",
            [guid, code, name, created_date, str(get_category_by_number(u_group))])
        new_row = cursor.fetchone()
        return new_row


def add_manufacturer(conn, code, name):
    cursor = conn.cursor()
    guid = str(uuid.uuid4())
    created_date = datetime.datetime.now()
    cursor.execute("SELECT * FROM main_manufacturer WHERE code = %s AND manufacturer_name = %s LIMIT 1", [code, name])
    row = cursor.fetchone()

    if row:
        return row
    else:
        cursor.execute(
            "INSERT INTO main_manufacturer (guid, code, manufacturer_name, created_date) VALUES (%s, %s, %s, "
            "%s) RETURNING id",
            [guid, code, name, created_date])
        new_row = cursor.fetchone()
        return new_row


def add_client(conn, cardcode, cardname, phone):
    cursor = conn.cursor()
    created_date = datetime.datetime.now()
    if phone:
        phone = phone[1:]
        cursor.execute("SELECT * FROM authentication_megauser WHERE phone = %s LIMIT 1", [phone])
        row = cursor.fetchone()

        if row:
            return row
        else:
            otp = generateOTP()
            cursor.execute(
                "INSERT INTO authentication_megauser (phone, password, is_superuser, date_joined, is_staff, "
                "is_active, card_code, card_name, otp, all_cashback, sale_cashback, sale_cashback_summa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                [phone, otp, False, created_date, False, True, cardcode, cardname, otp, 0, 0, 0])
            new_row = cursor.fetchone()
            return new_row
    else:
        pass


def add_item(conn, itemcode, itemname, category, sub_category, manufacturer, price):
    cursor = conn.cursor()
    created_date = datetime.datetime.now()
    cursor.execute("SELECT * FROM main_product WHERE itemcode = %s LIMIT 1", [itemcode])
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE main_product SET price=%s WHERE itemcode=%s", (float(price), itemcode))
        return row
    else:
        guid = str(uuid.uuid4())
        if sub_category != "None":
            cursor.execute(
                "INSERT INTO main_product (guid, created_date, itemcode, itemname, category_id, sub_category_id, "
                "manufacturer_id, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                [guid, created_date, itemcode, itemname, get_category_by_number(category),
                 get_subcategory_by_code(sub_category), get_manufacturer_by_code(manufacturer), 0])
            new_row = cursor.fetchone()
            return new_row
        else:
            cursor.execute(
                "INSERT INTO main_product (guid, created_date, itemcode, itemname, category_id, manufacturer_id, "
                "price) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                [guid, created_date, itemcode, itemname, get_category_by_number(category),
                 get_manufacturer_by_code(manufacturer), 0])
            new_row = cursor.fetchone()
            return new_row


def add_order_detail(conn, order_id, ItemCode, count, U_priceUZS, Price):
    cursor = conn.cursor()
    product_id = get_item_by_itemcode(ItemCode)
    if product_id is not None:
        cursor.execute("SELECT * FROM main_orderdetail WHERE order_id = %s and product_id = %s LIMIT 1",
                       [order_id, product_id])
        row = cursor.fetchone()
        if row is not None:
            return row
        else:
            cursor.execute("INSERT INTO main_orderdetail (order_id, product_id, count, total, total_uzs) VALUES (%s, "
                           "%s, %s, %s, %s) RETURNING id", [order_id, product_id, count, Price, U_priceUZS])
            new_row = cursor.fetchone()
            return new_row


def add_order(conn, DocEntry, DocNum, CardCode, DocTotal, DocDate, U_sumUZS):
    cursor = conn.cursor()
    user = get_user_by_cardcode(CardCode)
    if user is not None:
        cursor.execute("SELECT * FROM main_order WHERE doc_entry = %s AND doc_num = %s LIMIT 1", [DocEntry, DocNum])
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            guid = str(uuid.uuid4())
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            created_date = datetime.datetime.strptime(DocDate, date_format)
            cursor.execute("INSERT INTO main_order (guid, created_date, user_id, doc_entry, doc_num, summa, "
                           "u_sumuzs, is_sale) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                           [guid, created_date,
                            user[0], DocEntry, DocNum,
                            DocTotal, U_sumUZS, False])
            new_row = cursor.fetchone()
            if user[1]:
                check_user_sale(user[0])
            else:
                add_cashback_to_user(new_row[0], conn, CardCode)
            return new_row[0]
    else:
        return None


def add_postgres_invoices():
    session = get_session_id()
    url = ("Invoices?$select=DocEntry,DocNum,DocDate,DocDueDate,CardCode,CardName,"
           "DocTotal,U_sumUZS,DiscountPercent,DocumentLines$filter=CardCode eq 'FIZ0006670'")
    i = 1
    url = "Invoices?$filter=CardCode eq 'FIZ006670'"
    while True:
        # current_time = datetime.datetime.now()
        # two_minutes_ago = current_time - timedelta(minutes=1)
        # if current_time.minute == 0:
        #     two_minutes_ago = datetime.datetime.now()
        #
        # today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # current_time_formatted = current_time.strftime("%H:%M:%S")
        # two_minutes_ago_formatted = two_minutes_ago.strftime("%H:%M:%S")
        # url += (f",UpdateDate,UpdateTime&$orderby=UpdateDate,UpdateTime&$filter=(UpdateDate ge '{today_date}' and "
        #         f"UpdateTime ge '{current_time_formatted}') and (UpdateDate le '{today_date}' and UpdateTime le "
        #         f"'{two_minutes_ago_formatted}') and Cancelled eq 'tNO'")
        i += 1
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASS
        )
        results = []
        items = get_objects(url=url, session=session)
        results += [item for item in items['value']]
        for data in results:
            order = add_order(conn=conn,
                              DocEntry=str(data['DocEntry']),
                              CardCode=str(data['CardCode']),
                              DocNum=str(data['DocNum']),
                              DocTotal=data['DocTotal'],
                              DocDate=str(data['DocDate']),
                              U_sumUZS=data['U_sumUZS'])
            if order is not None:
                print("Order: ", order)
                details = data['DocumentLines']
                for detail in details:
                    add_order_detail(
                        conn=conn,
                        order_id=str(order),
                        Price=detail['Price'],
                        count=detail['Quantity'],
                        U_priceUZS=detail['U_priceUZS'],
                        ItemCode=detail['ItemCode']
                    )
        conn.commit()
        conn.close()
        if '@odata.nextLink' in items:
            url = items['@odata.nextLink']
        else:
            break


def add_postgres_category():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    json_data = categories()

    for data in json_data:
        category = add_category(
            conn=conn,
            groupname=str(data['GroupName']),
            number=str(data['Number'])
        )
        # print("Category", category[0])
    conn.commit()
    conn.close()


def add_postgres_users():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    json_data = clients()

    for data in json_data:
        if data['Phone1'] is not None:
            client = add_client(
                conn=conn,
                phone=data['Phone1'][0:],
                cardcode=data['CardCode'],
                cardname=data['CardName']
            )
            # print(client[0])
    conn.commit()
    conn.close()


def add_postgres_subcategory():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    json_data = sub_categories()

    for data in json_data:
        category = add_subcategory(
            conn=conn,
            code=str(data['Code']),
            name=str(data['Name']),
            u_group=str(data['U_group'])
        )
        # print("SubCategory", category[0])
    conn.commit()
    conn.close()


def add_postgres_manufacturer():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    json_data = manufacturers()

    for data in json_data:
        man = add_manufacturer(
            conn=conn,
            code=str(data['Code']),
            name=str(data['ManufacturerName']),
        )
        # print("Manufacturer", man[0])
    conn.commit()
    conn.close()


def add_postgres_item():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASS
    )

    json_data = items()

    for data in json_data:
        price = 0
        try:
            price = float(data['ItemPrices'][0]['Price'])
        except Exception as exx:
            price = 0
        item = add_item(
            conn=conn,
            itemcode=str(data['ItemCode']),
            itemname=str(data['ItemName']),
            category=str(data['ItemsGroupCode']),
            manufacturer=str(data['Manufacturer']),
            sub_category=str(data['U_Subgroup']),
            price=price
        )
        print("Product", item[0])
    conn.commit()
    conn.close()


def check_sale_cashback():
    current_date = datetime.date.today()

    last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]

    if current_date.day == last_day_of_month:
        url = f'https://arzon.maxone.uz/api/check_last_month_sale/'

        response = requests.request("GET", url)
        response_data = response.json()
        return response_data
    else:
        pass
