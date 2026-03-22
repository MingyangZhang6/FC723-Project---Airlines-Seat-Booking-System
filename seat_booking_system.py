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


def book_seat(seats):
    """
    Book a seat if it is free.

    The booking is only successful when:
    - the seat code is valid
    - the seat status is currently 'F'

    If the booking is successful, the seat status is changed
    from 'F' to 'R'.
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
        seats[seat_code] = "R"
        print(f"Seat {seat_code} has been successfully booked.")
    elif status == "R":
        print(f"Seat {seat_code} is already reserved.")
    elif status == "X":
        print(f"{seat_code} is an aisle and cannot be booked.")
    elif status == "S":
        print(f"{seat_code} is a storage area and cannot be booked.")


def free_seat(seats):
    """
    Free a previously reserved seat.

    A seat can only be freed if:
    - the seat code is valid
    - the seat status is currently 'R'

    If successful, the seat status is changed from 'R' to 'F'.
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

    # Only reserved seats can be freed
    if status == "R":
        seats[seat_code] = "F"
        print(f"Seat {seat_code} has been successfully freed.")
    elif status == "F":
        print(f"Seat {seat_code} is already free.")
    elif status == "X":
        print(f"{seat_code} is an aisle and cannot be changed.")
    elif status == "S":
        print(f"{seat_code} is a storage area and cannot be changed.")


def show_booking_status(seats):
    """
    Display the full seating layout of the aircraft.

    This allows the user to see the current booking status
    of all positions in the seating plan.
    """
    print("\n------------- Booking Status -------------")
    print("Legend: F = Free, R = Reserved, X = Aisle, S = Storage\n")

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
            book_seat(seats)

        elif choice == "3":
            free_seat(seats)

        elif choice == "4":
            show_booking_status(seats)

        elif choice == "5":
            print("Program terminated.")
            break

        else:
            # This message is shown if the input is not 1, 2, 3, 4, or 5
            print("Invalid choice. Please enter a number between 1 and 5.")


# This line ensures that the program starts by calling main()
# only when this file is run directly.
if __name__ == "__main__":
    main()

