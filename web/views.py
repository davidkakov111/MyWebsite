from django.shortcuts import render
import hashlib
import sqlite3
import psycopg2

def homepage(request):
    return render(request, 'index.html')

def game(request):
    return render(request, 'game.html')

def aboutme(request):
    return render(request, 'aboutme.html')

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("pasword")
        if password != password1:
            return render(request, "invalidpassword.html")
        def hashing(text):
            text_bytes = text.encode('utf-8')
            sha256_hash = hashlib.sha256()
            sha256_hash.update(text_bytes)
            hashed_text = sha256_hash.hexdigest()
            return hashed_text
        pasword = hashing(password)
        con = psycopg2.connect(
        database="verceldb",
        user="default",
        password="VfMnaTRB5Lg2",
        host="ep-broken-disk-55251045-pooler.us-east-1.postgres.vercel-storage.com",
        port="5432"
        )
        curs = con.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password Text)")
        curs.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = curs.fetchone()
        if existing_user:
            con.close()
            return render(request, "existingaccount.html")
        else:
            curs.execute("INSERT INTO users VALUES (%s, %s)", (email, pasword))
            curs.execute("SELECT * FROM users")
            curs.fetchall()
            con.commit()
            return render(request, "successfulsignup.html")
    
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        def hasheles(text):
            text_bytes = text.encode('utf-8')
            sha256_hash = hashlib.sha256()
            sha256_hash.update(text_bytes)
            hashed_text = sha256_hash.hexdigest()
            return hashed_text
        pasword = hasheles(password)
        con = psycopg2.connect(
        database="verceldb",
        user="default",
        password="VfMnaTRB5Lg2",
        host="ep-broken-disk-55251045-pooler.us-east-1.postgres.vercel-storage.com",
        port="5432"
        )
        curs = con.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password Text)")
        curs.execute("SELECT * FROM users")
        datas = curs.fetchall()
        c = (email, pasword)
        successful_login = False
        for i in datas:
            if i == c:
                successful_login = True
                break
        con.close()
        if successful_login:
            return render(request, "successfullogin.html")
        else:
            return render(request, "unsuccessfullogin.html")
        