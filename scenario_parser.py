"""シナリオテキスト解析モジュール.

投資家が記述した分析シナリオから、サポート/レジスタンスライン、
重要価格帯、予測シナリオなどを抽出する。
"""

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class PriceLevel:
    """価格レベル（サポート/レジスタンス）を表すクラス."""

    price: float
    level_type: str  # "support" or "resistance"
    timeframe: str  # "日足", "週足", "月足"
    description: str = ""


@dataclass
class PriceZone:
    """重要価格帯を表すクラス."""

    price_lower: float
    price_upper: float
    zone_type: str  # "support_zone" or "resistance_zone"
    description: str = ""


@dataclass
class TrendLine:
    """トレンドライン・予測を表すクラス."""

    start_price: float
    end_price: float
    start_time: str = ""
    end_time: str = ""
    description: str = ""


@dataclass
class ParsedScenario:
    """解析されたシナリオデータを格納するクラス."""

    raw_text: str
    symbol: str = ""
    analysis_date: str = ""
    support_levels: list[PriceLevel] = None
    resistance_levels: list[PriceLevel] = None
    support_zones: list[PriceZone] = None
    resistance_zones: list[PriceZone] = None
    trend_lines: list[TrendLine] = None
    notes: list[str] = None

    def __post_init__(self) -> None:
        """初期化後処理でリストを空リストに設定."""
        if self.support_levels is None:
            self.support_levels = []
        if self.resistance_levels is None:
            self.resistance_levels = []
        if self.support_zones is None:
            self.support_zones = []
        if self.resistance_zones is None:
            self.resistance_zones = []
        if self.trend_lines is None:
            self.trend_lines = []
        if self.notes is None:
            self.notes = []

    def to_dict(self) -> dict[str, Any]:
        """辞書形式に変換（JSON保存用）."""
        return {
            "raw_text": self.raw_text,
            "symbol": self.symbol,
            "analysis_date": self.analysis_date,
            "support_levels": [
                {
                    "price": sl.price,
                    "level_type": sl.level_type,
                    "timeframe": sl.timeframe,
                    "description": sl.description,
                }
                for sl in self.support_levels
            ],
            "resistance_levels": [
                {
                    "price": rl.price,
                    "level_type": rl.level_type,
                    "timeframe": rl.timeframe,
                    "description": rl.description,
                }
                for rl in self.resistance_levels
            ],
            "support_zones": [
                {
                    "price_lower": sz.price_lower,
                    "price_upper": sz.price_upper,
                    "zone_type": sz.zone_type,
                    "description": sz.description,
                }
                for sz in self.support_zones
            ],
            "resistance_zones": [
                {
                    "price_lower": rz.price_lower,
                    "price_upper": rz.price_upper,
                    "zone_type": rz.zone_type,
                    "description": rz.description,
                }
                for rz in self.resistance_zones
            ],
            "trend_lines": [
                {
                    "start_price": tl.start_price,
                    "end_price": tl.end_price,
                    "start_time": tl.start_time,
                    "end_time": tl.end_time,
                    "description": tl.description,
                }
                for tl in self.trend_lines
            ],
            "notes": self.notes,
        }


