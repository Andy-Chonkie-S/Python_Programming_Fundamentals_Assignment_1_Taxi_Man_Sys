# Name: Andrew Sevilla
# Student ID: s2010815T
# Code problems / unmet requirements: Part 3 Items 5 has not been formatted correctly and is still a work in progress. I'm pretty sure I've handled all other bugs but I'd be lying if I said I was 100% certain that my code was watertight and I didn't expect a bug to pop-up like the Spanish Inquisition. Nobody expects that. Furthermore the book a trip function is monolithic and REALLY should be refactored into smaller sub-functions, and there are other parts that aren't elegant, like hard-coding of formatting numbers, etc. I could also go back and f string all outputs but I'm le tired.

# Analysis / Reflection of code explaining :- 
## 1) Design process: 
### a) How I came up with the program design : My program design was iterative. I didn't really draw up a design as I was working through each part as recommended. I had read through the full spec initially to get an overview of data structures and logic, but I had to go back and re-write pieces as I didn't know what I didn't know until I got onto working on it. Factor in time commitments from competing priorities and I would have liked to have spent more time ont it.
### b) How I started writing the code after the design process : I started with the variables and the menu ( and their functions) and some of the existing-data data structures that were required (i.e. location_list and existing_customers) and just went forward with the parts in order via the requirements. 
## 2) Challenges I met during code development : Where do I start... existing_customers had to be changed from a list to a dictionary, so I went back and had to re-write a fair chunk of code later in the process, I initially had the display_existing_data function consolidated and wracked my brains on how to differentiate the two dictionaries by reading their original variable names from the parent function, couldn't figure it out after ages (I'd moved onto other code), decided to split them into 2 (one for rates, one for location / customer names), worked out the wording for that, then realised I could just look at the numeric data to differentiate the rates from the customers after ages. I felt so dumb. Like trying to determine the load bearing capacity of a swallow..

#.. Figuring out how to call a dictionary within a dictionary as well..

#.. I had the discount multiplier logic coupled with the initial existing_customer data in one block and there was repeeating code and it wasn't elegant, so I FINALLY figured out I should have the code separated. That took me longer than I care to admit. Almost like trying to accept return of a parrot that was of the deceased variety..

# References: (Sources of info / websites / tools other than course contents directly under Canvas / Modules) : I used google to check how functions worked and to help when I got stuck but no code was borrowed. This is all my ugly code, and that's not up for debate / contradiction, no matter how silly one's walk is..

import sys

discount_multiplier = 0.10
distance_fee = 0.00
basic_fee = 4.20
calculated_cost =  0.00
length_of_border = 60
booking_history_width = 30
location_list = ['Melbourne','Chadstone', 'Clayton','Brighton', 'Fitzroy']
discount = 0.00
existing_customers = { 
    'Louis' : None, 
    'Ella' : None 
    }

rate_dict = {
    'standard' : 1.50,
    'peak' : 1.80,
    'weekends' : 2.00,
    'holiday' : 2.50
    }

# This menu function uses a case statement to allow easy selection of menu items. The display items use the same function but pass in differing variables and the function identifies which type of output to display depending on the data passed to it.

def menu ():
    menu_input = ''
    while (menu_input != '0'):
        sys.stdout.write('Welcome to the RMIT taxi management system!\n\n')
        sys.stdout.write(('#' * length_of_border) + '\n')
        sys.stdout.write('You can choose from the following options:\n')
        sys.stdout.write('1: Book a trip\n')
        sys.stdout.write('2: Add/update rate types and prices\n')
        sys.stdout.write('3: Display existing customers\n')
        sys.stdout.write('4: Display existing locations\n')
        sys.stdout.write('5: Display existing rate types\n')
        sys.stdout.write('6: Add new locations\n')
        sys.stdout.write('7: Display the most valuable customer\n')
        sys.stdout.write('8: Display a customer booking history\n')                        
        sys.stdout.write('0: Exit the program\n')
        sys.stdout.write(('#' * length_of_border) + '\n\n')
        sys.stdout.write('Choose one option: \n')
        menu_input = sys.stdin.readline().strip()

        match menu_input:
            case '1':
                book_a_trip(discount_multiplier, distance_fee, basic_fee, calculated_cost, length_of_border, existing_customers, location_list, discount, rate_dict) 
            case '2':
                add_update_rates(rate_dict)
            case '3':
                display_existing_data(existing_customers)
            case '4':
                display_existing_data(location_list)
            case '5':
                display_existing_data(rate_dict)
            case '6':
                add_new_locations(location_list)
            case '7':
                disp_most_valuable_cust(existing_customers) 
            case '8':                
                disp_cust_booking_hist(existing_customers, booking_history_width)

# This function receives the rate dictionary argument and updates the rate dictionary with names and amounts, only if the amounts are valid (i.e. > 0).

