# scanner.py
import requests
import concurrent.futures
from colorama import Fore, Style, init
from sites import SITES
from urllib.parse import quote

init(autoreset=True)

class OSINTSanner:
    def __init__(self, username):
        self.username = username
        self.results = {}
        self.found_count = 0

    def check_site(self, site_name, url_template):
        """Check if a profile exists on a specific site"""
        # ইউজারনেম এনকোড করা (স্পেস ও বিশেষ ক্যারেক্টার হ্যান্ডেল করতে)
        encoded_username = quote(self.username, safe='')
        
        # URL-এ { } এর সংখ্যা চেক করে সঠিকভাবে ফরম্যাট করা
        try:
            if url_template.count('{}') == 1:
                url = url_template.format(encoded_username)
            else:
                # একাধিক {} থাকলে সব জায়গায় ইউজারনেম বসানো
                url = url_template.replace('{}', encoded_username)
        except Exception:
            return site_name, False, url_template
        
        try:
            resp = requests.get(url, timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if resp.status_code == 200:
                # Check for false positives (custom 404 pages)
                content = resp.text.lower()
                not_found_keywords = [
                    'not found', 'does not exist', 'page not found', 
                    'sorry, this page', 'account not found', 'user not found',
                    'no results found', 'profile not available', '404'
                ]
                for keyword in not_found_keywords:
                    if keyword in content:
                        return site_name, False, url
                return site_name, True, url
            else:
                return site_name, False, url
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return site_name, False, url
        except Exception:
            return site_name, False, url

    def scan_all(self):
        """Scan all sites in parallel using threading"""
        print(f"{Fore.CYAN}[*] Searching for '{self.username}' on {len(SITES)} sites...{Style.RESET_ALL}")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_site = {
                executor.submit(self.check_site, name, template): name 
                for name, template in SITES.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_site):
                site_name, found, url = future.result()
                if found:
                    self.results[site_name] = url
                    self.found_count += 1
                    print(f"{Fore.GREEN}[+] {site_name}: {url}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[-] {site_name}: Not Found{Style.RESET_ALL}")
        
        return self.results

    def generate_report(self, email_check=None):
        """Generate and save a text report"""
        report = f"""
{'='*60}
        OSINT BOMBER REPORT
        Username: {self.username}
{'='*60}

[+] Profiles Found: {self.found_count}
"""
        for site, url in self.results.items():
            report += f"  • {site}: {url}\n"
        
        if email_check:
            report += f"\n[+] Email Leak Check:\n{email_check}\n"
        
        report += f"\n{'='*60}\n"
        
        with open(f"output/report_{self.username}.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        return report