import pytest
import pandas as pd
from typing import List, Dict, Any, Callable, Optional, Union


def csv_data_provider(file_path: str,
                      filter_func: Optional[Callable] = None,
                      test_name_column: str = 'testcase',
                      delimiter: str = ',',
                      encoding: str = 'utf-8'):
    """
    Decorator để cung cấp dữ liệu test từ file CSV

    Args:
        file_path: Đường dẫn đến file CSV
        filter_func: Hàm tùy chọn để lọc dữ liệu (nhận DataFrame làm tham số)
        test_name_column: Tên cột chứa tên testcase để hiển thị trong báo cáo
        delimiter: Ký tự phân tách các trường trong file
        encoding: Mã hóa của file

    Returns:
        Pytest parametrize decorator với dữ liệu từ file CSV
    """

    def decorator(test_function):
        # Đọc dữ liệu từ file CSV vào DataFrame
        from pathlib import Path
        base_dir = Path(__file__).parent.parent / 'data'
        full_path = base_dir / file_path

        df = pd.read_csv(full_path, delimiter=delimiter, encoding=encoding)

        # Áp dụng filter nếu có
        if filter_func:
            df = filter_func(df)

        # Chuyển DataFrame thành list các dict
        test_data = df.fillna('').to_dict('records')

        # Tạo parameter ids để hiển thị trong báo cáo test
        ids = [f"{i + 1}-{row.get(test_name_column, f'row{i + 1}')}"
               for i, row in enumerate(test_data)]

        # Áp dụng pytest.mark.parametrize cho hàm test
        return pytest.mark.parametrize('test_data', test_data, ids=ids)(test_function)

    return decorator


def excel_data_provider(file_path: str,
                        sheet_name: str = 0,
                        filter_func: Optional[Callable] = None,
                        test_name_column: str = 'testcase'):
    """
    Decorator để cung cấp dữ liệu test từ file Excel

    Args:
        file_path: Đường dẫn đến file Excel
        sheet_name: Tên hoặc index của sheet
        filter_func: Hàm tùy chọn để lọc dữ liệu (nhận DataFrame làm tham số)
        test_name_column: Tên cột chứa tên testcase để hiển thị trong báo cáo

    Returns:
        Pytest parametrize decorator với dữ liệu từ file Excel
    """

    def decorator(test_function):
        # Đọc dữ liệu từ file Excel vào DataFrame
        from pathlib import Path
        base_dir = Path(__file__).parent.parent / 'data'
        full_path = base_dir / file_path

        df = pd.read_excel(full_path, sheet_name=sheet_name)

        # Áp dụng filter nếu có
        if filter_func:
            df = filter_func(df)

        # Chuyển DataFrame thành list các dict
        test_data = df.fillna('').to_dict('records')

        # Tạo parameter ids để hiển thị trong báo cáo test
        ids = [f"{i + 1}-{row.get(test_name_column, f'row{i + 1}')}"
               for i, row in enumerate(test_data)]

        # Áp dụng pytest.mark.parametrize cho hàm test
        return pytest.mark.parametrize('test_data', test_data, ids=ids)(test_function)

    return decorator


def filter_by_category(category: Union[str, List[str]]):
    """
    Hàm tiện ích để tạo filter function dựa trên category

    Args:
        category: Tên category hoặc list các category để lọc

    Returns:
        Hàm filter nhận DataFrame làm tham số
    """

    def filter_func(df):
        if 'category' in df.columns:
            if isinstance(category, list):
                return df[df['category'].isin(category)]
            return df[df['category'] == category]
        return df

    return filter_func

def filter_by_expected_message(expected_message: Union[str, List[str]]):
    """
    Hàm tiện ích để tạo filter function dựa trên expected_message

    Args:
        expected_message: Tên expected_message hoặc list các expected_message để lọc

    Returns:
        Hàm filter nhận DataFrame làm tham số
    """

    def filter_func(df):
        if 'expected_message' in df.columns:
            if isinstance(expected_message, list):
                return df[df['expected_message'].isin(expected_message)]
            return df[df['expected_message'] == expected_message]
        return df

    return filter_func


def filter_by_expected_result(expected_result: str):
    """
    Hàm tiện ích để tạo filter function dựa trên expected_result

    Args:
        expected_result: Kết quả mong đợi để lọc (ví dụ: 'success', 'error')

    Returns:
        Hàm filter nhận DataFrame làm tham số
    """

    def filter_func(df):
        if 'expected_result' in df.columns:
            return df[df['expected_result'] == expected_result]
        return df

    return filter_func



# def filter_by_condition(condition: Callable):
#     """
#     Hàm tiện ích để tạo filter function dựa trên một điều kiện tùy chỉnh
#
#     Args:
#         condition: Hàm nhận một hàng DataFrame và trả về True/False
#
#     Returns:
#         Hàm filter nhận DataFrame làm tham số
#     """
#
#     def filter_func(df):
#         return df[df.apply(condition, axis=1)]
#
#     return filter_func
