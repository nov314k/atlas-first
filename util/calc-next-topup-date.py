import datetime

ERR_MSG = 'Incorrect entry'


def process_topup():
    now = datetime.datetime.now()
    year = int(input(
            'Enter the year when the topup payment was made [4 digits]  : '))
    if year < now.year or year > 2020:
        raise Exception(ERR_MSG)
    month = int(input(
            'Enter the month when the topup payment was made [1-12]     : '))
    if month < 1 or month > 12:
        raise Exception(ERR_MSG)
    day = int(input(
            'Enter the day when the topup payment was made [1-31]       : '))
    if day < 1 or day > 31:
        raise Exception(ERR_MSG)
    sim = int(input(
            'Enter the code of the topped-up SIM [1=m:tel, 2=BH Telecom]: '))
    if sim not in [1, 2]:
        raise Exception(ERR_MSG)
    amount = float(input(
            'Enter the topup amount                                     : '))
    topup_expiry_days_margin = 1
    disconnection_grace_days_margin = 30
    topup_date = datetime.date(year, month, day)
    if sim == 2:
        sim_label = 'bhtel'
        disconnection_grace_days = 90
        if amount <= 0.99:
            topup_expiry_days = 0
        elif 1.00 <= amount <= 2.99:
            topup_expiry_days = 7
        elif 3.00 <= amount <= 4.99:
            topup_expiry_days = 10
        elif 5.00 <= amount <= 9.99:
            topup_expiry_days = 30
        elif 10.00 <= amount <= 19.99:
            topup_expiry_days = 90
        elif amount >= 20.00:
            topup_expiry_days = 180
        recommended_next_topup_date = topup_date \
            + datetime.timedelta(
                topup_expiry_days + disconnection_grace_days
                - disconnection_grace_days_margin)
    else:
        sim_label = 'mtel'
        disconnection_grace_days = 120
        if 2.00 <= amount <= 2.99:
            topup_expiry_days = 7
        elif 3.00 <= amount <= 3.99:
            topup_expiry_days = 10
        elif 4.00 <= amount <= 4.99:
            topup_expiry_days = 15
        elif 5.00 <= amount <= 9.99:
            topup_expiry_days = 25
        elif 10.00 <= amount <= 19.99:
            topup_expiry_days = 90
        elif 20.00 <= amount <= 29.99:
            topup_expiry_days = 90
        elif 30.00 <= amount <= 49.99:
            topup_expiry_days = 120
        elif amount >= 50.00:
            topup_expiry_days = 150
        recommended_next_topup_date = topup_date \
            + datetime.timedelta(topup_expiry_days - topup_expiry_days_margin)
    print('Your new topup task is: ')
    print(
        '- due:'
        + str(recommended_next_topup_date)
        + ' Top up SIM'
        + str(sim)
        + ' ('
        + sim_label
        + '). ZZD (manually) dur:20 +periodic')
    with open(sim_label + '.csv', 'a', newline='') as f:
        f.write('{:%d-%b-%Y},{:.2f}\n'.format(topup_date, amount))


if __name__ == '__main__':
    process_topup()
