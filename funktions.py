import datetime      # Modul för datum och tid, ex.hämta dagens datum eller räkna fram framtida dagar.
import json          # Modul för att läsa och skriva data i JSON-format, ex.spara bokningar i en fil.
import smtplib       # Modul för att skicka e‑post via SMTP-server (ex. Gmail).
import ssl           # Modul för att skapa en krypterad (TLS/SSL) anslutning när e‑post skickas.
from email.message import EmailMessage  # Klass för att bygga upp själva e‑postmeddelandet (ämne, avsändare, text osv.).

# Svenska datumnamn
SVENSKA_MONTHS = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni',
                  'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']

SVENSKA_WEEKDAYS = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag']

# Definierar fasta tillgängliga tider
AVAILABLE_TIMES = ["07:00", "12:00", "17:00"]

# Visar meny med 3 alternativ och returnerar användarens val som sträng
def show_menu():
    print("\nVälj ett alternativ:")
    print("1. Boka tid")
    print("2. Avboka tid")
    print("3. Avsluta")
    return input("Ange ditt val (1-3): ")

# Genererar lista med nästa 15 dagar (ex. September 29, fredag)
def get_next_15_days():
    today = datetime.date.today()
    days = []
    for i in range(15):
        d = today + datetime.timedelta(days=i)
        # ensure we have a date object
        if isinstance(d, datetime.datetime):
            d = d.date()
        month_idx = d.month - 1
        weekday_idx = d.weekday()
        month_name = SVENSKA_MONTHS[month_idx] if 0 <= month_idx < len(SVENSKA_MONTHS) else d.strftime("%B")
        weekday_name = SVENSKA_WEEKDAYS[weekday_idx] if 0 <= weekday_idx < len(SVENSKA_WEEKDAYS) else d.strftime("%A")
        days.append(f"{month_name} {d.day}, {weekday_name}")
    return days

# Hanterar datumval med bekräftelse (J/N), returnerar valt datum eller None
def choose_date():
    days = get_next_15_days()
    print("\nVälj ett datum:")
    for idx, text in enumerate(days, 1):
        print(f"{idx}. {text}")
    while True:
        val = input("Ange nummer för datum (1-15): ")
        if val.isdigit() and 1 <= int(val) <= 15:
            index = int(val)-1
            chosen = days[index]
            confirm = input(
                f"Du har valt \"{chosen}\"\n"
                "Tryck J för att boka\n"
                "Tryck N för att avbryta\n"
            ).lower()
            if confirm == "j":
                print(f"Bokningen bekräftad för {chosen}")
                return chosen
            else:
                print("Bokning avbruten.")
                return None
        else:
            print("Ogiltigt val, försök igen.")

# Filtrerar tillgängliga tider baserat på befintliga bokningar för specifikt datum
def get_available_times(bookings, date):
    booked = bookings.get(date, [])
    return [t for t in AVAILABLE_TIMES if t not in booked]

# Visar och hanterar tidsval bland lediga tider med bekräftelse (J/N) returnerar tid eller None
def choose_time(date, bookings):
    lediga = get_available_times(bookings, date)
    if not lediga:
        print("Alla tider är bokade för denna dag!")
        return None
    print("\nVälj en tid:")
    for idx, tid in enumerate(lediga, 1):
        print(f"{idx}. {tid}")
    while True:
        val = input(f"Ange nummer för tid (1-{len(lediga)}): ")
        if val.isdigit() and 1 <= int(val) <= len(lediga):
            chosen_time = lediga[int(val)-1]
            confirm = input(
                f"Du har valt {chosen_time}\n"
                "Tryck J för att bekräfta bokning\n"
                "Tryck N för att avbryta\n"
            ).lower()
            if confirm == "j":
                return chosen_time
            else:
                print("Avbrutet.")
                return None
        else:
            print("Ogiltigt val, försök igen.")

# Lägger till tid i boknings dict för datum, returnerar True om lyckad (ej dubblering)
def book_time(bookings, date, timeslot, user_email):
    if date not in bookings:
        bookings[date] = []
    if timeslot in bookings[date]:
        return False
    bookings[date].append(timeslot)
    print(f"Bokning lyckades för {user_email} den {date} kl {timeslot}")
    return True

# Tar bort tid från boknings dict, returnerar True om fanns och togs bort
def cancel_booking(bookings, date, timeslot):
    if date in bookings and timeslot in bookings[date]:
        bookings[date].remove(timeslot)
        print(f"Avbokning lyckades för {date} kl {timeslot}")
        return True
    else:
        print("Bokningen kunde inte hittas.")
        return False

# Kontrollerar om email finns i godkända set, returnerar bool
def is_email_approved(email, approved_set):
    return email in approved_set

# Laddar bokningar från JSON-fil, returnerar {} vid fel
def load_bookings(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Sparar boknings dict som JSON med UTF-8 och indent
def save_bookings(filename, bookings):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

# Skickar email via Gmail SMTP/TLS med UTF-8, returnerar True vid framgång
def send_gmx_email(sender_email, sender_password, receiver_email, subject, body):
    smtp_server = "smtp.gmail.com"
    port = 587  # TLS port

    msg = EmailMessage()
    msg['From'] = 'Booking System <get.tube.25@gmail.com>'
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)

    # Specificera att texten är UTF-8
    msg.set_charset('utf-8')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Bekräftelsemail skickat!")
        return True
    except Exception as e:
        print("Fel vid skickande av mail:", e)
        return False

