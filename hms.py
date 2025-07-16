import os
import subprocess
import sys
import time # Import time for potential debugging sleep, though not used in final code
from datetime import date # Import date for date comparisons

# Define the project directory name
project_dir = "hotel_management_system"
main_project_name = "hotel_management"
app_name = "hotel"

# --- Step 1: Create project directory and navigate into it ---
print(f"Creating project directory: {project_dir}")
os.makedirs(project_dir, exist_ok=True)
# Change to the project directory
try:
    os.chdir(project_dir)
    print(f"Changed current directory to: {os.getcwd()}")
except OSError as e:
    print(f"Error changing directory to {project_dir}: {e}")
    sys.exit(1) # Exit if we can't change directory

# --- Step 2: Install Django (if not already installed) ---
print("Checking for Django installation...")
try:
    # Check if django-admin is available
    subprocess.run(["django-admin", "--version"], check=True, capture_output=True)
    print("Django is already installed.")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Django not found. Installing Django...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "django"], check=True)
        print("Django installed successfully.")
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode() if e.stderr else "No error output."
        print(f"Error installing Django: {error_output}")
        sys.exit(1)

# --- Step 3: Create Django project ---
print(f"Creating Django project: {main_project_name}")
try:
    # Corrected: Use 'python -m django startproject' to create the project and manage.py
    subprocess.run([sys.executable, "-m", "django", "startproject", main_project_name, "."], check=True)
    print("Django project created successfully.")
except subprocess.CalledProcessError as e:
    error_output = e.stderr.decode() if e.stderr else "No error output."
    print(f"Error creating Django project: {error_output}")
    sys.exit(1)

# --- Step 4: Configure basic settings (ALLOWED_HOSTS and Static Files) ---
settings_file_path = os.path.join(main_project_name, "settings.py")
print(f"Configuring settings file: {settings_file_path}")
try:
    with open(settings_file_path, 'r') as f:
        settings_content = f.read()

    # Ensure 'import os' is at the top if not already present
    if "import os" not in settings_content:
        settings_content = "import os\n" + settings_content

    # Add '*' to ALLOWED_HOSTS
    settings_content = settings_content.replace(
        "ALLOWED_HOSTS = []",
        "ALLOWED_HOSTS = ['*']"
    )

    # Add STATIC_URL, STATICFILES_DIRS, and STATIC_ROOT for serving static files
    # Check if STATIC_URL is defined, then replace or append
    if "STATIC_URL = 'static/'" in settings_content:
        settings_content = settings_content.replace(
            "STATIC_URL = 'static/'",
            """STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'hotel/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Add STATIC_ROOT
"""
        )
    else:
        # Fallback if STATIC_URL line is different or missing
        settings_content += """
# Custom static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'hotel/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Add STATIC_ROOT
"""

    with open(settings_file_path, 'w') as f:
        f.write(settings_content)
    print("Settings file configured successfully (ALLOWED_HOSTS and Static Files updated).")
except FileNotFoundError:
    print(f"Error: settings.py not found at {settings_file_path}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while modifying settings.py: {e}")
    sys.exit(1)

# --- Step 5: Create Django app ---
print(f"Creating Django app: {app_name}")
try:
    subprocess.run([sys.executable, "manage.py", "startapp", app_name], check=True)
    print(f"Django app '{app_name}' created successfully.")
except subprocess.CalledProcessError as e:
    error_output = e.stderr.decode() if e.stderr else "No error output."
    print(f"Error creating Django app: {error_output}")
    sys.exit(1)

# --- Step 6: Add the app to INSTALLED_APPS ---
print(f"Adding '{app_name}' to INSTALLED_APPS in settings.py")
try:
    with open(settings_file_path, 'r') as f:
        settings_content = f.read()

    # Check if 'hotel' is already in INSTALLED_APPS to avoid duplicates
    if f"'{app_name}'," not in settings_content and f"'{app_name}'" not in settings_content:
        installed_apps_start = settings_content.find("INSTALLED_APPS = [")
        if installed_apps_start != -1:
            installed_apps_end = settings_content.find("]", installed_apps_start)
            if installed_apps_end != -1:
                settings_content = (
                    settings_content[:installed_apps_end]
                    + f"    '{app_name}',\n"
                    + settings_content[installed_apps_end:]
                )
                with open(settings_file_path, 'w') as f:
                    f.write(settings_content)
                print(f"'{app_name}' app added to INSTALLED_APPS.")
            else:
                print("Error: Could not find closing bracket for INSTALLED_APPS.")
        else:
            print("Error: Could not find INSTALLED_APPS list in settings.py.")
    else:
        print(f"'{app_name}' app is already in INSTALLED_APPS.")

except FileNotFoundError:
    print(f"Error: settings.py not found at {settings_file_path}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while modifying settings.py: {e}")
    sys.exit(1)

# --- Step 7: Define models in hotel/models.py ---
models_file_path = os.path.join(app_name, "models.py")
print(f"Creating/Updating models.py at: {models_file_path}")
models_content = """
from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='available') # e.g., available, booked, maintenance

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

class Guest(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField() # e.g., address, phone, email

    def __str__(self):
        return self.name

class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, default='pending') # e.g., confirmed, pending, cancelled

    def __str__(self):
        return f"Booking for {self.guest} in Room {self.room.room_number}"

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Booking ID {self.booking.id}"
"""
try:
    with open(models_file_path, 'w') as f:
        f.write(models_content)
    print("models.py created/updated successfully with defined models.")
