import datetime as dt
from dateutil.relativedelta import relativedelta


class DateGenerator:
    td = dt.date.today()

    yesterday = td - dt.timedelta(days=1)
    minus_two_days = yesterday - dt.timedelta(days=1)
    minus_three_days = minus_two_days - dt.timedelta(days=1)

    first_day_of_month = dt.date.today().replace(day=1)
    first_day_of_the_post_month = first_day_of_month - relativedelta(months=1)
    first_day_of_the_year = first_day_of_month.replace(month=1)

    last_year_yesterday = yesterday - relativedelta(years=1)
    last_year_minus_two_days = minus_two_days - relativedelta(years=1)
    last_year_minus_three_days = minus_three_days - relativedelta(years=1)

    last_year_first_day_of_month = first_day_of_month - relativedelta(years=1)
    last_year_first_day_of_the_post_month = first_day_of_the_post_month - relativedelta(years=1)
    last_year_first_day_of_the_year = first_day_of_the_year - relativedelta(years=1)

    DATE_1 = (str(yesterday), str(minus_two_days), str(minus_three_days),
              str(first_day_of_the_post_month), str(last_year_yesterday),
              str(last_year_minus_two_days), str(last_year_minus_three_days),
              str(last_year_first_day_of_month),
              str(last_year_first_day_of_the_post_month))

    DATE_2 = (str(yesterday), str(first_day_of_month), str(first_day_of_the_post_month))

    DATE_3 = (str(yesterday), str(minus_two_days), str(minus_three_days), str(first_day_of_month),
              str(first_day_of_the_post_month), str(last_year_yesterday), str(last_year_minus_two_days),
              str(last_year_minus_three_days), str(last_year_first_day_of_month),
              str(last_year_first_day_of_the_post_month))
