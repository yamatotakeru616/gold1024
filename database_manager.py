"""データベース管理モジュール.

シナリオの保存・取得・検索機能を提供する。
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any


class DatabaseManager:
    """シナリオデータベースを管理するクラス."""

    def __init__(self, db_path: str = "data/scenarios.db") -> None:
        """初期化.

        Args:
            db_path: データベースファイルのパス
        """
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self) -> None:
        """データベースファイルとテーブルを作成する."""
        # dataディレクトリが存在しない場合は作成
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # scenariosテーブルの作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                symbol TEXT NOT NULL,
                raw_text TEXT NOT NULL,
                parsed_data TEXT NOT NULL,
                notes TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_scenario(
        self,
        symbol: str,
        raw_text: str,
        parsed_data: dict[str, Any],
        notes: str = "",
    ) -> int:
        """シナリオを保存する.

        Args:
            symbol: 銘柄コード
            raw_text: 元のシナリオテキスト
            parsed_data: 解析済みデータ（辞書形式）
            notes: 追加メモ

        Returns:
            保存されたレコードのID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO scenarios (created_at, symbol, raw_text, parsed_data, notes)
            VALUES (?, ?, ?, ?, ?)
        """,
            (created_at, symbol, raw_text, json.dumps(parsed_data, ensure_ascii=False), notes),
        )

        scenario_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return scenario_id

    def get_scenario(self, scenario_id: int) -> dict[str, Any] | None:
        """指定IDのシナリオを取得する.

        Args:
            scenario_id: シナリオID

        Returns:
            シナリオデータ（辞書形式）、存在しない場合はNone
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, created_at, symbol, raw_text, parsed_data, notes
            FROM scenarios
            WHERE id = ?
        """,
            (scenario_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "created_at": row[1],
            "symbol": row[2],
            "raw_text": row[3],
            "parsed_data": json.loads(row[4]),
            "notes": row[5],
        }

    def list_scenarios(
        self,
        symbol: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """シナリオ一覧を取得する.

        Args:
            symbol: 銘柄コードでフィルタ（Noneの場合は全件）
            limit: 取得件数の上限

        Returns:
            シナリオデータのリスト
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if symbol:
            cursor.execute(
                """
                SELECT id, created_at, symbol, raw_text, parsed_data, notes
                FROM scenarios
                WHERE symbol = ?
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (symbol, limit),
            )
        else:
            cursor.execute(
                """
                SELECT id, created_at, symbol, raw_text, parsed_data, notes
                FROM scenarios
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            )

        rows = cursor.fetchall()
        conn.close()

        scenarios = []
        for row in rows:
            scenarios.append(
                {
                    "id": row[0],
                    "created_at": row[1],
                    "symbol": row[2],
                    "raw_text": row[3],
                    "parsed_data": json.loads(row[4]),
                    "notes": row[5],
                }
            )

        return scenarios

    def delete_scenario(self, scenario_id: int) -> bool:
        """シナリオを削除する.

        Args:
            scenario_id: シナリオID

        Returns:
            削除に成功した場合True
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM scenarios WHERE id = ?", (scenario_id,))

        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return deleted

    def search_scenarios_by_date_range(
        self,
        start_date: str,
        end_date: str,
        symbol: str | None = None,
    ) -> list[dict[str, Any]]:
        """日付範囲でシナリオを検索する.

        Args:
            start_date: 開始日時（ISO形式）
            end_date: 終了日時（ISO形式）
            symbol: 銘柄コードでフィルタ（Noneの場合は全件）

        Returns:
            シナリオデータのリスト
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if symbol:
            cursor.execute(
                """
                SELECT id, created_at, symbol, raw_text, parsed_data, notes
                FROM scenarios
                WHERE symbol = ? AND created_at BETWEEN ? AND ?
                ORDER BY created_at DESC
            """,
                (symbol, start_date, end_date),
            )
        else:
            cursor.execute(
                """
                SELECT id, created_at, symbol, raw_text, parsed_data, notes
                FROM scenarios
                WHERE created_at BETWEEN ? AND ?
                ORDER BY created_at DESC
            """,
                (start_date, end_date),
            )

        rows = cursor.fetchall()
        conn.close()

        scenarios = []
        for row in rows:
            scenarios.append(
                {
                    "id": row[0],
                    "created_at": row[1],
                    "symbol": row[2],
                    "raw_text": row[3],
                    "parsed_data": json.loads(row[4]),
                    "notes": row[5],
                }
            )

        return scenarios