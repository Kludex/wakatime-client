from __future__ import annotations

from datetime import date
from typing import Any, Literal, TypeAlias

import httpx

Year: TypeAlias = str
"""YYYY format for year."""
YearMonth: TypeAlias = str
"""YYYY-MM format for year and month."""


class WakatimeClient:
    def __init__(self, api_key: str | None, base_url: str = "https://api.wakatime.com/api/v1/"):
        self.client = httpx.Client(base_url=base_url, headers={"Authorization": f"Basic {api_key}"})

    def projects(self, user: str = "current", q: str | None = None) -> Any:
        params = {"q": q} if q else None
        response = self.client.get(f"/users/{user}/projects", params=params)
        response.raise_for_status()
        return response.json()

    def all_time_since_today(self, user: str = "current", project: str | None = None) -> Any:
        params = {"project": project} if project else None
        response = self.client.get(f"/users/{user}/all_time_since_today", params=params)
        response.raise_for_status()
        return response.json()

    def program_languages(self) -> Any:
        response = self.client.get("/program_languages")
        response.raise_for_status()
        return response.json()

    def stats(
        self,
        user: str = "current",
        range: Year
        | YearMonth
        | Literal["last_7_days", "last_30_days", "last_6_months", "last_year", "all_time"] = "last_year",
        timeout: int | None = None,
        writes_only: bool | None = None,
    ) -> Any:
        """A user's coding activity for the given time range.

        Ref.: https://wakatime.com/developers#stats
        """
        params: dict[str, Any] = {}
        if timeout:
            params["timeout"] = timeout
        if writes_only is not None:
            params["writes_only"] = writes_only
        response = self.client.get(f"/users/{user}/stats/{range}", params=params)
        response.raise_for_status()
        return response.json()

    def durations(
        self,
        date: date,
        *,
        user: str = "current",
        project: str | None = None,
        branches: str | None = None,
        timeout: int | None = None,
        writes_only: bool | None = None,
        timezone: str | None = None,
        slice_by: Literal["entity", "language", "dependencies", "os", "editor", "category", "machine"] = "entity",
    ) -> Any:
        """A user's coding activity for the given day as an array of durations.

        Ref.: https://wakatime.com/developers#durations
        """
        params: dict[str, Any] = {"date": date}
        if project:
            params["project"] = project
        if branches:
            params["branches"] = branches
        if timeout:
            params["timeout"] = timeout
        if writes_only is not None:
            params["writes_only"] = writes_only
        if timezone:
            params["timezone"] = timezone
        params["slice_by"] = slice_by
        response = self.client.get(f"/users/{user}/durations", params=params)
        response.raise_for_status()
        return response.json()

    def insights(
        self,
        user: str = "current",
        insight_type: Literal[
            "weekday",
            "days",
            "best_day",
            "daily_average",
            "projects",
            "languages",
            "editors",
            "categories",
            "machines",
            "operating_systems",
        ] = "projects",
        range: Year
        | YearMonth
        | Literal["last_7_days", "last_30_days", "last_6_months", "last_year", "all_time"] = "last_year",
        timeout: int | None = None,
        writes_only: bool | None = None,
        weekday: int | None = None,
    ) -> Any:
        """An insight about the user’s coding activity for the given time range.

        Ref.: https://wakatime.com/developers#insights
        """
        params: dict[str, Any] = {}
        if timeout:
            params["timeout"] = timeout
        if writes_only is not None:
            params["writes_only"] = writes_only
        if weekday:
            params["weekday"] = weekday
        response = self.client.get(f"/users/{user}/insights/{insight_type}/{range}", params=params)
        response.raise_for_status()
        return response.json()

    def summaries(
        self,
        start: date,
        end: date,
        *,
        user: str = "current",
        project: str | None = None,
        branches: str | None = None,
        timeout: int | None = None,
        writes_only: bool | None = None,
        timezone: str | None = None,
        range: Literal[
            "Today",
            "Yesterday",
            "Last 7 Days",
            "Last 7 Days from Yesterday",
            "Last 14 Days",
            "Last 30 Days",
            "This Week",
            "Last Week",
            "Last Month",
        ] = "Last Month",
    ) -> Any:
        """A user's coding activity for the given time range as an array of summaries segmented by day.

        Ref.: https://wakatime.com/developers#summaries
        """
        params: dict[str, Any] = {"start": start, "end": end, "range": range}
        if project:
            params["project"] = project
        if branches:
            params["branches"] = branches
        if timeout:
            params["timeout"] = timeout
        if writes_only is not None:
            params["writes_only"] = writes_only
        if timezone:
            params["timezone"] = timezone
        response = self.client.get(f"/users/{user}/summaries", params=params)
        response.raise_for_status()
        return response.json()
