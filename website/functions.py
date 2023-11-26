def get_datetime():
    from datetime import datetime

    now = datetime.now()

    now_format = f'{now.hour}:{now.minute}:{now.second} - {now.day}/{now.month}/{now.year}'

    return now_format