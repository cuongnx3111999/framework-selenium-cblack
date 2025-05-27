import random
import string
import datetime
from faker import Faker
from typing import List, Dict, Any, Optional


class TestDataGenerator:
    """Lớp tiện ích để tạo dữ liệu test ngẫu nhiên"""

    def __init__(self, locale: str = 'en_US'):
        """
        Khởi tạo TestDataGenerator với locale chỉ định

        Args:
            locale: Locale để tạo dữ liệu theo ngôn ngữ và khu vực (mặc định là en_US)
        """
        self.faker = Faker(locale)

    def generate_user_data(self, count: int = 1, include_password: bool = True) -> List[Dict[str, str]]:
        """
        Tạo dữ liệu người dùng ngẫu nhiên

        Args:
            count: Số lượng bản ghi cần tạo
            include_password: Có tạo mật khẩu ngẫu nhiên hay không

        Returns:
            List các dict chứa dữ liệu người dùng
        """
        users = []

        for _ in range(count):
            user = {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name(),
                'username': self.faker.user_name(),
                'email': self.faker.email(),
                'phone': self.faker.phone_number(),
                'address': self.faker.address().replace('\n', ', ')
            }

            if include_password:
                user['password'] = self.generate_password()

            users.append(user)

        return users

    def generate_password(self, length: int = 10, include_special_chars: bool = True) -> str:
        """
        Tạo mật khẩu ngẫu nhiên

        Args:
            length: Độ dài của mật khẩu
            include_special_chars: Có bao gồm ký tự đặc biệt hay không

        Returns:
            Mật khẩu ngẫu nhiên
        """
        chars = string.ascii_letters + string.digits
        if include_special_chars:
            chars += string.punctuation

        return ''.join(random.choice(chars) for _ in range(length))

    def generate_product_data(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Tạo dữ liệu sản phẩm ngẫu nhiên

        Args:
            count: Số lượng sản phẩm cần tạo

        Returns:
            List các dict chứa dữ liệu sản phẩm
        """
        products = []

        for _ in range(count):
            product = {
                'product_id': self.faker.uuid4(),
                'name': self.faker.catch_phrase(),
                'description': self.faker.paragraph(),
                'price': round(random.uniform(10, 1000), 2),
                'category': random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports']),
                'stock': random.randint(0, 100),
                'rating': round(random.uniform(1, 5), 1)
            }

            products.append(product)

        return products

    def generate_date(self, start_date: Optional[datetime.date] = None,
                      end_date: Optional[datetime.date] = None) -> datetime.date:
        """
        Tạo ngày ngẫu nhiên trong khoảng thời gian cho trước

        Args:
            start_date: Ngày bắt đầu (mặc định là 5 năm trước)
            end_date: Ngày kết thúc (mặc định là ngày hiện tại)

        Returns:
            Ngày ngẫu nhiên
        """
        if start_date is None:
            start_date = datetime.date.today() - datetime.timedelta(days=365 * 5)

        if end_date is None:
            end_date = datetime.date.today()

        return self.faker.date_between(start_date=start_date, end_date=end_date)
