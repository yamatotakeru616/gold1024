"""市場データ取得モジュール.

Yahoo Financeから市場データを取得する。
"""

import os
import shutil
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


class DataFetcher:
    """市場データを取得するクラス."""

    def __init__(self) -> None:
        """初期化."""
        self._setup_ssl_cert()

    def _setup_ssl_cert(self) -> None:
        """SSL証明書の設定（ASCII安全なパスに配置）."""
        try:
            import certifi

            src = certifi.where()
            dest = os.path.join(os.environ.get("TEMP", "/tmp"), "cacert_project.pem")
            shutil.copy2(src, dest)
            os.environ["SSL_CERT_FILE"] = dest
            os.environ["CURL_CA_BUNDLE"] = dest
        except Exception as e:
            print(f"SSL証明書設定エラー: {e}")

    def fetch_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1h",
    ) -> pd.DataFrame:
        """市場データを取得する.

        Args:
            symbol: 銘柄コード（例: "GC=F", "USDJPY=X"）
            period: 取得期間（例: "1d", "5d", "1mo", "1y"）
            interval: 時間枠（例: "1m", "5m", "1h", "1d"）

        Returns:
            OHLCV データを含むDataFrame
        """
        try:
            data = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
            )

            if isinstance(data, pd.DataFrame) and not data.empty:
                # MultiIndex列の場合はフラット化
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)

                # 列名を小文字に統一
                data.columns = data.columns.str.lower()

                return data
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"データ取得エラー ({symbol}): {e}")
            return pd.DataFrame()

    def fetch_data_by_date_range(
        self,
        symbol: str,
        start_date: str | datetime,
        end_date: str | datetime,
        interval: str = "1h",
    ) -> pd.DataFrame:
        """日付範囲を指定して市場データを取得する.

        Args:
            symbol: 銘柄コード
            start_date: 開始日時（ISO形式文字列またはdatetimeオブジェクト）
            end_date: 終了日時（ISO形式文字列またはdatetimeオブジェクト）
            interval: 時間枠

        Returns:
            OHLCV データを含むDataFrame
        """
        try:
            data = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False,
            )

            if isinstance(data, pd.DataFrame) and not data.empty:
                # MultiIndex列の場合はフラット化
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)

                # 列名を小文字に統一
                data.columns = data.columns.str.lower()

                return data
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"データ取得エラー ({symbol}): {e}")
            return pd.DataFrame()

    def fetch_latest_data(
        self,
        symbol: str,
        lookback_days: int = 30,
        interval: str = "1h",
    ) -> pd.DataFrame:
        """最新の市場データを取得する.

        Args:
            symbol: 銘柄コード
            lookback_days: 過去何日分のデータを取得するか
            interval: 時間枠

        Returns:
            OHLCV データを含むDataFrame
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)

        return self.fetch_data_by_date_range(
            symbol,
            start_date,
            end_date,
            interval,
        )

    def get_available_symbols(self) -> list[str]:
        """利用可能な銘柄コードのリストを取得する.

        Returns:
            銘柄コードのリスト
        """
        return [
            "GC=F",  # GOLD
            "EURUSD=X",  # ユーロドル
            "GBPUSD=X",  # ポンドドル
            "USDJPY=X",  # ドル円
            "AUDUSD=X",  # 豪ドル米ドル
            "USDCAD=X",  # 米ドルカナダドル
            "USDCHF=X",  # 米ドルスイスフラン
            "NZDUSD=X",  # NZドル米ドル
            "EURJPY=X",  # ユーロ円
        ]

    def get_symbol_name(self, symbol: str) -> str:
        """銘柄コードから表示名を取得する.

        Args:
            symbol: 銘柄コード

        Returns:
            表示名
        """
        name_map = {
            "GC=F": "GOLD（金）",
            "EURUSD=X": "EUR/USD（ユーロドル）",
            "GBPUSD=X": "GBP/USD（ポンドドル）",
            "USDJPY=X": "USD/JPY（ドル円）",
            "AUDUSD=X": "AUD/USD（豪ドル米ドル）",
            "USDCAD=X": "USD/CAD（米ドルカナダドル）",
            "USDCHF=X": "USD/CHF（米ドルスイスフラン）",
            "NZDUSD=X": "NZD/USD（NZドル米ドル）",
            "EURJPY=X": "EUR/JPY（ユーロ円）",
        }

        return name_map.get(symbol, symbol)
