### Hotel Management System (HMS)
Alright, so this is a Django web app for running a hotel. It helps you handle room bookings, guest stuff, and see what rooms are free. You've got a main dashboard for a quick look, and then separate sections for all the detailed work.

## Let's Install It
# Get the project files:

```
git clone https://github.com/mavid3v/hotel_management_system.git
```

Go into that project folder:

```
cd hotel_management_system
```

Creat Python Virtual Environment with

```
python -m venv venv
cd venv
cd Scripts
activate
```

Go back to the "hotel_management_system" directory

```
cd ..
cd ..
```

Install Django (Python Framework):

```
pip install django
```

# Run the setup script:
This hms.py (or whatever setup script you have) does all the Django setup for you.

```
python hms.py
```

# This script will:

Make the hotel_management_system folder (if it's not there) and jump into it.

- Install Django if you don't have it.

- Set up the main Django project (hotel_management).

- Fix up settings.py (like allowing all hosts and handling static files).

- Create the hotel app.

- Add the hotel app to your Django settings.

- Put in all the models.py, forms.py, and views.py stuff for the hotel app.

- Make the static files folder and style.css.

- Set up all the web addresses (urls.py) for the main project and the hotel app.

- Run the database updates (makemigrations and migrate).

- Gather all the static files.

- And then, it'll kick off the Django web server.

# How to Use It
Once that server is running (after the setup script finishes), just open your web browser and go to:

```
http://127.0.0.1:8000/
```

- You'll see the dashboard. Just use the menu on the side to jump to different parts of the app:

- Dashboard: Your main overview.

- Room Booking: Where you manage all your rooms (add, view, change, delete).

- Room Availability: Check which rooms are free for specific dates.

- Customers: Handle all your guest details (add, view, change, delete, and search).

- Invoices: See and manage all the bookings.

## What It Does (Features)
# Dashboard:

- Shows you how many rooms are generally available.

- Got this calendar thing that actually works now (you can click through months!).

- Lists recent guests.

- Shows recent bookings (like your invoices).

# Room Management:

- You can see all your rooms.

- Check out details for each room.

- Add new rooms, easy.

- Update room info if you need to.

- And yeah, delete rooms too.

# Booking Management:

- See all your bookings in one place.

- Detailed view for each booking.

- Make new bookings, picking guests and rooms.

- Change existing bookings.

- Delete bookings.

# Smart Booking:
It won't let you double-book a room for the same dates, that's handled!

# Guest Management:

- All your guests are listed.

- You can search for guests by name or contact info.

- See guest details.

- Add new guests.

- Update guest info.

- Delete guests.

# Room Availability Check:

- There's a special tab just for checking room availability for specific check-in and check-out dates.

- It filters rooms based on what's free and what's already booked.

- Gives you clear messages about what's available.

# User Feedback:
You'll see messages pop up – like "success!", "warning!", or "error!" – so you know what's going on.

# Looks Good:
Basic styling is in there, so it's clean and works on different screen sizes.

# How to Get It Running (Setup)
Just follow these steps to get this Hotel Management System working on your computer.

# Stuff You Need First
Python 3.x

pip (that's Python's package installer)

## How the Project's Built (Structure)
It's set up like a normal Django project, pretty standard:

```
hotel_management_system/
├── hotel_management/             # The main Django project stuff
│   ├── __init__.py
│   ├── settings.py               # Project settings (the script sets this up)
│   ├── urls.py                   # Main web addresses (the script sets this up)
│   └── wsgi.py
├── hotel/                        # This is your actual hotel app
│   ├── migrations/
│   ├── static/
│   │   └── hotel/
│   │       └── css/
│   │           └── style.css     # Your custom look and feel
│   ├── templates/
│   │   └── hotel/                # All the HTML pages for the app
│   │       ├── base.html         # The main template for all pages
│   │       ├── home.html         # The dashboard page
│   │       ├── room_list.html
│   │       ├── room_detail.html
│   │       ├── room_form.html
│   │       ├── room_confirm_delete.html
│   │       ├── booking_list.html
│   │       ├── booking_detail.html
│   │       ├── booking_form.html
│   │       ├── booking_confirm_delete.html
│   │       ├── guest_list.html
│   │       ├── guest_detail.html
│   │       ├── guest_form.html
│   │       ├── guest_confirm_delete.html
│   │       └── room_availability.html # That special availability page
│   ├── __init__.py
│   ├── admin.py                  # For Django's admin panel
│   ├── apps.py
│   ├── models.py                 # Defines your database tables (Rooms, Guests, Bookings, etc.)
│   ├── forms.py                  # The forms you use for input
│   ├── tests.py
│   └── views.py                  # All the logic for your app
│   └── urls.py                   # The web addresses just for this app
├── manage.py                     # Django's command line tool
└── db.sqlite3                    # Your default database file
```
# What Tech It Uses
- Backend: Python, Django (that's the server side)

- Frontend: HTML, CSS (your custom styles), JavaScript (for that cool interactive calendar on the dashboard!)

- Database: SQLite (it's built-in for development)

- Icons: Font Awesome (for all those neat little symbols)

# Want to Help Out?
Go ahead, fork it, make it better, send in your changes!

## License
This project is licensed under the terms of the MIT License. See the [License](./LICENSE) file for details.

---
