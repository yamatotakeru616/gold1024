"""市場分析シナリオ可視化システム - メインアプリケーション.

PyQt6を使用したGUIアプリケーション。
"""

import sys
from datetime import datetime

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from chart_renderer import ChartRenderer
from data_fetcher import DataFetcher
from database_manager import DatabaseManager
from scenario_parser import ScenarioParser


class MainWindow(QMainWindow):
    """メインウィンドウクラス."""

    def __init__(self) -> None:
        """初期化."""
        super().__init__()

        # モジュールの初期化
        self.data_fetcher = DataFetcher()
        self.scenario_parser = ScenarioParser()
        self.chart_renderer = ChartRenderer()
        self.db_manager = DatabaseManager()

        # 現在のシナリオ
        self.current_scenario = None
        self.current_df = None

        self._init_ui()

    def _init_ui(self) -> None:
        """UIを初期化する."""
        self.setWindowTitle("市場分析シナリオ可視化システム")
        self.setGeometry(100, 100, 1400, 900)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # メインレイアウト（水平分割）
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # スプリッター（左右分割）
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # 左側パネル（シナリオ入力・保存）
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        # 右側パネル（チャート表示）
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)

        # スプリッターの初期サイズ
        splitter.setSizes([400, 1000])

    def _create_left_panel(self) -> QWidget:
        """左側パネルを作成する.

        Returns:
            左側パネルのウィジェット
        """
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # タイトル
        title_label = QLabel("<h2>シナリオ分析</h2>")
        layout.addWidget(title_label)

        # 銘柄選択
        symbol_layout = QHBoxLayout()
        symbol_label = QLabel("銘柄:")
        self.symbol_combo = QComboBox()
        symbols = self.data_fetcher.get_available_symbols()
        for symbol in symbols:
            display_name = self.data_fetcher.get_symbol_name(symbol)
            self.symbol_combo.addItem(display_name, symbol)
        symbol_layout.addWidget(symbol_label)
        symbol_layout.addWidget(self.symbol_combo)
        layout.addLayout(symbol_layout)

        # シナリオテキスト入力
        scenario_label = QLabel("分析シナリオ:")
        layout.addWidget(scenario_label)

        self.scenario_text = QTextEdit()
        self.scenario_text.setPlaceholderText(
            "ここに分析シナリオを入力またはペーストしてください...\n\n"
            "例:\n"
            "日足ベースのサポートラインは4317近辺と4218近辺です。\n"
            "レジスタンスラインは4418近辺です。\n"
            "4317近辺～4320近辺のサポート帯を下抜けなければ上昇トレンド継続です。"
        )
        layout.addWidget(self.scenario_text)

        # ボタン配置
        button_layout = QHBoxLayout()

        self.analyze_button = QPushButton("分析 & 表示")
        self.analyze_button.clicked.connect(self._on_analyze)
        button_layout.addWidget(self.analyze_button)

        self.save_button = QPushButton("シナリオ保存")
        self.save_button.clicked.connect(self._on_save)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

        # 過去シナリオ一覧
        history_label = QLabel("<h3>過去のシナリオ</h3>")
        layout.addWidget(history_label)

        self.scenario_list = QListWidget()
        self.scenario_list.itemDoubleClicked.connect(self._on_load_scenario)
        layout.addWidget(self.scenario_list)

        # シナリオ一覧の更新
        self._refresh_scenario_list()

        return panel

    def _create_right_panel(self) -> QWidget:
        """右側パネルを作成する.

        Returns:
            右側パネルのウィジェット
        """
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # チャートタイトル
        self.chart_title_label = QLabel("<h2>チャート表示</h2>")
        layout.addWidget(self.chart_title_label)

        # Webビュー（Plotlyチャート表示用）
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        return panel

    def _on_analyze(self) -> None:
        """分析ボタンクリック時の処理."""
        # テキスト取得
        text = self.scenario_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "警告", "シナリオテキストを入力してください。")
            return

        # シナリオ解析
        self.current_scenario = self.scenario_parser.parse(text)

        # 銘柄コード取得
        symbol = self.symbol_combo.currentData()
        self.current_scenario.symbol = symbol

        # 市場データ取得
        self.current_df = self.data_fetcher.fetch_data(
            symbol,
            period="3mo",
            interval="1h",
        )

        if self.current_df.empty:
            QMessageBox.critical(
                self,
                "エラー",
                f"{symbol} のデータ取得に失敗しました。",
            )
            return

        # チャート描画
        symbol_name = self.data_fetcher.get_symbol_name(symbol)
        fig = self.chart_renderer.create_chart(
            self.current_df,
            self.current_scenario,
            title=f"{symbol_name} - シナリオ分析",
        )

        # HTMLとして表示
        html = fig.to_html(include_plotlyjs="cdn")
        self.web_view.setHtml(html)

        # 保存ボタンを有効化
        self.save_button.setEnabled(True)

        QMessageBox.information(
            self,
            "成功",
            "シナリオを解析し、チャートに表示しました。",
        )

    def _on_save(self) -> None:
        """保存ボタンクリック時の処理."""
        if self.current_scenario is None:
            return

        # データベースに保存
        scenario_id = self.db_manager.save_scenario(
            symbol=self.current_scenario.symbol,
            raw_text=self.current_scenario.raw_text,
            parsed_data=self.current_scenario.to_dict(),
            notes="",
        )

        QMessageBox.information(
            self,
            "成功",
            f"シナリオを保存しました。(ID: {scenario_id})",
        )

        # シナリオ一覧を更新
        self._refresh_scenario_list()

    def _refresh_scenario_list(self) -> None:
        """シナリオ一覧を更新する."""
        self.scenario_list.clear()

        scenarios = self.db_manager.list_scenarios(limit=50)
        for scenario in scenarios:
            # 日時と銘柄を表示
            created_at = datetime.fromisoformat(scenario["created_at"])
            display_text = (
                f"{created_at.strftime('%Y-%m-%d %H:%M')} - "
                f"{self.data_fetcher.get_symbol_name(scenario['symbol'])}"
            )

            self.scenario_list.addItem(display_text)
            # IDをデータとして保存
            item = self.scenario_list.item(self.scenario_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, scenario["id"])

    def _on_load_scenario(self, item: QListWidget) -> None:
        """シナリオをダブルクリックで読み込む.

        Args:
            item: リストアイテム
        """
        scenario_id = item.data(Qt.ItemDataRole.UserRole)
        scenario_data = self.db_manager.get_scenario(scenario_id)

        if scenario_data is None:
            QMessageBox.critical(self, "エラー", "シナリオの読み込みに失敗しました。")
            return

        # シナリオ作成日時
        created_at = datetime.fromisoformat(scenario_data["created_at"])

        # データ取得（シナリオ作成時点までのデータ）
        historical_df = self.data_fetcher.fetch_data_by_date_range(
            symbol=scenario_data["symbol"],
            start_date=created_at - pd.Timedelta(days=30),
            end_date=created_at,
            interval="1h",
        )

        # シナリオ作成後から現在までのデータ
        future_df = self.data_fetcher.fetch_data_by_date_range(
            symbol=scenario_data["symbol"],
            start_date=created_at,
            end_date=datetime.now(),
            interval="1h",
        )

        if historical_df.empty:
            QMessageBox.critical(
                self,
                "エラー",
                "過去のデータ取得に失敗しました。",
            )
            return

        # シナリオデータを再構築
        parsed_data = scenario_data["parsed_data"]
        from scenario_parser import ParsedScenario, PriceLevel, PriceZone

        loaded_scenario = ParsedScenario(
            raw_text=parsed_data["raw_text"],
            symbol=parsed_data["symbol"],
            analysis_date=parsed_data["analysis_date"],
        )

        # サポートレベルの復元
        for sl_data in parsed_data["support_levels"]:
            loaded_scenario.support_levels.append(
                PriceLevel(
                    price=sl_data["price"],
                    level_type=sl_data["level_type"],
                    timeframe=sl_data["timeframe"],
                    description=sl_data["description"],
                )
            )

        # レジスタンスレベルの復元
        for rl_data in parsed_data["resistance_levels"]:
            loaded_scenario.resistance_levels.append(
                PriceLevel(
                    price=rl_data["price"],
                    level_type=rl_data["level_type"],
                    timeframe=rl_data["timeframe"],
                    description=rl_data["description"],
                )
            )

        # サポートゾーンの復元
        for sz_data in parsed_data["support_zones"]:
            loaded_scenario.support_zones.append(
                PriceZone(
                    price_lower=sz_data["price_lower"],
                    price_upper=sz_data["price_upper"],
                    zone_type=sz_data["zone_type"],
                    description=sz_data["description"],
                )
            )

        # レジスタンスゾーンの復元
        for rz_data in parsed_data["resistance_zones"]:
            loaded_scenario.resistance_zones.append(
                PriceZone(
                    price_lower=rz_data["price_lower"],
                    price_upper=rz_data["price_upper"],
                    zone_type=rz_data["zone_type"],
                    description=rz_data["description"],
                )
            )

        # 検証チャートの作成
        fig = self.chart_renderer.create_verification_chart(
            historical_df=historical_df,
            future_df=future_df,
            scenario=loaded_scenario,
            scenario_date=created_at.strftime("%Y-%m-%d %H:%M"),
        )

        # HTMLとして表示
        html = fig.to_html(include_plotlyjs="cdn")
        self.web_view.setHtml(html)

        # テキストエリアに元のシナリオを表示
        self.scenario_text.setPlainText(scenario_data["raw_text"])

        # 銘柄コンボボックスを選択
        index = self.symbol_combo.findData(scenario_data["symbol"])
        if index >= 0:
            self.symbol_combo.setCurrentIndex(index)

        QMessageBox.information(
            self,
            "読み込み完了",
            f"過去のシナリオを読み込み、検証チャートを表示しました。\n"
            f"作成日時: {created_at.strftime('%Y-%m-%d %H:%M')}",
        )


def main() -> None:
    """アプリケーションのエントリーポイント."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
