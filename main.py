#SOJA KYA DAKH RAHA HA

import os
import sys
import platform
import subprocess
import importlib.util
import time

# ============================================
# DEVICE ARCHITECTURE CHECK
# ============================================

def check_device_architecture():
    print("\n" + "="*50)
    print("CHECKING DEVICE COMPATIBILITY")
    print("="*50)
    
    machine = platform.machine()
    print(f"[•] Machine architecture: {machine}")
    
    processor = platform.processor()
    print(f"[•] Processor: {processor}")
    
    is_64bits = sys.maxsize > 2**32
    print(f"[•] Python architecture: {'64-bit' if is_64bits else '32-bit'}")
    
    try:
        uname_output = subprocess.check_output(['uname', '-m'], text=True).strip()
        print(f"[•] Kernel architecture: {uname_output}")
        
        if uname_output in ['aarch64', 'arm64', 'x86_64', 'amd64']:
            print(f"[✓] Device is 64-bit ({uname_output})")
            return True, uname_output
        elif uname_output in ['armv7l', 'armv8l', 'i686', 'i386']:
            print(f"[✗] Device is 32-bit ({uname_output})")
            return False, uname_output
        else:
            if is_64bits:
                print(f"[✓] Device appears to be 64-bit (based on Python)")
                return True, uname_output
            else:
                print(f"[✗] Device appears to be 32-bit (based on Python)")
                return False, uname_output
                
    except Exception as e:
        print(f"[!] Could not determine via uname: {e}")
        if is_64bits:
            print(f"[✓] Device appears to be 64-bit (based on Python)")
            return True, machine
        else:
            print(f"[✗] Device appears to be 32-bit (based on Python)")
            return False, machine

def check_compiled_module_compatibility():
    if os.path.exists('run.cpython-312.so'):
        try:
            file_check = subprocess.check_output(['file', 'run.cpython-312.so'], text=True)
            print(f"[•] Module info: {file_check.strip()}")
            
            if '64-bit' in file_check:
                print("[✓] Compiled module is 64-bit")
                return True
            elif '32-bit' in file_check:
                print("[!] Compiled module is 32-bit")
                return False
            else:
                print("[!] Could not determine module architecture")
                return None
        except:
            print("[!] Could not analyze module file")
            return None
    return None

# ============================================
# GIT PULL FUNCTION
# ============================================

def git_pull_updates():
    print("\n" + "="*50)
    print("CHECKING FOR UPDATES")
    print("="*50)
    
    if os.path.exists('.git'):
        try:
            branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
            print(f"[•] Current branch: {branch}")
            
            subprocess.run(['git', 'fetch'], capture_output=True)
            
            status = subprocess.check_output(['git', 'status', '-uno'], text=True)
            
            if 'Your branch is behind' in status:
                print("[!] Updates available!")
                choice = input("[?] Do you want to pull latest updates? (y/n): ").strip().lower()
                
                if choice == 'y':
                    print("[•] Pulling latest updates...")
                    result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print("[✓] Successfully updated!")
                        print(f"[•] {result.stdout}")
                        return True
                    else:
                        print(f"[✗] Update failed: {result.stderr}")
                        return False
                else:
                    print("[•] Skipping update")
                    return False
            else:
                print("[✓] Already up to date")
                return False
                
        except Exception as e:
            print(f"[!] Git operation failed: {e}")
            return False
    else:
        print("[!] Not a git repository")
        return False

# ============================================
# MODULE LOADING
# ============================================