class ScenarioParser:
    """シナリオテキストを解析するクラス."""

    def __init__(self) -> None:
        """初期化."""
        # 価格抽出用の正規表現パターン
        self.price_pattern = re.compile(r"(\d{4,5}(?:\.\d{1,2})?)")

    def parse(self, text: str) -> ParsedScenario:
        """シナリオテキストを解析する.

        Args:
            text: 分析シナリオのテキスト

        Returns:
            解析結果を格納したParsedScenarioオブジェクト
        """
        scenario = ParsedScenario(raw_text=text)

        # 銘柄コードの抽出（例: GOLD, GC=F）
        scenario.symbol = self._extract_symbol(text)

        # 分析日時の抽出
        scenario.analysis_date = self._extract_date(text)

        # サポートラインの抽出
        scenario.support_levels = self._extract_support_levels(text)

        # レジスタンスラインの抽出
        scenario.resistance_levels = self._extract_resistance_levels(text)

        # サポートゾーンの抽出
        scenario.support_zones = self._extract_support_zones(text)

        # レジスタンスゾーンの抽出
        scenario.resistance_zones = self._extract_resistance_zones(text)

        # 重要メモの抽出
        scenario.notes = self._extract_notes(text)

        return scenario

    def _extract_symbol(self, text: str) -> str:
        """銘柄コードを抽出する.

        Args:
            text: 分析テキスト

        Returns:
            銘柄コード（例: "GC=F"）
        """
        # GOLDというキーワードがあればGC=Fを返す
        if "GOLD" in text.upper() or "ゴールド" in text:
            return "GC=F"

        # その他の通貨ペアも検出可能にする
        symbol_map = {
            "ドル円": "USDJPY=X",
            "ユーロドル": "EURUSD=X",
            "ポンドドル": "GBPUSD=X",
        }

        for key, value in symbol_map.items():
            if key in text:
                return value

        return "GC=F"  # デフォルト

    def _extract_date(self, text: str) -> str:
        """分析日時を抽出する.

        Args:
            text: 分析テキスト

        Returns:
            日時文字列
        """
        # 日付パターンの抽出（例: 2025年10月21日 8時00分）
        date_pattern = re.compile(
            r"(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2})時(\d{1,2})分"
        )
        match = date_pattern.search(text)

        if match:
            year, month, day, hour, minute = match.groups()
            return f"{year}-{month:0>2}-{day:0>2} {hour:0>2}:{minute:0>2}"

        return ""

    def _extract_support_levels(self, text: str) -> list[PriceLevel]:
        """サポートラインを抽出する.

        Args:
            text: 分析テキスト

        Returns:
            サポートラインのリスト
        """
        support_levels = []

        # 日足ベースのサポートライン
        daily_pattern = re.compile(
            r"日足ベースのサポートラインは([\d\.]+近辺(?:と[\d\.]+近辺)*)"
        )
        match = daily_pattern.search(text)
        if match:
            prices_text = match.group(1)
            prices = self.price_pattern.findall(prices_text)
            for price_str in prices:
                support_levels.append(
                    PriceLevel(
                        price=float(price_str),
                        level_type="support",
                        timeframe="日足",
                        description="日足ベースのサポート",
                    )
                )

        # 週足ベースのサポートライン
        weekly_pattern = re.compile(
            r"週足ベースのサポートラインは([\d\.]+近辺(?:と[\d\.]+近辺)*)"
        )
        match = weekly_pattern.search(text)
        if match:
            prices_text = match.group(1)
            prices = self.price_pattern.findall(prices_text)
            for price_str in prices:
                support_levels.append(
                    PriceLevel(
                        price=float(price_str),
                        level_type="support",
                        timeframe="週足",
                        description="週足ベースのサポート",
                    )
                )

        # 月足ベースのサポートライン
        monthly_pattern = re.compile(
            r"月足ベースのサポートラインは([\d\.]+近辺(?:と[\d\.]+近辺)*)"
        )
        match = monthly_pattern.search(text)
        if match:
            prices_text = match.group(1)
            prices = self.price_pattern.findall(prices_text)
            for price_str in prices:
                support_levels.append(
                    PriceLevel(
                        price=float(price_str),
                        level_type="support",
                        timeframe="月足",
                        description="月足ベースのサポート",
                    )
                )

        return support_levels

    def _extract_resistance_levels(self, text: str) -> list[PriceLevel]:
        """レジスタンスラインを抽出する.

        Args:
            text: 分析テキスト

        Returns:
            レジスタンスラインのリスト
        """
        resistance_levels = []

        # 日足ベースのレジスタンスライン
        daily_pattern = re.compile(
            r"日足ベースのレジスタンスラインは([\d\.]+近辺(?:と[\d\.]+近辺)*)"
        )
        match = daily_pattern.search(text)
        if match:
            prices_text = match.group(1)
            prices = self.price_pattern.findall(prices_text)
            for price_str in prices:
                resistance_levels.append(
                    PriceLevel(
                        price=float(price_str),
                        level_type="resistance",
                        timeframe="日足",
                        description="日足ベースのレジスタンス",
                    )
                )

        # 週足ベースのレジスタンスライン
        weekly_pattern = re.compile(
            r"週足ベースのレジスタンスラインは([\d\.]+近辺(?:と[\d\.]+近辺)*)"
        )
        match = weekly_pattern.search(text)
        if match:
            prices_text = match.group(1)
            prices = self.price_pattern.findall(prices_text)
            for price_str in prices:
                resistance_levels.append(
                    PriceLevel(
                        price=float(price_str),
                        level_type="resistance",
                        timeframe="週足",
                        description="週足ベースのレジスタンス",
                    )
                )

        return resistance_levels

    def _extract_support_zones(self, text: str) -> list[PriceZone]:
        """サポートゾーンを抽出する.

        Args:
            text: 分析テキスト

        Returns:
            サポートゾーンのリスト
        """
        support_zones = []

        # サポート帯のパターン（例: 4317近辺～4320近辺のサポート帯）
        zone_pattern = re.compile(r"([\d\.]+)近辺～([\d\.]+)近辺のサポート帯")
        matches = zone_pattern.finditer(text)

        for match in matches:
            lower = float(match.group(1))
            upper = float(match.group(2))
            support_zones.append(
                PriceZone(
                    price_lower=lower,
                    price_upper=upper,
                    zone_type="support_zone",
                    description=f"{lower}～{upper}のサポート帯",
                )
            )

        return support_zones

    def _extract_resistance_zones(self, text: str) -> list[PriceZone]:
        """レジスタンスゾーンを抽出する.

        Args:
            text: 分析テキスト

        Returns:
            レジスタンスゾーンのリスト
        """
        resistance_zones = []

        # レジスタンス帯のパターン
        zone_pattern = re.compile(r"([\d\.]+)近辺～([\d\.]+)近辺のレジスタンス帯")
        matches = zone_pattern.finditer(text)

        for match in matches:
            lower = float(match.group(1))
            upper = float(match.group(2))
            resistance_zones.append(
                PriceZone(
                    price_lower=lower,
                    price_upper=upper,
                    zone_type="resistance_zone",
                    description=f"{lower}～{upper}のレジスタンス帯",
                )
            )

        return resistance_zones

    def _extract_notes(self, text: str) -> list[str]:
        """重要なメモを抽出する.

        Args:
            text: 分析テキスト

        Returns:
            メモのリスト
        """
        notes = []

        # 急落の警告など重要なフレーズを抽出
        if "急落に注意" in text:
            notes.append("急落に注意が必要")

        if "上昇トレンド継続" in text:
            notes.append("上昇トレンド継続の可能性")

        return notes
