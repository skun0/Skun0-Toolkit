# Developed by https://github.com/skun0

import os, requests, time, ctypes, phonenumbers, subprocess, json, socket, asyncio, dns.resolver, whois, string, re

from scapy.all import ARP, Ether, srp
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.text import Text
from phonenumbers import geocoder, carrier, timezone
from requests.structures import CaseInsensitiveDict

VERSION = 1.0
UP_TO_DATE = True # maybe using this later

console = Console()
user = os.getenv("USERNAME") or os.getenv("USER") or "user"

def gradient_text(text, end="\n"):
    start = (255, 255, 0)
    end_color = (255, 140, 0)

    result = Text()

    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        newline = line[len(content):]

        width = max(len(content), 1)

        for i, char in enumerate(content):
            progress = i / max(width - 1, 1)

            r = int(start[0] + (end_color[0] - start[0]) * progress)
            g = int(start[1] + (end_color[1] - start[1]) * progress)
            b = int(start[2] + (end_color[2] - start[2]) * progress)

            result.append(
                char,
                style=f"rgb({r},{g},{b})"
            )

        if newline:
            result.append(newline)

    console.print(result, end=end)


def set_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def pause():
    gradient_text("Press enter to continue...")
    os.system("pause > nul")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def return_to_menu():
    gradient_text("Returning to menu in 3 seconds...")
    time.sleep(3)
    menu()


def save_json(option, data):
    folder = Path("results")
    folder.mkdir(exist_ok=True)

    filename = folder / f"{option}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    gradient_text(f"Saved: {filename}")

def update():
    gradient_text("[*] Checking for updates...")

    try:
        subprocess.run(
            ["git", "fetch"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        local = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True
        ).strip()

        remote = subprocess.check_output(
            ["git", "rev-parse", "@{u}"],
            text=True
        ).strip()

        if local != remote:
            gradient_text("[*] Update available!")

            subprocess.run(
                ["git", "pull"],
                check=True
            )

            gradient_text("[+] Updated successfully.")

        else:
            gradient_text("[+] Already up to date.")

    except subprocess.CalledProcessError:
        gradient_text("[-] Could not update.")

def menu():
    banner = f'''
        ███████╗██╗  ██╗██╗   ██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
        ██╔════╝██║ ██╔╝██║   ██║████╗  ██║██╔═████╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
        ███████╗█████╔╝ ██║   ██║██╔██╗ ██║██║██╔██║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
        ╚════██║██╔═██╗ ██║   ██║██║╚██╗██║████╔╝██║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
        ███████║██║  ██╗╚██████╔╝██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
        ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝

                                        Version: {VERSION}      
                                        ╔════════════════════════════════════╗
                                        ║                                    ║
                                        ║                                    ║
                                        ║   [1] OSINT                        ║
                                        ║   [2] Domain Recon                 ║
                                        ║   [3] CCTV                         ║
                                        ║   [4] Network Scanner              ║
                                        ║   [U] Check for updates            ║
                                        ║                                    ║
                                        ║                                    ║
                                        ╚════════════════════════════════════╝
    '''

    clear()

    set_title("Skuno | MENU")
    gradient_text(banner)

    gradient_text(f"║\n╚═ root@{user}:~$ ", end="")

    cmd = input()

    if cmd == "1":
        osint()
        pass

    elif cmd == "2":
        domain_recon()
        pass

    elif cmd == "3":
        cctv()
        pass

    elif cmd == "4":
        network_scanner()
        pass

    elif cmd == "U":
        update()
        pass
    else:
        gradient_text("Invalid input.")

def network_scanner():
        banner = f'''
        ███████╗██╗  ██╗██╗   ██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
        ██╔════╝██║ ██╔╝██║   ██║████╗  ██║██╔═████╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
        ███████╗█████╔╝ ██║   ██║██╔██╗ ██║██║██╔██║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
        ╚════██║██╔═██╗ ██║   ██║██║╚██╗██║████╔╝██║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
        ███████║██║  ██╗╚██████╔╝██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
        ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝

                                        Version: {VERSION}      
                                        ╔════════════════════════════════════╗
                                        ║                                    ║
                                        ║                                    ║
                                        ║   [1] Port Scanner                 ║
                                        ║   [2] ARP Discovery                ║
                                        ║   [3] ?                            ║
                                        ║   [4] ?                            ║
                                        ║                                    ║
                                        ║                                    ║
                                        ╚════════════════════════════════════╝
    '''

        clear()
        gradient_text(banner)
        gradient_text(f"║\n╚═ root@{user}:~$ ", end="")
        cmd = input()

        def port_scanner():

            async def scan_port(ip, port, semaphore):
                async with semaphore:
                    try:
                        _, writer = await asyncio.wait_for(
                            asyncio.open_connection(ip, port),
                            timeout=0.5
                        )

                        writer.close()
                        await writer.wait_closed()

                        return port

                    except (TimeoutError, ConnectionRefusedError, OSError):
                        return None

            async def async_port_scan(ip, start_port, end_port):
                semaphore = asyncio.Semaphore(500)

                tasks = [
                    scan_port(ip, port, semaphore)
                    for port in range(start_port, end_port + 1)
                ]

                results = await asyncio.gather(*tasks)

                return sorted(
                    port for port in results
                    if port is not None
                )

            gradient_text("IP: ", end="")
            ip = input().strip()

            gradient_text("Start Port: ", end="")
            start_port = int(input())

            gradient_text("End Port: ", end="")
            end_port = int(input())

            try:
                open_ports = asyncio.run(
                    async_port_scan(ip, start_port, end_port)
                )

                if open_ports:
                    for port in open_ports:
                        gradient_text(f"[+] Port {port} OPEN")
                else:
                    gradient_text("[-] No open ports found.")

            except ValueError:
                gradient_text("[-] Invalid port.")

            except Exception as e:
                gradient_text(f"Error: {e}")

            pause()
            return_to_menu()


        def arp_discovery():
            try:
                gradient_text("Network (192.168.1.0/24): ", end="")
                network = input().strip()

                if network == "":
                    network = "192.168.1.0/24"

                gradient_text(f"Scanning {network}...")

                packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)

                answered = srp(
                    packet,
                    timeout=3,
                    verbose=False
                )[0]

                if not answered:
                    gradient_text("[-] No devices found.")
                else:
                    for _, received in answered:
                        gradient_text(
                            f"[+] {received.psrc} | {received.hwsrc}"
                        )

                    gradient_text(f"\n[+] {len(answered)} device(s) found.")

            except Exception as e:
                gradient_text(f"Error: {e}")

            pause()
            return_to_menu() 

        if cmd == "1":
            port_scanner()
        
        elif cmd == "2":
            arp_discovery()
            print()

        elif cmd == "3":
            gradient_text("Coming next update.")
            return_to_menu()
        
        elif cmd == "4":
            gradient_text("Coming next update.")
            return_to_menu()

        else:
            gradient_text("Invalid input.")
            return_to_menu()

