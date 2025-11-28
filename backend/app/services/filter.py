"""Filtering service for tender announcements."""
import logging
import re
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class FilterService:
    """Service for filtering tender announcements based on rules."""

    @staticmethod
    def apply_filters(
        title: str,
        content: str,
        filter_rules: Optional[Dict[str, Any]],
    ) -> tuple[bool, Optional[str]]:
        """
        Apply filter rules to tender announcement.

        Args:
            title: Tender title
            content: Tender content
            filter_rules: Filter rules dictionary

        Returns:
            Tuple of (is_filtered, filter_reason)
            - is_filtered: True if item should be filtered out
            - filter_reason: Reason for filtering, or None if not filtered

        Filter rules format:
        {
            "include_keywords": ["keyword1", "keyword2"],  # Must contain at least one
            "exclude_keywords": ["keyword3", "keyword4"],  # Must not contain any
            "title_include": ["keyword5"],  # Title must contain at least one
            "title_exclude": ["keyword6"],  # Title must not contain any
            "min_budget": 100000,  # Minimum budget (optional, requires extraction first)
            "max_budget": 5000000,  # Maximum budget (optional)
        }
        """
        if not filter_rules:
            return False, None

        combined_text = f"{title} {content}".lower()

        # Check exclude keywords (in title or content)
        exclude_keywords = filter_rules.get("exclude_keywords", [])
        for keyword in exclude_keywords:
            if keyword.lower() in combined_text:
                return True, f"Contains excluded keyword: {keyword}"

        # Check title exclude keywords
        title_exclude = filter_rules.get("title_exclude", [])
        for keyword in title_exclude:
            if keyword.lower() in title.lower():
                return True, f"Title contains excluded keyword: {keyword}"

        # Check include keywords (must have at least one)
        include_keywords = filter_rules.get("include_keywords", [])
        if include_keywords:
            has_keyword = any(keyword.lower() in combined_text for keyword in include_keywords)
            if not has_keyword:
                return True, f"Does not contain any required keywords: {include_keywords}"

        # Check title include keywords
        title_include = filter_rules.get("title_include", [])
        if title_include:
            has_keyword = any(keyword.lower() in title.lower() for keyword in title_include)
            if not has_keyword:
                return True, f"Title does not contain required keywords: {title_include}"

        return False, None

    @staticmethod
    def apply_budget_filters(
        budget_amount: Optional[float],
        filter_rules: Optional[Dict[str, Any]],
    ) -> tuple[bool, Optional[str]]:
        """
        Apply budget-based filters.

        Args:
            budget_amount: Extracted budget amount
            filter_rules: Filter rules dictionary

        Returns:
            Tuple of (is_filtered, filter_reason)
        """
        if not filter_rules or budget_amount is None:
            return False, None

        # Check minimum budget
        min_budget = filter_rules.get("min_budget")
        if min_budget is not None and budget_amount < min_budget:
            return True, f"Budget {budget_amount} below minimum {min_budget}"

        # Check maximum budget
        max_budget = filter_rules.get("max_budget")
        if max_budget is not None and budget_amount > max_budget:
            return True, f"Budget {budget_amount} above maximum {max_budget}"

        return False, None


# Create singleton instance
filter_service = FilterService()
