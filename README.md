# Search & Book Application

**Event:** Python Weekend  
**Date:** 23-25 FEB 2018  
**Autor:** Martin Began  
[Task Description](https://engeto.online/study/lesson/_wl9/unit/_36ZR)

***

## Description  
This program consists of three main functions and eight arguments:

*  `def search_flight(new_search)`  
*  `def check_flight(booking_token, new_search)`  
*  `def save_booking(booking_token, new_search)`  
***
*  `--date` - **mendatory parameter**, input format: 'YYYY-MM-DD'
*  `--from` - **mendatory parameter**, input format: [IATA](https://en.wikipedia.org/wiki/IATA_airport_code)
*  `--to` - **mendatory parameter**, input format: [IATA](https://en.wikipedia.org/wiki/IATA_airport_code)
*  `--one-way` - optional parameter, boolean, default: True
*  `--return` - optional parameter, input format: *int*
*  `--cheapest` - optional parameter, boolean
*  `--fastest` - optional parameter, boolean
*  `--bags` - optional parameter, input format: *int* 0, 1 or 2, default: 0
***
1. The program will search for a flight or combinations based on input parameters.  
2. It will finds first suitable combination from [https://api.skypicker.com/flights?](https://api.skypicker.com/flights?). If `--bags` were selected, it will finds first combination with existing baggage price.  
3. Based on booking_token from the most suitable combination, the program will check selected combination with [https://booking-api.skypicker.com/api/v0.1/check_flights](https://booking-api.skypicker.com/api/v0.1/check_flights) while required parameters 'flights_checked' is not True and 'flights_invalid' is not False  
4. After successful check, [https://booking-api.skypicker.com/api/v0.1/check_flights](https://booking-api.skypicker.com/api/v0.1/check_flights) is called and the combination is booked  

## Behaviour
