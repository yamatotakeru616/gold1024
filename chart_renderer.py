"""チャート描画モジュール.

Plotlyを使用してローソク足チャートにシナリオ情報を
オーバーレイ表示する。
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scenario_parser import ParsedScenario


class ChartRenderer:
    """チャートを描画するクラス."""

    def __init__(self) -> None:
        """初期化."""
        # カラーテーマ
        self.colors = {
            "support_daily": "#2ecc71",  # 緑
            "support_weekly": "#27ae60",  # 濃い緑
            "support_monthly": "#16a085",  # さらに濃い緑
            "resistance_daily": "#e74c3c",  # 赤
            "resistance_weekly": "#c0392b",  # 濃い赤
            "resistance_monthly": "#a93226",  # さらに濃い赤
            "support_zone": "rgba(46, 204, 113, 0.2)",  # 半透明緑
            "resistance_zone": "rgba(231, 76, 60, 0.2)",  # 半透明赤
        }

    def create_chart(
        self,
        df: pd.DataFrame,
        scenario: ParsedScenario | None = None,
        title: str = "市場分析チャート",
    ) -> go.Figure:
        """チャートを作成する.

        Args:
            df: 市場データ（OHLCV）を含むDataFrame
            scenario: シナリオ解析結果（Noneの場合は市場データのみ）
            title: チャートのタイトル

        Returns:
            Plotly Figureオブジェクト
        """
        # サブプロットの作成（将来的にボリュームチャートも追加可能）
        fig = make_subplots(
            rows=1,
            cols=1,
            shared_xaxes=True,
            subplot_titles=[title],
        )

        # ローソク足チャートの追加
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="価格",
                increasing_line_color="#26a69a",
                decreasing_line_color="#ef5350",
            ),
            row=1,
            col=1,
        )

        # シナリオ情報をオーバーレイ
        if scenario:
            self._add_scenario_overlay(fig, scenario, df)

        # レイアウト設定
        fig.update_layout(
            title=title,
            yaxis_title="価格",
            xaxis_title="日時",
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            template="plotly_white",
            height=800,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.8)",
            ),
        )

        # X軸の設定（日時範囲の自動調整）
        fig.update_xaxes(
            rangeslider_visible=False,
            type="date",
        )

        return fig

    def _add_scenario_overlay(
        self,
        fig: go.Figure,
        scenario: ParsedScenario,
        df: pd.DataFrame,
    ) -> None:
        """シナリオ情報をチャートにオーバーレイする.

        Args:
            fig: Plotly Figure
            scenario: シナリオ解析結果
            df: 市場データ
        """
        # サポートレベルの追加
        for support in scenario.support_levels:
            color = self._get_support_color(support.timeframe)
            self._add_horizontal_line(
                fig,
                df,
                support.price,
                color,
                f"サポート ({support.timeframe}): {support.price}",
                support.description,
            )

        # レジスタンスレベルの追加
        for resistance in scenario.resistance_levels:
            color = self._get_resistance_color(resistance.timeframe)
            self._add_horizontal_line(
                fig,
                df,
                resistance.price,
                color,
                f"レジスタンス ({resistance.timeframe}): {resistance.price}",
                resistance.description,
            )

        # サポートゾーンの追加
        for zone in scenario.support_zones:
            self._add_price_zone(
                fig,
                df,
                zone.price_lower,
                zone.price_upper,
                self.colors["support_zone"],
                f"サポート帯: {zone.price_lower}-{zone.price_upper}",
            )

        # レジスタンスゾーンの追加
        for zone in scenario.resistance_zones:
            self._add_price_zone(
                fig,
                df,
                zone.price_lower,
                zone.price_upper,
                self.colors["resistance_zone"],
                f"レジスタンス帯: {zone.price_lower}-{zone.price_upper}",
            )

    def _get_support_color(self, timeframe: str) -> str:
        """時間枠に応じたサポートラインの色を取得.

        Args:
            timeframe: 時間枠（日足、週足、月足）

        Returns:
            色コード
        """
        if "月足" in timeframe:
            return self.colors["support_monthly"]
        elif "週足" in timeframe:
            return self.colors["support_weekly"]
        else:
            return self.colors["support_daily"]

    def _get_resistance_color(self, timeframe: str) -> str:
        """時間枠に応じたレジスタンスラインの色を取得.

        Args:
            timeframe: 時間枠（日足、週足、月足）

        Returns:
            色コード
        """
        if "月足" in timeframe:
            return self.colors["resistance_monthly"]
        elif "週足" in timeframe:
            return self.colors["resistance_weekly"]
        else:
            return self.colors["resistance_daily"]

    def _add_horizontal_line(
        self,
        fig: go.Figure,
        df: pd.DataFrame,
        price: float,
        color: str,
        name: str,
        description: str,
    ) -> None:
        """水平線を追加する.

        Args:
            fig: Plotly Figure
            df: 市場データ
            price: 価格
            color: 線の色
            name: 線の名前
            description: 詳細説明
        """
        fig.add_trace(
            go.Scatter(
                x=[df.index[0], df.index[-1]],
                y=[price, price],
                mode="lines",
                line=dict(color=color, width=2, dash="dash"),
                name=name,
                hovertemplate=f"<b>{name}</b><br>{description}<br>価格: %{{y:.2f}}<extra></extra>",
                showlegend=True,
            )
        )

    def _add_price_zone(
        self,
        fig: go.Figure,
        df: pd.DataFrame,
        price_lower: float,
        price_upper: float,
        color: str,
        name: str,
    ) -> None:
        """価格帯（ゾーン）を追加する.

        Args:
            fig: Plotly Figure
            df: 市場データ
            price_lower: 下限価格
            price_upper: 上限価格
            color: ゾーンの色
            name: ゾーンの名前
        """
        fig.add_trace(
            go.Scatter(
                x=[df.index[0], df.index[-1], df.index[-1], df.index[0], df.index[0]],
                y=[
                    price_lower,
                    price_lower,
                    price_upper,
                    price_upper,
                    price_lower,
                ],
                fill="toself",
                fillcolor=color,
                line=dict(width=0),
                name=name,
                hovertemplate=f"<b>{name}</b><extra></extra>",
                showlegend=True,
            )
        )

    def create_verification_chart(
        self,
        historical_df: pd.DataFrame,
        future_df: pd.DataFrame,
        scenario: ParsedScenario,
        scenario_date: str,
    ) -> go.Figure:
        """検証用チャートを作成する.

        過去のシナリオと、その後の実際の値動きを重ねて表示する。

        Args:
            historical_df: シナリオ作成時点までの市場データ
            future_df: シナリオ作成後の市場データ
            scenario: シナリオ解析結果
            scenario_date: シナリオ作成日時

        Returns:
            Plotly Figureオブジェクト
        """
        # 全データを結合
        combined_df = pd.concat([historical_df, future_df])

        # ベースチャートの作成
        fig = self.create_chart(
            combined_df,
            scenario,
            title=f"シナリオ検証: {scenario.symbol} ({scenario_date})",
        )

        # シナリオ作成時点の垂直線を追加
        fig.add_vline(
            x=historical_df.index[-1],
            line_width=3,
            line_dash="solid",
            line_color="blue",
            annotation_text="シナリオ作成時点",
            annotation_position="top",
        )

        # 未来データ部分を異なる色で強調
        fig.add_trace(
            go.Candlestick(
                x=future_df.index,
                open=future_df["open"],
                high=future_df["high"],
                low=future_df["low"],
                close=future_df["close"],
                name="実際の値動き（検証対象）",
                increasing_line_color="#00acc1",
                decreasing_line_color="#ff6f00",
                opacity=0.7,
            )
        )

        return fig
