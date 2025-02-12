import requests
import mysql.connector
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nisha@21",
    database="web_scrp"
)
cursor = conn.cursor()
cursor.execute("create database if not exists web_scrp")
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    price VARCHAR(50)
)
""")
for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    cursor.execute("INSERT INTO books (title, price) VALUES (%s, %s)", (title, price))



# to fetch the book name and its price
cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()
for row in rows:
    print(row)  
# to see the tables
cursor.execute("show tables")
for i in cursor:
    print(i)
cursor.execute("desc books ")
for r in cursor:
    print(r)
# fetching only the book names
cursor.execute("SELECT title from books ")
rows = cursor.fetchall()
for n in rows:
    print(n)  
cursor.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INT AUTO_INCREMENT PRIMARY KEY,
        link VARCHAR(255)
    )
""")
links=soup.find_all("a")
for link in links:
    href=(link.get("href"))
    if href:  
        cursor.execute("INSERT INTO links (link) VALUES (%s)", (href,))

conn.commit()
cursor.close()
conn.close()

print("Data stored successfully!")
