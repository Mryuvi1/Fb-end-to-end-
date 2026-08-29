import json
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'

def clear_screen():
    os.system('clear')

def print_logo():
    logo = f"""{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║{Colors.GREEN}Owner Contact: 9919180262{Colors.CYAN}                                                                              
║{Colors.GREEN}tool: Cookie Loader{Colors.CYAN}                     



YYYYYYY       YYYYYYYUUUUUUUU     UUUUUUUUVVVVVVVV           VVVVVVVVIIIIIIIIII
Y:::::Y       Y:::::YU::::::U     U::::::UV::::::V           V::::::VI::::::::I
Y:::::Y       Y:::::YU::::::U     U::::::UV::::::V           V::::::VI::::::::I
Y::::::Y     Y::::::YUU:::::U     U:::::UUV::::::V           V::::::VII::::::II
YYY:::::Y   Y:::::YYY U:::::U     U:::::U  V:::::V           V:::::V   I::::I  
   Y:::::Y Y:::::Y    U:::::D     D:::::U   V:::::V         V:::::V    I::::I  
    Y:::::Y:::::Y     U:::::D     D:::::U    V:::::V       V:::::V     I::::I  
     Y:::::::::Y      U:::::D     D:::::U     V:::::V     V:::::V      I::::I  
      Y:::::::Y       U:::::D     D:::::U      V:::::V   V:::::V       I::::I  
       Y:::::Y        U:::::D     D:::::U       V:::::V V:::::V        I::::I  
       Y:::::Y        U:::::D     D:::::U        V:::::V:::::V         I::::I  
       Y:::::Y        U::::::U   U::::::U         V:::::::::V          I::::I  
       Y:::::Y        U:::::::UUU:::::::U          V:::::::V         II::::::II
    YYYY:::::YYYY      UU:::::::::::::UU            V:::::V          I::::::::I
    Y:::::::::::Y        UU:::::::::UU               V:::V           I::::::::I
    YYYYYYYYYYYYY          UUUUUUUUU                  VVV            IIIIIIIIII
  
                                                  
║{Colors.YELLOW}Facebook Inbox End to End Tool{Colors.CYAN}              
║{Colors.YELLOW}KING MAKER YUVI{Colors.CYAN}                                                                       
║{Colors.GREEN}Created by: KING MAKER YUVI{Colors.CYAN}                   
║                                                           
╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    
    lines = logo.split('\n')
    for line in lines:
        print(line)
        time.sleep(0.05)
    print()

def print_separator(char='═', length=60, color=Colors.CYAN):
    print(f"{color}{char * length}{Colors.RESET}")

def print_success(message):
    print(f"{Colors.GREEN}{Colors.BOLD}✓ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}{Colors.BOLD}✗ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.BLUE}{Colors.BOLD}ℹ {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠ {message}{Colors.RESET}")

def animate_loading(text, duration=2):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{Colors.CYAN}{chars[i % len(chars)]} {text}{Colors.RESET}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * (len(text) + 5) + '\r')
    sys.stdout.flush()

class FacebookMessenger:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.firefox_binary = None
        self.geckodriver_path = None
        self.haters_name = ""
        self.messages = []
        self.speed_seconds = 10
        self.target_uid = ""
        
    def find_firefox_binary(self):
        possible_paths = [
            '/data/data/com.termux/files/usr/bin/firefox',
            '/data/data/com.termux/files/usr/lib/firefox/firefox',
            os.path.expanduser('~/firefox/firefox'),
            'firefox'
        ]
        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        return None
    
    def find_geckodriver(self):
        possible_paths = [
            '/data/data/com.termux/files/usr/bin/geckodriver',
            os.path.expanduser('~/geckodriver'),
            'geckodriver'
        ]
        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        return None
    
    def load_messages_from_file(self, filepath):
        try:
            if not os.path.exists(filepath):
                print_error(f"File not found: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.messages = [line.strip() for line in lines if line.strip()]
            
            if not self.messages:
                print_error("No messages found in file")
                return False
            
            print_success(f"Loaded {len(self.messages)} messages from file")
            return True
            
        except Exception as e:
            print_error(f"Error reading file: {e}")
            return False
    
    def setup_driver(self):
        
        try:
            animate_loading("Initializing browser setup", 1)
            
            self.firefox_binary = self.find_firefox_binary()
            self.geckodriver_path = self.find_geckodriver()
            
            if not self.firefox_binary:
                print_error("Firefox not found")
                print_info("Install with: pkg install firefox")
                return False
            
            if not self.geckodriver_path:
                print_error("Geckodriver not found")
                print_info("Install with: pkg install geckodriver")
                return False
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            
            options.set_preference('network.http.pipelining', True)
            options.set_preference('network.http.proxy.pipelining', True)
            options.set_preference('network.http.pipelining.maxrequests', 8)
            options.set_preference('network.http.max-connections', 96)
            options.set_preference('network.http.max-connections-per-server', 32)
            options.set_preference('network.http.max-persistent-connections-per-server', 8)
            options.set_preference('network.http.connection-retry-timeout', 0)
            options.set_preference('network.http.connection-timeout', 90)
            options.set_preference('network.http.response.timeout', 300)
            options.set_preference('network.http.request.max-start-delay', 10)
            options.set_preference('network.http.keep-alive.timeout', 600)
            
         
            options.set_preference('browser.cache.disk.enable', False)
            options.set_preference('browser.cache.memory.enable', True)
            options.set_preference('browser.cache.memory.capacity', 65536)
            
            options.set_preference('dom.disable_beforeunload', True)
            options.set_preference('browser.tabs.remote.autostart', False)
            
            options.binary_location = self.firefox_binary
            
            service = Service(executable_path=self.geckodriver_path)
            self.driver = webdriver.Firefox(service=service, options=options)
            

            self.driver.set_page_load_timeout(120)
            self.driver.set_script_timeout(60)
            self.wait = WebDriverWait(self.driver, 30)
            
            print_success("Setup completed")
            return True
            
        except Exception as e:
            print_error(f"Setup failed: {e}")
            return False

    def parse_cookies(self, cookie_string):
        """Parse cookie string"""
        cookies = []
        for pair in cookie_string.split(';'):
            pair = pair.strip()
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.facebook.com',
                    'path': '/',
                    'secure': True
                })
        return cookies

    def login_with_cookies(self, cookie_string):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                animate_loading(f"Authenticating with Facebook (Attempt {retry_count + 1}/{max_retries})", 2)
                
                cookies = self.parse_cookies(cookie_string)
                
                try:
                    self.driver.get("https://www.facebook.com")
                    time.sleep(3)
                except Exception as e:
                    print_warning(f"Network issue, retrying... ({e})")
                    retry_count += 1
                    time.sleep(5)
                    continue
                
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                    except:
                        pass
                
                self.driver.refresh()
                time.sleep(4)
                
                
                indicators = [
                    "//a[@aria-label='Messenger']",
                    "//div[@role='navigation']",
                    "//div[@aria-label='Account']",
                    "//a[contains(@href, '/messages')]"
                ]
                
                for indicator in indicators:
                    try:
                        elements = self.driver.find_elements(By.XPATH, indicator)
                        if elements:
                            return True
                    except:
                        continue
                
                retry_count += 1
                if retry_count < max_retries:
                    print_warning("Login verification failed, retrying...")
                    time.sleep(5)
                
            except Exception as e:
                print_error(f"Login attempt failed: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(5)
        
        return False

    def send_single_message(self, message):
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                full_message = f"{self.haters_name} {message}" if self.haters_name else message
                
                selectors = [
                    "//div[@aria-label='Message'][@contenteditable='true']",
                    "//div[@role='textbox'][@contenteditable='true']",
                    "//div[@data-lexical-editor='true']",
                    "//p[@data-editor-content='true']",
                    "//div[contains(@class, 'notranslate')][@contenteditable='true']",
                ]
                
                message_box = None
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        if elements and elements[0].is_displayed():
                            message_box = elements[0]
                            break
                    except:
                        continue
                
                if not message_box:
                    js_script = """
                    var editables = document.querySelectorAll('[contenteditable="true"]');
                    for (var i = 0; i < editables.length; i++) {
                        var elem = editables[i];
                        if (elem.offsetParent !== null && 
                            (elem.getAttribute('role') === 'textbox' || 
                             elem.getAttribute('aria-label') === 'Message')) {
                            return elem;
                        }
                    }
                    return null;
                    """
                    message_box = self.driver.execute_script(js_script)
                
                if not message_box:
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue
                    return False
                
                # Focus and clear
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", message_box)
                time.sleep(0.2)
                
                try:
                    message_box.click()
                except:
                    self.driver.execute_script("arguments[0].focus(); arguments[0].click();", message_box)
                
                time.sleep(0.3)
                
                # Clear existing content
                self.driver.execute_script("""
                    var elem = arguments[0];
                    elem.focus();
                    elem.innerHTML = '';
                    elem.textContent = '';
                """, message_box)
                
                time.sleep(0.2)
                
                # Insert message using JavaScript
                escaped_msg = (full_message
                    .replace('\\', '\\\\')
                    .replace("'", "\\'")
                    .replace('"', '\\"')
                    .replace('\n', '\\n')
                    .replace('\r', '\\r')
                    .replace('\t', '\\t'))
                
                js_code = f"""
                var elem = arguments[0];
                var text = '{escaped_msg}';
                
                elem.textContent = text;
                elem.dispatchEvent(new Event('input', {{ bubbles: true, cancelable: true }}));
                elem.dispatchEvent(new Event('change', {{ bubbles: true, cancelable: true }}));
                elem.dispatchEvent(new InputEvent('input', {{ bubbles: true, cancelable: true, data: text }}));
                
                var range = document.createRange();
                var sel = window.getSelection();
                range.selectNodeContents(elem);
                range.collapse(false);
                sel.removeAllRanges();
                sel.addRange(range);
                
                return elem.textContent.length;
                """
                
                self.driver.execute_script(js_code, message_box)
                time.sleep(0.3)
                
                # Send message
                sent = False
                
                # Try Enter key
                try:
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.RETURN).perform()
                    sent = True
                except:
                    pass
                
                # Try Send button
                if not sent:
                    send_selectors = [
                        "//div[@aria-label='Send']",
                        "//div[@aria-label='Press enter to send']",
                        "//button[contains(@aria-label, 'Send')]",
                    ]
                    
                    for selector in send_selectors:
                        try:
                            send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            send_btn.click()
                            sent = True
                            break
                        except:
                            continue
                
                # JavaScript send
                if not sent:
                    try:
                        js_send = """
                        var elem = arguments[0];
                        var enterEvent = new KeyboardEvent('keydown', {
                            key: 'Enter',
                            code: 'Enter',
                            keyCode: 13,
                            which: 13,
                            bubbles: true,
                            cancelable: true
                        });
                        elem.dispatchEvent(enterEvent);
                        """
                        self.driver.execute_script(js_send, message_box)
                        sent = True
                    except:
                        pass
                
                if sent:
                    return True
                elif attempt < max_attempts - 1:
                    time.sleep(2)
                    
            except Exception as e:
                if attempt < max_attempts - 1:
                    time.sleep(2)
                    continue
        
        return False

    def start_sending(self):
        message_index = 0
        message_count = 0
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        clear_screen()
        print_logo()
        print_info("Message sending started - Press Ctrl+C to stop")
        print_separator()
        print()
        
        while True:
            try:
                message = self.messages[message_index]
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Send message
                success = self.send_single_message(message)
                message_count += 1
                
                if success:
                    consecutive_failures = 0
                    
                    # Display beautiful formatted output
                    print(f"{Colors.CYAN}{Colors.BOLD}┌─────────────────────────────────────────────────────────┐{Colors.RESET}")
                    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}{Colors.BOLD}Message #{message_count}{Colors.RESET}")
                    print(f"{Colors.CYAN}│{Colors.RESET}")
                    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.MAGENTA}Target UID:{Colors.RESET} {Colors.WHITE}{self.target_uid}{Colors.RESET}")
                    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.MAGENTA}Message:{Colors.RESET} {Colors.WHITE}{message[:40]}{'...' if len(message) > 40 else ''}{Colors.RESET}")
                    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.MAGENTA}Time:{Colors.RESET} {Colors.WHITE}{current_time}{Colors.RESET}")
                    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.MAGENTA}Status:{Colors.RESET} {Colors.GREEN}{Colors.BOLD}✓ SENT{Colors.RESET}")
                    print(f"{Colors.CYAN}{Colors.BOLD}└─────────────────────────────────────────────────────────┘{Colors.RESET}")
                else:
                    consecutive_failures += 1
                    
                    print(f"{Colors.RED}{Colors.BOLD}┌─────────────────────────────────────────────────────────┐{Colors.RESET}")
                    print(f"{Colors.RED}│{Colors.RESET} {Colors.YELLOW}{Colors.BOLD}Message #{message_count}{Colors.RESET}")
                    print(f"{Colors.RED}│{Colors.RESET}")
                    print(f"{Colors.RED}│{Colors.RESET} {Colors.MAGENTA}Target UID:{Colors.RESET} {Colors.WHITE}{self.target_uid}{Colors.RESET}")
   