def add_update_rates(rate_dict):

    positive_rates_only_flag = False

    while not positive_rates_only_flag:

        sys.stdout.write('Please enter the list of rate name(s) to update the current list. The rate types must be entered as a list that separates by commas (e.g. metropolitan, deluxe, premium.)\n')
        rate_names_update = sys.stdin.readline().strip().split(',')

        rate_names_update = [rate_names.strip() for rate_names in rate_names_update]

        sys.stdout.write('\n\nNow please enter the list of rate amount(s) corresponding to the above list in that order. The rate amounts must also be entered as a list that separates by commas (e.g. 2.0, 2.5, 2.2.)\n')
        rate_amounts_update = sys.stdin.readline().strip().split(',')

        rate_amounts_update = [rate_amounts.strip() for rate_amounts in rate_amounts_update]
 
        # Try / Except block is used to determine whether the rate amounts are numbers. I believe the logic here could be improved as I had to use a break statement if an invalid number was detected, but I couldn't work that out.

        try:
            rate_dict_update = {
                rate_names_update[i]: float(rate_amounts_update[i]) for i in range(len(rate_names_update))
                }
            
            for i in rate_dict_update:
                if rate_dict_update[i] <= 0:
                    positive_rates_only_flag = False
                    sys.stdout.write('\nAn invalid rate amount was detetected please reenter the rate names and amounts.\n\n')
                    break
                else:
                    positive_rates_only_flag = True
        except Exception as e:
            sys.stdout.write('\nA rate amount that was entered was invalid. Please only enter valid rate amount numbers.\n\n' + str(e))

    rate_dict.update(rate_dict_update)
    sys.stdout.write('Updated rate list is : ' + str(rate_dict) + '\n\n')

    return rate_dict
 
# This function is used to display existing data. The function first checks if a list is passed to it, identifying that the data has come from the location list. If it's a dictionary and there are numbers in the values then it determines that the data passed to it is from the rates dictionary, if not it's from the existing customer list dictionary.

def display_existing_data(display_data):
    sys.stdout.write('\nThe list of data you requested to dispaly is as follows:-\n\n')

    if type(display_data) == list:
        sys.stdout.write('Here is the location list as requested: ' + str(display_data) + '\n\n')

    elif type(display_data) == dict:

        rate_dict_value_test = next(iter(display_data.values()))

        if type(rate_dict_value_test) == float:
            sys.stdout.write('Here are the rate types & rates requested:\n\n')
            sys.stdout.write('[')
            for i in display_data:
                sys.stdout.write('\'' + str(i) + '\' : ')
                sys.stdout.write('\'' + (str(format(display_data[i], '.2f'))) + '\'')
                if display_data[i] != (list(display_data.values())[-1]):
                    sys.stdout.write(', ')
            sys.stdout.write(']\n\n')            

        else:
            sys.stdout.write('Here is the customer list as requested: ' + str(list(display_data.keys())) +'\n\n')
 
# The function to add new locations actually lists 3 funny location names in Australia. Monty Python would be proud. It accepts a list of location names separated by commas, disregards commas, and checks to see if the locations already exist. There was no requirement to set the location to the capitalisation format, which was unfortunate, so whatever the user inputted was accepted verbatim and then this updated list is returned to the parent function.

def add_new_locations(location_list):

    sys.stdout.write('\nPlease enter the list of locations to update the current list. The locations must be entered as a list that separates by commas (e.g. Bummaroo, Humpybong, Mamungkukumpurangkuntjunya)\n')
    location_names_update = sys.stdin.readline().strip().split(',')

    existing_location_list = []

    for item in location_names_update:
        item = item.strip()
        if item not in location_list:
            location_list.append(item)
        else:
            existing_location_list.append(item)

    if existing_location_list:
        sys.stdout.write('\nThese locations are duplicates and have been omitted: ')
        for i in range(len(existing_location_list)):
            sys.stdout.write(existing_location_list[i])
            if i != (len(existing_location_list)-1):
                sys.stdout.write(', ')
        sys.stdout.write('.\n')

    sys.stdout.write('\nUpdated location list is : ' + str(location_list) + '\n\n')

    return location_list

# This function displays the most valuable customer by accepting the existing customer dictionary, creating a dictionary of the customer name keys from that dictionary and initialising their totals to 0. The totals from each of the bookings within the existing_customers dictionary is then summed to a variable and rounded off in case a float is created with excessive superfluous precision. The maximum value in this dictionary is identified and this along with the customer whose value this belongs to is printed.

