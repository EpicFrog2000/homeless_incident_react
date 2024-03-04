import psycopg2
import datetime

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="oto_dom_db",
    user="postgres",
    password="haslo123",
    host="127.0.0.1",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Get today's date
todays_date = datetime.datetime.now()
todays_date = str(todays_date.year) + "-" + str(todays_date.month)  + "-" + str(todays_date.day)

# Define functions for inserting data

def insert_data(oferta):
    sql = "INSERT INTO data (date, lokacja, cena, cena_m2, powierzchnia, liczba_pokoi, pietro, czynsz, forma_wlasnosci, stan_wykonczenia, balkon_ogrod_taras, miejsce_parkingowe, ogrzewanie, certyfikat_energetyczny, rynek, typ_ogloszeniodawcy, dostepne_od, rok_budowy, rodzaj_zabudowy, okna, winda, media, zabezpieczenia, wyposazenie, informacje_dodatkowe, material_budynku) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    values = (
        todays_date,
        oferta.lokacja,
        oferta.cena,
        oferta.cena_m2,
        oferta.powierzchnia,
        oferta.liczba_pokoi,
        oferta.pietro,
        oferta.czynsz,
        oferta.forma_wlasnosci,
        oferta.stan_wykonczenia,
        oferta.balkon_ogrod_taras,
        oferta.miejsce_parkingowe,
        oferta.ogrzewanie,
        oferta.certyfikat_energetyczny,
        oferta.rynek,
        oferta.typ_ogloszeniodawcy,
        oferta.dostepne_od,
        oferta.rok_budowy,
        oferta.rodzaj_zabudowy,
        oferta.okna,
        oferta.winda,
        oferta.media,
        oferta.zabezpieczenia,
        oferta.wyposazenie,
        oferta.informacje_dodatkowe,
        oferta.material_budynku,
    )

    # Execute the SQL query
    try:
        cur.execute(sql, values)
        conn.commit()
    except Exception as e:
        print("Error:", e)
    

def insert_historic_data():
    # Count num of numbers that day
    cur.execute("SELECT COUNT(date) AS count FROM data;")
    count_of_all_offers = cur.fetchone()
    val = (count_of_all_offers[0], todays_date)
    sql = "INSERT INTO historic_count (count, date) VALUES (%s, %s)"
    cur.execute(sql, val)
    conn.commit()

def close_connections():
    # Close the cursor and the connection when finished
    cur.close()
    conn.close()