except Exception as e:
    print(f"An error occurred while writing to models.py: {e}")
    sys.exit(1)

# --- Step 8: Create forms in hotel/forms.py ---
forms_file_path = os.path.join(app_name, "forms.py")
print(f"Creating forms.py at: {forms_file_path}")
forms_content = """
from django import forms
from .models import Room, Booking, Guest

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'status']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest', 'room', 'check_in_date', 'check_out_date', 'status']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'contact_info']
"""
try:
    with open(forms_file_path, 'w') as f:
        f.write(forms_content)
    print("forms.py created successfully.")
except Exception as e:
    print(f"An error occurred while writing to forms.py: {e}")
    sys.exit(1)

# --- Step 9: Create views in hotel/views.py ---
views_file_path = os.path.join(app_name, "views.py")
print(f"Creating/Updating views.py at: {views_file_path}")
views_content = """
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q # Import Q for complex lookups
from .models import Room, Booking, Guest
from .forms import RoomForm, BookingForm, GuestForm
from django.contrib import messages # Import messages for feedback
from datetime import date # Import date for date comparisons

def home(request):
    \"\"\"A simple home view for the application.\"\"\"
    available_rooms_count = Room.objects.filter(status='available').count()
    recent_guests = Guest.objects.order_by('-id')[:5] # Get 5 most recent guests
    recent_bookings = Booking.objects.order_by('-id')[:5] # Get 5 most recent bookings

    context = {
        'available_rooms_count': available_rooms_count,
        'recent_guests': recent_guests,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'hotel/home.html', context)

def book_room_from_dashboard(request):
    # This view is kept for its core booking logic, though the dashboard form is removed.
    # It can be called by other parts of the application or for testing.
    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')
        guest_name = request.POST.get('name')
        guest_contact_info = request.POST.get('email')

        if not all([room_type, check_in_date_str, check_out_date_str, guest_name, guest_contact_info]):
            messages.error(request, "All fields are required to book a room.")
            return redirect('home')

        try:
            check_in_date_obj = date.fromisoformat(check_in_date_str)
            check_out_date_obj = date.fromisoformat(check_out_date_str)

            if check_in_date_obj >= check_out_date_obj:
                messages.error(request, "Check-out date must be after check-in date.")
                return redirect('home')

            guest, created = Guest.objects.get_or_create(
                name=guest_name,
                defaults={'contact_info': guest_contact_info}
            )
            if not created:
                if guest.contact_info != guest_contact_info:
                    guest.contact_info = guest_contact_info
                    guest.save()

            booked_room_ids = Booking.objects.filter(
                Q(check_in_date__lte=check_out_date_obj) & Q(check_out_date__gte=check_in_date_obj)
            ).values_list('room__id', flat=True)

            available_room = Room.objects.filter(
                room_type=room_type,
                status='available'
            ).exclude(id__in=booked_room_ids).first()


            if available_room:
                booking = Booking.objects.create(
                    guest=guest,
                    room=available_room,
                    check_in_date=check_in_date_obj,
                    check_out_date=check_out_date_obj,
                    status='confirmed'
                )
                messages.success(request, f"Room {available_room.room_number} booked successfully for {guest.name}! Booking ID: {booking.id}")
            else:
                messages.warning(request, f"No available rooms of type '{room_type}' for the selected dates.")

        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
        except Exception as e:
            messages.error(request, f"An error occurred during booking: {e}")

    return redirect('home')


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'hotel/room_detail.html', {'room': room})

def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Room {form.instance.room_number} created successfully!")
            return redirect('room_list')
        else:
            messages.error(request, "Error creating room. Please check the form.")
    else:
        form = RoomForm()
    return render(request, 'hotel/room_form.html', {'form': form})

def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f"Room {room.room_number} updated successfully!")
            return redirect('room_detail', pk=pk)
        else:
            messages.error(request, "Error updating room. Please check the form.")
    else:
        form = RoomForm(instance=room)
    return render(request, 'hotel/room_form.html', {'form': form})

def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_number = room.room_number # Store before deleting
        room.delete()
        messages.success(request, f"Room {room_number} deleted successfully!")
        return redirect('room_list')
    return render(request, 'hotel/room_confirm_delete.html', {'room': room})

def room_availability(request):
    \"\"\"A view for room availability with date filtering.\"\"\"
    rooms = Room.objects.all().order_by('room_number')
    check_in = request.GET.get('check_in_date')
    check_out = request.GET.get('check_out_date')
    available_rooms = []
    message = ""

    if check_in and check_out:
        try:
            check_in_date_obj = date.fromisoformat(check_in)
            check_out_date_obj = date.fromisoformat(check_out)

            if check_in_date_obj >= check_out_date_obj:
                messages.error(request, "Check-out date must be after check-in date.")
                context = {
                    'rooms': [], # No rooms displayed if dates are invalid
                    'current_month': 'Invalid Dates',
                    'check_in_date': check_in,
                    'check_out_date': check_out,
                    'message': "Check-out date must be after check-in date."
                }
                return render(request, 'hotel/room_availability.html', context)

            booked_room_ids = Booking.objects.filter(
                Q(check_in_date__lte=check_out_date_obj) & Q(check_out_date__gte=check_in_date_obj)
            ).values_list('room__id', flat=True)

            available_rooms = Room.objects.filter(
                status='available'
            ).exclude(id__in=booked_room_ids).order_by('room_number')

            if not available_rooms.exists():
                message = "No rooms available for the selected dates."
            else:
                message = f"{available_rooms.count()} rooms available for the selected dates."

        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            message = "Invalid date format. Please use YYYY-MM-DD."
            available_rooms = [] # Clear rooms on invalid date
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            message = f"An error occurred: {e}"
            available_rooms = []
    else:
        available_rooms = Room.objects.filter(status='available').order_by('room_number')
        message = f"Currently showing all available rooms ({available_rooms.count()}). Select dates to filter."


    context = {
        'rooms': available_rooms,
        'current_month': 'Current View',
        'check_in_date': check_in,
        'check_out_date': check_out,
        'message': message,
    }
    return render(request, 'hotel/room_availability.html', context)

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'hotel/booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'hotel/booking_detail.html', {'booking': booking})

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date_obj = form.cleaned_data['check_in_date']
            check_out_date_obj = form.cleaned_data['check_out_date']
            room = form.cleaned_data['room']

            # Check for overlapping bookings for the selected room
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_in_date__lte=check_out_date_obj,
                check_out_date__gte=check_in_date_obj
            ).exclude(pk=form.instance.pk if form.instance.pk else None) # Exclude self if updating

            if overlapping_bookings.exists():
                messages.error(request, f"Room {room.room_number} is already booked for some part of the selected dates.")
                return render(request, 'hotel/booking_form.html', {'form': form})

            form.save()
            messages.success(request, f"Booking for Room {room.room_number} created successfully!")
            return redirect('booking_list')
        else:
            messages.error(request, "Error creating booking. Please check the form.")
    else:
        form = BookingForm()
    return render(request, 'hotel/booking_form.html', {'form': form})

def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            check_in_date_obj = form.cleaned_data['check_in_date']
            check_out_date_obj = form.cleaned_data['check_out_date']
            room = form.cleaned_data['room']

            # Check for overlapping bookings for the selected room, excluding the current booking being updated
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_in_date__lte=check_out_date_obj,
                check_out_date__gte=check_in_date_obj
            ).exclude(pk=booking.pk)

            if overlapping_bookings.exists():
                messages.error(request, f"Room {room.room_number} is already booked for some part of the selected dates.")
                return render(request, 'hotel/booking_form.html', {'form': form})

            form.save()
            messages.success(request, f"Booking ID {booking.id} updated successfully!")
            return redirect('booking_detail', pk=pk)
        else:
            messages.error(request, "Error updating booking. Please check the form.")
    else:
        form = BookingForm(instance=booking)
    return render(request, 'hotel/booking_form.html', {'form': form})

def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking_id = booking.id
        booking.delete()
        messages.success(request, f"Booking ID {booking_id} deleted successfully!")
        return redirect('booking_list')
    return render(request, 'hotel/booking_confirm_delete.html', {'booking': booking})


def guest_list(request):
    guests = Guest.objects.all()
    search_query = request.GET.get('q') # Get the search query from the URL parameter 'q'

    if search_query:
        # Filter guests by name or contact_info (email)
        guests = guests.filter(
            Q(name__icontains=search_query) | Q(contact_info__icontains=search_query)
        )
    return render(request, 'hotel/guest_list.html', {'guests': guests, 'search_query': search_query})

def guest_detail(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    return render(request, 'hotel/guest_detail.html', {'guest': guest})

def guest_create(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Guest {form.instance.name} created successfully!")
            return redirect('guest_list')
        else:
            messages.error(request, "Error creating guest. Please check the form.")
    else:
        form = GuestForm()
    return render(request, 'hotel/guest_form.html', {'form': form})

def guest_update(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            messages.success(request, f"Guest {guest.name} updated successfully!")
            return redirect('guest_detail', pk=pk)
        else:
            messages.error(request, "Error updating guest. Please check the form.")
    else:
        form = GuestForm(instance=guest)
    return render(request, 'hotel/guest_form.html', {'form': form})

def guest_delete(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        guest_name = guest.name
        guest.delete()
        messages.success(request, f"Guest {guest_name} deleted successfully!")
        return redirect('guest_list')
    return render(request, 'hotel/guest_confirm_delete.html', {'guest': guest})
"""
try:
    with open(views_file_path, 'w') as f:
        f.write(views_content)
    print("views.py created/updated successfully with defined views.")
