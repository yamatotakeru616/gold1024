# 金市場シナリオ分析システム

## 概要

本プロジェクトは、PyQt6ベースのGUIアプリケーションとJupyter Notebookによる検証環境を備えた、金（Gold）市場向けのシナリオ分析・可視化システムです。

- シナリオテキストを自動解析し、チャート上に可視化
- Yahoo Financeから市場データを取得
- SQLiteによるシナリオ履歴管理
- Plotlyによるインタラクティブチャート
- Jupyter Notebookによる検証・分析
- uvによる高速なPython環境構築
- GitHub ActionsによるCI/CD

## 主な機能

- シナリオテキストの自動解析（ルールベース）
- 市場データの自動取得（yfinance）
- チャートへのシナリオオーバーレイ表示（Plotly）
- シナリオの保存・履歴管理（SQLite）
- GUIアプリケーション（PyQt6）
- Jupyter Notebookによる動作検証
- ユニットテスト・型チェック・リント

## セットアップ

1. **uvのインストール**
   - Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **仮想環境の作成とパッケージインストール**
   ```powershell
   uv venv
   .venv\Scripts\Activate.ps1
   uv pip install -e ".[dev,jupyter]"
   ```

3. **Jupyter Notebookの起動**
   ```powershell
   python -m jupyter lab
   # または
   python -m jupyter notebook
   ```

4. **GUIアプリケーションの起動**
   ```powershell
   python main_app.py
   # または
   .\run_app.ps1
   ```

詳細は `UV_SETUP.md` と `QUICKSTART.md` を参照してください。

## ディレクトリ構成

```
├── main_app.py              # PyQt6 GUIアプリ本体
├── chart_renderer.py        # チャート描画モジュール
├── data_fetcher.py          # 市場データ取得モジュール
├── database_manager.py      # DB管理モジュール
├── scenario_parser.py       # シナリオ解析エンジン
├── unit_tests.py            # ユニットテスト
├── verification_notebook.py # Notebook用サンプル
├── UV_SETUP.md              # uvセットアップガイド
├── QUICKSTART.md            # クイックスタート
├── requirements.txt         # 依存パッケージ
├── pyproject.toml           # uv/PEP管理
├── .github/workflows/       # GitHub Actions
└── ...
```

## 開発・テスト

- テスト実行: `python -m pytest unit_tests.py -v`
- 型チェック: `uv run mypy *.py`
- リント: `uv run ruff check .`
- カバレッジ: `python -m pytest unit_tests.py --cov`

## ライセンス

MIT License

