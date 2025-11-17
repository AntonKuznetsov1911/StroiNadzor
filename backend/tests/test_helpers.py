"""
Тесты для вспомогательных утилит
"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal

from app.utils.helpers import (
    generate_unique_id,
    calculate_hash,
    format_file_size,
    parse_date_range,
    calculate_age_days,
    calculate_completion_percentage,
    truncate_text,
    extract_numbers,
    sanitize_filename,
    create_pagination_metadata,
    calculate_statistics,
    group_by_date,
    convert_decimal_to_float,
    chunk_list,
    calculate_expiry_status,
    format_currency
)


class TestGenerateUniqueID:
    """Тесты для generate_unique_id"""

    def test_generate_without_prefix(self):
        uid = generate_unique_id()
        assert isinstance(uid, str)
        assert len(uid) > 10

    def test_generate_with_prefix(self):
        uid = generate_unique_id("PRJ")
        assert uid.startswith("PRJ-")
        assert len(uid.split("-")) == 3

    def test_uniqueness(self):
        uid1 = generate_unique_id()
        uid2 = generate_unique_id()
        assert uid1 != uid2


class TestCalculateHash:
    """Тесты для calculate_hash"""

    def test_sha256(self):
        hash_val = calculate_hash("test", "sha256")
        assert len(hash_val) == 64
        # Повторный вызов должен дать тот же результат
        assert hash_val == calculate_hash("test", "sha256")

    def test_md5(self):
        hash_val = calculate_hash("test", "md5")
        assert len(hash_val) == 32

    def test_invalid_algorithm(self):
        with pytest.raises(ValueError):
            calculate_hash("test", "invalid")


class TestFormatFileSize:
    """Тесты для format_file_size"""

    def test_bytes(self):
        assert format_file_size(100) == "100.0 B"

    def test_kilobytes(self):
        assert format_file_size(1024) == "1.0 KB"

    def test_megabytes(self):
        assert format_file_size(1024 * 1024) == "1.0 MB"

    def test_gigabytes(self):
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"


class TestParseDateRange:
    """Тесты для parse_date_range"""

    def test_valid_dates(self):
        start, end = parse_date_range("2024-01-01", "2024-12-31")
        assert start == date(2024, 1, 1)
        assert end == date(2024, 12, 31)

    def test_none_dates(self):
        start, end = parse_date_range(None, None)
        assert start is None
        assert end is None

    def test_invalid_format(self):
        start, end = parse_date_range("invalid", "2024-12-31")
        assert start is None
        assert end == date(2024, 12, 31)


class TestCalculateAgeDays:
    """Тесты для calculate_age_days"""

    def test_today(self):
        today = datetime.now().date()
        assert calculate_age_days(today) == 0

    def test_yesterday(self):
        yesterday = datetime.now().date() - timedelta(days=1)
        assert calculate_age_days(yesterday) == 1

    def test_week_ago(self):
        week_ago = datetime.now().date() - timedelta(days=7)
        assert calculate_age_days(week_ago) == 7


class TestCalculateCompletionPercentage:
    """Тесты для calculate_completion_percentage"""

    def test_full_completion(self):
        assert calculate_completion_percentage(10, 10) == 100.0

    def test_partial_completion(self):
        assert calculate_completion_percentage(5, 10) == 50.0

    def test_zero_completion(self):
        assert calculate_completion_percentage(0, 10) == 0.0

    def test_zero_total(self):
        assert calculate_completion_percentage(0, 0) == 0.0


class TestTruncateText:
    """Тесты для truncate_text"""

    def test_short_text(self):
        text = "Short"
        assert truncate_text(text, 100) == "Short"

    def test_long_text(self):
        text = "A" * 200
        truncated = truncate_text(text, 100)
        assert len(truncated) == 100
        assert truncated.endswith("...")

    def test_custom_suffix(self):
        text = "A" * 200
        truncated = truncate_text(text, 100, suffix=">>")
        assert truncated.endswith(">>")


class TestExtractNumbers:
    """Тесты для extract_numbers"""

    def test_single_number(self):
        assert extract_numbers("Price: 100") == [100.0]

    def test_multiple_numbers(self):
        assert extract_numbers("Size: 10x20x30") == [10.0, 20.0, 30.0]

    def test_decimal_numbers(self):
        assert extract_numbers("Price: 99.99") == [99.99]

    def test_no_numbers(self):
        assert extract_numbers("No numbers here") == []


class TestSanitizeFilename:
    """Тесты для sanitize_filename"""

    def test_clean_filename(self):
        assert sanitize_filename("document.pdf") == "document.pdf"

    def test_invalid_characters(self):
        filename = 'file<name>:with|bad*chars.txt'
        sanitized = sanitize_filename(filename)
        assert '<' not in sanitized
        assert '>' not in sanitized
        assert ':' not in sanitized
        assert '|' not in sanitized
        assert '*' not in sanitized

    def test_empty_filename(self):
        assert sanitize_filename("") == "unnamed_file"


class TestCreatePaginationMetadata:
    """Тесты для create_pagination_metadata"""

    def test_first_page(self):
        meta = create_pagination_metadata(total=100, page=1, page_size=10)
        assert meta["total"] == 100
        assert meta["page"] == 1
        assert meta["pages"] == 10
        assert meta["has_next"] is True
        assert meta["has_prev"] is False

    def test_last_page(self):
        meta = create_pagination_metadata(total=100, page=10, page_size=10)
        assert meta["has_next"] is False
        assert meta["has_prev"] is True

    def test_middle_page(self):
        meta = create_pagination_metadata(total=100, page=5, page_size=10)
        assert meta["has_next"] is True
        assert meta["has_prev"] is True


class TestCalculateStatistics:
    """Тесты для calculate_statistics"""

    def test_valid_values(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        stats = calculate_statistics(values)
        assert stats["min"] == 1.0
        assert stats["max"] == 5.0
        assert stats["avg"] == 3.0
        assert stats["sum"] == 15.0
        assert stats["count"] == 5

    def test_empty_list(self):
        stats = calculate_statistics([])
        assert stats["min"] == 0.0
        assert stats["max"] == 0.0
        assert stats["count"] == 0


class TestGroupByDate:
    """Тесты для group_by_date"""

    def test_grouping(self):
        items = [
            {"created_at": datetime(2024, 1, 1), "value": 1},
            {"created_at": datetime(2024, 1, 1), "value": 2},
            {"created_at": datetime(2024, 1, 2), "value": 3},
        ]
        grouped = group_by_date(items)
        assert len(grouped) == 2
        assert len(grouped["2024-01-01"]) == 2
        assert len(grouped["2024-01-02"]) == 1


class TestConvertDecimalToFloat:
    """Тесты для convert_decimal_to_float"""

    def test_decimal_value(self):
        assert convert_decimal_to_float(Decimal("10.5")) == 10.5

    def test_dict_with_decimal(self):
        data = {"price": Decimal("99.99")}
        result = convert_decimal_to_float(data)
        assert result["price"] == 99.99
        assert isinstance(result["price"], float)

    def test_nested_structure(self):
        data = {
            "items": [
                {"price": Decimal("10.5")},
                {"price": Decimal("20.5")}
            ]
        }
        result = convert_decimal_to_float(data)
        assert all(isinstance(item["price"], float) for item in result["items"])


class TestChunkList:
    """Тесты для chunk_list"""

    def test_even_chunks(self):
        items = [1, 2, 3, 4, 5, 6]
        chunks = chunk_list(items, 2)
        assert len(chunks) == 3
        assert chunks == [[1, 2], [3, 4], [5, 6]]

    def test_uneven_chunks(self):
        items = [1, 2, 3, 4, 5]
        chunks = chunk_list(items, 2)
        assert len(chunks) == 3
        assert chunks[-1] == [5]


class TestCalculateExpiryStatus:
    """Тесты для calculate_expiry_status"""

    def test_no_expiry(self):
        assert calculate_expiry_status(None) == "no_expiry"

    def test_expired(self):
        past_date = datetime.now().date() - timedelta(days=1)
        assert calculate_expiry_status(past_date) == "expired"

    def test_expiring_soon(self):
        soon_date = datetime.now().date() + timedelta(days=15)
        assert calculate_expiry_status(soon_date, warning_days=30) == "expiring_soon"

    def test_valid(self):
        future_date = datetime.now().date() + timedelta(days=100)
        assert calculate_expiry_status(future_date, warning_days=30) == "valid"


class TestFormatCurrency:
    """Тесты для format_currency"""

    def test_rub(self):
        formatted = format_currency(Decimal("1000.50"), "RUB")
        assert "1,000.50" in formatted
        assert "₽" in formatted

    def test_usd(self):
        formatted = format_currency(Decimal("1000.00"), "USD")
        assert "$" in formatted

    def test_eur(self):
        formatted = format_currency(Decimal("1000.00"), "EUR")
        assert "€" in formatted