def disp_most_valuable_cust(existing_customers):

    total_cost_dict = {}
    total_cost_dict = dict.fromkeys(existing_customers.keys(), 0)

    for customer_name in existing_customers.keys():

        sum_of_total_costs = 0.0

        if existing_customers[customer_name] != None:
            for bookings in existing_customers[customer_name].values():
 
                if 'total_cost' in bookings.keys():
                    sum_of_total_costs += bookings['total_cost']
                    total_cost_dict[customer_name] = round(sum_of_total_costs, 3)

    highest_total_cost = max(total_cost_dict.values())
    most_valuable_cust = {i for i in total_cost_dict if total_cost_dict[i] == highest_total_cost}

    sys.stdout.write('The most valuable customer(s) is/are: ' + (str(most_valuable_cust)[1:-1]) + ', with the highest total cost of: ' + str(format(highest_total_cost, '.2f')) + ' (AUD).\n\n')

# The display customer booking history function "works" but is not formatted correctly. Yes, I know, I'm a very naughty boy.

def disp_cust_booking_hist(existing_customers, booking_history_width):
    
    input_name = None

    while (input_name not in existing_customers):
        sys.stdout.write('Enter the name of the customer [e.g. Huong]:\n')
        input_name = sys.stdin.readline().strip()

    sys.stdout.write(f'\nThis is the booking history of {input_name}.\n')

    if existing_customers[input_name] != None:
        number_of_bookings = max(existing_customers[input_name])

        sys.stdout.write(' ' * booking_history_width)
        for booking_number in existing_customers[input_name]:
            sys.stdout.write('Booking ' + str(booking_number) + (' ' * (booking_history_width - 9)))

        sys.stdout.write('\nDeparture' + (' ' * (booking_history_width - 9)))

        booking_number = 1

        while booking_number < number_of_bookings + 1:
            departure_value = existing_customers[input_name][booking_number].get('departure')
            sys.stdout.write(str(departure_value) + (' ' * (booking_history_width - len(str(departure_value)))))
            booking_number += 1

        sys.stdout.write('\nDestination' + (' ' * (booking_history_width - 11)))

        booking_number = 1

        while booking_number < number_of_bookings + 1:
            destination_values = existing_customers[input_name][booking_number].get('destination')
            format_destinations = ', '.join(destination_values)
            sys.stdout.write(str(format_destinations) + (' ' * (booking_history_width - len(format_destinations))))
            booking_number += 1            

        sys.stdout.write('\nTotal Cost' + (' ' * (booking_history_width - 10)))

        booking_number = 1

        while booking_number < number_of_bookings + 1:
            total_value = existing_customers[input_name][booking_number].get('total_cost')
            sys.stdout.write(str(total_value) + (' ' * (booking_history_width - len(str(format(total_value, '.2f'))))))
            booking_number += 1

    sys.stdout.write('\n\n')    


# The () monolithic :( ) book a trip function accepts the existing data and updates the existing customer dictionary.