ご質問・不具合は[GitHub Issues](https://github.com/yamatotakeru616/gold1024/issues)まで。

## 依存関係・環境要件まとめ

### 必須環境
- Python: **3.10以上**
- OS: Windows, macOS, Linux
- データベース: SQLite（外部DB不要）

### 主要依存パッケージ
- PyQt6, PyQt6-WebEngine（GUI）
- plotly（チャート描画）
- yfinance（市場データ取得）
- pandas, numpy（データ処理）
- SQLite（標準ライブラリ）

### Jupyter/Notebook関連
- jupyter, jupyterlab, notebook, ipykernel, ipywidgets

### 開発・テスト・ドキュメント
- pytest, pytest-cov（テスト）
- ruff（リント）
- mypy（型チェック）
- bandit（セキュリティ）
- pdoc3（ドキュメント生成）

### 推奨パッケージ管理
- **uv**（高速な仮想環境・依存管理）
- `requirements.txt`/`pyproject.toml` で全依存管理

### インストール例
```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -e ".[dev,jupyter]"
```

### 注意事項
- `pyproject.toml` の `requires-python` でバージョン指定あり
- `.venv` や `.uv` フォルダは `.gitignore` 済み
- 詳細は `requirements.txt` および `pyproject.toml` を参照

---

## モジュール構成と責務まとめ

本プロジェクトの主要モジュールと責務は以下の通りです。

| モジュール名           | 主な責務・役割                                      |
|-----------------------|---------------------------------------------------|
| data_fetcher.py       | 市場データの取得（Yahoo Finance→DataFrame化）      |
| chart_renderer.py     | 取得データ・シナリオ情報のPlotlyチャート描画        |
| scenario_parser.py    | シナリオテキストの解析・構造化                      |
| database_manager.py   | シナリオ履歴等のDB管理（SQLite）                    |
| main_app.py           | PyQt6によるGUI全体制御・各モジュール連携            |

### データ取得からチャート表示までの流れ
1. ユーザー操作（GUI）
2. `data_fetcher.py`で市場データ取得
3. `scenario_parser.py`でシナリオ解析（必要時）
4. `chart_renderer.py`でチャート生成
5. `main_app.py`でGUIに表示

各モジュールの責務分離により、保守性・拡張性の高い設計となっています。

---

## 可視化手法・拡張性
---

## テスト網羅状況・ドキュメント整備状況

### テスト（unit_tests.py）

- 対象：ScenarioParserクラス
- 網羅内容：
  - シナリオテキストのパース（正常系・空文字）
  - 銘柄コード抽出
  - 日付抽出
  - サポート/レジスタンスライン抽出（日足・週足）
  - サポートゾーン抽出
  - メモ抽出（急落警告など）
  - パース結果のdict変換
- 未網羅・拡張余地：
  - レジスタンスゾーン抽出
  - トレンドライン抽出
  - 異常系（不正なフォーマット、極端な値など）
  - 他モジュール（データ取得・チャート描画・DB管理等）のテスト

   ※ 機能拡張時は新たなテストケース追加が推奨されます。

### ドキュメント（QUICKSTART.md）
- 起動方法（PowerShell/バッチ/直接実行）
- GUIの使い方（シナリオ入力・銘柄選択・解析・保存・再表示）
- チャート操作方法（ズーム・パン・リセット・ホバー）
- トラブルシューティング
- シナリオテキストの書き方（例付き）
- 充実度：初心者でも迷わず使えるレベルで十分に整備

※ 用途に応じて「Web版の使い方」や「API連携例」などを追加しても良いでしょう。

---

### 現在のチャート表示方法
- Plotly（plotly.graph_objects）によるインタラクティブなローソク足チャート＋シナリオ情報のオーバーレイ
- PyQt6アプリ内ではQWebEngineView等でHTMLとして埋め込み表示
- Jupyter NotebookやWebブラウザでもそのまま可視化可能

### 用途に応じた拡張性
- PlotlyのままDashやStreamlit等のWebアプリに展開可能（既存のcreate_chart返り値をそのまま利用）
- Matplotlib（静的画像/PDF化）、Bokeh（Web向けインタラクティブ）、Altair等への移植も可能
- チャート生成部分のロジックを一部書き換えれば、他ライブラリへの切り替え・併用も容易

### Web発信・ダッシュボード化の展望
- PlotlyベースのままDashやStreamlitへ展開するのが最もスムーズ
- 既存のチャート生成関数（go.Figure返却）をそのままWebアプリに組み込める

---

---

## シナリオ解析の仕組み・拡張性

### 解析の概要
- 投資家が記述した自然言語のシナリオテキストから、サポート/レジスタンスライン、価格帯、トレンド、メモ等を抽出し、構造化データ（ParsedScenario）へ変換します。
- パース結果はJSON形式で保存・連携可能です。

### 主なデータ構造
- PriceLevel：価格・種別（support/resistance）・足種（日足/週足/月足）・説明
- PriceZone：価格帯（上下限）・種別（support_zone/resistance_zone）・説明
- TrendLine：トレンド線（始点/終点価格・時刻・説明）
- ParsedScenario：上記すべて＋元テキスト・銘柄・日付・メモ

### 解析の流れ
1. 銘柄コード抽出（例: GOLD→GC=F, ドル円→USDJPY=X）
2. 分析日付抽出（例: 2025年10月21日 8時00分）
3. サポート/レジスタンスライン抽出（日足/週足/月足ごとに正規表現で抽出）
4. サポート/レジスタンスゾーン抽出（「xxxx近辺～yyyy近辺のサポート帯」等）
5. 重要メモ抽出（「急落に注意」など特定フレーズ）

### 拡張性
- 入力は自然言語テキスト（日本語）だが、パース結果はJSON化できるため外部保存や他システム連携も容易。
- JSONやYAML形式のシナリオ定義も、変換メソッドを追加すれば柔軟に対応可能。
- 正規表現や抽出ロジックを追加・修正することで、独自のシナリオ記法や新しい分析要素も拡張可能。

#### JSONシナリオ定義例
```json
{
   "symbol": "GC=F",
   "support_levels": [
      {
         "price": 4300,
         "level_type": "support",
         "timeframe": "日足",
         "description": "主要サポート"
      }
   ],
   "notes": [
      "急落に注意"
   ]
}
```

---
