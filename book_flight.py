import argparse as arg
import datetime as dt
import json
import requests as rq
import sys
import time


parser = arg.ArgumentParser()
parser.add_argument('--date', required=True)
parser.add_argument('--from', dest='flyFrom', required=True)
parser.add_argument('--to', dest='flyTo', required=True)
parser.add_argument('--one-way', dest='one_way', action='store_true', default=True)
parser.add_argument('--return', dest='days', type=int)
parser.add_argument('--cheapest', action='store_true')
parser.add_argument('--fastest', action='store_true')
parser.add_argument('--bags', choices=[0, 1, 2], type=int, default=0)


class UnexpectedError(Exception):
    pass


def search_flight(new_search):
    """
    The function returns json with combinations from the search
    Default API parameter for 'sort' is 'price' and 'asc' = 1 - from cheapest flights to the most expensive
    If --fastest == True and --cheapest == True then 'sort' = 'duration'
    """
    try:
        # Check date format
        dt.datetime.strptime(new_search.date, '%Y-%m-%d')
    except ValueError:
        print('Error: Time data \'{}\' does not match format \'YYYY-MM-DD\'.'.format(new_search.date))
        sys.exit(1)
    else:
        if new_search.days < 0:
            # Check if number of days in destination is bigger or equal to 0
            print('Error: Number of days for \'--return\' has to be greater or equal to 0.')
            sys.exit(1)
        if dt.datetime.strptime(new_search.date, '%Y-%m-%d').date() == dt.datetime.now().date():
            # If date == today then departure date = now + 4h
            departure = dt.datetime.strftime(dt.datetime.now() + dt.timedelta(hours=4), '%d/%m/%Y')
        elif dt.datetime.strptime(new_search.date, '%Y-%m-%d') < dt.datetime.now():
            # Check if the selected date is not in the past
            print('Error: Departure date cannot be less than or equal current date.')
            sys.exit(1)
        else:
            departure = dt.datetime.strftime(dt.datetime.strptime(new_search.date, '%Y-%m-%d'), '%d/%m/%Y')
        params_optional = ''
        params_return = ''
        if new_search.days:
            # Calculation of the required return date
            duration = dt.timedelta(days=int(new_search.days))
            datetime_return = dt.datetime.strftime(dt.datetime.strptime(new_search.date, '%Y-%m-%d') + duration,
                                                   '%d/%m/%Y')
            params_return = '&returnFrom={}&returnTo={}'.format(datetime_return, datetime_return)
        if new_search.fastest:
            # Sort parameter modification for the fastest available combinations
            params_optional = '&sort=duration'
        url = 'https://api.skypicker.com/flights?'
        params = 'flyFrom={}&to={}&dateFrom={}&dateFrom={}{}{}'.format(new_search.flyFrom.upper(),
                                                                       new_search.flyTo.upper(), departure, departure,
                                                                       params_return, params_optional)
        search_json = rq.get(url + params).json()['data']
        return search_json


def check_flights(booking_token, new_search):
    """
    The function checks combination's availability
    """
    parameters = {'v': 2,
                  'pnum': 1,
                  'bnum': new_search.bags,
                  'booking_token': booking_token}
    response = rq.get('https://booking-api.skypicker.com/api/v0.1/check_flights', params=parameters).json()
    checked = response['flights_checked']
    invalid = response['flights_invalid']
    return checked, invalid


def save_booking(booking_token, new_search):
    """
    Book flight for the default passenger
    """
    data_json = {
            'bags': new_search.bags,
            'booking_token': booking_token,
            'currency': 'EUR',
            'passengers': [{'birthday': '1989-01-25',
                            'documentID': 'EH000000',
                            'email': 'martin.began@kiwi.com',
                            'firstName': 'test',
                            'lastName': 'test',
                            'title': 'Mr'}]}
    headers = {'Content-type': 'application/json'}
    url = 'http://128.199.48.38:8080/booking'
    response = rq.post(url, data=json.dumps(data_json), headers=headers).json()
    return response


if __name__ == '__main__':
    args = parser.parse_args()
    bags = args.bags
    combinations = search_flight(args)
    if len(combinations) == 0:
        print('No flight found, please try again.')
        sys.exit(0)
    if bags > 0:
        try:
            # Find booking with existing bag price for requested number of bags
            i = 0
            while str(bags) not in combinations[i]['bags_price'] and i < len(combinations):
                i += 1
            token = combinations[i]['booking_token']
        except IndexError:
            print('No suitable combination found for requested number of bags: {}'.format(args.bags))
            sys.exit(0)
    else:
        token = combinations[0]['booking_token']
    try:
        # Check and book the combination
        flight_checked, flight_invalid = False, False
        rep = 1
        while flight_checked is not True and flight_invalid is not True and rep < 50:
            flight_checked, flight_invalid = check_flights(combinations[rep]['booking_token'], args)
            print('Checking flights... {}'.format(rep))
            rep += 1
            if not flight_checked and not flight_invalid:
                time.sleep(5)
        if flight_checked == True and flight_invalid == False:
            booking = save_booking(token, args)
            print('Checked: {}'.format(flight_checked))
            print('Invalid: {}'.format(flight_invalid))
            print('PNR: {}'.format(booking['pnr']))
            print('Status: {}'.format(booking['status']))
        else:
            print('I was not able to check selected combination with Kiwi.com API :(.')
            print('Please try again later.')
            sys.exit(0)
    except UnexpectedError:
        print('Unknown Error.')
        sys.exit(1)
