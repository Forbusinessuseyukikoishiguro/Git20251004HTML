"""
【新人エンジニア向け】Selenium初期設定完全ガイド

1. 必要なモジュールのインストール
2. WebDriverの初期化
3. 基本的な操作例
"""

# ============================================================
# 1. 必要なモジュールのインストール
# ============================================================

"""
ターミナルで以下のコマンドを実行してください：

pip install selenium
pip install webdriver-manager

または

pip install selenium webdriver-manager
"""

# ============================================================
# 2. 必要なモジュールのインポート
# ============================================================

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


# ============================================================
# 3. ロガーの設定
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================================
# 4. WebDriverの初期化関数
# ============================================================

def setup_driver():
    """WebDriverを初期化する関数
    
    Returns:
        WebDriver: 初期化済みのWebDriverオブジェクト
    
    Examples:
        >>> driver = setup_driver()
        >>> driver.get("https://www.google.com")
    """
    try:
        logger.info("WebDriverを初期化しています...")
        
        # ChromeDriverのサービスを設定
        service = Service(ChromeDriverManager().install())
        
        # WebDriverを作成
        driver = webdriver.Chrome(service=service)
        
        # ウィンドウを最大化
        driver.maximize_window()
        
        logger.info("WebDriverの初期化が完了しました")
        return driver
    
    except Exception as e:
        logger.error(f"WebDriverの初期化に失敗: {e}")
        raise


def setup_driver_with_options():
    """オプション付きでWebDriverを初期化する関数
    
    Returns:
        WebDriver: 初期化済みのWebDriverオブジェクト
    """
    try:
        logger.info("WebDriver（オプション付き）を初期化しています...")
        
        # Chromeのオプション設定
        options = webdriver.ChromeOptions()
        
        # よく使うオプション
        options.add_argument('--start-maximized')  # 最大化で起動
        options.add_argument('--disable-notifications')  # 通知を無効化
        options.add_argument('--disable-popup-blocking')  # ポップアップブロック無効化
        
        # ヘッドレスモード（画面を表示しない）
        # options.add_argument('--headless')  # 本番環境で使用
        
        # User-Agentを設定（bot検出を回避）
        # options.add_argument('user-agent=Mozilla/5.0 ...')
        
        # サービスを設定
        service = Service(ChromeDriverManager().install())
        
        # WebDriverを作成
        driver = webdriver.Chrome(service=service, options=options)
        
        # 暗黙的な待機時間を設定（要素が見つかるまで最大10秒待つ）
        driver.implicitly_wait(10)
        
        logger.info("WebDriverの初期化が完了しました")
        return driver
    
    except Exception as e:
        logger.error(f"WebDriverの初期化に失敗: {e}")
        raise


# ============================================================
# 5. 基本的な操作例
# ============================================================

def example_google_search(driver):
    """Googleで検索する例
    
    Args:
        driver: WebDriverオブジェクト
    """
    try:
        logger.info("Googleにアクセスします")
        
        # Googleを開く
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # 検索ボックスを見つける
        logger.info("検索ボックスを探しています")
        search_box = driver.find_element(By.NAME, "q")
        
        # 検索キーワードを入力
        keyword = "Python Selenium"
        logger.info(f"キーワード「{keyword}」を入力します")
        search_box.send_keys(keyword)
        
        # Enterキーを押す
        logger.info("検索を実行します")
        search_box.send_keys(Keys.RETURN)
        
        # 結果が表示されるまで待つ
        time.sleep(3)
        
        # タイトルを取得
        logger.info(f"ページタイトル: {driver.title}")
        
        # 検索結果のタイトルを取得（最初の5件）
        logger.info("検索結果を取得します")
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        
        for i, result in enumerate(results[:5], 1):
            logger.info(f"  {i}. {result.text}")
        
        logger.info("検索が完了しました")
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise


def example_wait_for_element(driver):
    """要素が表示されるまで待つ例
    
    Args:
        driver: WebDriverオブジェクト
    """
    try:
        logger.info("要素の待機処理の例")
        
        driver.get("https://www.google.com")
        
        # 明示的な待機（最大10秒）
        wait = WebDriverWait(driver, 10)
        
        # 検索ボックスが表示されるまで待つ
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        logger.info("検索ボックスが見つかりました")
        
        # クリック可能になるまで待つ
        clickable_element = wait.until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        
        clickable_element.send_keys("Selenium待機処理")
        clickable_element.send_keys(Keys.RETURN)
        
        logger.info("待機処理が完了しました")
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise


# ============================================================
# 6. 実践例: ふわふわ大福店のWeb自動化
# ============================================================

class WebAutomation:
    """Web自動化クラス"""
    
    def __init__(self):
        """初期化"""
        self.driver = None
        logger.info("WebAutomationクラスを初期化しました")
    
    def start(self):
        """ブラウザを起動"""
        logger.info("ブラウザを起動します")
        self.driver = setup_driver_with_options()
    
    def stop(self):
        """ブラウザを終了"""
        if self.driver:
            logger.info("ブラウザを終了します")
            self.driver.quit()
            self.driver = None
    
    def search_daifuku_recipe(self, keyword: str = "大福 レシピ"):
        """大福のレシピを検索
        
        Args:
            keyword: 検索キーワード
        """
        if not self.driver:
            raise ValueError("ブラウザが起動していません")
        
        try:
            logger.info(f"「{keyword}」を検索します")
            
            # Googleを開く
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            # 検索
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # 結果を表示
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
            logger.info(f"{len(results)}件の検索結果が見つかりました")
            
            for i, result in enumerate(results[:3], 1):
                logger.info(f"  {i}. {result.text}")
        
        except Exception as e:
            logger.error(f"検索中にエラー: {e}")
            raise
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """スクリーンショットを保存
        
        Args:
            filename: 保存するファイル名
        """
        if not self.driver:
            raise ValueError("ブラウザが起動していません")
        
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"スクリーンショットを保存しました: {filename}")
        
        except Exception as e:
            logger.error(f"スクリーンショット保存エラー: {e}")
            raise


# ============================================================
# 7. メイン処理
# ============================================================

def main():
    """メイン処理"""
    
    print("=" * 60)
    print("Selenium初期設定完全ガイド")
    print("=" * 60)
    
    # 方法1: シンプルな初期化
    print("\n【方法1: シンプルな初期化】")
    driver1 = setup_driver()
    
    try:
        # Google検索の例
        example_google_search(driver1)
        
        # スクリーンショット
        driver1.save_screenshot("google_search.png")
        logger.info("スクリーンショットを保存: google_search.png")
    
    finally:
        logger.info("ブラウザを終了します")
        driver1.quit()
    
    time.sleep(2)
    
    # 方法2: オプション付き初期化
    print("\n【方法2: オプション付き初期化】")
    driver2 = setup_driver_with_options()
    
    try:
        # 待機処理の例
        example_wait_for_element(driver2)
    
    finally:
        logger.info("ブラウザを終了します")
        driver2.quit()
    
    time.sleep(2)
    
    # 方法3: クラスを使った自動化
    print("\n【方法3: クラスを使った自動化】")
    automation = WebAutomation()
    
    try:
        automation.start()
        automation.search_daifuku_recipe("ふわふわ大福 作り方")
        automation.take_screenshot("daifuku_search.png")
    
    finally:
        automation.stop()
    
    print("\n" + "=" * 60)
    print("すべての処理が完了しました")
    print("=" * 60)


if __name__ == "__main__":
    main()
