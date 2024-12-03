import os
import subprocess
import shutil
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
Automatic Multiple Tor Proxy Service

Kategori:   Python
Paket:      Multi Tor Proxy Service
Yazar:      Özgür Şahin <0zgur>
Lisans:     https://raw.githubusercontent.com/02gur/AutomaticTorServices/main/LICENSE  APACHE Lisansı
Bağlantı:   https://raw.githubusercontent.com/02gur/AutomaticTorServices
"""

BASE_DIR = os.path.expanduser("~/tor-instances")

def create_tor_instances(num_instances):
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    for i in range(num_instances):
        instance_name = f"tor{i+1}"
        instance_dir = os.path.join(BASE_DIR, instance_name)
        os.makedirs(instance_dir, exist_ok=True)

        torrc_path = os.path.join(instance_dir, "torrc")
        with open(torrc_path, "w") as torrc:
            port = 9050 + i * 2
            torrc.write(f"SocksPort {port}\n")
            torrc.write(f"DataDirectory {instance_dir}/data\n")
            torrc.write("Log notice stdout\n")

        # Initialize data directory
        os.makedirs(f"{instance_dir}/data", exist_ok=True)
        subprocess.run(["tor", "--quiet", "-f", torrc_path, "--DataDirectory", f"{instance_dir}/data", "--initialize-only"])

        print(f"Created instance {instance_name} with SocksPort {port}")

def start_tor_instances():
    processes = []
    for instance in os.listdir(BASE_DIR):
        instance_dir = os.path.join(BASE_DIR, instance)
        torrc_path = os.path.join(instance_dir, "torrc")
        port = None

        # Read port information from torrc
        if os.path.exists(torrc_path):
            with open(torrc_path, "r") as torrc:
                for line in torrc:
                    if line.startswith("SocksPort"):
                        port = line.split()[1].strip()
                        break

        cmd = ["tor", "-f", torrc_path]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append((instance, process, port))
        print(f"Started {instance} from {instance_dir} on SocksPort {port}")
        time.sleep(1)
    return processes

def check_port(instance, port, timeout=10):
    try:
        print(f"Checking SocksPort {port} for {instance}...")
        result = subprocess.check_output(
            ["curl", "--socks5", f"127.0.0.1:{port}", "--silent", "--max-time", str(timeout), "https://api.myip.com"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        response = json.loads(result)
        if "ip" in response and "country" in response:
            print(f"[+] {instance} is working. IP: {response['ip']}, Country: {response['country']}")
            return True
        else:
            raise ValueError("Missing 'ip' or 'country' in response.")
    except Exception as e:
        print(f"[-] {instance} failed: {e}")
        return False

def restart_tor_instance(instance, port):
    instance_dir = os.path.join(BASE_DIR, instance)
    torrc_path = os.path.join(instance_dir, "torrc")
    print(f"Restarting {instance} on SocksPort {port}...")
    cmd = ["tor", "-f", torrc_path]
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Allow time for restart
    print(f"Restarted {instance} on SocksPort {port}")
    return process

def check_ports(processes, max_threads=10):
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(check_port, instance, port): (instance, port) for instance, _, port in processes}

        for future in as_completed(futures):
            instance, port = futures[future]
            try:
                if not future.result():
                    print(f"[-] {instance} failed. Restarting...")
                    restart_tor_instance(instance, port)
            except Exception as e:
                print(f"Error checking {instance} on SocksPort {port}: {e}")

def list_tor_instances():
    if not os.path.exists(BASE_DIR) or not os.listdir(BASE_DIR):
        print("No Tor instances found.")
        return

    print("Existing Tor instances and their ports:")
    for instance in os.listdir(BASE_DIR):
        instance_dir = os.path.join(BASE_DIR, instance)
        torrc_path = os.path.join(instance_dir, "torrc")
        if os.path.exists(torrc_path):
            with open(torrc_path, "r") as torrc:
                for line in torrc:
                    if line.startswith("SocksPort"):
                        port = line.split()[1].strip()
                        print(f"{instance} - SocksPort: {port}")

def cleanup_tor_instances():
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
        print("All Tor instances cleaned up.")
    else:
        print("No Tor instances to clean.")

def check_all_instances():
    processes = []
    for instance in os.listdir(BASE_DIR):
        instance_dir = os.path.join(BASE_DIR, instance)
        torrc_path = os.path.join(instance_dir, "torrc")
        port = None

        # Read port information from torrc
        if os.path.exists(torrc_path):
            with open(torrc_path, "r") as torrc:
                for line in torrc:
                    if line.startswith("SocksPort"):
                        port = line.split()[1].strip()
                        processes.append((instance, None, port))
                        break

    print("Checking all instances...")
    check_ports(processes)

def main():
    while True:
        print("\nTor Service Manager")
        print("1. Create Tor instances")
        print("2. Start Tor instances")
        print("3. List Tor instances and ports")
        print("4. Cleanup Tor instances")
        print("5. Check and restart all instances")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            num = int(input("How many Tor instances would you like to create? "))
            create_tor_instances(num)
        elif choice == "2":
            print("Starting all Tor instances...")
            processes = start_tor_instances()
            print("Checking all ports...")
            check_ports(processes)
        elif choice == "3":
            list_tor_instances()
        elif choice == "4":
            confirm = input("Are you sure you want to delete all instances? (y/n): ").strip().lower()
            if confirm == "y":
                cleanup_tor_instances()
        elif choice == "5":
            check_all_instances()
        elif choice == "6":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
