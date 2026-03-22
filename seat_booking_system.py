# Apache Airlines Burak757 Seat Booking System
# FC723 Project - Part A
# This program is a basic seat-booking system for the Burak757.
# It allows the user to:
# 1. Check availability of a seat
# 2. Book a seat
# 3. Free a seat
# 4. Show booking status
# 5. Exit the program
#
# Seat symbols used in the system:
# F = Free seat
# R = Reserved seat
# X = Aisle
# S = Storage
## This version is the Part A basic version only.
# It does not yet include booking references or a database.
# Those features can be added later in Part B.

import random
import string
import sqlite3

def create_seat_map():
    """
    Create the seating plan for the Burak757 aircraft.

    The seating plan is stored in a dictionary.
    Each key is a seat code such as '1A' or '3F'.
    Each value is the status of that position.

    This basic version uses:
    F = free seat
    R = reserved seat
    X = aisle
    S = storage

    The seating layout is fixed in this version.
    """
    seats = {
        "1A": "F", "1B": "F", "1C": "X", "1D": "F", "1E": "F", "1F": "F",
        "2A": "F", "2B": "F", "2C": "X", "2D": "F", "2E": "F", "2F": "F",
        "3A": "F", "3B": "F", "3C": "X", "3D": "F", "3E": "F", "3F": "F",
        "4A": "F", "4B": "F", "4C": "X", "4D": "F", "4E": "F", "4F": "F",
        "5A": "S", "5B": "S", "5C": "X", "5D": "S", "5E": "S", "5F": "S"
    }
    return seats


def display_menu():
    """
    Display the main menu to the user.

    This menu must remain available until the user chooses
    to exit the program.
    """
    print("\n==========================================")
    print(" Apache Airlines Seat Booking System ")
    print("==========================================")
    print("1. Check availability of seat")
    print("2. Book a seat")
    print("3. Free a seat")
    print("4. Show booking status")
    print("5. Exit program")


def normalise_seat_code(seat_code):
    """
    Convert user input into a standard seat-code format.

    Example:
    '1a' becomes '1A'
    ' 2d ' becomes '2D'

    This helps reduce user input errors.
    """
    return seat_code.strip().upper()


def is_valid_seat_code(seat_code, seats):
    """
    Check whether the entered seat code exists
    in the seating plan.

    Returns:
    True  -> if the seat code exists
    False -> if the seat code does not exist
    """
    return seat_code in seats

def generate_booking_reference(existing_references):
    """
    Generate a unique booking reference for a customer.

    The booking reference must:
    - contain exactly 8 characters
    - use only uppercase letters and digits
    - be unique

    Parameter:
    existing_references
        A collection (for example a set or list) containing all
        booking references that are already in use.

    Return:
    A unique 8-character alphanumeric booking reference.
    """

    # Create a string containing all valid characters that may be used
    # in the booking reference.
    # Uppercase letters A-Z are used together with digits 0-9.
    valid_characters = string.ascii_uppercase + string.digits

    # Keep generating references until a unique one is found.
    while True:
        # Randomly select 8 characters from the valid character set.
        # The selected characters are then joined together to form
        # one single booking reference string.
        booking_reference = "".join(random.choices(valid_characters, k=8))

        # Check whether the generated reference already exists.
        # If it does not exist, it is unique and can be returned.
        if booking_reference not in existing_references:
            return booking_reference

        # If the reference already exists, the loop continues
        # and a new reference is generated.
        
def create_database():
    """
    Create a connection to the SQLite database.

    The database file is stored in the same folder as the program.
    If the database file does not already exist, SQLite will create it.
    """
    connection = sqlite3.connect("bookings.db")
    return connection


def create_bookings_table(connection):
    """
    Create the bookings table if it does not already exist.

    The table stores:
    - booking reference
    - passport number
    - first name
    - last name
    - seat row
    - seat column
    """
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_reference TEXT PRIMARY KEY,
            passport_number TEXT,
            first_name TEXT,
            last_name TEXT,
            seat_row INTEGER,
            seat_column TEXT
        )
    """)

    connection.commit()


def get_existing_references(connection):
    """
    Read all booking references already stored in the database.

    This is used to make sure that every new booking reference is unique.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT booking_reference FROM bookings")

    rows = cursor.fetchall()

    # Convert the query result into a set of strings
    existing_references = set()
    for row in rows:
        existing_references.add(row[0])

    return existing_references


def save_booking_to_database(connection, booking_reference, passport_number,
                             first_name, last_name, seat_code):
    """
    Save a new booking into the database table.

    The seat code is split into:
    - seat row number
    - seat column letter
    """
    cursor = connection.cursor()

    # Example: '12A' -> row = 12, column = 'A'
    seat_row = int(seat_code[:-1])
    seat_column = seat_code[-1]

    cursor.execute("""
        INSERT INTO bookings (
            booking_reference,
            passport_number,
            first_name,
            last_name,
            seat_row,
            seat_column
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (booking_reference, passport_number, first_name,
          last_name, seat_row, seat_column))

    connection.commit()


def delete_booking_from_database(connection, booking_reference):
    """
    Delete a booking from the database using its booking reference.

    This is used when a reserved seat is freed.
    """
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM bookings
        WHERE booking_reference = ?
    """, (booking_reference,))

    connection.commit()


