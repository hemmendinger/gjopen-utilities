import datetime


def calculate_daily_brier_score(forecasts: list, answer_keys: dict):
    """
    :param forecasts:
    :param answer_keys: Dictionary with answer keys as keys and True or False as the values
    :return:
    """

    # timestamp formatted as  '2017-09-03T16:31:49Z'
    prev_dt = datetime.datetime.strptime(forecasts[0]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')

    for fc in forecasts:
        # see if date is equal to same day as prev, if
        pass


def score_forecast(forecast: dict, answer_key: dict):
    """
    Order is irrelevant.
    :param forecast:
    :param answer_key:
    :return:
    """
    # Converts string percent to decimal
    pct = lambda x: int(x.strip('%')) / 100

    score = 0

    for k in answer_key.keys():
        if answer_key[k] is False:
            score += (0 - pct(forecast[k]))**2
        else:
            score += (1 - pct(forecast[k]))**2

    return score


def score_ordered_forecast(forecast: dict, answer_key: dict, answer_order: dict):
    """
    :param forecast: {'answer a': 'value%', ...
    :param answer_key: {'answer a': True, ...
    :param answer_order: {1: 'answer a', 2: 'answer b', ...
    :return:
    """
    start = list()
    end = list()

    start_has_correct = True

    # Push keys in reverse order
    for n in range(len(answer_order), 0, -1):
        start.append(answer_order[n])

    pct_to_float = lambda x: int(x.strip('%')) / 100
    decimal_fc = {key: pct_to_float(val) for key,val in forecast.items()}

    if sum(decimal_fc.values()) != 1.0:
        print('Warning: forecast conversion to floats does not sum to 1.0 ---> ', sum(decimal_fc))

    popped_answer = start.pop()
    groups = 0
    score = 0
    while start:
        end.append(popped_answer)
        groups += 1

        # This should only trigger once, checks if correct answer
        if answer_key[popped_answer]:
            start_has_correct = False

        if start_has_correct:
            score += ((sum_from_keys(end, decimal_fc) - 0)**2 + (sum_from_keys(start, decimal_fc) - 1)**2)
        else:
            score += ((sum_from_keys(end, decimal_fc) - 1)**2 + (sum_from_keys(start, decimal_fc) - 0)**2)

        popped_answer = start.pop()

    return score / groups


def sum_from_keys(keys, lookup):

    return sum([lookup[k] for k in keys])


def question_daily_average(forecasts: list, info: dict):

    open_date = info['open'].date()
    close_date = info['close'].date()

    # No forecasts exist for days that have not happened
    if close_date > datetime.datetime.utcnow().date():
        close_date = datetime.datetime.utcnow().date()

    days = dict()

    date_keys = [open_date + datetime.timedelta(n) for n in range(int((close_date - open_date).days + 1))]
    days = {key: list() for key in date_keys}
    #print(days)

    for fc in forecasts:
        fc_date = datetime.datetime.strptime(fc['timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()
        days[fc_date].append(fc)

    #print(days)
    averages = list()

    pct = lambda x: int(x.strip('%')) / 100

    for date in date_keys:
        avg = dict()
        avg['forecasts'] = 0
        avg['date'] = date
        for ans in info['answers']:
            avg[ans] = 0

        for fc in days[date]:
            avg['forecasts'] += 1
            for ans in info['answers']:
                avg[ans] += pct(fc[ans])

        for ans in info['answers']:
            avg[ans] = avg[ans] / avg['forecasts']


        averages.append(avg)

    return averages


def get_user_forecasts(complete: list, username):
    forecasts = list()

    for fc in complete:
        if fc['username'] == username:
            forecasts.append(fc.copy())

    return forecasts
