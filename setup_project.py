#!/usr/bin/env python3
"""プロジェクト初期化スクリプト.

このスクリプトは市場分析シナリオ可視化システムの
フォルダ構造と設定ファイルを自動生成します。
"""

import os
from pathlib import Path


def create_project_structure() -> None:
    """プロジェクトのフォルダ構造を作成する."""
    print("🚀 プロジェクト初期化中...")

    # フォルダ構成
    folders = [
        "spec",
        "src",
        "src/modules",
        "notebook",
        "test",
        "docs/adr",
        "data",
        ".github/workflows",
        ".devcontainer",
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"✓ {folder}")

    # .gitignoreの生成
    gitignore_content = """# 仮想環境
.venv/
venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
build/
dist/
*.egg-info/
.pytest_cache/

# Notebook
.ipynb_checkpoints/

# IDE
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
!.vscode/launch.json

# Secrets
*.env
.env
secrets.toml

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Data
data/*.csv
data/*.parquet
!data/.gitkeep
"""

    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("✓ .gitignore")

    # pyproject.tomlの生成
    pyproject_content = """[project]
name = "market-scenario-analyzer"
version = "1.0.0"
description = "市場分析シナリオ可視化システム"
requires-python = ">=3.10"
dependencies = [
    "yfinance>=0.2.0",
    "pandas>=2.0.0",
    "plotly>=5.0.0",
    "sqlalchemy>=2.0.0",
    "PyQt6>=6.5.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "jupyter>=1.0.0",
]

[tool.ruff]
target-version = "py310"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "D", "UP", "ANN", "B"]
ignore = ["D203", "D213", "ANN101", "ANN102"]

[tool.ruff.lint.pydocstyle]
convention = "google"
"""

    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)
    print("✓ pyproject.toml")

    # requirements.txtの生成
    requirements_content = """# コアライブラリ
yfinance>=0.2.0
pandas>=2.0.0
plotly>=5.0.0
sqlalchemy>=2.0.0
PyQt6>=6.5.0
certifi>=2023.0.0

# 開発・品質ツール
ruff>=0.1.0
mypy>=1.5.0
pytest>=7.4.0
pytest-cov>=4.1.0

# Notebook
jupyter>=1.0.0
ipykernel>=6.25.0
ipywidgets>=8.0.0
"""

    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("✓ requirements.txt")

    # README.mdの生成
    readme_content = """# 市場分析シナリオ可視化システム

## プロジェクト状態
- **現在フェーズ**: フェーズ1（設計）
- **進捗率**: 10%

## 概要
TradingViewライクなインタラクティブチャートで市場分析シナリオを可視化し、
過去のシナリオ検証を通じて投資スキルを向上させるプラットフォーム。

## セットアップ

```bash
# 仮想環境作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 依存パッケージインストール
pip install -r requirements.txt
```

## 開発タスク進捗ログ

### フェーズ1: 設計 🔄
- [x] プロジェクト構造作成
- [ ] 要件定義書の確定
- [ ] アーキテクチャ設計

### フェーズ2: 実装
- [ ] シナリオ解析モジュール
- [ ] データ取得モジュール
- [ ] チャート描画モジュール
- [ ] GUI実装
- [ ] データベース実装

### フェーズ3: テスト
- [ ] ユニットテスト
- [ ] 統合テスト

### フェーズ4: 完成
- [ ] ドキュメント整備
- [ ] リリース準備
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✓ README.md")

    # change_log.mdの生成
    changelog_content = """# 変更履歴

## [2025-10-23 初期化] プロジェクト作成

**変更内容**:
- プロジェクト構造を作成
- 設定ファイル(.gitignore, pyproject.toml, requirements.txt)を生成

**品質チェック**:
- [x] フォルダ構造確認
- [x] 設定ファイル確認
"""

    with open("change_log.md", "w", encoding="utf-8") as f:
        f.write(changelog_content)
    print("✓ change_log.md")

    # data/.gitkeepの生成
    Path("data/.gitkeep").touch()

    print("\n✅ プロジェクト初期化完了！")
    print("\n次のステップ:")
    print("1. python -m venv .venv")
    print("2. source .venv/bin/activate  # または .venv\\Scripts\\activate")
    print("3. pip install -r requirements.txt")


if __name__ == "__main__":
    create_project_structure()
