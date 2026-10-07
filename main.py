import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# --- SETTINGS ---
TARGET_POST_URL = "https://www.instagram.com/reel/DOn8PZcjeip/" # Reels URL to be targeted
# ---------------

def read_file(file_name):
    """General function to read lines from a given text file"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: {file_name} file not found!")
        return []

def wait_for_action(min_sec, max_sec, action_name="Action"):
    """Pauses the script for a random duration between actions to mimic human behavior"""
    wait_time = random.randint(min_sec, max_sec)
    print(f"   [⏳] {action_name} completed. Waiting for {wait_time} seconds for safety...")
    time.sleep(wait_time)

def force_click(driver, labels):
    """
    Finds and forcefully clicks elements that might be hidden or covered by other divs.
    Targeting parent elements or using JS click to bypass UI blockages.
    """
    conditions = " or ".join([f"@aria-label='{label}'" for label in labels])
    xpath = f"//*[local-name()='svg' and ({conditions})]"

    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )

    for el in elements:
        try:
            # Scroll element into the center of the view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(0.5)

            try:
                # Method 1: Try to click the interactable parent container
                parent_element = el.find_element(By.XPATH, "./ancestor::*[@role='button' or name()='button' or name()='a'][1]")
                driver.execute_script("arguments[0].click();", parent_element)
                return True
            except:
                # Method 2: Fallback to clicking the SVG directly
                driver.execute_script("arguments[0].click();", el)
                return True
        except:
            continue
            
    raise Exception("Button was found on screen but could not be clicked.")

def main():
    session_ids = read_file("accounts.txt")
    target_users = read_file("target_users.txt")
    
    if not session_ids:
        print("No accounts found. Program is terminating.")
        return
        
    if not target_users:
        print("WARNING: target_users.txt file is empty or missing!")
        return

    failed_sessions = []

    for index, session_id in enumerate(session_ids, start=1):
        print(f"\n--- [{index}/{len(session_ids)}] Testing Account (Selenium) ---")
        
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized") 
        # chrome_options.add_argument("--headless") # Uncomment to run in background
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            print(" -> Browser initialized, injecting session_id...")
            driver.get("https://www.instagram.com/robots.txt")
            driver.add_cookie({
                'name': 'sessionid',
                'value': session_id,
                'domain': '.instagram.com'
            })
            
            driver.get(TARGET_POST_URL)
            
            # Mimic watching the reel
            watch_time = random.randint(15, 35) 
            print(f"[+] Login successful! Watching the video for {watch_time} seconds...")
            time.sleep(watch_time)
            
            if "login" in driver.current_url:
                raise Exception("Redirected to login page. Session is invalid.")

            # --- ACTION 1: LIKE ---
            try:
                print(" -> Liking the post...")
                force_click(driver, ['Beğen', 'Like'])
                wait_for_action(3, 7, "Like")
            except Exception as e:
                print("   [-] Already liked or button could not be found.")

            # --- ACTION 2: SAVE ---
            try:
                print(" -> Saving the post...")
                force_click(driver, ['Kaydet', 'Save'])
                wait_for_action(3, 6, "Save")
            except Exception as e:
                print("   [-] Already saved or button could not be found.")

            # --- ACTION 3: SHARE (DM) ---
            try:
                print(" -> Opening share menu (DM)...")
                force_click(driver, ['Gönderiyi paylaş', 'Share Post', 'Paylaş', 'Share', 'Şununla paylaş', 'Share with'])
                wait_for_action(3, 6, "Opening Share Menu") 
                
                # Pick max 3 random users from the target list
                selected_users = random.sample(target_users, min(3, len(target_users)))
                print(f" -> Searching for selected users: {selected_users}")
                
                search_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@type='text' or @name='query' or @placeholder='Ara' or @placeholder='Search']"))
                )

                for user in selected_users:
                    # Safely clear the search box
                    driver.execute_script("arguments[0].value = '';", search_box) 
                    search_box.send_keys(Keys.CONTROL + "a")
                    search_box.send_keys(Keys.BACKSPACE)
                    time.sleep(1)
                    
                    # Type the username and wait for results
                    search_box.send_keys(user)
                    time.sleep(random.uniform(2.5, 4.0)) 
                    
                    # Click on the user's name or the radio/checkbox button
                    first_result = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"(//div[@role='dialog']//span[text()='{user}']/ancestor::div[@role='button'] | //div[@role='dialog']//input[@type='checkbox']/parent::*)[1]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_result)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", first_result)
                    time.sleep(random.uniform(1.0, 2.0))
                
                print(" -> Clicking the send button...")
                send_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[@role='button' and (.//text()='Gönder' or .//text()='Send' or text()='Gönder' or text()='Send')]"))
                )
                driver.execute_script("arguments[0].click();", send_button)
                wait_for_action(4, 8, "Sending DM")
                
            except Exception as e:
                print(f"   [-] Share action could not be completed. Error: {e}")

            print("[*] Actions COMPLETED for this account!")

        except Exception as e:
            print(f"[-] WARNING: Account {index} failed or could not access the page.")
            failed_sessions.append((index, session_id))
            
        finally:
            driver.quit()
            
        # 3. TRANSITION TO NEXT ACCOUNT
        if index < len(session_ids):
            if (index, session_id) in failed_sessions:
                wait_for_action(30, 60, "Skipping failed account")
            else:
                print("\n[*] Process successful. Entering long sleep cycle...")
                wait_for_action(7200, 18000, "Transition to next account (Long Sleep)")

    print("\n" + "="*40)
    print("ALL ACTIONS COMPLETED FOR ALL ACCOUNTS!")
    print("="*40)
    
    if failed_sessions:
        print("\n[!] WARNING: The following session_ids have failed:")
        with open("failed_accounts.txt", "w", encoding="utf-8") as f:
            for line_num, failed_id in failed_sessions:
                report = f"Line {line_num}: {failed_id}"
                print(f" - {report}")
                f.write(report + "\n")

if __name__ == "__main__":
    main()