def check_availability(seats):
    """
    Check whether a seat is available.

    A seat is available only if:
    - the seat code is valid
    - the seat status is 'F'

    This function also informs the user if the selected
    position is reserved, an aisle, or a storage area.
    """
    # Ask the user to type a seat code
    seat_code = input("Enter the seat code to check: ")

    # Convert the input into standard format
    seat_code = normalise_seat_code(seat_code)

    # Check whether the seat code exists in the system
    if not is_valid_seat_code(seat_code, seats):
        print("Invalid seat code.")
        return

    # Read the current status of the selected seat
    status = seats[seat_code]

    # Display a message based on the current seat status
    if status == "F":
        print(f"Seat {seat_code} is available.")
    elif status == "R":
        print(f"Seat {seat_code} is already reserved.")
    elif status == "X":
        print(f"{seat_code} is an aisle and cannot be booked.")
    elif status == "S":
        print(f"{seat_code} is a storage area and cannot be booked.")


def book_seat(seats, connection):
    """
    Book a seat if it is free, then store the booking reference
    in the seat data structure and save passenger details in
    the database.

    In this refactored Part B version:
    - free seats still use "F"
    - restricted areas still use "X" or "S"
    - booked seats now store the booking reference instead of "R"
    """
    # Ask the user for the seat they want to reserve
    seat_code = input("Enter the seat code to book: ")

    # Standardise the input
    seat_code = normalise_seat_code(seat_code)

    # Check whether the entered seat exists
    if not is_valid_seat_code(seat_code, seats):
        print("Invalid seat code.")
        return

    # Check the current status of the selected seat
    status = seats[seat_code]

    # Only free seats can be booked
    if status == "F":
        # Ask the user for passenger details
        passport_number = input("Enter passport number: ").strip()
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()

        # Get all references already stored in the database
        existing_references = get_existing_references(connection)

        # Generate a new unique booking reference
        booking_reference = generate_booking_reference(existing_references)

        # Store the booking reference in the seat data structure
        seats[seat_code] = booking_reference

        # Save the passenger details and seat information to the database
        save_booking_to_database(
            connection,
            booking_reference,
            passport_number,
            first_name,
            last_name,
            seat_code
        )

        print(f"Seat {seat_code} has been successfully booked.")
        print(f"Booking reference: {booking_reference}")

    elif status == "X":
        print(f"{seat_code} is an aisle and cannot be booked.")

    elif status == "S":
        print(f"{seat_code} is a storage area and cannot be booked.")

    else:
        # If the seat is not F, X, or S, it is already booked
        print(f"Seat {seat_code} is already reserved. Booking reference: {status}")


def free_seat(seats, connection):
    """
    Free a previously reserved seat.

    In this refactored Part B version:
    - the system reads the booking reference stored in the seat
    - removes the related booking record from the database
    - changes the seat status back to "F"
    """
    # Ask the user which seat they want to free
    seat_code = input("Enter the seat code to free: ")

    # Convert the seat code into the standard format
    seat_code = normalise_seat_code(seat_code)

    # Check whether the seat exists in the seating plan
    if not is_valid_seat_code(seat_code, seats):
        print("Invalid seat code.")
        return

    # Read the current status of the seat
    status = seats[seat_code]

    # Restricted areas cannot be changed
    if status == "X":
        print(f"{seat_code} is an aisle and cannot be changed.")
        return

    if status == "S":
        print(f"{seat_code} is a storage area and cannot be changed.")
        return

    # Free seats do not need to be released
    if status == "F":
        print(f"Seat {seat_code} is already free.")
        return

    # If the seat is booked, the stored value is the booking reference
    booking_reference = status

    # Remove the booking from the database
    delete_booking_from_database(connection, booking_reference)

    # Change the seat status back to free
    seats[seat_code] = "F"

    print(f"Seat {seat_code} has been successfully freed.")


def show_booking_status(seats):
    """
    Display the full seating layout of the aircraft.

    This allows the user to see the current booking status
    of all positions in the seating plan.
    """
    print("\n------------- Booking Status -------------")
    print("Legend: F = Free, X = Aisle, S = Storage, other values = Booking Reference\n")

    # Define the row numbers used in this seating layout
    rows = [1, 2, 3, 4, 5]

    # Define the seat letters used in each row
    columns = ["A", "B", "C", "D", "E", "F"]

    # Loop through each row
    for row in rows:
        row_display = []

        # Loop through each seat letter in the row
        for column in columns:
            seat_code = str(row) + column
            seat_status = seats[seat_code]

            # Create a display string such as 1A:F
            row_display.append(f"{seat_code}:{seat_status}")

        # Print one full row of the aircraft layout
        print("   ".join(row_display))


def main():
    """
    Main program function.

    This function controls the overall flow of the program.
    It:
    - creates the seat map
    - repeatedly shows the menu
    - runs the correct function based on user choice
    - stops only when the user selects the exit option
    """
    # Create the initial seating plan
    seats = create_seat_map()
    connection = create_database()
    create_bookings_table(connection)

    # Keep running until the user chooses to exit
    while True:
        # Display the menu each time the loop starts
        display_menu()

        # Ask the user for a menu choice
        choice = input("Enter your choice (1-5): ").strip()

        # Use selection statements to call the correct function
        if choice == "1":
            check_availability(seats)

        elif choice == "2":
            book_seat(seats, connection)

        elif choice == "3":
            free_seat(seats, connection)

        elif choice == "4":
            show_booking_status(seats)

        elif choice == "5":
            connection.close()
            print("Program terminated.")
            break

        else:
            # This message is shown if the input is not 1, 2, 3, 4, or 5
            print("Invalid choice. Please enter a number between 1 and 5.")


# This line ensures that the program starts by calling main()
# only when this file is run directly.
if __name__ == "__main__":
    main()

