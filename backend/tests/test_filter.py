"""Tests for filter service."""
import pytest
from app.services.filter import filter_service


class TestFilterService:
    """Test cases for FilterService."""

    def test_no_filters(self):
        """Test with no filter rules."""
        is_filtered, reason = filter_service.apply_filters(
            title="Test title",
            content="Test content",
            filter_rules=None,
        )
        assert is_filtered is False
        assert reason is None

    def test_exclude_keywords(self):
        """Test exclude keywords filtering."""
        filter_rules = {
            "exclude_keywords": ["废标", "流标"],
        }

        # Should be filtered
        is_filtered, reason = filter_service.apply_filters(
            title="某项目废标公告",
            content="由于投标人不足，本项目废标",
            filter_rules=filter_rules,
        )
        assert is_filtered is True
        assert "废标" in reason

        # Should not be filtered
        is_filtered, reason = filter_service.apply_filters(
            title="某项目招标公告",
            content="欢迎投标",
            filter_rules=filter_rules,
        )
        assert is_filtered is False

    def test_include_keywords(self):
        """Test include keywords filtering."""
        filter_rules = {
            "include_keywords": ["软件", "系统"],
        }

        # Should not be filtered (has keyword)
        is_filtered, reason = filter_service.apply_filters(
            title="办公软件采购",
            content="采购办公软件",
            filter_rules=filter_rules,
        )
        assert is_filtered is False

        # Should be filtered (no keyword)
        is_filtered, reason = filter_service.apply_filters(
            title="办公家具采购",
            content="采购办公桌椅",
            filter_rules=filter_rules,
        )
        assert is_filtered is True

    def test_title_filters(self):
        """Test title-specific filters."""
        filter_rules = {
            "title_include": ["招标"],
            "title_exclude": ["废标"],
        }

        # Should not be filtered
        is_filtered, reason = filter_service.apply_filters(
            title="某项目招标公告",
            content="内容",
            filter_rules=filter_rules,
        )
        assert is_filtered is False

        # Should be filtered (no required keyword in title)
        is_filtered, reason = filter_service.apply_filters(
            title="某项目公告",
            content="招标内容",
            filter_rules=filter_rules,
        )
        assert is_filtered is True

        # Should be filtered (excluded keyword in title)
        is_filtered, reason = filter_service.apply_filters(
            title="某项目招标废标公告",
            content="内容",
            filter_rules=filter_rules,
        )
        assert is_filtered is True

    def test_budget_filters(self):
        """Test budget filtering."""
        filter_rules = {
            "min_budget": 100000,
            "max_budget": 1000000,
        }

        # Should not be filtered
        is_filtered, reason = filter_service.apply_budget_filters(
            budget_amount=500000,
            filter_rules=filter_rules,
        )
        assert is_filtered is False

        # Should be filtered (too low)
        is_filtered, reason = filter_service.apply_budget_filters(
            budget_amount=50000,
            filter_rules=filter_rules,
        )
        assert is_filtered is True

        # Should be filtered (too high)
        is_filtered, reason = filter_service.apply_budget_filters(
            budget_amount=2000000,
            filter_rules=filter_rules,
        )
        assert is_filtered is True

        # Should not be filtered (no budget)
        is_filtered, reason = filter_service.apply_budget_filters(
            budget_amount=None,
            filter_rules=filter_rules,
        )
        assert is_filtered is False
