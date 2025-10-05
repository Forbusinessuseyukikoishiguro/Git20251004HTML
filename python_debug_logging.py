"""
【新人エンジニア向け】Pythonデバッグツール＆ロギング完全ガイド

1. デバッグツールのインストール
2. ロギング処理の書き方
3. 実践例
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# 1. デバッグツールのインストール方法
# ============================================================

"""
■ 基本的なデバッグツール（インストール不要、標準ライブラリ）
- pdb: Python Debugger（対話的デバッガ）
- logging: ログ出力
- traceback: エラー情報の詳細表示

■ インストールが必要なデバッグツール

pip install ipdb          # IPythonベースのデバッガ（使いやすい）
pip install pudb          # ビジュアルデバッガ
pip install loguru        # 簡単で強力なロギング
pip install icecream      # デバッグプリント改善
pip install coloredlogs   # ログに色付け

■ VSCodeでのデバッグ
- VSCode標準機能を使用（拡張機能不要）
- F5キーでデバッグ実行
- ブレークポイント設定可能
"""


# ============================================================
# 2. 標準loggingモジュールの基本
# ============================================================

def basic_logging_example():
    """基本的なロギングの使い方"""
    
    print("\n" + "="*60)
    print("基本的なロギング")
    print("="*60)
    
    # 基本設定
    logging.basicConfig(
        level=logging.DEBUG,  # ログレベル設定
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 5つのログレベル
    logging.debug("デバッグ情報（開発時のみ）")
    logging.info("一般的な情報")
    logging.warning("警告メッセージ")
    logging.error("エラーが発生")
    logging.critical("致命的なエラー")


# ============================================================
# 3. ファイルにログを保存
# ============================================================

def file_logging_example():
    """ログをファイルに保存する"""
    
    print("\n" + "="*60)
    print("ファイルロギング")
    print("="*60)
    
    # ログディレクトリ作成
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # ログファイル名（日時付き）
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # ロガーの設定
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # ファイルハンドラ
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # フォーマッター
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラを追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # ログ出力
    logger.debug("これはデバッグログ（ファイルのみ）")
    logger.info("これは情報ログ（ファイル＋コンソール）")
    logger.warning("これは警告ログ")
    logger.error("これはエラーログ")
    
    print(f"\nログファイル保存先: {log_file}")
    
    return logger


# ============================================================
# 4. 実践的なロガークラス
# ============================================================

class AppLogger:
    """アプリケーション用ロガークラス
    
    使い方:
        logger = AppLogger("MyApp")
        logger.info("アプリ起動")
    """
    
    def __init__(self, name: str = "App", log_to_file: bool = True):
        """
        Args:
            name: ロガー名
            log_to_file: ファイルにも出力するか
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 既存のハンドラをクリア
        self.logger.handlers.clear()
        
        # コンソールハンドラ
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # ファイルハンドラ（オプション）
        if log_to_file:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """デバッグログ"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """情報ログ"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告ログ"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """エラーログ"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str):
        """致命的エラーログ"""
        self.logger.critical(message)


# ============================================================
# 5. エラー処理とロギングの組み合わせ
# ============================================================

def error_handling_with_logging():
    """エラー処理とロギングの実践例"""
    
    print("\n" + "="*60)
    print("エラー処理＋ロギング")
    print("="*60)
    
    logger = AppLogger("ErrorDemo", log_to_file=False)
    
    def divide(a: float, b: float) -> float:
        """割り算（エラー処理付き）"""
        try:
            logger.debug(f"計算開始: {a} ÷ {b}")
            result = a / b
            logger.info(f"計算成功: {a} ÷ {b} = {result}")
            return result
        
        except ZeroDivisionError:
            logger.error(f"ゼロ除算エラー: {a} ÷ {b}", exc_info=True)
            return None
        
        except Exception as e:
            logger.critical(f"予期しないエラー: {e}", exc_info=True)
            raise
    
    # 正常なケース
    divide(10, 2)
    
    # エラーケース
    divide(10, 0)


# ============================================================
# 6. デコレータを使ったロギング
# ============================================================

def log_function_call(logger: AppLogger):
    """関数呼び出しを自動ログ出力するデコレータ"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"関数 {func.__name__} 開始")
            logger.debug(f"  引数: args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                logger.info(f"関数 {func.__name__} 成功")
                logger.debug(f"  戻り値: {result}")
                return result
            
            except Exception as e:
                logger.error(f"関数 {func.__name__} でエラー: {e}", exc_info=True)
                raise
        
        return wrapper
    return decorator


# ============================================================
# 7. 実践例: うさうさ店長のふわふわ大福店
# ============================================================

class DaifukuShop:
    """ふわふわ大福店（ロギング付き）"""
    
    def __init__(self, name: str):
        self.name = name
        self.stock = 0
        self.sales = 0.0
        self.logger = AppLogger(name, log_to_file=True)
        self.logger.info(f"{name} を開店しました")
    
    @log_function_call
    def make_daifuku(self, count: int) -> bool:
        """大福を作る"""
        if count <= 0:
            self.logger.warning(f"不正な個数: {count}")
            return False
        
        self.stock += count
        self.logger.info(f"大福 {count}個 作成完了 → 在庫 {self.stock}個")
        return True
    
    @log_function_call
    def sell(self, count: int, price: float) -> bool:
        """大福を販売"""
        if count <= 0:
            self.logger.warning(f"不正な販売個数: {count}")
            return False
        
        if self.stock < count:
            self.logger.error(f"在庫不足: 要求{count}個、在庫{self.stock}個")
            return False
        
        self.stock -= count
        self.sales += count * price
        self.logger.info(f"販売成功: {count}個 × {price}円 = {count * price}円")
        self.logger.info(f"現在の状態: 在庫{self.stock}個、売上{self.sales}円")
        return True
    
    def close_shop(self):
        """閉店処理"""
        self.logger.info("="*40)
        self.logger.info("閉店処理")
        self.logger.info(f"本日の売上: {self.sales}円")
        self.logger.info(f"残り在庫: {self.stock}個")
        self.logger.info("="*40)


# ============================================================
# 8. pdbデバッガの使い方（コメント形式で説明）
# ============================================================

def pdb_example():
    """pdbデバッガの使い方
    
    実行して試す場合は、import pdb を追加して
    pdb.set_trace() の行のコメントを外してください
    """
    
    print("\n" + "="*60)
    print("pdbデバッガの使い方")
    print("="*60)
    
    x = 10
    y = 20
    
    # デバッガを起動（コメントを外すと対話モード開始）
    # import pdb; pdb.set_trace()
    
    result = x + y
    
    print(f"計算結果: {result}")
    
    print("""
pdbコマンド一覧:
  n (next)     : 次の行へ
  s (step)     : 関数の中に入る
  c (continue) : 次のブレークポイントまで実行
  l (list)     : 現在のコード表示
  p 変数名      : 変数の値を表示
  pp 変数名     : 変数を整形して表示
  q (quit)     : デバッガ終了
  h (help)     : ヘルプ表示
    """)


# ============================================================
# メイン処理
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("Pythonデバッグ＆ロギング完全ガイド")
    print("="*60)
    
    # 1. 基本的なロギング
    basic_logging_example()
    
    # 2. ファイルロギング
    file_logging_example()
    
    # 3. エラー処理＋ロギング
    error_handling_with_logging()
    
    # 4. pdbの使い方
    pdb_example()
    
    # 5. 実践例: うさうさ店長
    print("\n" + "="*60)
    print("実践例: ふわふわ大福店")
    print("="*60)
    
    # デコレータ用のロガー
    @log_function_call
    def demo_shop():
        shop = DaifukuShop("ふわふわ大福店")
        
        # 営業開始
        shop.make_daifuku(20)
        
        # 販売
        shop.sell(3, 300)
        shop.sell(5, 300)
        
        # 在庫不足エラー
        shop.sell(15, 300)
        
        # 閉店
        shop.close_shop()
    
    demo_shop()
    
    print("\n" + "="*60)
    print("完了")
    print("="*60)
    print("""
次のステップ:
1. logsフォルダ内のログファイルを確認
2. VSCodeでブレークポイントを設定してデバッグ実行
3. エラーが起きた時のログを確認する習慣をつける
    """)