def cctv():
    banner = f'''
            ███████╗██╗  ██╗██╗   ██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
            ██╔════╝██║ ██╔╝██║   ██║████╗  ██║██╔═████╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
            ███████╗█████╔╝ ██║   ██║██╔██╗ ██║██║██╔██║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
            ╚════██║██╔═██╗ ██║   ██║██║╚██╗██║████╔╝██║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
            ███████║██║  ██╗╚██████╔╝██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
            ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
    
            [!] https://github.com/skun0
        '''

    clear()
    gradient_text(banner)
    # set_title("")

    try:
        url = "http://www.insecam.org/en/jsoncountries/"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "*/*"
        headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64)"
        country = None

        try:
            response = requests.get(url, headers=headers)
            try:
                data = response.json()
                countries = data.get('countries', {})
            except Exception:
                gradient_text("Could not parse JSON. API may be in maintenance!")

            if not countries:
                gradient_text("Could not retrieve country list. Enter code manually")

            else:
                rows = []

                for key, value in countries.items():
                    country = value["country"]
                    count = value["count"]

                    code = f"({key})"
                    count_text = f"[{count}]"

                    rows.append((code, country, count_text))

                max_country_width = max(
                    len(country) for _, country, _ in rows
                )
                max_count_width = max(
                    len(count) for _, _, count in rows
                )

                inner_width = (
                    len("  Code: ")
                    + max(len(code) for code, _, _ in rows)
                    + len(" → ")
                    + max_country_width
                    + 1
                    + max_count_width
                    + 1
                )

                gradient_text(
                    "╔" + "═" * (inner_width + 2) + "╗"
                )

                title = "Country Codes"
                title_padding = (inner_width + 2 - len(title)) // 2

                gradient_text(
                    "║"
                    + " " * title_padding
                    + title
                    + " " * (
                        inner_width
                        + 2
                        - title_padding
                        - len(title)
                    )
                    + "║"
                )

                gradient_text(
                    "╠" + "═" * (inner_width + 2) + "╣"
                )

                for code, country, count_text in rows:
                    text = Text()

                    text.append("║  Code: ", style="bold cyan")
                    text.append(code, style="bold yellow")
                    text.append(" → ", style="bold cyan")
                    text.append(
                        country.ljust(max_country_width),
                        style="bold white"
                    )
                    text.append(" ", style="bold white")
                    text.append(
                        count_text.rjust(max_count_width),
                        style="bold magenta"
                    )
                    text.append(" ║", style="bold cyan")

                    console.print(text)

                gradient_text(
                    "╚" + "═" * (inner_width + 2) + "╝"
                )

                print()

                print()
                gradient_text("Country Code: ", end="")
                country = input()

                res = requests.get(f"http://www.insecam.org/en/bycountry/{country}", headers=headers)
                last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)
                last_page = int(last_page[0]) if last_page else 1

                os.makedirs("cams", exist_ok=True)
                with open(f'cams/{country}.txt', 'w') as f:
                    for page in range(last_page):
                        res = requests.get(
                            f"http://www.insecam.org/en/bycountry/{country}/?page={page}",
                            headers=headers
                        )
                        find_ip = re.findall(r"http://\d+\.\d+\.\d+\.\d+:\d+", res.text)
                        for ip in find_ip:
                            gradient_text(f"[+] Found cam: {ip}")
                            f.write(f'{ip}\n')
                            time.sleep(0.05)

        except Exception as e:
            gradient_text(f"Error: {e}")
            pause()
            return_to_menu()

        finally:
            if country:
                gradient_text(f"Saved to file: {country}.txt")
                pause()
                return_to_menu()

            else:
                gradient_text(f"No cams saved due to an earlier error.")
                pause()
                return_to_menu()

    except KeyboardInterrupt:
        return_to_menu()


    except Exception as e:
        gradient_text(f"Error: {e}")
        pause()
        return_to_menu()