except Exception as e:
    print(f"An error occurred while writing to views.py: {e}")
    sys.exit(1)

# --- Step 10: Create static directories and style.css ---
static_css_dir = os.path.join(app_name, "static", app_name, "css")
os.makedirs(static_css_dir, exist_ok=True)
style_css_path = os.path.join(static_css_dir, "style.css")

print(f"Creating style.css at: {style_css_path}")
style_css_content = """
/* General Body and Layout */
body {
    font-family: 'Inter', sans-serif; /* Assuming Inter font from image */
    margin: 0;
    padding: 0;
    background-color: #f0f2f5; /* Light gray background */
    display: flex;
    min-height: 100vh;
    color: #333;
}

.container {
    display: flex;
    width: 100%;
}

/* Sidebar Styling */
.sidebar {
    width: 250px;
    background-color: #2c3e50; /* Dark blue/gray */
    color: #ecf0f1; /* Light text */
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
}

.sidebar h2 {
    color: #fff;
    text-align: center;
    margin-bottom: 30px;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar ul li {
    margin-bottom: 10px;
}

.sidebar ul li a {
    color: #ecf0f1;
    text-decoration: none;
    padding: 10px 15px;
    display: block;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.sidebar ul li a:hover,
.sidebar ul li a.active {
    background-color: #34495e; /* Slightly lighter dark blue/gray */
}

.sidebar ul li a i {
    margin-right: 10px;
}

/* Main Content Area */
.main-content {
    flex-grow: 1;
    padding: 20px;
    display: flex;
    flex-direction: column;
}

.header {
    background-color: #fff;
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    font-size: 1.5em;
    font-weight: bold;
    color: #2c3e50;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

/* Card Styling */
.card {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.card h3 {
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

/* Form Styling */
.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #555;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="date"],
.form-group select,
.form-group textarea {
    width: calc(100% - 20px); /* Account for padding */
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1em;
    box-sizing: border-box; /* Include padding in width */
}

.form-group input[type="submit"],
.button {
    background-color: #3498db; /* Blue button */
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s ease;
    text-decoration: none; /* For anchor tags styled as buttons */
    display: inline-block;
    text-align: center;
}

.form-group input[type="submit"]:hover,
.button:hover {
    background-color: #2980b9; /* Darker blue on hover */
}

.button.delete {
    background-color: #e74c3c; /* Red for delete */
}

.button.delete:hover {
    background-color: #c0392b;
}

/* Table Styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

table th, table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}

table th {
    background-color: #f2f2f2;
    font-weight: bold;
}

/* Specific elements from image */
.room-booking-card, .room-availability-card, .customer-details-card, .invoice-generation-card {
    /* Specific styling if needed, otherwise use general card styles */
}

.room-availability-card .calendar {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    gap: 5px;
}

.room-availability-card .calendar .day-header {
    font-weight: bold;
    color: #777;
}

.room-availability-card .calendar .day {
    padding: 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.room-availability-card .calendar .day:hover {
    background-color: #e0e0e0;
}

.room-availability-card .calendar .day.selected {
    background-color: #3498db;
    color: white;
    font-weight: bold;
}

.room-availability-card .calendar .day.inactive {
    color: #ccc;
    cursor: not-allowed;
}

.invoice-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #eee;
}

.invoice-item:last-child {
    border-bottom: none;
}

.invoice-item .download-icon {
    color: #3498db;
    cursor: pointer;
    font-size: 1.2em;
}

.booking-success-message {
    background-color: #d4edda; /* Light green */
    color: #155724; /* Dark green text */
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #c3e6cb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-top: 20px;
}

.booking-success-message i {
    margin-right: 10px;
    font-size: 1.2em;
}

/* Utility classes for spacing and alignment */
.text-center {
    text-align: center;
}

.mt-20 {
    margin-top: 20px;
}

.mb-20 {
    margin-bottom: 20px;
}

/* Font Awesome Icons */
/* Ensure Font Awesome is linked in base.html */
"""
try:
    with open(style_css_path, 'w') as f:
        f.write(style_css_content)
    print("style.css created successfully with dashboard styling.")
