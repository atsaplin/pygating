from datetime import datetime
from unittest.mock import Mock

import pytest

from src.pygating.gates import DateGate


class TestDateGate:
    # Gate is open when start_date and end_date are None
    def test_gate_open_when_dates_none(self):
        gate = DateGate()
        assert gate._check_gate() == True

    # Gate is open when current date is between start_date and end_date
    def test_gate_open_when_current_date_between_dates(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        gate = DateGate(start_date=start_date, end_date=end_date)

        gate._get_current_datetime = Mock(return_value=datetime(2022, 6, 5))
        assert gate._check_gate() == True

    # Gate is open when current date is equal to start_date or end_date
    def test_gate_open_when_current_date_equal_to_dates(self):
        current_date = datetime(2022, 6, 5)
        gate = DateGate(start_date=current_date, end_date=current_date)
        gate._get_current_datetime = Mock(return_value=current_date)
        assert gate._check_gate() == True

    # Gate is closed when current date is before start_date and end_date are defined
    def test_gate_closed_when_current_date_before_start_date(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        gate = DateGate(start_date=start_date, end_date=end_date)

        gate._get_current_datetime = Mock(return_value=datetime(2021, 6, 5))
        assert gate._check_gate() == False

    # Gate is closed when current date is after end_date and start_date are defined
    def test_gate_closed_when_current_date_after_end_date(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        gate = DateGate(start_date=start_date, end_date=end_date)

        gate._get_current_datetime = Mock(return_value=datetime(2024, 6, 5))
        assert gate._check_gate() == False

    # Gate is open when current date is equal to start_date or end_date and allow is False
    def test_gate_open_when_current_date_equal_to_dates_and_allow_false(self):
        current_date = datetime(2022, 6, 5)
        gate = DateGate(start_date=current_date, end_date=current_date, allow=False)
        gate._get_current_datetime = Mock(return_value=current_date)
        assert gate._check_gate() == True
        assert gate.check() == False

    # Test from_json with valid data
    def test_from_json_with_valid_data(self):
        json_data = {
            "start_date": "2022-01-01T00:00:00",
            "end_date": "2022-12-31T23:59:59",
            "allow": True,
        }
        gate = DateGate.from_json(json_data)
        assert gate.start_date == datetime(2022, 1, 1, 0, 0, 0)
        assert gate.end_date == datetime(2022, 12, 31, 23, 59, 59)
        assert gate.allow == True

    # Test from_json with missing dates
    def test_from_json_with_missing_dates(self):
        json_data = {"allow": False}
        with pytest.raises(ValueError):
            DateGate.from_json(json_data)

    # Test from_json with invalid date format raises ValueError
    def test_from_json_with_invalid_date_format_raises_value_error(self):
        json_data = {
            "start_date": "invalid_date",
            "end_date": "2022-12-31T23:59:59",
            "allow": True,
        }
        with pytest.raises(ValueError):
            DateGate.from_json(json_data)

        json_data = {
            "start_date": "2022-01-01T00:00:00",
            "end_date": "invalid_date",
            "allow": True,
        }
        with pytest.raises(ValueError):
            DateGate.from_json(json_data)

    # Gate is open when passed date is between start_date and end_date
    def test_gate_open_when_passed_date_between_dates(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        gate = DateGate(start_date=start_date, end_date=end_date)

        passed_date = datetime(2022, 6, 5)
        assert gate._check_gate(entity=passed_date) == True

    # Gate is closed when passed date is before start_date
    def test_gate_closed_when_passed_date_before_start_date(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        gate = DateGate(start_date=start_date, end_date=end_date)

        passed_date = datetime(2021, 6, 5)
        assert gate._check_gate(entity=passed_date) == False

    # Gate is closed when passed date is after end_date
    def test_gate_closed_when_passed_date_after_end_date(self):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        gate = DateGate(start_date=start_date, end_date=end_date)

        passed_date = datetime(2024, 6, 5)
        assert gate._check_gate(entity=passed_date) == False

    # Gate is open when passed date is equal to start_date or end_date
    def test_gate_open_when_passed_date_equal_to_dates(self):
        current_date = datetime(2022, 6, 5)
        gate = DateGate(start_date=current_date, end_date=current_date)
        assert gate._check_gate(entity=current_date) == True