def osint():
    banner = f'''
        ███████╗██╗  ██╗██╗   ██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
        ██╔════╝██║ ██╔╝██║   ██║████╗  ██║██╔═████╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
        ███████╗█████╔╝ ██║   ██║██╔██╗ ██║██║██╔██║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
        ╚════██║██╔═██╗ ██║   ██║██║╚██╗██║████╔╝██║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
        ███████║██║  ██╗╚██████╔╝██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
        ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝

                                        Version: {VERSION}      
                                        ╔════════════════════════════════════╗
                                        ║                                    ║
                                        ║                                    ║
                                        ║   [1] Holehe                       ║
                                        ║   [2] IP Geolocation               ║
                                        ║   [3] Phone Number Lookup          ║
                                        ║   [4] ?                            ║
                                        ║                                    ║
                                        ║                                    ║
                                        ╚════════════════════════════════════╝
    '''

    clear()
    gradient_text(banner)
    gradient_text(f"║\n╚═ root@{user}:~$ ", end="")
    cmd = input()

    def holehe():
        gradient_text("E-Mail: ", end="")
        email = input()

        subprocess.run(["holehe", email])
        pause()
        return_to_menu()

    def ip_geolocation():
        gradient_text("IP: ", end="")
        ip = input()

        response = requests.get(f"http://ip-api.com/json/{ip}")
        result = response.json()

        print()
        gradient_text(f"Country: {result['country']}")
        gradient_text(f"Region: {result['regionName']}")
        gradient_text(f"City: {result['city']}")
        gradient_text(f"ZIP: {result['zip']}")
        gradient_text(f"ISP: {result['isp']}")
        gradient_text(f"ORG: {result['org']}")
        gradient_text(f"AS: {result['as']}")
        print()
        pause()
        return_to_menu()

    def phone_lookup():
        gradient_text("Phone Number: ", end="")
        pn = input()

        parsed = phonenumbers.parse(pn, None)
        country = geocoder.description_for_number(parsed, "en") or "Unknown"
        carrier_name = carrier.name_for_number(parsed, "en") or "Unknown"
        valid = phonenumbers.is_valid_number(parsed)

        region = phonenumbers.region_code_for_number(parsed) or "Unknown"
        country_code = parsed.country_code
        national_number = parsed.national_number

        number_type = phonenumbers.number_type(parsed)

        type_names = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line / Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
        }

        phone_type = type_names.get(number_type, "Unknown")

        timezones = timezone.time_zones_for_number(parsed)
        timezones = list(timezones) if timezones else ["Unknown"]

        international = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        national = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.NATIONAL
        )

        e164 = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )

        rfc3966 = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.RFC3966
        )

        possible = phonenumbers.is_possible_number(parsed)

        print()
        gradient_text(f"Country: {country}")
        gradient_text(f"Region: {region}")
        gradient_text(f"Country Code: +{country_code}")
        gradient_text(f"National Number: {national_number}")
        gradient_text(f"Carrier: {carrier_name}")
        gradient_text(f"Type: {phone_type}")
        gradient_text(f"Valid: {valid}")
        gradient_text(f"Possible: {possible}")
        gradient_text(f"Timezone: {', '.join(timezones)}")
        gradient_text(f"International: {international}")
        gradient_text(f"National: {national}")
        gradient_text(f"E.164: {e164}")
        gradient_text(f"RFC3966: {rfc3966}")
        print()

        pause()
        return_to_menu()
    
    if cmd == "1":
        holehe()

    elif cmd == "2":
        ip_geolocation()

    elif cmd == "3":
        phone_lookup()

    elif cmd == "4":
        gradient_text("Coming next update.")
        pause()
        return_to_menu()
    else:
        gradient_text("Invalid input.")


    return_to_menu()


