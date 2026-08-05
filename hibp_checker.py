import requests
from colorama import Fore, Style

class HIBPChecker:
    def __init__(self, email):
        self.email = email
        self.api_url = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"
        
    def check(self):
        try:
            url = self.api_url.format(self.email)
            # হেডার যোগ করলাম
            headers = {
                'User-Agent': 'OSINT-Bomber/1.0',
                'hibp-api-key': ''  # ফ্রি টায়ারে খালি রাখা যায়
            }
            resp = requests.get(url, timeout=10, headers=headers)
            
            if resp.status_code == 200:
                breaches = resp.json()
                result = f"{Fore.RED}[!] DANGER! Your email was found in {len(breaches)} data breaches!{Style.RESET_ALL}\n"
                for b in breaches[:5]:
                    result += f"    • {b['Name']} ({b['BreachDate']}) - {b['Description'][:100]}...\n"
                if len(breaches) > 5:
                    result += f"    • ... and {len(breaches)-5} more\n"
                return result
            elif resp.status_code == 404:
                return f"{Fore.GREEN}[✓] Good news! Your email was NOT found in any known breaches!{Style.RESET_ALL}"
            elif resp.status_code == 401:
                return f"{Fore.YELLOW}[!] API Key needed. Get free key from: https://haveibeenpwned.com/API/Key{Style.RESET_ALL}"
            else:
                return f"{Fore.YELLOW}[?] API check failed (Status: {resp.status_code}){Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.YELLOW}[?] Email check error: {str(e)}{Style.RESET_ALL}"