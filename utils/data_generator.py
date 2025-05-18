import random
import string
import datetime


class DataGenerator:
    @staticmethod
    def random_string(length=10):
        """Generate a random string of fixed length."""
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def random_email(domain="example.com"):
        """Generate a random email address."""
        username = DataGenerator.random_string(8).lower()
        return f"{username}@{domain}"

    @staticmethod
    def random_password(length=12):
        """Generate a random password."""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def random_phone():
        """Generate a random phone number."""
        return f"+1{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"

    @staticmethod
    def random_date(start_date=None, end_date=None):
        """Generate a random date between start_date and end_date."""
        if not start_date:
            start_date = datetime.date(2000, 1, 1)
        if not end_date:
            end_date = datetime.date.today()

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_days = random.randrange(days_between_dates)
        return start_date + datetime.timedelta(days=random_days)
