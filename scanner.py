#!/usr/bin/env python3

import socket
import threading
import argparse
import sys
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from colorama import Fore, Style, init, Back

# Initialize colorama
init(autoreset=True)

# Global variables
print_lock = threading.Lock()
open_ports = []
scan_interrupted = False
total_ports = 0
scanned_ports = 0


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global scan_interrupted
    
    with print_lock:
        print(f"\n{Fore.YELLOW}[!] Interrupted by user. Saving partial results...{Style.RESET_ALL}")
    
    scan_interrupted = True
    save_results()
    print(f"{Fore.GREEN}[+] Partial results saved.{Style.RESET_ALL}")
    sys.exit(0)


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)


def is_host_alive(ip, port=80, timeout=1):
    """Check if host is alive by trying to connect to common port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False


def get_service_banner(sock, port):
    """
    Enhanced banner grabbing with protocol-specific requests
    """
    try:
        # Send protocol-specific probe
        probes = {
            21: b"USER anonymous\r\n",      # FTP
            22: b"",                         # SSH
            25: b"HELO test.com\r\n",        # SMTP
            80: b"HEAD / HTTP/1.0\r\n\r\n", # HTTP
            110: b"",                        # POP3
            143: b"",                        # IMAP
            443: b"HEAD / HTTP/1.0\r\n\r\n", # HTTPS
            3306: b"",                       # MySQL
            3389: b"",                       # RDP
            8080: b"HEAD / HTTP/1.0\r\n\r\n" # Proxy
        }
        
        # Set shorter timeout for banner grabbing
        sock.settimeout(2)
        
        # Send probe if available
        if port in probes and probes[port]:
            try:
                sock.send(probes[port])
            except:
                pass
        
        # Receive banner
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        
        # Clean up banner
        banner = banner.replace('\r', ' ').replace('\n', ' ').strip()
        
        if not banner or len(banner) == 0:
            return "No Banner"
        
        # Limit banner length
        if len(banner) > 100:
            banner = banner[:97] + "..."
        
        return banner
        
    except socket.timeout:
        return "Timeout"
    except Exception:
        return "No Banner"


def tcp_scan(ip, port):
    """
    Scan a single TCP port
    """
    global scanned_ports
    
    try:
        # Create TCP socket
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.settimeout(1.5)
        
        # Attempt connection
        result = tcp.connect_ex((ip, port))
        
        # Port is open
        if result == 0:
            # Service detection
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            
            # Enhanced banner grabbing
            banner = get_service_banner(tcp, port)
            
            # Save result
            with print_lock:
                open_ports.append({
                    'ip': ip,
                    'port': port,
                    'service': service,
                    'banner': banner,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Colorful output
                print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════╗")
                print(f"{Fore.GREEN}║ {Fore.WHITE}OPEN PORT FOUND{Fore.GREEN}                                            ║")
                print(f"{Fore.GREEN}╠══════════════════════════════════════════════════════════╣")
                print(f"{Fore.GREEN}║ {Fore.CYAN}Host:{Fore.RESET} {ip:<50} {Fore.GREEN}║")
                print(f"{Fore.GREEN}║ {Fore.CYAN}Port:{Fore.RESET} {port:<51} {Fore.GREEN}║")
                print(f"{Fore.GREEN}║ {Fore.CYAN}Service:{Fore.RESET} {service:<49} {Fore.GREEN}║")
                print(f"{Fore.GREEN}║ {Fore.CYAN}Banner:{Fore.RESET} {banner:<49} {Fore.GREEN}║")
                print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Update progress counter
        with print_lock:
            scanned_ports += 1
            if scanned_ports % 100 == 0:
                progress = (scanned_ports / total_ports) * 100
                print(f"{Fore.BLUE}[*] Progress: {progress:.1f}% ({scanned_ports}/{total_ports}){Style.RESET_ALL}")
        
    except socket.error:
        pass
    except Exception as e:
        with print_lock:
            print(f"{Fore.RED}[!] Error scanning port {port}: {str(e)}{Style.RESET_ALL}")
    finally:
        try:
            tcp.close()
        except:
            pass


def scan_host(ip, start_port, end_port, max_workers=100):
    """
    Scan a single host with thread pool
    """
    global total_ports, scanned_ports
    
    total_ports = end_port - start_port + 1
    scanned_ports = 0
    
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}[*] Starting TCP scan on host: {Fore.CYAN}{ip}")
    print(f"{Fore.MAGENTA}[*] Port range: {Fore.YELLOW}{start_port}-{end_port}")
    print(f"{Fore.MAGENTA}[*] Max threads: {Fore.YELLOW}{max_workers}")
    print(f"{Fore.MAGENTA}[*] Start time: {Fore.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")
    
    # Use thread pool instead of creating unlimited threads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        for port in range(start_port, end_port + 1):
            future = executor.submit(tcp_scan, ip, port)
            futures.append(future)
        
        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                with print_lock:
                    print(f"{Fore.RED}[!] Thread error: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}[+] Scan complete for host: {Fore.CYAN}{ip}")
    print(f"{Fore.GREEN}[+] End time: {Fore.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.GREEN}[+] Open ports found: {Fore.YELLOW}{len([p for p in open_ports if p['ip'] == ip])}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")


def scan_network(network, start_port, end_port, max_workers=100, skip_dead_hosts=False):
    """
    Scan an entire network range
    """
    print(f"\n{Fore.MAGENTA}{'#'*60}")
    print(f"{Fore.MAGENTA}# Network Scan Mode")
    print(f"{Fore.MAGENTA}# Target network: {Fore.CYAN}{network}.0/24")
    print(f"{Fore.MAGENTA}# Total hosts: {Fore.YELLOW}254")
    print(f"{Fore.MAGENTA}# Skip dead hosts: {Fore.YELLOW}{skip_dead_hosts}")
    print(f"{Fore.MAGENTA}# Start time: {Fore.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.MAGENTA}{'#'*60}{Style.RESET_ALL}")
    
    alive_count = 0
    for host in range(1, 255):
        ip = f"{network}.{host}"
        
        # Optional: Check if host is alive before scanning
        if skip_dead_hosts and not is_host_alive(ip):
            continue
        
        if skip_dead_hosts:
            alive_count += 1
        
        scan_host(ip, start_port, end_port, max_workers)
    
    if skip_dead_hosts:
        print(f"\n{Fore.CYAN}[*] Scanned {alive_count} alive hosts out of 254{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}{'#'*60}")
    print(f"{Fore.GREEN}# Network scan complete!")
    print(f"{Fore.GREEN}# Total open ports found: {Fore.YELLOW}{len(open_ports)}")
    print(f"{Fore.GREEN}{'#'*60}{Style.RESET_ALL}")


def save_results():
    """
    Save results to file with detailed format
    """
    if not open_ports:
        print(f"{Fore.YELLOW}[!] No results to save{Style.RESET_ALL}")
        return
    
    filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(filename, "w") as file:
            file.write("="*80 + "\n")
            file.write("TCP PORT SCAN RESULTS\n")
            file.write(f"Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Total open ports found: {len(open_ports)}\n")
            file.write("="*80 + "\n\n")
            
            # Group results by IP
            hosts = {}
            for result in open_ports:
                ip = result['ip']
                if ip not in hosts:
                    hosts[ip] = []
                hosts[ip].append(result)
            
            for ip in sorted(hosts.keys()):
                file.write(f"\nHost: {ip}\n")
                file.write("-"*60 + "\n")
                
                for result in hosts[ip]:
                    file.write(f"  Port {result['port']}/TCP\n")
                    file.write(f"    Service: {result['service']}\n")
                    file.write(f"    Banner : {result['banner']}\n")
                    file.write(f"    Time   : {result['timestamp']}\n\n")
        
        print(f"\n{Fore.GREEN}[+] Results saved to: {Fore.CYAN}{filename}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error saving results: {str(e)}{Style.RESET_ALL}")


def validate_ports(start_port, end_port):
    """
    Validate port range
    """
    if start_port < 1 or start_port > 65535:
        print(f"{Fore.RED}[!] Start port must be between 1-65535{Style.RESET_ALL}")
        return False
    
    if end_port < 1 or end_port > 65535:
        print(f"{Fore.RED}[!] End port must be between 1-65535{Style.RESET_ALL}")
        return False
    
    if start_port > end_port:
        print(f"{Fore.RED}[!] Start port must be less than or equal to end port{Style.RESET_ALL}")
        return False
    
    return True


def validate_ip(ip_string):
    """
    Validate IP address format
    """
    parts = ip_string.split('.')
    
    if len(parts) != 4:
        return False
    
    try:
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    except ValueError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Multi-threaded TCP Port Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 192.168.1.1 1 1000                    # Scan single host
  %(prog)s 192.168.1 1 1000 --network            # Scan network range
  %(prog)s 192.168.1.1 20 443 -w 200             # Scan with 200 threads
  %(prog)s 192.168.1.1 1 65535 -w 150            # Full port scan
  %(prog)s 192.168.1 1 1000 --network --skip-dead # Skip dead hosts
        """
    )
    
    parser.add_argument(
        "target",
        help="Target IP address (single) or network (without last octet, e.g., 192.168.1)"
    )
    
    parser.add_argument(
        "start_port",
        type=int,
        help="Start port (1-65535)"
    )
    
    parser.add_argument(
        "end_port",
        type=int,
        help="End port (1-65535)"
    )
    
    parser.add_argument(
        "-n", "--network",
        action="store_true",
        help="Scan entire network range (/24)"
    )
    
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100,
        help="Maximum number of threads (default: 100, max: 500)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Custom output filename (default: auto-generated)"
    )
    
    parser.add_argument(
        "--skip-dead",
        action="store_true",
        help="Skip dead hosts when scanning network (faster)"
    )
    
    args = parser.parse_args()
    
    # Validate ports
    if not validate_ports(args.start_port, args.end_port):
        sys.exit(1)
    
    # Limit workers
    if args.workers > 500:
        print(f"{Fore.YELLOW}[!] Reducing workers from {args.workers} to 500{Style.RESET_ALL}")
        args.workers = 500
    elif args.workers < 1:
        print(f"{Fore.YELLOW}[!] Setting workers to minimum 1{Style.RESET_ALL}")
        args.workers = 1
    
    # Display banner
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}       Python TCP Port Scanner v2.0")
    print(f"{Fore.CYAN}       Multi-threaded Network Scanner")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # Scan network
    if args.network:
        # Validate network format
        if '.' in args.target and args.target.count('.') == 3:
            network_parts = args.target.split('.')
            network = '.'.join(network_parts[:3])
        else:
            network = args.target
        
        scan_network(network, args.start_port, args.end_port, args.workers, args.skip_dead)
    
    # Scan single host
    else:
        # Validate IP
        if not validate_ip(args.target):
            print(f"{Fore.RED}[!] Invalid IP address format: {args.target}{Style.RESET_ALL}")
            sys.exit(1)
        
        scan_host(args.target, args.start_port, args.end_port, args.workers)
    
    # Save results only if not interrupted
    if not scan_interrupted:
        save_results()
    
    print(f"\n{Fore.GREEN}[+] Scan completed successfully!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
