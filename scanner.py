
import socket
import threading
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init()

# Thread lock for clean output
print_lock = threading.Lock()

# Store open ports
open_ports = []


# Scan function
def scan_port(target, port):

    try:
        # Create TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Timeout
        s.settimeout(1)

        # Connect to target
        result = s.connect_ex((target, port))

        # If port is open
        if result == 0:

            # Detect service
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"

            # Banner grabbing
            try:
                banner = s.recv(1024).decode().strip()

                if banner == "":
                    banner = "No Banner"

            except:
                banner = "No Banner"

            # Thread-safe printing
            with print_lock:

                print(
                    Fore.GREEN
                    + f"[OPEN] Port {port} | Service: {service} | Banner: {banner}"
                    + Style.RESET_ALL
                )

            # Save result
            open_ports.append((port, service, banner))

        s.close()

    except:
        pass


# Main function
def main():

    # Argument parser
    parser = argparse.ArgumentParser(
        description="Multi-threaded TCP Port Scanner"
    )

    parser.add_argument(
        "-t",
        "--target",
        required=True,
        help="Target IP or hostname"
    )

    parser.add_argument(
        "-p",
        "--ports",
        required=True,
        help="Port range example: 1-1000"
    )

    args = parser.parse_args()

    target = args.target

    # Parse port range
    start_port, end_port = map(int, args.ports.split("-"))

    print(
        Fore.CYAN
        + f"\n[+] Scanning Target: {target}"
    )

    print(
        Fore.CYAN
        + f"[+] Port Range: {start_port}-{end_port}\n"
        + Style.RESET_ALL
    )

    threads = []

    # Create threads
    for port in range(start_port, end_port + 1):

        thread = threading.Thread(
            target=scan_port,
            args=(target, port)
        )

        threads.append(thread)

        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    # Save results
    with open("scan_results.txt", "w") as file:

        for port, service, banner in open_ports:

            file.write(
                f"Port: {port} | Service: {service} | Banner: {banner}\n"
            )

    print(
        Fore.YELLOW
        + "\n[+] Scan Complete!"
    )

    print(
        Fore.YELLOW
        + "[+] Results saved to scan_results.txt"
        + Style.RESET_ALL
    )


# Run program
if __name__ == "__main__":
    main()

