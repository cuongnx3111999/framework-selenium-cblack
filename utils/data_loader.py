import os
import json
import pandas as pd
from typing import List, Dict, Any, Union


class DataLoader:
    """
    Lớp tiện ích để đọc dữ liệu test từ các file Excel, CSV và JSON
    """

    def __init__(self, base_path: str = None):
        """
        Khởi tạo DataLoader với đường dẫn cơ sở tùy chọn

        Args:
            base_path: Đường dẫn cơ sở cho các file dữ liệu (mặc định là thư mục data/ trong dự án)
        """
        # Nếu không có base_path, sử dụng thư mục data/ trong dự án
        if base_path is None:
            # Lấy đường dẫn tuyệt đối của thư mục chứa file hiện tại
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Lấy đường dẫn tuyệt đối của thư mục gốc dự án (lên 1 cấp từ utils/)
            project_root = os.path.dirname(current_dir)
            # Đường dẫn đến thư mục data/
            self.base_path = os.path.join(project_root, 'data')
        else:
            self.base_path = base_path

        # Tạo các thư mục con nếu chưa tồn tại
        for subdir in ['csv', 'excel', 'json']:
            dir_path = os.path.join(self.base_path, subdir)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def _validate_file_path(self, file_path: str) -> str:
        """
        Xác thực và trả về đường dẫn đầy đủ của file

        Args:
            file_path: Đường dẫn tương đối hoặc tuyệt đối đến file

        Returns:
            Đường dẫn đầy đủ đến file

        Raises:
            FileNotFoundError: Nếu file không tồn tại
        """
        # Nếu đường dẫn là tương đối, thêm base_path vào trước
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.base_path, file_path)

        # Kiểm tra xem file có tồn tại không
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File không tồn tại: {file_path}")

        return file_path

    def load_excel(self, file_path: str, sheet_name: str = 0) -> List[Dict[str, Any]]:
        """
        Đọc dữ liệu từ file Excel

        Args:
            file_path: Đường dẫn đến file Excel
            sheet_name: Tên hoặc index của sheet (mặc định là sheet đầu tiên)

        Returns:
            List các dict, mỗi dict đại diện cho một hàng dữ liệu
        """
        # Xác thực đường dẫn file
        full_path = self._validate_file_path(file_path)

        # Đọc file Excel vào DataFrame
        df = pd.read_excel(full_path, sheet_name=sheet_name)

        # Chuyển DataFrame thành list các dict
        return df.fillna('').to_dict('records')

    def load_csv(self, file_path: str, delimiter: str = ',', encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """
        Đọc dữ liệu từ file CSV

        Args:
            file_path: Đường dẫn đến file CSV
            delimiter: Ký tự phân tách các trường trong file (mặc định là dấu phẩy)
            encoding: Mã hóa của file (mặc định là UTF-8)

        Returns:
            List các dict, mỗi dict đại diện cho một hàng dữ liệu
        """
        # Xác thực đường dẫn file
        full_path = self._validate_file_path(file_path)

        # Đọc file CSV vào DataFrame
        df = pd.read_csv(full_path, delimiter=delimiter, encoding=encoding)

        # Chuyển DataFrame thành list các dict
        return df.fillna('').to_dict('records')

    def load_json(self, file_path: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Đọc dữ liệu từ file JSON

        Args:
            file_path: Đường dẫn đến file JSON

        Returns:
            Dữ liệu từ file JSON dưới dạng dict hoặc list
        """
        # Xác thực đường dẫn file
        full_path = self._validate_file_path(file_path)

        # Đọc file JSON
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def save_to_excel(self, data: List[Dict[str, Any]], file_path: str, sheet_name: str = 'Sheet1') -> str:
        """
        Lưu dữ liệu vào file Excel

        Args:
            data: List các dict chứa dữ liệu cần lưu
            file_path: Đường dẫn đến file Excel
            sheet_name: Tên của sheet (mặc định là 'Sheet1')

        Returns:
            Đường dẫn đầy đủ của file đã lưu
        """
        # Nếu đường dẫn là tương đối, thêm base_path vào trước
        if not os.path.isabs(file_path):
            # Đảm bảo thư mục cha tồn tại
            dir_name = os.path.dirname(os.path.join(self.base_path, file_path))
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            file_path = os.path.join(self.base_path, file_path)

        # Chuyển dữ liệu thành DataFrame và lưu vào file Excel
        df = pd.DataFrame(data)
        df.to_excel(file_path, sheet_name=sheet_name, index=False)

        return file_path

    def save_to_csv(self, data: List[Dict[str, Any]], file_path: str, delimiter: str = ',',
                    encoding: str = 'utf-8') -> str:
        """
        Lưu dữ liệu vào file CSV

        Args:
            data: List các dict chứa dữ liệu cần lưu
            file_path: Đường dẫn đến file CSV
            delimiter: Ký tự phân tách các trường trong file (mặc định là dấu phẩy)
            encoding: Mã hóa của file (mặc định là UTF-8)

        Returns:
            Đường dẫn đầy đủ của file đã lưu
        """
        # Nếu đường dẫn là tương đối, thêm base_path vào trước
        if not os.path.isabs(file_path):
            # Đảm bảo thư mục cha tồn tại
            dir_name = os.path.dirname(os.path.join(self.base_path, file_path))
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            file_path = os.path.join(self.base_path, file_path)

        # Chuyển dữ liệu thành DataFrame và lưu vào file CSV
        df = pd.DataFrame(data)
        df.to_csv(file_path, sep=delimiter, encoding=encoding, index=False)

        return file_path

    def save_to_json(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], file_path: str) -> str:
        """
        Lưu dữ liệu vào file JSON

        Args:
            data: Dữ liệu cần lưu (dict hoặc list)
            file_path: Đường dẫn đến file JSON

        Returns:
            Đường dẫn đầy đủ của file đã lưu
        """
        # Nếu đường dẫn là tương đối, thêm base_path vào trước
        if not os.path.isabs(file_path):
            # Đảm bảo thư mục cha tồn tại
            dir_name = os.path.dirname(os.path.join(self.base_path, file_path))
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            file_path = os.path.join(self.base_path, file_path)

        # Lưu dữ liệu vào file JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return file_path
