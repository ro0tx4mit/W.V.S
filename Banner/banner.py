from termcolor import cprint

class Banner:
    def display(self):
        try:
            banner = r'''
 __        __     __     __      ____  
 \ \      / /     \ \   / /     / ___|
  \ \ /\ / /       \ \ / /      \___ \
   \ V  V /    _    \ V /    _   ___) |
    \_/\_/    (_)    \_/    (_) |____/  
                                         
     W . V . S  -  Web Vulnerability Scanner
          Developed By: SUDO EXPLOIT
                Version: 1.0
            '''
            cprint(banner, 'cyan', attrs=['bold'])

        except ImportError:
            print("Error: termcolor module is not installed.")
            print(banner)