except Exception as e:
    print(f"An error occurred while writing to style.css: {e}")
    sys.exit(1)

# --- Step 11: Create base.html and update other templates to extend it ---
templates_dir = os.path.join(app_name, "templates", app_name)

# Ensure the templates directory exists before trying to create files in it
print(f"Ensuring template directory exists: {templates_dir}")
try:
    os.makedirs(templates_dir, exist_ok=True)
    # Optional: Add a small delay if timing is suspected to be an issue on certain systems
    # time.sleep(0.1)
    if not os.path.isdir(templates_dir): # Double check if directory exists
        raise OSError(f"Failed to create directory: {templates_dir}")
except Exception as e:
    print(f"Error creating template directory {templates_dir}: {e}")
    sys.exit(1)

# Create base.html
base_html_path = os.path.join(templates_dir, "base.html")
print(f"Creating base.html at: {base_html_path}")
base_html_content = """
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Hotel Management System{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'hotel/css/style.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Fonts - Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>HMS</h2>
            <ul>
                <li><a href="{% url 'home' %}" class="{% if request.resolver_match.url_name == 'home' %}active{% endif %}"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li><a href="{% url 'room_list' %}" class="{% if 'room' in request.resolver_match.url_name %}active{% endif %}"><i class="fas fa-bed"></i> Room Booking</a></li>
                <li><a href="{% url 'room_availability' %}" class="{% if request.resolver_match.url_name == 'room_availability' %}active{% endif %}"><i class="fas fa-calendar-alt"></i> Room Availability</a></li>
                <li><a href="{% url 'guest_list' %}" class="{% if 'guest' in request.resolver_match.url_name %}active{% endif %}"><i class="fas fa-users"></i> Customers</a></li>
                <li><a href="{% url 'booking_list' %}" class="{% if 'booking' in request.resolver_match.url_name %}active{% endif %}"><i class="fas fa-file-invoice"></i> Invoices</a></li>
            </ul>
        </div>
        <div class="main-content">
            <div class="header">
                {% block header_title %}Dashboard{% endblock %}
            </div>
            {% if messages %}
                <ul class="messages">
                    {% for message in messages %}
                        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
            {% block content %}
            {% endblock %}
        </div>
    </div>
</body>
</html>
"""
try:
    with open(base_html_path, 'w') as f:
        f.write(base_html_content)
    print("base.html created successfully.")
