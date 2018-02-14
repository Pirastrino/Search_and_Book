# Search & Book Application

**Event:** Python Weekend  
**Date:** 23-25 FEB 2018  
**Autor:** Martin Began  
[Task Description](https://engeto.online/study/lesson/_wl9/unit/_36ZR)

## Description  
This program consists of three main functions and eight arguments:

*  `def search_flight(new_search)`  
*  `def check_flight(booking_token, new_search)`  
*  `def save_booking(booking_token, new_search)`  

***

*  `--date` - **mendatory parameter**, input format: 'YYYY-MM-DD'
*  `--from` - **mendatory parameter**, input format: [IATA](https://en.wikipedia.org/wiki/IATA_airport_code)
*  `--to` - **mendatory parameter**, input format: [IATA](https://en.wikipedia.org/wiki/IATA_airport_code)
*  `--one-way` - optional parameter, boolean, default: *True*
*  `--return` - optional parameter, input format: *int*
*  `--cheapest` - optional parameter, boolean
*  `--fastest` - optional parameter, boolean
*  `--bags` - optional parameter, input format: *int* 0, 1 or 2, default: 0  

***

1. The program will search for a flight or combinations based on input parameters.  
2. It will finds first suitable combination from [https://api.skypicker.com/flights?](https://api.skypicker.com/flights?). If `--bags` were selected, it will finds first combination with existing baggage price.  
3. Based on *booking_token*, the program will check selected combination with [https://booking-api.skypicker.com/api/v0.1/check_flights](https://booking-api.skypicker.com/api/v0.1/check_flights) while required parameters *'flights_checked'* is not *True* and *'flights_invalid'* is not *False*  
4. After successful check, [http://128.199.48.38:8080/booking](http://128.199.48.38:8080/booking) is called and the combination is booked  

## Behaviour
* `--from` and `--to` parameters accept any string but if selected destinations will not be in IATA format, no combination will be found. IATA code can be written with small letters as well (e.g. `--from PRG` and `--from prg` etc. are eqvivalent).  
* `--return` parameter has higher priority than default parameter `--one-way`, that means if both parameters were selected e.g. `--one-way --return 5` then a return combination will be booked
* `--fastest` parameter has higher priority than default parameter `--cheapest`, that means if both parameters were selected e.g. `--cheapest --fastest` then the fastest combination will be booked

**Please note that the cheapest price does not include baggage price. The cheapest flight is selected based on base flight/combination price (fare).**

**If `--date` is today then it will search for combinations with departure 'now + 4 hours'. That also means that if you search after 8PM then booked combination will have departure date of the first flight next day!**

**The program will try to check combination 50 times first and it will book the combination only if *flights_checked = True* and *flights_invalid = False*.**

**Successfully checked combination is booked by [http://128.199.48.38:8080/booking](http://128.199.48.38:8080/booking) API.**  
