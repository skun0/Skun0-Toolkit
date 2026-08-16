# Developed by https://github.com/skun0
# Next Update: 
import os, requests, time, ctypes, phonenumbers, subprocess, json, socket, asyncio, dns.resolver

from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.text import Text
from phonenumbers import geocoder, carrier, timezone

VERSION = 1.0
UP_TO_DATE = True

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
            "git fetch",
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

        local = subprocess.check_output(
            "git rev-parse HEAD",
            shell=True,
            text=True
        ).strip()

        remote = subprocess.check_output(
            "git rev-parse @{u}",
            shell=True,
            text=True
        ).strip()

        if local != remote:
            gradient_text("[*] Update available!")
            subprocess.run(
                "git pull",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )
            gradient_text("[*] Updated successfully.")
        else:
            gradient_text("[*] Already up to date.")

    except subprocess.CalledProcessError:
        gradient_text("[-] Could not check for updates.")

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
                                        ║   [3] DoS Attack                   ║
                                        ║   [4] Port Scanner                 ║
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
        # domain_recon()
        pass

    elif cmd == "3":
        # dos_attack()
        pass

    elif cmd == "4":
        # port_scanner()
        pass

    elif cmd == "U":
        # update()
        pass
    else:
        gradient_text("Invalid input.")

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
                                        ║   [3] Subdomain Finderr            ║
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
            gradient_text("Coming Soon.")

        def whois():
            gradient_text("Coming Soon.")

        def subdomain_finder():
            gradient_text("Coming Soon.")

        
        if cmd == "1":
            dns_records()

        elif cmd == "2":
            whois()

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
