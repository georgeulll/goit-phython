from datetime import datetime, timedelta


WEEKDAYS = ("\nMonday", "\nTuesday", "\nWednesday", "\nThursday", "\nFriday")
USERS = [
    {"name": "Nickola", "birthday": datetime(year=1990, month=11, day=8).date()},
    {"name": "Elena", "birthday": datetime(
        year=1996, month=7, day=20).date()},
    {"name": "Natasha", "birthday": datetime(year=1954, month=3, day=3).date()},
    {"name": "Olga", "birthday": datetime(year=1958, month=11, day=9).date()},
    {"name": "Luba", "birthday": datetime(year=1998, month=11, day=10).date()},
]


def close_birthday_users(users, start, end):
    now = datetime.today().date()
    result = []
    for user in users:
        birthday = user["birthday"]
        birthday = birthday.replace(year=now.year)
        if start <= birthday <= end:
            result.append(user)
    return result


def get_birthdays_per_week(users):
    now = datetime.today().date()
    current_week_day = now.weekday()
    if current_week_day >= 5:
        start_date = now - timedelta(days=(7 - current_week_day))
    elif current_week_day == 0:
        start_date = now - timedelta(days=2)
    else:
        start_date = now
    days_ahead = 4 - current_week_day
    if days_ahead < 0:
        days_ahead += 7
    end_date = now + timedelta(days=days_ahead)
    birthday_users = close_birthday_users(
        users, start=start_date, end=end_date)
    weekday = None
    for user in sorted(
        birthday_users, key=lambda x: x["birthday"].replace(year=now.year)
    ):
        user_birthday = user["birthday"].replace(year=now.year).weekday()
        try:
            user_congratulation_day = WEEKDAYS[user_birthday]
        except IndexError:
            user_congratulation_day = WEEKDAYS[0]
        if weekday != user_congratulation_day:
            weekday = user_congratulation_day
            print(weekday,':',user["name"])


if __name__ == "__main__":
    get_birthdays_per_week(USERS)