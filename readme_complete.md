# 市場分析シナリオ可視化システム

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

## 📋 プロジェクト状態

- **現在フェーズ**: フェーズ2（実装）
- **進捗率**: 85%
- **最終更新**: 2025-10-24

## 🎯 概要

本システムは、投資家の分析スキル向上を支援する**戦略的分析・学習プラットフォーム**です。

### 核心機能

1. **直感的な分析**: テキストシナリオと市場データをTradingViewライクなインタラクティブチャートで融合表示
2. **経験の資産化**: 分析シナリオをデータベースに蓄積し、いつでも振り返り可能
3. **スキルの向上**: 過去のシナリオと実際の値動きを視覚的に比較検証

## 🚀 クイックスタート

### 必要環境

- Python 3.10以上
- pip または uv

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/market-scenario-analyzer.git
cd market-scenario-analyzer

# 仮想環境を作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

### アプリケーションの起動

```bash
# GUIアプリケーションを起動
python src/main.py
```

### Notebookでの動作確認

```bash
# Jupyter Notebookを起動
jupyter notebook

# notebook/scenario_analysis_verification.ipynb を開く
```

## 📁 プロジェクト構造

```
market-scenario-analyzer/
├── src/
│   ├── main.py                    # GUIアプリケーション
│   └── modules/
│       ├── scenario_parser.py     # シナリオ解析
│       ├── data_fetcher.py        # 市場データ取得
│       ├── chart_renderer.py      # チャート描画
│       └── database.py            # データベース管理
├── notebook/
│   └── scenario_analysis_verification.ipynb  # 動作検証
├── test/
│   └── test_scenario_parser.py    # ユニットテスト
├── data/
│   └── scenarios.db               # シナリオデータベース
├── spec/
│   └── workflow_spec_v3.3.md      # 開発仕様書
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 💡 使い方

### 1. シナリオの入力と分析

1. アプリケーションを起動
2. 銘柄を選択（例: GOLD）
3. 分析シナリオをテキストエリアに入力
4. 「分析 & 表示」ボタンをクリック

**シナリオ例:**

```
日足ベースのサポートラインは4317近辺と4218近辺です。
レジスタンスラインは4418近辺と4540近辺です。
4317近辺～4320近辺のサポート帯を下抜けなければ上昇トレンド継続です。
```

### 2. シナリオの保存

1. 分析結果を確認
2. 「シナリオ保存」ボタンをクリック
3. データベースに自動保存されます

### 3. 過去シナリオの検証

1. 左側パネルの「過去のシナリオ」リストから任意のシナリオをダブルクリック
2. シナリオ作成時点までのチャートと、その後の実際の値動きが重ねて表示されます
3. サポート/レジスタンスラインが機能したかを視覚的に確認できます

## 🔬 機能詳細

### シナリオ解析機能

テキストから以下の情報を自動抽出します:

- ✅ 銘柄コード（GOLD, ドル円など）
- ✅ 分析日時
- ✅ サポートライン（日足/週足/月足）
- ✅ レジスタンスライン（日足/週足/月足）
- ✅ 重要価格帯（サポート帯/レジスタンス帯）
- ✅ 注意事項（急落警告など）

### インタラクティブチャート機能

**Plotlyによる高度な操作性:**

- 🖱️ マウスホイールで拡大・縮小
- 🖱️ ドラッグでパン（表示範囲移動）
- 🖱️ ホバーで詳細情報表示
- 📊 ローソク足 + サポート/レジスタンスラインの重ね表示
- 🎨 時間枠別の色分け（日足/週足/月足）

### データベース機能

**SQLiteによる永続化:**

- 💾 シナリオの保存・読み込み
- 🔍 銘柄・日付での検索
- 📚 無制限のシナリオ履歴
- 🗑️ 不要なシナリオの削除

## 🧪 テスト実行

```bash
# ユニットテストの実行
pytest test/ -v

# カバレッジ付きテスト
pytest test/ --cov=src --cov-report=html

# 品質チェック（Ruff lint + format）
ruff check src/ test/ notebook/
ruff format src/ test/ notebook/
```

## 📊 開発タスク進捗ログ

### フェーズ1: 設計 ✅
- [x] 要件定義書の作成
- [x] アーキテクチャ設計
- [x] プロジェクト構造の整備

### フェーズ2: 実装 🔄
- [x] シナリオ解析モジュール (`scenario_parser.py`)
- [x] データ取得モジュール (`data_fetcher.py`)
- [x] チャート描画モジュール (`chart_renderer.py`)
- [x] データベース管理モジュール (`database.py`)
- [x] GUIアプリケーション (`main.py`)
- [x] **Notebook動作検証** (`scenario_analysis_verification.ipynb`)
- [x] ユニットテスト作成

### フェーズ3: テスト 🔜
- [ ] 統合テスト
- [ ] エッジケーステスト
- [ ] パフォーマンステスト

### フェーズ4: 完成 🔜
- [ ] ドキュメント完全版
- [ ] デプロイパッケージ作成
- [ ] リリースノート作成

## 🛠️ 技術スタック

| カテゴリ | 技術 |
|---------|------|
| 言語 | Python 3.10+ |
| GUI | PyQt6 |
| チャート | Plotly |
| データ取得 | yfinance |
| データ処理 | pandas |
| データベース | SQLite3 |
| テスト | pytest |
| コード品質 | Ruff, mypy |

## 📖 ドキュメント

- [要件定義書 Ver. 2.0](spec/requirements_v2.0.md)
- [開発仕様書 v3.3](spec/workflow_spec_v3.3.md)
- [変更履歴](change_log.md)
- [品質チェックリスト](quality_check.md)

## 🔐 セキュリティ

- ✅ APIキー不要（Yahoo Financeは無料公開API）
- ✅ ローカル実行（データは全てローカル保存）
- ✅ 外部送信なし

## 🤝 貢献

プルリクエストを歓迎します！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

### 開発時の注意事項

本プロジェクトは**スペック駆動開発**を採用しています。

- 📝 変更前に `spec/workflow_spec_v3.3.md` を必ず確認
- 🔍 コード品質チェック（Ruff lint）を必ずパス
- 📓 新規コードは必ずNotebookで動作検証
- ✅ ユニットテストを追加
- 📄 変更内容を `change_log.md` に記録

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

## 👤 作成者

**AI協働開発チーム**

- プロジェクト開始: 2025年10月
- 連絡先: [メールアドレス]

## 🙏 謝辞

- [yfinance](https://github.com/ranaroussi/yfinance) - 市場データ取得
- [Plotly](https://plotly.com/) - インタラクティブチャート
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUIフレームワーク

## 🐛 バグ報告・機能リクエスト

問題を発見した場合や新機能のアイデアがある場合は、[Issues](https://github.com/yourusername/market-scenario-analyzer/issues)で報告してください。

---

**⚠️ 免責事項**: このシステムは教育・研究目的です。投資判断は自己責任で行ってください。