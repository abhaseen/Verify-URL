"""
Tool Name: Verify URL
Tool Author: Andre Bhaseen
Version: 0.3
Licence: MIT Liscence
Description: A Tool used to verify the return code of a URL
"""
import argparse  # used for parsing customized command line arguemnts
import sys  # used for grabbing command line argmuents

# import codecs #originally used for parsing...

# Using beautiful soup for parsing HTML
# Setting up Beautiful Soup

import colorama
from colorama import Fore

import bs4 as bs
import requests  # used for receiving requests codes

# Initializing color
colorama.init(autoreset=True)

# Setting up range for request codes
# last number in range is not included - range in python works as: [m,n)

# Informational
info_code = range(100, 200)
# Success code range
success_code = range(200, 300)
# Redirection
redirect_code = range(300, 400)
# Error code range
client_err_code = range(400, 500)
# Server Error range
server_err_code = range(500, 600)

# Creating an array to store URLs
urls = []

# Testing URLs:
# urls.append("https://google.com")  # 200
# urls.append("http://google.com/nothere")  # 404
# urls.append('http://api.github.com/user')  # 401


def generate_status_message(status_code):
    """Generate message strings based on passed website Status Code.

    Args:
        status_code (interger): Status code returned by website

    Returns:
       color [colorama.Fore.COLOR]: Colorama Foreground Color option selected.
       status_string [string]: Display string associated to Status Code
    """
    status_out_dict = [
        {"color": Fore.CYAN, "string": " - Informational return code ℹ️ - URL:"},
        {"color": Fore.GREEN, "string": " - Success, this site exists! ✔️ - URL:"},
        {"color": Fore.BLUE, "string": " - This site will redirect you. ↩ - URL:"},
        {"color": Fore.RED, "string": " - Failed to reach this site. ❌ - URL:"},
        {"color": Fore.RED, "string": " - Encountered a server error. 🚫 - URL:"},
        {"color": Fore.RED, "string": " - Unknown Return Code ⚠️ -  URL:"},
    ]

    status_string = f"Status Code: {status_code}"
    if status_code in info_code:
        message_code = 0
    elif status_code in success_code:
        message_code = 1
    elif status_code in redirect_code:
        message_code = 2
    elif status_code in client_err_code:
        message_code = 3
    elif status_code in server_err_code:
        message_code = 4
    else:
        # Unknown Error
        message_code = 5

    color = status_out_dict[message_code]["color"]
    status_string = f"{status_string}{status_out_dict[message_code]['string']}"
    return (color, status_string)


def check_urls():
    """Make requests to all found urls (be it from file or -u argument) to identify their
    status code.

    Raises:
        RuntimeError: Request Error -> Error occured while attempting to make a request.
    """
    for url in urls:
        try:
            url_req = requests.get(url, timeout=5)
            print_message(url_req.status_code, url)
        except requests.exceptions.Timeout:
            print_message(
                -2,
                "Status Code: Read Timed Out - Failed to reach this site. "
                f"Read Timed Out. ❌ - URL: {url}",
            )
        except requests.exceptions.ConnectionError:
            print_message(
                -2,
                "Status Code: Connection refused - Failed to reach this site. "
                f"Connection Refused. ❌ - URL: {url}",
            )
        except requests.exceptions.RequestException as req_error:
            raise RuntimeError("Request Exception") from req_error
        except:
            print("Unexpected Error")


def read_html_file(html_file):
    """Parse html file passed to the string for all urls."""
    if html_file[0].endswith(".html"):
        try:
            with open(html_file[0], "r") as local_html:
                source = local_html.read()
                soup = bs.BeautifulSoup(source, "lxml")
            for url in soup.find_all("a"):
                urls.append(url.get_text("href"))
        except FileNotFoundError:
            print_message(-2, "File not found. Please enter a valid HTML file.")
    else:
        print_message(
            -2,
            "File should be in HTML format, for single URLs please use the -u/--url"
            "arguments before the URL.",
        )


def print_message(status, print_val):
    """Print message with the correct colors to the screen.

    Args:
        status (integer): Code used to identify the color: Status Code or Negative numbers (-1, -2)
        print_val (string): Message we want to print to the screen.
    """
    if status == -1:
        # Header
        print_color = Fore.MAGENTA
        out_string = ""
    elif status == -2:
        # Program Warning
        print_color = Fore.YELLOW
        out_string = "⚠️"
    else:
        print_color, out_string = generate_status_message(status)
    print_val = f"{out_string} {print_val}"
    print(print_color + print_val)


# Main Component of Program
def main(single_url, version, html_file):
    """Parse through program arguments. Starting subroutines based on arguments.

    Args:
        single_url (string): User passed URL
        version (bool): Identify if the user passed -v or --version
        html_file (string): Local html file to parse for urls.
    """
    if version is True:
        print_message(-1, "Verify URL Tool -- Version: 0.3")
    elif single_url == "const":
        print_message(
            -2,
            "URL has not been entered, please enter a URL after the -u/--url"
            "argument to analyze.",
        )
    else:
        if single_url not in ("default", "const"):
            urls.append(single_url)
        elif html_file:
            read_html_file(html_file)
        else:
            if len(sys.argv) == 1:
                parser.print_help(sys.stderr)
                sys.exit(1)
        check_urls()


# adding ability to add arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool used for verifyinig the return code of a URL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Details information about the tool (version and name of tool)",
        required=False,
        dest="version",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        nargs="?",
        default="default",
        const="const",
        help="Used for single urls",
        required=False,
        dest="singleUrl",
    )
    args, filename = parser.parse_known_args()
    # args = parser.parse_args()
    main(args.singleUrl, args.version, filename)
