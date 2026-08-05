import os
from colorama import Fore, Style, init
from scanner import OSINTSanner
from hibp_checker import HIBPChecker

init(autoreset=True)

def banner():
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   {Fore.RED}██╗  ██╗███████╗██╗███╗   ██╗████████╗{Fore.CYAN}        ║
║   {Fore.RED}██║  ██║██╔════╝██║████╗  ██║╚══██╔══╝{Fore.CYAN}        ║
║   {Fore.RED}███████║███████╗██║██╔██╗ ██║   ██║   {Fore.CYAN}        ║
║   {Fore.RED}██╔══██║╚════██║██║██║╚██╗██║   ██║   {Fore.CYAN}        ║
║   {Fore.RED}██║  ██║███████║██║██║ ╚████║   ██║   {Fore.CYAN}        ║
║   {Fore.RED}╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   {Fore.CYAN}        ║
║                                                          ║
║        {Fore.YELLOW}OSINT BOMBER v2.0 - 50+ Site Scanner{Fore.CYAN}        ║
║        {Fore.YELLOW}Ethical Hacking Tool - For Education Only{Fore.CYAN}     ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

def main():
    os.makedirs("output", exist_ok=True)
    banner()
    
    print(f"{Fore.YELLOW}[!] WARNING: This tool is for checking YOUR OWN accounts only{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Scanning others without permission is ILLEGAL{Style.RESET_ALL}\n")
    
    username = input(f"{Fore.CYAN}[?] Enter username to scan: {Style.RESET_ALL}").strip()
    if not username:
        print(f"{Fore.RED}[!] Username cannot be empty!{Style.RESET_ALL}")
        return
    
    scanner = OSINTSanner(username)
    scanner.scan_all()
    
    email = input(f"\n{Fore.CYAN}[?] Do you want to check an email for breaches? (Enter email / skip): {Style.RESET_ALL}").strip()
    email_result = None
    if email and email.lower() != 'skip':
        checker = HIBPChecker(email)
        email_result = checker.check()
        print(f"\n{email_result}")
    
    report = scanner.generate_report(email_result)
    print(f"\n{Fore.GREEN}[✓] Report saved to: output/report_{username}.txt{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{report}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()