def domain_recon():
        banner = f'''
        ███████╗██╗  ██╗██╗   ██╗███╗   ██╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
        ██╔════╝██║ ██╔╝██║   ██║████╗  ██║██╔═████╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
        ███████╗█████╔╝ ██║   ██║██╔██╗ ██║██║██╔██║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
        ╚════██║██╔═██╗ ██║   ██║██║╚██╗██║████╔╝██║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
        ███████║██║  ██╗╚██████╔╝██║ ╚████║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
        ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝

                                        Version: {VERSION}      
                                        ╔════════════════════════════════════╗
                                        ║                                    ║
                                        ║                                    ║
                                        ║   [1] DNS Records                  ║
                                        ║   [2] WHOIS                        ║
                                        ║   [3] Subdomain Finder             ║
                                        ║   [4] ?                            ║
                                        ║                                    ║
                                        ║                                    ║
                                        ╚════════════════════════════════════╝
    '''

        clear()
        gradient_text(banner)
        gradient_text(f"║\n╚═ root@{user}:~$ ", end="")
        cmd = input()

        def dns_records():
            gradient_text("Domain: ", end="")
            domain = input()
            record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "CAA"]
            results = {}

            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)

                    results[record_type] = [answer.to_text() for answer in answers]

                except (
                    dns.resolver.NoAnswer,
                    dns.resolver.NXDOMAIN,
                    dns.resolver.NoNameservers,
                    dns.exception.Timeout
                ):
                    results[record_type] = []

                for record_type, records in results.items():
                    gradient_text(f"{record_type}:")

                    if records:
                        for record in records:
                            gradient_text(f"  {record}")
                    else:
                        gradient_text("  None")

            pause()
            return_to_menu()

        def whois_domain():
            gradient_text("Domain: ", end="")
            domain = input()

            try:
                data = whois.whois(domain)

                results = {
                    "domain": data.domain,
                    "registrar": data.registrar,
                    "whois_server": data.whois_server,
                    "creation_date": str(data.creation_date),
                    "expiration_date": str(data.expiration_date),
                    "updated_date": str(data.updated_date),
                    "name_servers": data.name_servers,
                    "status": data.status,
                    "emails": data.emails,
                    "organization": data.org,
                    "country": data.country
                }

                for key, value in results.items():
                    gradient_text(f"{key}: {value}")

            except Exception as e:
                gradient_text(f"Error: {e}")


            pause()
            return_to_menu()

        def subdomain_finder():
            gradient_text("Coming next update.")
            return_to_menu()

        
        if cmd == "1":
            dns_records()

        elif cmd == "2":
            whois_domain()

        elif cmd == "3":
            subdomain_finder()

        elif cmd == "4":
            gradient_text("Coming next update.")
            pause()
            return_to_menu()

        else:
            gradient_text("Invalid input.")


        return_to_menu()
        

while True:
    menu()