import itertools
import threading
import time
from queue import Queue
import random
import string
import os
# ___________________________________________________________ #
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
def obfuscate(text): return ''.join(random.choice(string.ascii_letters + string.digits) for _ in text)

def color(text):
    color_map = {
        '0': '\033[30m', '1': '\033[34m', '2': '\033[32m', '3': '\033[36m',
        '4': '\033[31m', '5': '\033[35m', '6': '\033[33m', '7': '\033[37m',
        '8': '\033[90m', '9': '\033[94m', 'a': '\033[92m', 'b': '\033[96m',
        'c': '\033[91m', 'd': '\033[95m', 'e': '\033[93m', 'f': '\033[97m',
        'l': '\033[1m', 'o': '\033[3m', 'r': '\033[0m'
    }
    
    result = []
    obfuscating = False
    i = 0
    
    while i < len(text):
        if text[i] == '§' and i + 1 < len(text):
            code = text[i + 1]
            if code == 'k':
                obfuscating = True
                i += 2
                continue
            elif obfuscating:
                obfuscating = False
            if code in color_map:
                result.append(color_map[code])
                i += 2
                continue
        
        if obfuscating: result.append(obfuscate(text[i]))
        else: result.append(text[i])
        
        i += 1
    
    return f"{''.join(result)}\033[0m"
# ___________________________________________________________ #
def worker(password, charset, queue, result, stop_event, update_interval):
    count = 0
    while not queue.empty() and not stop_event.is_set():
        length = queue.get()
        for guess in itertools.product(charset, repeat=length):
            guess_str = ''.join(guess)
            if count % update_interval == 0: print(color(f"§ftried password: §c{guess_str}"), end='\r')
            if guess_str == password:
                result.append(guess_str)
                stop_event.set()
                break
            count += 1
        queue.task_done()

def brute_forcer(password, num_threads=8, update_interval=10000):
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
    max_length = len(password)
    queue = Queue()
    result = []
    stop_event = threading.Event()

    for length in range(1, max_length + 1): queue.put(length)
    threads = [threading.Thread(target=worker, args=(password, charset, queue, result, stop_event, update_interval)) for _ in range(num_threads)]

    for thread in threads: thread.start()
    queue.join()

    for thread in threads: thread.join()
    return result[0] if result else None

def password_from_list(password):
    password_list_path = os.path.join(os.path.dirname(__file__), 'passlist.txt')
    try:
        with open(password_list_path, 'r') as file:
            for line in file:
                if line.strip() == password:
                    return password
    except FileNotFoundError: print(color('§cPassword list file not found. Proceeding with brute force...'))
    return None

clear()
print(color("""§0██████╗░██████╗░██╗░░░██╗████████╗███████╗  ███████╗░█████╗░██████╗░░█████╗░███████╗
§8██╔══██╗██╔══██╗██║░░░██║╚══██╔══╝██╔════╝  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
§8██████╦╝██████╔╝██║░░░██║░░░██║░░░█████╗░░  █████╗░░██║░░██║██████╔╝██║░░╚═╝█████╗░░
§7██╔══██╗██╔══██╗██║░░░██║░░░██║░░░██╔══╝░░  ██╔══╝░░██║░░██║██╔══██╗██║░░██╗██╔══╝░░
§f██████╦╝██║░░██║╚██████╔╝░░░██║░░░███████╗  ██║░░░░░╚█████╔╝██║░░██║╚█████╔╝███████╗
§f╚═════╝░╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░╚══════╝  ╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░╚════╝░╚══════╝\n"""))
print(color(f"§a@aitji's §r§lbrute_force_attacker\n§rthis is my §eprogram§r to run testing brute force cracking da §epassword§r\nmax threading: §a8\n§rtype: §cexit§r to stop the program!\n§4* §lwarning:§r§4 for §llow spec§r§4 pc it might take a long time, recommend playing with 1-6 letter\n\nenter §cpassword§r to test run brute force (only letter & english) §kheheboi"))

while True:
    password = input(': ')
    if password.lower() == 'exit':
        print(color('sure §l§cgoodbye!'))
        break

    method = input(color('§fDo you want to §l§6filter password§r§f from list first? (§ay§f/§cn§f): §r')).strip().lower()

    start_time = time.time()
    found_password = None

    if method in ['yes', 'y', 'yee', 'yep', '1']:
        n_time = time.time()
        found_password = password_from_list(password)
        e_time = time.time()
        print(color(f'§fTime taken (to scan §6file§f): §a{e_time - n_time:.2f} seconds'))
        if found_password: print(color(f'\n§fPassword found in list:§a {found_password}'))

    if not found_password: found_password = brute_forcer(password)
    end_time = time.time()

    if found_password: print(color(f'§fPassword found:§a {found_password}'))
    else: print(color('§fPassword §cnot found'))

    print(color(f'§fTime taken: §a{end_time - start_time:.2f} seconds'))