except Exception as e:
    print(f"An error occurred while writing to base.html: {e}")
    sys.exit(1)

# Create room_availability.html
room_availability_html_path = os.path.join(templates_dir, "room_availability.html")
print(f"Creating room_availability.html at: {room_availability_html_path}")
room_availability_html_content = """
{% extends 'hotel/base.html' %}

{% block title %}Room Availability{% endblock %}
{% block header_title %}Room Availability{% endblock %}

{% block content %}
    <div class="card">
        <h3>Room Availability Overview</h3>
        <form method="get" action="{% url 'room_availability' %}" class="mb-20" style="display: flex; align-items: center; gap: 10px;">
            <label for="check_in_date">Check-in:</label>
            <input type="date" id="check_in_date" name="check_in_date" value="{{ check_in_date|default_if_none:'' }}">
            <label for="check_out_date">Check-out:</label>
            <input type="date" id="check_out_date" name="check_out_date" value="{{ check_out_date|default_if_none:'' }}">
            <button type="submit" class="button">Check Availability</button>
        </form>

        {% if message %}
            <p class="mt-10 mb-10">{{ message }}</p>
        {% endif %}

        <table>
            <thead>
                <tr>
                    <th>Room Number</th>
                    <th>Room Type</th>
                    <th>Price</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for room in rooms %}
                    <tr>
                        <td>{{ room.room_number }}</td>
                        <td>{{ room.room_type }}</td>
                        <td>{{ room.price }}</td>
                        <td>{{ room.status }}</td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="4">No rooms found for the selected criteria.</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
        <p class="mt-20">This is a simplified view. A full calendar would show daily availability.</p>
    </div>
{% endblock %}
"""
try:
    with open(room_availability_html_path, 'w') as f:
        f.write(room_availability_html_content)
    print("room_availability.html created successfully.")
except Exception as e:
    print(f"An error occurred while writing to room_availability.html: {e}")
    sys.exit(1)

