"""Tests for TenderExtractModel."""
import pytest
from datetime import datetime
from app.schemas.tender import TenderExtractModel


class TestTenderExtractModel:
    """Test cases for TenderExtractModel."""

    def test_valid_data(self):
        """Test with valid data."""
        data = {
            "project_name": "办公设备采购",
            "budget_amount": 500000,
            "budget_currency": "CNY",
            "deadline": "2024-12-31T17:00:00",
            "contact_person": "张三",
            "contact_phone": "010-12345678",
            "contact_email": "test@example.com",
            "location": "北京市",
        }

        model = TenderExtractModel(**data)

        assert model.project_name == "办公设备采购"
        assert model.budget_amount == 500000
        assert model.budget_currency == "CNY"
        assert isinstance(model.deadline, datetime)
        assert model.contact_person == "张三"

    def test_budget_parsing(self):
        """Test budget amount parsing."""
        # Test integer
        model = TenderExtractModel(budget_amount=100000)
        assert model.budget_amount == 100000.0

        # Test float
        model = TenderExtractModel(budget_amount=100000.5)
        assert model.budget_amount == 100000.5

        # Test string with "万元"
        model = TenderExtractModel(budget_amount="50万元")
        assert model.budget_amount == 500000.0

        # Test string with commas
        model = TenderExtractModel(budget_amount="1,000,000元")
        assert model.budget_amount == 1000000.0

        # Test None
        model = TenderExtractModel(budget_amount=None)
        assert model.budget_amount is None

        # Test empty string
        model = TenderExtractModel(budget_amount="")
        assert model.budget_amount is None

    def test_optional_fields(self):
        """Test that all fields are optional."""
        model = TenderExtractModel()

        assert model.project_name is None
        assert model.budget_amount is None
        assert model.budget_currency == "CNY"  # Has default
        assert model.deadline is None
        assert model.contact_person is None

    def test_validation(self):
        """Test field validation."""
        # Negative budget should fail
        with pytest.raises(Exception):
            TenderExtractModel(budget_amount=-100)

        # Valid budget
        model = TenderExtractModel(budget_amount=0)
        assert model.budget_amount == 0
