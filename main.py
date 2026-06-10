from funktions import (
    show_menu,
    is_email_approved,
    choose_date,
    choose_time,
    book_time,
    cancel_booking,
    load_bookings,
    save_bookings,
    send_gmx_email,

)


BOOKINGS_FILE = "bokningar.json"


def main():
    approved_emails = {"exempel2@gmail.com",
                       "exempel@gmail.com"}
    bookings = load_bookings(BOOKINGS_FILE)

    print("Välkommen till bokningssystemet!")
    while True:
        email = input("Ange din e-post: ")
        if is_email_approved(email, approved_emails):
            print("E-post godkänd!")
            while True:
                val = show_menu()
                if val == "1":
                    chosen_date = choose_date()
                    if chosen_date:
                        chosen_time = choose_time(chosen_date, bookings)
                        if chosen_time:
                            if book_time(bookings, chosen_date, chosen_time, email):
                                print("Du har bokat tiden!")
                                save_bookings(BOOKINGS_FILE, bookings)

                                sender_email = "get.tube.25@gmail.com"
                                sender_password = "ueth maet lhio exfs"
                                subject = "Din bokning – Sporthallen"
                                body = (
                                    f"Hej!\n\nDu har bokat tiden: {chosen_time}\n"
                                    f"Datum: {chosen_date}\n\nVälkommen!"
                                )
                                send_gmx_email(sender_email, sender_password, email, subject, body)
                            else:
                                print("Tiden är redan bokad!")

                elif val == "2":
                    # Avbokning
                    user_dates = [date for date in bookings if bookings[date]]
                    if not user_dates:
                        print("Du har inga bokningar att avboka.")
                        continue
                    print("Dina bokade datum:")
                    for i, date in enumerate(user_dates, 1):
                        print(f"{i}. {date}")
                    val_date = input(f"Välj datum att avboka (1-{len(user_dates)}) eller N för att avbryta: ")
                    if val_date.lower() == "n":
                        continue
                    if val_date.isdigit() and 1 <= int(val_date) <= len(user_dates):
                        selected_date = user_dates[int(val_date) - 1]
                        tidslista = bookings[selected_date]
                        for j, tid in enumerate(tidslista, 1):
                            print(f"{j}. {tid}")
                        val_tid = input(f"Välj tid att avboka (1-{len(tidslista)}) eller N för att avbryta: ")
                        if val_tid.lower() == "n":
                            continue
                        if val_tid.isdigit() and 1 <= int(val_tid) <= len(tidslista):
                            selected_tid = tidslista[int(val_tid) - 1]
                            if cancel_booking(bookings, selected_date, selected_tid):
                                print("Tiden avbokad!")
                                save_bookings(BOOKINGS_FILE, bookings)

                                # Skicka avboknings bekräftelse mail
                                sender_email = "get.tube.25@gmail.com"
                                sender_password = "ueth maet lhio exfs"
                                subject = "Bekräftelse på avbokning – Sporthallen"
                                body = (
                                    f"Hej!\n\nDu har avbokat tiden: {selected_tid}\n"
                                    f"Datum: {selected_date}\n\nVi hoppas att se dig en annan gång!"
                                )
                                send_gmx_email(sender_email, sender_password, email, subject, body)

                            else:
                                print("Kunde inte avboka tiden.")
                        else:
                            print("Ogiltigt val.")
                    else:
                        print("Ogiltigt val.")

                elif val == "3":
                    print("Avslutar programmet.")
                    save_bookings(BOOKINGS_FILE, bookings)
                    return
                else:
                    print("Ogiltigt val, försök igen.")
        else:
            print("Ogiltig e-post, försök igen.")

if __name__ == "__main__":
    main()