# Update existing HTML templates to extend base.html and use blocks
html_files_to_update = {
    "home.html": """
{% extends 'hotel/base.html' %}

{% block title %}Dashboard{% endblock %}
{% block header_title %}Dashboard{% endblock %}

{% block content %}
    <div class="dashboard-grid">
        {# Removed Room Booking card from dashboard as per user request #}

        <div class="card room-availability-card">
            <h3>Room Availability</h3>
            <div class="calendar-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <i class="fas fa-chevron-left" id="prevMonth"></i>
                <h4 id="currentMonthYear"></h4>
                <i class="fas fa-chevron-right" id="nextMonth"></i>
            </div>
            <div class="calendar" id="dashboardCalendar">
                <div class="day-header">S</div>
                <div class="day-header">M</div>
                <div class="day-header">T</div>
                <div class="day-header">W</div>
                <div class="day-header">T</div>
                <div class="day-header">F</div>
                <div class="day-header">S</div>
                {# Calendar days will be rendered by JavaScript #}
            </div>
            <p style="text-align: center; margin-top: 15px;">Total Available Rooms: <strong>{{ available_rooms_count }}</strong></p>
            <div class="mt-20 text-center">
                <a href="{% url 'room_availability' %}" class="button">View Full Availability</a>
            </div>
        </div>

        <div class="card customer-details-card">
            <h3>Customer Details</h3>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <form method="get" action="{% url 'guest_list' %}" style="display: flex; flex-grow: 1;">
                    <input type="text" name="q" placeholder="Search..." style="flex-grow: 1; margin-right: 10px;">
                    <button type="submit" class="button"><i class="fas fa-search"></i></button>
                </form>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Contact Info</th>
                    </tr>
                </thead>
                <tbody>
                    {% for guest in recent_guests %}
                    <tr>
                        <td>{{ guest.name }}</td>
                        <td>{{ guest.contact_info }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="2">No recent guests found.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="mt-20 text-center">
                <a href="{% url 'guest_list' %}" class="button">View All Customers</a>
            </div>
        </div>

        <div class="card invoice-generation-card">
            <h3>Recent Invoices (Bookings)</h3>
            {% for booking in recent_bookings %}
            <div class="invoice-item">
                <span>INV-{{ booking.id }}</span>
                <span>{{ booking.check_in_date|date:"M d, Y" }}</span>
                <a href="{% url 'booking_detail' pk=booking.pk %}" class="download-icon"><i class="fas fa-info-circle"></i></a>
            </div>
            {% empty %}
            <p>No recent bookings to display.</p>
            {% endfor %}
            <div class="mt-20 text-center">
                <a href="{% url 'booking_list' %}" class="button">View All Invoices</a>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const monthYearDisplay = document.getElementById('currentMonthYear');
            const calendarDaysContainer = document.getElementById('dashboardCalendar');
            const prevMonthBtn = document.getElementById('prevMonth');
            const nextMonthBtn = document.getElementById('nextMonth');

            let currentMonth = new Date().getMonth();
            let currentYear = new Date().getFullYear();

            function renderCalendar() {
                calendarDaysContainer.innerHTML = `
                    <div class="day-header">S</div>
                    <div class="day-header">M</div>
                    <div class="day-header">T</div>
                    <div class="day-header">W</div>
                    <div class="day-header">T</div>
                    <div class="day-header">F</div>
                    <div class="day-header">S</div>
                `; // Clear and re-add headers

                const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
                const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
                const firstDayOfWeek = firstDayOfMonth.getDay(); // 0 for Sunday, 1 for Monday, etc.

                monthYearDisplay.textContent = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long', year: 'numeric' });

                // Add empty divs for preceding days of the week
                for (let i = 0; i < firstDayOfWeek; i++) {
                    const emptyDay = document.createElement('div');
                    emptyDay.classList.add('day', 'inactive');
                    calendarDaysContainer.appendChild(emptyDay);
                }

                // Add days of the month
                for (let day = 1; day <= daysInMonth; day++) {
                    const dayElement = document.createElement('div');
                    dayElement.classList.add('day');
                    dayElement.textContent = day;
                    if (day === new Date().getDate() && currentMonth === new Date().getMonth() && currentYear === new Date().getFullYear()) {
                        dayElement.classList.add('selected'); // Highlight current day
                    }
                    calendarDaysContainer.appendChild(dayElement);
                }
            }

            prevMonthBtn.addEventListener('click', function() {
                currentMonth--;
                if (currentMonth < 0) {
                    currentMonth = 11;
                    currentYear--;
                }
                renderCalendar();
            });

            nextMonthBtn.addEventListener('click', function() {
                currentMonth++;
                if (currentMonth > 11) {
                    currentMonth = 0;
                    currentYear++;
                }
                renderCalendar();
            });

            // Initial render
            renderCalendar();
        });
    </script>
{% endblock %}
""",
    "room_list.html": """
{% extends 'hotel/base.html' %}

{% block title %}Room List{% endblock %}
{% block header_title %}Room List{% endblock %}

{% block content %}
    <div class="card">
        <a href="{% url 'room_create' %}" class="button mb-20">Add New Room</a>
        <table>
            <thead>
                <tr>
                    <th>Room Number</th>
                    <th>Room Type</th>
                    <th>Price</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for room in rooms %}
                    <tr>
                        <td>{{ room.room_number }}</td>
                        <td>{{ room.room_type }}</td>
                        <td>{{ room.price }}</td>
                        <td>{{ room.status }}</td>
                        <td>
                            <a href="{% url 'room_detail' pk=room.pk %}" class="button">View</a>
                            <a href="{% url 'room_update' pk=room.pk %}" class="button">Edit</a>
                            <a href="{% url 'room_delete' pk=room.pk %}" class="button delete">Delete</a>
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="5">No rooms found.</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}
""",
    "room_detail.html": """
{% extends 'hotel/base.html' %}

{% block title %}Room Detail{% endblock %}
{% block header_title %}Room Detail{% endblock %}

{% block content %}
    <div class="card">
        <h3>Room {{ room.room_number }}</h3>
        <p><strong>Room Type:</strong> {{ room.room_type }}</p>
        <p><strong>Price:</strong> {{ room.price }}</p>
        <p><strong>Status:</strong> {{ room.status }}</p>
        <div class="mt-20">
            <a href="{% url 'room_list' %}" class="button">Back to Room List</a>
            <a href="{% url 'room_update' pk=room.pk %}" class="button">Edit</a>
            <a href="{% url 'room_delete' pk=room.pk %}" class="button delete">Delete</a>
        </div>
    </div>
{% endblock %}
""",
    "room_form.html": """
{% extends 'hotel/base.html' %}

{% block title %}Room Form{% endblock %}
{% block header_title %}{% if form.instance.pk %}Edit Room{% else %}Add New Room{% endif %}{% endblock %}

{% block content %}
    <div class="card">
        <form method="post">
            {% csrf_token %}
            {% for field in form %}
                <div class="form-group">
                    {{ field.label_tag }}
                    {{ field }}
                    {% if field.help_text %}
                        <small>{{ field.help_text }}</small>
                    {% endif %}
                    {% for error in field.errors %}
                        <p style="color: red;">{{ error }}</p>
                    {% endfor %}
                </div>
            {% endfor %}
            <button type="submit" class="button">Save</button>
            <a href="{% url 'room_list' %}" class="button delete">Cancel</a>
        </form>
    </div>
{% endblock %}
""",
    "room_confirm_delete.html": """
{% extends 'hotel/base.html' %}

{% block title %}Confirm Delete Room{% endblock %}
{% block header_title %}Confirm Delete Room{% endblock %}

{% block content %}
    <div class="card">
        <p>Are you sure you want to delete "Room {{ room.room_number }}"?</p>
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="button delete">Yes, Delete</button>
            <a href="{% url 'room_detail' pk=room.pk %}" class="button">Cancel</a>
        </form>
    </div>
{% endblock %}
""",
    "booking_list.html": """
{% extends 'hotel/base.html' %}

{% block title %}Booking List{% endblock %}
{% block header_title %}Booking List{% endblock %}

{% block content %}
    <div class="card">
        <a href="{% url 'booking_create' %}" class="button mb-20">Add New Booking</a>
        <table>
            <thead>
                <tr>
                    <th>Booking ID</th>
                    <th>Guest</th>
                    <th>Room</th>
                    <th>Check-in Date</th>
                    <th>Check-out Date</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for booking in bookings %}
                    <tr>
                        <td>{{ booking.id }}</td>
                        <td>{{ booking.guest }}</td>
                        <td>{{ booking.room.room_number }}</td>
                        <td>{{ booking.check_in_date }}</td>
                        <td>{{ booking.check_out_date }}</td>
                        <td>{{ booking.status }}</td>
                        <td>
                            <a href="{% url 'booking_detail' pk=booking.pk %}" class="button">View</a>
                            <a href="{% url 'booking_update' pk=booking.pk %}" class="button">Edit</a>
                            <a href="{% url 'booking_delete' pk=booking.pk %}" class="button delete">Delete</a>
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="7">No bookings found.</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}
""",
    "booking_detail.html": """
{% extends 'hotel/base.html' %}

{% block title %}Booking Detail{% endblock %}
{% block header_title %}Booking Detail{% endblock %}

{% block content %}
    <div class="card">
        <h3>Booking ID: {{ booking.id }}</h3>
        <p><strong>Guest:</strong> {{ booking.guest }}</p>
        <p><strong>Room:</strong> {{ booking.room.room_number }}</p>
        <p><strong>Check-in Date:</strong> {{ booking.check_in_date }}</p>
        <p><strong>Check-out Date:</strong> {{ booking.check_out_date }}</p>
        <p><strong>Status:</strong> {{ booking.status }}</p>
        <div class="mt-20">
            <a href="{% url 'booking_list' %}" class="button">Back to Booking List</a>
            <a href="{% url 'booking_update' pk=booking.pk %}" class="button">Edit</a>
            <a href="{% url 'booking_delete' pk=booking.pk %}" class="button delete">Delete</a>
        </div>
    </div>
{% endblock %}
""",
    "booking_form.html": """
{% extends 'hotel/base.html' %}

{% block title %}Booking Form{% endblock %}
{% block header_title %}{% if form.instance.pk %}Edit Booking{% else %}Add New Booking{% endif %}{% endblock %}

{% block content %}
    <div class="card">
        <form method="post">
            {% csrf_token %}
            {% for field in form %}
                <div class="form-group">
                    {{ field.label_tag }}
                    {{ field }}
                    {% if field.help_text %}
                        <small>{{ field.help_text }}</small>
                    {% endif %}
                    {% for error in field.errors %}
                        <p style="color: red;">{{ error }}</p>
                    {% endfor %}
                </div>
            {% endfor %}
            <button type="submit" class="button">Save</button>
            <a href="{% url 'booking_list' %}" class="button delete">Cancel</a>
        </form>
    </div>
{% endblock %}
""",
    "booking_confirm_delete.html": """
{% extends 'hotel/base.html' %}

{% block title %}Confirm Delete Booking{% endblock %}
{% block header_title %}Confirm Delete Booking{% endblock %}

{% block content %}
    <div class="card">
        <p>Are you sure you want to delete Booking ID {{ booking.id }}?</p>
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="button delete">Yes, Delete</button>
            <a href="{% url 'booking_detail' pk=booking.pk %}" class="button">Cancel</a>
        </form>
    </div>
{% endblock %}
""",
    "guest_list.html": """
{% extends 'hotel/base.html' %}

{% block title %}Guest List{% endblock %}
{% block header_title %}Guest List{% endblock %}

{% block content %}
    <div class="card">
        <form method="get" action="{% url 'guest_list' %}" class="mb-20" style="display: flex; align-items: center;">
            <input type="text" name="q" placeholder="Search guests by name or email..." value="{{ search_query|default_if_none:'' }}" style="flex-grow: 1; margin-right: 10px;">
            <button type="submit" class="button">Search</button>
            <a href="{% url 'guest_create' %}" class="button ml-10">Add New Guest</a>
        </form>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Contact Info</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for guest in guests %}
                    <tr>
                        <td>{{ guest.name }}</td>
                        <td>{{ guest.contact_info }}</td>
                        <td>
                            <a href="{% url 'guest_detail' pk=guest.pk %}" class="button">View</a>
                            <a href="{% url 'guest_update' pk=guest.pk %}" class="button">Edit</a>
                            <a href="{% url 'guest_delete' pk=guest.pk %}" class="button delete">Delete</a>
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="3">No guests found.</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}
""",
    "guest_detail.html": """
{% extends 'hotel/base.html' %}

{% block title %}Guest Detail{% endblock %}
{% block header_title %}Guest Detail{% endblock %}

{% block content %}
    <div class="card">
        <h3>Guest: {{ guest.name }}</h3>
        <p><strong>Contact Info:</strong> {{ guest.contact_info }}</p>
        <div class="mt-20">
            <a href="{% url 'guest_list' %}" class="button">Back to Guest List</a>
            <a href="{% url 'guest_update' pk=guest.pk %}" class="button">Edit</a>
            <a href="{% url 'guest_delete' pk=guest.pk %}" class="button delete">Delete</a>
        </div>
    </div>
{% endblock %}
""",
    "guest_form.html": """
{% extends 'hotel/base.html' %}

{% block title %}Guest Form{% endblock %}
{% block header_title %}{% if form.instance.pk %}Edit Guest{% else %}Add New Guest{% endif %}{% endblock %}

{% block content %}
    <div class="card">
        <form method="post">
            {% csrf_token %}
            {% for field in form %}
                <div class="form-group">
                    {{ field.label_tag }}
                    {{ field }}
                    {% if field.help_text %}
                        <small>{{ field.help_text }}</small>
                    {% endif %}
                    {% for error in field.errors %}
                        <p style="color: red;">{{ error }}</p>
                    {% endfor %}
                </div>
            {% endfor %}
            <button type="submit" class="button">Save</button>
            <a href="{% url 'guest_list' %}" class="button delete">Cancel</a>
        </form>
    </div>
{% endblock %}
""",
    "guest_confirm_delete.html": """
{% extends 'hotel/base.html' %}

{% block title %}Confirm Delete Guest{% endblock %}
{% block header_title %}Confirm Delete Guest{% endblock %}

{% block content %}
    <div class="card">
        <p>Are you sure you want to delete "{{ guest.name }}"?</p>
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="button delete">Yes, Delete</button>
            <a href="{% url 'guest_detail' pk=guest.pk %}" class="button">Cancel</a>
        </form>
    </div>
{% endblock %}
"""
}

