"""ScenarioParserのユニットテスト."""

import sys
from pathlib import Path

import pytest

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from modules.scenario_parser import ScenarioParser


@pytest.fixture
def parser() -> ScenarioParser:
    """ScenarioParserのフィクスチャ.

    Returns:
        ScenarioParserインスタンス
    """
    return ScenarioParser()


@pytest.fixture
def sample_scenario_text() -> str:
    """サンプルシナリオテキストのフィクスチャ.

    Returns:
        シナリオテキスト
    """
    return """
現在（2025年10月21日 8時00分）のGOLD環境認識
日足ベースのサポートラインは4317近辺と4218近辺と4094近辺
週足ベースのサポートラインは4209近辺と3973近辺
月足ベースのサポートラインは4320近辺と3989近辺
日足ベースのレジスタンスラインは4418近辺と4540近辺
週足ベースのレジスタンスラインは4443近辺と4734近辺
4317近辺～4320近辺のサポート帯を下抜けなければ上昇トレンド継続
"""


class TestScenarioParser:
    """ScenarioParserクラスのテスト."""

    def test_parse_returns_parsed_scenario(
        self,
        parser: ScenarioParser,
        sample_scenario_text: str,
    ) -> None:
        """parseメソッドがParsedScenarioを返すことを確認."""
        result = parser.parse(sample_scenario_text)

        assert result is not None
        assert result.raw_text == sample_scenario_text

    def test_extract_symbol_gold(self, parser: ScenarioParser) -> None:
        """GOLDキーワードからGC=Fを抽出できることを確認."""
        text = "GOLDの分析です"
        symbol = parser._extract_symbol(text)

        assert symbol == "GC=F"

    def test_extract_date(self, parser: ScenarioParser) -> None:
        """日時を正しく抽出できることを確認."""
        text = "現在（2025年10月21日 8時00分）の分析"
        date = parser._extract_date(text)

        assert date == "2025-10-21 08:00"

    def test_extract_support_levels_daily(
        self,
        parser: ScenarioParser,
        sample_scenario_text: str,
    ) -> None:
        """日足サポートラインを正しく抽出できることを確認."""
        result = parser.parse(sample_scenario_text)
        daily_supports = [
            sl for sl in result.support_levels if sl.timeframe == "日足"
        ]

        assert len(daily_supports) == 3
        assert daily_supports[0].price == 4317
        assert daily_supports[1].price == 4218
        assert daily_supports[2].price == 4094

    def test_extract_resistance_levels_weekly(
        self,
        parser: ScenarioParser,
        sample_scenario_text: str,
    ) -> None:
        """週足レジスタンスラインを正しく抽出できることを確認."""
        result = parser.parse(sample_scenario_text)
        weekly_resistances = [
            rl for rl in result.resistance_levels if rl.timeframe == "週足"
        ]

        assert len(weekly_resistances) == 2
        assert weekly_resistances[0].price == 4443
        assert weekly_resistances[1].price == 4734

    def test_extract_support_zones(
        self,
        parser: ScenarioParser,
        sample_scenario_text: str,
    ) -> None:
        """サポートゾーンを正しく抽出できることを確認."""
        result = parser.parse(sample_scenario_text)

        assert len(result.support_zones) == 1
        assert result.support_zones[0].price_lower == 4317
        assert result.support_zones[0].price_upper == 4320

    def test_to_dict_returns_valid_dict(
        self,
        parser: ScenarioParser,
        sample_scenario_text: str,
    ) -> None:
        """to_dictメソッドが有効な辞書を返すことを確認."""
        result = parser.parse(sample_scenario_text)
        data = result.to_dict()

        assert isinstance(data, dict)
        assert "raw_text" in data
        assert "symbol" in data
        assert "support_levels" in data
        assert "resistance_levels" in data
        assert isinstance(data["support_levels"], list)

    def test_parse_empty_text(self, parser: ScenarioParser) -> None:
        """空のテキストでも正常に動作することを確認."""
        result = parser.parse("")

        assert result is not None
        assert len(result.support_levels) == 0
        assert len(result.resistance_levels) == 0

    def test_extract_notes_with_alert(self, parser: ScenarioParser) -> None:
        """急落警告を含むメモを抽出できることを確認."""
        text = "急落に注意してください"
        result = parser.parse(text)

        assert len(result.notes) > 0
        assert "急落に注意" in result.notes[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
