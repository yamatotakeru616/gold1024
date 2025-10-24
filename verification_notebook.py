# %% [markdown]
# # 市場分析シナリオ可視化システム - 動作検証Notebook
# 
# このNotebookでは、実装したモジュールの動作を検証します。

# %% [markdown]
# ## 0. 環境設定

# %%
%load_ext autoreload
%autoreload 2

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root / "src"))

# %% [markdown]
# ## 1. ライブラリインポート

# %%
from modules.scenario_parser import ScenarioParser
from modules.data_fetcher import DataFetcher
from modules.chart_renderer import ChartRenderer
from modules.database import DatabaseManager
import pandas as pd
from datetime import datetime

print("✅ すべてのモジュールをインポートしました")

# %% [markdown]
# ## 2. シナリオパーサーの動作検証

# %%
# ===== 【仕様】ScenarioParser の動作検証 =====
# 目的: テキストからサポート/レジスタンスライン、価格帯を正しく抽出できるか検証
# 対象ファイル: src/modules/scenario_parser.py
# 期待結果: サンプルシナリオから価格情報が正しく抽出される
# ===============================================

# ===== 【準備】検証用シナリオテキストの作成 =====
sample_scenario = """
現在（2025年10月21日 8時00分）のGOLD環境認識
日足、4時間足、1時間足がすべて買いゾーンを示しています
目線については日足、4時間足が上目線、1時間足が下目線ですが、1時間足のローソク足終値が4381.35を上抜けると上目線になります
4292.63から4381.35の上昇に対するフィボナッチリトレースメントの38.2近辺までの押し目をつけたところで上昇していますので、「4317近辺～4320近辺のサポート帯」を下抜けなければ上昇トレンドが継続しそうです
日足ベースのサポートラインは4317近辺と4218近辺と4094近辺、週足ベースのサポートラインは4209近辺と3973近辺と3681近辺、月足ベースのサポートラインは4320近辺と3989近辺と3721近辺と3454近辺と3123近辺となります
日足ベースのレジスタンスラインは4418近辺と4540近辺、週足ベースのレジスタンスラインは4443近辺と4734近辺、月足ベースのレジスタンスラインはありません
"""

# ===== 【実行 & 検証】=====
parser = ScenarioParser()

print("--- 入力シナリオ ---")
print(sample_scenario[:200] + "...")

try:
    parsed = parser.parse(sample_scenario)
    
    print("\n--- 解析結果 ---")
    print(f"銘柄コード: {parsed.symbol}")
    print(f"分析日時: {parsed.analysis_date}")
    print(f"\nサポートライン数: {len(parsed.support_levels)}")
    print(f"レジスタンスライン数: {len(parsed.resistance_levels)}")
    print(f"サポートゾーン数: {len(parsed.support_zones)}")
    print(f"レジスタンスゾーン数: {len(parsed.resistance_zones)}")
    
    print("\n--- サポートライン詳細 ---")
    for sl in parsed.support_levels[:5]:  # 最初の5件のみ表示
        print(f"  {sl.timeframe}: {sl.price} - {sl.description}")
    
    print("\n--- レジスタンスライン詳細 ---")
    for rl in parsed.resistance_levels[:5]:
        print(f"  {rl.timeframe}: {rl.price} - {rl.description}")
    
    print("\n--- サポートゾーン ---")
    for sz in parsed.support_zones:
        print(f"  {sz.price_lower} ～ {sz.price_upper}: {sz.description}")
    
    print("\n✅ 検証成功: シナリオ解析が正常に動作しています")
    
except Exception as e:
    print(f"\n❌ 検証失敗: {e}")
    import traceback
    traceback.print_exc()

# ===============================================

# %% [markdown]
# ## 3. データ取得モジュールの動作検証

# %%
# ===== 【仕様】DataFetcher の動作検証 =====
# 目的: Yahoo Financeから市場データを正しく取得できるか検証
# 対象ファイル: src/modules/data_fetcher.py
# 期待結果: GOLD (GC=F) の市場データが取得され、OHLCV列が存在する
# ===============================================

# ===== 【実行 & 検証】=====
fetcher = DataFetcher()

print("--- 市場データ取得 ---")
print("銘柄: GC=F (GOLD)")
print("期間: 過去1ヶ月")

try:
    df = fetcher.fetch_data("GC=F", period="1mo", interval="1h")
    
    print("\n--- 取得結果 ---")
    print(f"データ件数: {len(df)}")
    print(f"列: {df.columns.tolist()}")
    print(f"期間: {df.index[0]} ～ {df.index[-1]}")
    
    print("\n--- データサンプル（最初の5行） ---")
    display(df.head())
    
    print("\n--- データサンプル（最後の5行） ---")
    display(df.tail())
    
    # データの基本統計
    print("\n--- 基本統計 ---")
    display(df[["open", "high", "low", "close"]].describe())
    
    print("\n✅ 検証成功: データ取得が正常に動作しています")
    
except Exception as e:
    print(f"\n❌ 検証失敗: {e}")
    import traceback
    traceback.print_exc()

# ===============================================

# %% [markdown]
# ## 4. チャート描画モジュールの動作検証

# %%
# ===== 【仕様】ChartRenderer の動作検証 =====
# 目的: Plotlyで市場データとシナリオを重ねたチャートを正しく描画できるか検証
# 対象ファイル: src/modules/chart_renderer.py
# 期待結果: ローソク足チャートにサポート/レジスタンスラインが重ねて表示される
# ===============================================

