# UV環境構築ガイド

## 🚀 uvのインストール

### Windows (PowerShell)
```powershell
# uvをインストール
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 📦 プロジェクトのセットアップ

### 1. 仮想環境の作成とパッケージインストール

```bash
# プロジェクトディレクトリで実行
cd gold1024

# 仮想環境を作成し、依存関係をインストール
uv venv

# 仮想環境を有効化
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate

# 基本パッケージをインストール
uv pip install -e .

# 開発ツールをインストール
uv pip install -e ".[dev]"

# Jupyter環境をインストール
uv pip install -e ".[jupyter]"

# または全部まとめて
uv pip install -e ".[dev,jupyter]"
```

### 2. uvによる高速インストール

```bash
# 特定のパッケージを追加
uv pip install パッケージ名

# requirements.txtから一括インストール（互換性のため残す場合）
uv pip install -r requirements.txt

# パッケージのアップグレード
uv pip install --upgrade パッケージ名
```

## 📊 Jupyter Notebookの使用

### Jupyter Labを起動
```bash
# 仮想環境を有効化した状態で
jupyter lab
```

### Jupyter Notebookを起動
```bash
jupyter notebook
```

### VS CodeでNotebookを使用
1. VS Codeで`.ipynb`ファイルを開く
2. カーネルを選択: `.venv`の環境を選択
3. セルを実行

## 🧪 開発ツールの使用

### テストの実行
```bash
# 全テストを実行
uv run pytest

# カバレッジ付きで実行
uv run pytest --cov
```

### コードフォーマット
```bash
# チェックのみ
uv run ruff check .

# 自動修正
uv run ruff check --fix .

# フォーマット
uv run ruff format .
```

### 型チェック
```bash
uv run mypy *.py
```

### セキュリティチェック
```bash
uv run bandit -r .
```

## 🏃 アプリケーションの実行

### GUIアプリケーションを起動
```bash
uv run python main_app.py

# または pyproject.toml に定義したスクリプトで
uv run gold-analyze
```

## 📝 依存関係の管理

### パッケージの追加
```bash
# pyproject.toml に手動で追加してから
uv pip install -e .

# または直接インストール
uv pip install 新しいパッケージ
```

### 依存関係の同期
```bash
# pyproject.toml の内容を反映
uv pip sync
```

### インストール済みパッケージの確認
```bash
uv pip list
```

## 🔧 uvの利点

- ⚡ **高速**: pipの10-100倍速いインストール
- 🔒 **確実**: 依存関係の解決が正確
- 🎯 **シンプル**: 設定ファイル1つで管理
- 🌐 **互換性**: pip互換のインターフェース
- 💾 **効率的**: グローバルキャッシュで容量節約

## 📚 参考リンク

- [uv公式ドキュメント](https://github.com/astral-sh/uv)
- [pyproject.toml仕様](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