for filename, content in html_files_to_update.items():
    file_path = os.path.join(templates_dir, filename)
    try:
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Updated {file_path} to extend base.html and use styling classes.")
    except Exception as e:
        print(f"An error occurred while writing to {file_path}: {e}")
        sys.exit(1)

print("HTML templates updated with dynamic data, forms, and navigation links.")

# --- Step 12: Configure URLs in hotel/urls.py ---
app_urls_file_path = os.path.join(app_name, "urls.py")
print(f"Creating/Updating {app_urls_file_path}")
app_urls_content = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Home page for the hotel app
    path('book_room_from_dashboard/', views.book_room_from_dashboard, name='book_room_from_dashboard'), # New URL for dashboard booking

    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/new/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/new/', views.booking_create, name='booking_create'),
    path('bookings/<int:pk>/edit/', views.booking_update, name='booking_update'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),

    # Guest URLs
    path('guests/', views.guest_list, name='guest_list'),
    path('guests/<int:pk>/', views.guest_detail, name='guest_detail'),
    path('guests/new/', views.guest_create, name='guest_create'),
    path('guests/<int:pk>/edit/', views.guest_update, name='guest_update'),
    path('guests/<int:pk>/delete/', views.guest_delete, name='guest_delete'),
    path('room_availability/', views.room_availability, name='room_availability'), # New URL for room availability
]
"""
try:
    with open(app_urls_file_path, 'w') as f:
        f.write(app_urls_content)
    print(f"{app_name}/urls.py created/updated successfully.")
except Exception as e:
    print(f"An error occurred while writing to {app_urls_file_path}: {e}")
    sys.exit(1)

# --- Step 13: Configure main project's urls.py to include app URLs ---
project_urls_file_path = os.path.join(main_project_name, "urls.py")
print(f"Configuring main project's urls.py: {project_urls_file_path}")

# Explicitly define the content for the main urls.py to ensure correctness
# This will overwrite the existing urls.py to ensure the root path is handled.
project_urls_content_new = f"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{app_name}.urls')), # Include the hotel app's URLs at the root
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
try:
    with open(project_urls_file_path, 'w') as f:
        f.write(project_urls_content_new.strip()) # .strip() removes leading/trailing newlines
    print(f"Main project's {main_project_name}/urls.py configured successfully.")
except Exception as e:
    print(f"An error occurred while writing to {project_urls_file_path}: {e}")
    sys.exit(1)

# --- Step 14: Run migrations ---
print("Running Django migrations...")
try:
    subprocess.run([sys.executable, "manage.py", "makemigrations", app_name], check=True)
    subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
    print("Migrations applied successfully.")
except subprocess.CalledProcessError as e:
    error_output = e.stderr.decode() if e.stderr else "No error output."
    print(f"Error running migrations: {error_output}")
    sys.exit(1)

# --- Step 15: Collect static files (important for production, good practice for dev) ---
print("Collecting static files...")
try:
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
    print("Static files collected successfully.")
except subprocess.CalledProcessError as e:
    error_output = e.stderr.decode() if e.stderr else "No error output."
    print(f"Error collecting static files: {error_output}")
    sys.exit(1)


# --- Step 16: Run the development server ---
print("Starting Django development server...")
print("Access the application at: http://127.0.0.1:8000/")
print("Press Ctrl+C to stop the server.")
try:
    process = subprocess.Popen([sys.executable, "manage.py", "runserver", "8000"])
    process.wait() # Wait for the process to terminate
except FileNotFoundError:
    print("Error: 'python' command not found. Make sure Python is in your PATH.")
except Exception as e:
    print(f"An error occurred while starting the server: {e}")