def load_compiled_module():
    try:
        import run
        print("[✓] Successfully loaded compiled module")
        return run, True
    except ImportError:
        try:
            if os.path.exists('run.py'):
                spec = importlib.util.spec_from_file_location("run", "run.py")
                run = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(run)
                print("[!] Running in development mode (Python)")
                return run, False
            else:
                print("[✗] Could not find run module")
                return None, False
        except Exception as e:
            print(f"[✗] Error loading module: {e}")
            return None, False

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    
    if platform.system().lower() != 'windows':
        sys.stdout.write('\x1b]2; Yunick Facebook Tool v2.1\x07')
    
    # Banner
    print("""
╔════════════════════════════════════════════════════════════╗
║           Yunick Facebook Tool - Cython Edition           ║
║                    Version 2.1                             ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    is_64bit, arch = check_device_architecture()
    
    if not is_64bit:
        print("\n" + "="*50)
        print("SORRY! INCOMPATIBLE DEVICE")
        print("="*50)
        print("""
    This tool requires a 64-bit device to run properly.
    
    Your device appears to be 32-bit which is not supported.
    
    Requirements:
    • 64-bit processor (aarch64/arm64/x86_64)
    • Android 7.0+ or Linux
    • Python 3.8+
    
    Your device info:
    • Architecture: {arch}
    • Python: {bits}
    
    Please use a 64-bit device to run this tool.
        """.format(arch=arch, bits='64-bit' if sys.maxsize > 2**32 else '32-bit'))
        
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
    
    print("\n[✓] Device check passed - 64-bit system detected")
    
    module_compat = check_compiled_module_compatibility()
    
    if module_compat is False:
        print("\n" + "="*50)
        print("MODULE ARCHITECTURE MISMATCH")
        print("="*50)
        print("""
    The compiled module (run.cpython-312.so) is 32-bit
    but your device is 64-bit.
    
    Please recompile the module for 64-bit:
    
    Option 1: Recompile on this device
    $ python setup.py build_ext --inplace
    
    Option 2: Use development mode
    $ python run.py
    
    Option 3: Download 64-bit version
        """)
        
        choice = input("\nContinue in development mode? (y/n): ").strip().lower()
        if choice != 'y':
            print("\nExiting...")
            sys.exit(1)
    
    git_pull_updates()
    
    if platform.system().lower() == 'android' or 'ANDROID_ROOT' in os.environ:
        base_path = "/sdcard"
        print("[•] Android environment detected")
    else:
        base_path = os.path.expanduser("~")
    
    dirs = [
        os.path.join(base_path, "Yunick"),
        os.path.join(base_path, "Yunick/logs"),
        os.path.join(base_path, "Yunick/accounts"),
        os.path.join(base_path, "Yunick/2fa")
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print(f"[✓] Directories created in {base_path}/Yunick")
    
    run_module, is_compiled = load_compiled_module()
    
    if run_module is None:
        print("\n[✗] Failed to load required module")
        print("Please make sure run.cpython-312.so or run.py exists")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
    
    print("\n" + "="*50)
    print("VERIFYING MODULE FUNCTIONS")
    print("="*50)
    
    required_funcs = ['method', 'auto', 'createfb_method_1', 'createfb_method_2', 'createfb_method_3']
    missing_funcs = []
    
    for func in required_funcs:
        if hasattr(run_module, func):
            print(f"[✓] Found: {func}")
        else:
            missing_funcs.append(func)
            print(f"[✗] Missing: {func}")
    
    if missing_funcs:
        print("\n[!] Warning: Some functions are missing")
        print(f"Missing: {', '.join(missing_funcs)}")
        
        choice = input("\nContinue anyway? (y/n): ").strip().lower()
        if choice != 'y':
            print("\nExiting...")
            sys.exit(1)
    
    print("\n" + "="*50)
    print("INITIALIZATION COMPLETE")
    print("="*50)
    print(f"Mode: {'Compiled (Cython)' if is_compiled else 'Development (Python)'}")
    print(f"Architecture: {arch}")
    print("="*50 + "\n")
    
    time.sleep(1)
    
    try:
        if hasattr(run_module, 'method'):
            run_module.method()
        elif hasattr(run_module, 'main'):
            run_module.main()
        elif hasattr(run_module, 'auto'):
            run_module.auto()
        else:
            print("\n[!] Could not find entry point")
            print("Available functions:")
            
            available = [attr for attr in dir(run_module) 
                        if not attr.startswith('__') and callable(getattr(run_module, attr))]
            
            for i, func in enumerate(available, 1):
                print(f"  {i}. {func}")
            
            try:
                choice = int(input("\nSelect function number: ")) - 1
                if 0 <= choice < len(available):
                    func_name = available[choice]
                    func = getattr(run_module, func_name)
                    func()
                else:
                    print("[✗] Invalid selection")
            except (ValueError, IndexError):
                print("[✗] Invalid input")
                
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        print(f"\n[✗] Runtime error: {e}")
    
    print("\n" + "="*50)
    print("Thank you for using Yunick Facebook Tool")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)