import requests
import psycopg2
from psycopg2 import sql

# ------------------- THÔNG TIN KẾT NỐI DATABASE -------------------
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'shopee_ratings'
DB_USER = 'postgres'
DB_PASSWORD = '123456'

TABLE_NAME = 'shopee_ratings'
# ------------------------------------------------------------------

url = "https://shopee.vn/api/v2/item/get_ratings?flag=1&limit=10&request_source=3&exclude_filter=1&fold_filter=0&relevant_reviews=false&itemid=29911154536&shopid=487028617&filter=0&inherit_only_view=false&fe_toggle=%5B2%2C3%5D&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1&offset=0"
headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "af-ac-enc-dat": "bfb584dd6a277ac2",
    "af-ac-enc-sz-token": "209DIKJ5DUilOuA6XJrxqA==|mvHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQyzAmzMhEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZnHj|E9S6bKuiBbShck7F|08|3",
    "content-type": "application/json",
    "referer": "https://shopee.vn/shop/487028617/item/29911154536/rating",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    "x-api-source": "rweb",
    "x-csrftoken": "oO4ZvdS1lhSae6iCm6hXnvyFJHm9Rfy8",
    "x-requested-with": "XMLHttpRequest",
    "x-sap-ri": "c4889368bcfdcf95bc60eb310701e00c68db0e112db994fdc414",
    "x-sap-sec": "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",
    "x-shopee-language": "vi",
    "x-sz-sdk-version": "1.12.21"
}


response = requests.get(url, headers=headers)
# ------------------------------------------------------

if response.status_code == 200:
    data = response.json()
    ratings = data.get("data", {}).get("ratings", [])

    # ------------------- KẾT NỐI DATABASE --------------
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

                # Tạo bảng nếu chưa có
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                orderid BIGINT,
                itemid BIGINT,
                cmtid BIGINT,
                ctime TIMESTAMP,
                rating INTEGER,
                rating_star INTEGER,
                userid BIGINT,
                shopid BIGINT,
                comment TEXT,
                status INTEGER,
                mtime TIMESTAMP
            )
        """).format(sql.Identifier(TABLE_NAME))

        cur.execute(create_table_query)
        conn.commit()

        # Insert dữ liệu
        insert_query = sql.SQL("""
            INSERT INTO {} (
                orderid, itemid, cmtid, ctime, rating,
                rating_star, userid, shopid, comment,
                status, mtime
            )
            VALUES (%s, %s, %s, to_timestamp(%s), %s,
                    %s, %s, %s, %s, %s, to_timestamp(%s))
        """).format(sql.Identifier(TABLE_NAME))

        for r in ratings:
            orderid = r.get("orderid", 0)
            itemid = r.get("itemid", None)
            cmtid = r.get("cmtid", None)
            ctime = r.get("ctime", None)
            rating = r.get("rating", None)
            rating_star = r.get("rating_star", None)
            userid = r.get("userid", None)
            shopid = r.get("shopid", None)
            comment = r.get("comment", "")
            status = r.get("status", None)
            mtime = r.get("mtime", None)

            cur.execute(insert_query, (
                orderid, itemid, cmtid, ctime, rating,
                rating_star, userid, shopid, comment,
                status, mtime
            ))

        conn.commit()
        print("Save successful: PostgreSQL.")

    except Exception as e:
        print("Error connecting to or writing data:", e)
    finally:
        if conn:
            cur.close()
            conn.close()
else:
    print("Error fetching data:", response.status_code)