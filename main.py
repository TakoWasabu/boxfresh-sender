import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

id = input("誰に送りたいの :")


def open_browser():
    # Chromeの設定
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # ウィンドウを最大化
    # Chromeの起動
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_random_input(file_path):
    # ファイルからランダムに一行選択する
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 空行を除外
    lines = [line.strip() for line in lines if line.strip()]
    return random.choice(lines) if lines else None

def perform_action(driver, input_text):
    try:
        # 1. 指定のサイトへ移動
        driver.get("https://boxfreshapp.com/" + id)  

        # 2. ボタンを探してクリック
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.button-form-submit.center-block"))
        )
        button.click()
        
        time.sleep(2)

        # 3. 指定の文字を入力
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control.text.required.user-form-text"))
        )
        input_field.send_keys(input_text)

        # 4. 確定ボタンを押す
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.button-form-submit.center-block"))
        )
        submit_button.click()

        time.sleep(2)

    except Exception as e:
        print(f"エラー発生: {e}")
        time.sleep(5)  # エラーが発生したら少し待って再試行


max_attempts = int(input("ランダムに選べる回数を入力してください: "))


# 無限ループで繰り返し
for _ in range(max_attempts):
    driver = open_browser()  # 新しいブラウザを開く
    random_input_text = get_random_input('odai.txt')  # ランダムに選ばれる入力テキスト
    if random_input_text:
        perform_action(driver, random_input_text)  # ランダムに選ばれた入力を使ってアクションを実行
    else:
        print("入力するテキストが見つかりませんでした。")
    driver.quit()  # 処理後にブラウザを閉じる
    time.sleep(2)  # 少し待ってから次の繰り返し