def book_a_trip(discount_multiplier, distance_fee, basic_fee, calculated_cost, length_of_border, existing_customers, location_list, discount, rate_dict):
    sys.stdout.write('Enter the name of the customer [e.g. Huong]:\n')
    input_name = sys.stdin.readline().strip()

    # Check that the name is alphabetic

    while (not input_name.isalpha()):
        sys.stdout.write('Please only enter alphabetic characters for the name of the customer [e.g. Huong]:\n')
        input_name = sys.stdin.readline().strip()

    existing_customer_flag = False

    # Check to see if customer is pre-existing for discount qualification / appending a new booking later

    if input_name in existing_customers:
        existing_customer_flag = True

    input_departure = None

    # Force selection of a valid (i.e. existing) location

    while (input_departure not in location_list):
        sys.stdout.write('Enter the departure location [enter a valid location only, e.g. Melbourne]:\n')
        input_departure = sys.stdin.readline().strip()

        if ((input_departure != None) and (input_departure not in location_list)):
            sys.stdout.write('The departure location is not valid. Please enter a valid location.\n\n')

    # Flag to check if user wants to enter multiple destinations
    multiple_destination_flag = 'y'
    # Variable to compare current destination with most recent to avoid user entering same location twice in a row
    previous_destination = None

    destination_list = []
    distance_list = []

    while multiple_destination_flag == 'y':
        input_destination = None

        #Loop while destination is invalid
        while (input_destination not in location_list or input_destination == input_departure):
            sys.stdout.write('Enter the destination location [enter a valid location only, e.g. Chadstone]:\n')
            input_destination = sys.stdin.readline().strip()

            if ((input_destination != None) and ((input_destination not in location_list) or (input_destination == input_departure) or (input_destination == previous_destination))):
                sys.stdout.write('The destination location is not valid. Please enter a valid location.\n\n')

        #Update previous destination to avoid location twice in a row issue
        previous_destination = input_destination
        valid_distance_flag = False

        #Loop while distance is invalid. Try / Except block used to ensure a valid number is entered for the distance when logic expecting a number isapplied. This logic ensures the distance is greater than 0.
        while (valid_distance_flag is False):
            sys.stdout.write('Enter the distance (km) [enter a positive number only, e.g. 12.5, 6.8]:\n')
            input_distance = sys.stdin.readline().strip()

            try:
                input_distance = float(input_distance)
                if (float(input_distance) > 0):
                    input_distance = float(round(input_distance, 3))
                    valid_distance_flag = True
            except Exception as e:
                valid_distance_flag = False
                sys.stdout.write('Distance needs to be a valid number. Please enter a valid distance.\n\n' + str(e) + '\n\n')

        destination_list.append(input_destination)
        distance_list.append(input_distance)

        sys.stdout.write('Do you want to enter another destination?\n')
        multiple_destination_flag = sys.stdin.readline().strip()

        #Loop until confirmation (or not) of entry of more destinations is received.
        while multiple_destination_flag not in ('y', 'n'):
            sys.stdout.write('The response is not valid. Do you want to enter another destination? (i.e. \'y\' or \'n\')\n')
            multiple_destination_flag = sys.stdin.readline().strip()

    input_rate_type = None

    #Loop until an existing rate is entered.
    while (input_rate_type not in rate_dict):
        sys.stdout.write('Enter the rate type [enter a valid type only, e.g. standard, peak, weekends, holiday]:\n')
        input_rate_type = sys.stdin.readline().strip()

        if (input_rate_type != None and input_rate_type not in rate_dict):
            sys.stdout.write('The rate type entered is invalid. Please enter a valid type only [i.e.standard, peak, weekends or holiday]: \n\n')

    #Calculate initial distance fee without discount
    distance_fee = rate_dict[input_rate_type] * input_distance

    booking_number = 1
    calculated_cost = 0

    #Determine how to update existing_customers dictionary as additional entry of data needs to be handled differently to new customer or customers used to initialise dictionary as  booking numbers may not have been set as keys yet.
    if (existing_customer_flag) and existing_customers.get(input_name) != None:
        booking_number = max(existing_customers[input_name]) + 1
        existing_customers[input_name][booking_number] =  { 'departure' : input_departure, 'destination' : destination_list, 'total_cost' : round(calculated_cost, 3) }
    else:
        existing_customers[input_name] = { booking_number : { 'departure' : input_departure, 'destination' : destination_list, 'total_cost' : round(calculated_cost, 3)} }                        

    #Apply discount to existing customers, or not.
    if (existing_customer_flag):
        discount = distance_fee * discount_multiplier
        calculated_cost = distance_fee - (discount)
    else:
        calculated_cost = distance_fee

    #Add the basic blanket fee to the total cost now to all
    calculated_cost += basic_fee

    #Update the existing_customers dictionary with this final total cost for booking
    existing_customers[input_name][booking_number]['total_cost'] = round(calculated_cost, 3)

    #Format & print final booking data
    sys.stdout.write(('-' * length_of_border) + '\n')
    sys.stdout.write((' ' * ((length_of_border // 2) - 6)) + 'Taxi Receipt\n')
    sys.stdout.write(('-' * length_of_border) + '\n')

    sys.stdout.write('Name:' + (' ' * ((length_of_border // 2) - 5)) + input_name + '\n')
    sys.stdout.write('Departure:' + (' ' * ((length_of_border // 2) - 10)) + input_departure + '\n')

    for (dest, dist) in zip (destination_list, distance_list):
        sys.stdout.write('Destination:' + (' ' * ((length_of_border // 2) - 12)) + dest + '\n')

        sys.stdout.write('Distance:' + (' ' * ((length_of_border // 2) - 9)) + str(format(dist, '.2f')) + ' (km)\n')

    sys.stdout.write('Rate:' + (' ' * ((length_of_border // 2) - 5)) + str(format(rate_dict[input_rate_type], '.2f')) + ' (AUD per km)\n')
    sys.stdout.write('Total Distance:' + (' ' * ((length_of_border // 2) - 15)) + str(format(input_distance, '.2f')) + ' (km)\n')
                 
    sys.stdout.write(('-' * length_of_border) + '\n')

    sys.stdout.write('Basic fee:' + (' ' * ((length_of_border // 2) - 10)) + str(format(basic_fee, '.2f')) + ' (AUD)\n')
    sys.stdout.write('Distance fee:' + (' ' * ((length_of_border // 2) - 13)) + str(format(distance_fee, '.2f')) + ' (AUD)\n')
    sys.stdout.write('Discount:' + (' ' * ((length_of_border // 2) - 9)) + str(format(discount, '.2f')) + ' (AUD)\n')

    sys.stdout.write(('-' * length_of_border) + '\n')

    sys.stdout.write('Total cost:' + (' ' * ((length_of_border // 2) - 11)) + str(format(calculated_cost, '.2f')) + ' (AUD)\n\n')

    return existing_customers

# Finally the menu function is called at the end, to ensure that all the other logic has been loaded.

menu()