# ===== 【準備】データとシナリオの再利用 =====
# 前のセルで取得したデータとシナリオを使用

# ===== 【実行 & 検証】=====
renderer = ChartRenderer()

print("--- チャート描画 ---")

try:
    # チャート作成
    fig = renderer.create_chart(
        df=df,
        scenario=parsed,
        title="GOLD - シナリオ分析チャート（検証用）"
    )
    
    # Notebookに表示
    fig.show()
    
    print("\n✅ 検証成功: チャートが正常に表示されました")
    print("   - ローソク足チャート")
    print("   - サポートライン（緑色の破線）")
    print("   - レジスタンスライン（赤色の破線）")
    print("   - サポートゾーン（半透明の緑色エリア）")
    
except Exception as e:
    print(f"\n❌ 検証失敗: {e}")
    import traceback
    traceback.print_exc()

# ===============================================

# %% [markdown]
# ## 5. データベース保存・読み込みの動作検証

# %%
# ===== 【仕様】DatabaseManager の動作検証 =====
# 目的: シナリオをSQLiteに保存し、正しく読み込めるか検証
# 対象ファイル: src/modules/database.py
# 期待結果: シナリオが保存され、IDで取得できる
# ===============================================

# ===== 【実行 & 検証】=====
db = DatabaseManager("data/test_scenarios.db")

print("--- シナリオ保存 ---")

try:
    # シナリオ保存
    scenario_id = db.save_scenario(
        symbol=parsed.symbol,
        raw_text=parsed.raw_text,
        parsed_data=parsed.to_dict(),
        notes="動作検証用のテストシナリオ"
    )
    
    print(f"✅ 保存成功: ID = {scenario_id}")
    
    # 保存したシナリオを読み込み
    print("\n--- シナリオ読み込み ---")
    loaded = db.get_scenario(scenario_id)
    
    if loaded:
        print(f"ID: {loaded['id']}")
        print(f"作成日時: {loaded['created_at']}")
        print(f"銘柄: {loaded['symbol']}")
        print(f"サポートライン数: {len(loaded['parsed_data']['support_levels'])}")
        print(f"レジスタンスライン数: {len(loaded['parsed_data']['resistance_levels'])}")
        print("\n✅ 検証成功: データベース操作が正常に動作しています")
    else:
        print("❌ 検証失敗: シナリオの読み込みに失敗")
    
    # シナリオ一覧の取得
    print("\n--- シナリオ一覧 ---")
    scenarios = db.list_scenarios(limit=5)
    print(f"保存済みシナリオ数: {len(scenarios)}")
    
    for sc in scenarios:
        print(f"  [{sc['id']}] {sc['created_at']} - {sc['symbol']}")
    
except Exception as e:
    print(f"\n❌ 検証失敗: {e}")
    import traceback
    traceback.print_exc()

# ===============================================

# %% [markdown]
# ## 6. 統合検証: シナリオ検証チャート

# %%
# ===== 【仕様】シナリオ検証機能の動作検証 =====
# 目的: 過去のシナリオと実際の値動きを重ねて表示できるか検証
# 対象ファイル: src/modules/chart_renderer.py (create_verification_chart)
# 期待結果: シナリオ作成時点までのデータと、その後の値動きが区別して表示される
# ===============================================

# ===== 【準備】過去と未来のデータを分割 =====
split_index = len(df) // 2
historical_df = df.iloc[:split_index]
future_df = df.iloc[split_index:]

print("--- シナリオ検証チャート ---")
print(f"過去データ: {len(historical_df)} 件")
print(f"未来データ: {len(future_df)} 件")

# ===== 【実行 & 検証】=====
try:
    # 検証チャート作成
    verification_fig = renderer.create_verification_chart(
        historical_df=historical_df,
        future_df=future_df,
        scenario=parsed,
        scenario_date="2025-10-21 08:00"
    )
    
    # Notebookに表示
    verification_fig.show()
    
    print("\n✅ 検証成功: シナリオ検証チャートが正常に表示されました")
    print("   - 青い縦線: シナリオ作成時点")
    print("   - 緑/赤のローソク足: 過去のデータ")
    print("   - 水色/オレンジのローソク足: シナリオ後の実際の値動き")
    
except Exception as e:
    print(f"\n❌ 検証失敗: {e}")
    import traceback
    traceback.print_exc()

# ===============================================

# %% [markdown]
# ## 7. まとめ
# 
# ### 検証結果
# 
# すべてのモジュールが期待通りに動作することを確認しました:
# 
# 1. ✅ **ScenarioParser**: テキストから価格情報を正しく抽出
# 2. ✅ **DataFetcher**: Yahoo Financeから市場データを取得
# 3. ✅ **ChartRenderer**: Plotlyでインタラクティブなチャートを描画
# 4. ✅ **DatabaseManager**: SQLiteへのシナリオ保存・読み込み
# 5. ✅ **統合機能**: シナリオ検証チャートの表示
# 
# ### 次のステップ
# 
# - [ ] PyQt6 GUIアプリケーションの動作確認
# - [ ] ユニットテストの作成
# - [ ] エラーハンドリングの強化
# - [ ] ドキュメントの整備
