# Tool Name: Verify URL
# Tool Author: Andre Bhaseen
# Version: 0.2
# Liscence: MIT Liscence
# Description: A Tool used to verify the return code of a URL

import argparse  # used for parsing customized command line arguemnts
import sys  # used for grabbing command line argmuents

# import codecs #originally used for parsing...

# Using beautiful soup for parsing HTML
# Setting up Beautiful Soup

import bs4 as bs
import requests  # used for receiving requests codes

# Setting up colors for output
# Grabbed code from here: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python # The origin of the code however is from Blender


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ORANGEWARNING = "\033[38;5;214m"
    INFOCYAN = "\033[36m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Setting up range for request codes
# last number in range is not included - range in python works as: [m,n)

# Informational
informationalCode = range(100, 200)
# Success code range
successCode = range(200, 300)
# Redirection
redirectCode = range(300, 400)
# Error code range
errorCode = range(400, 500)
# Server Error range
serverErrorCode = range(500, 600)

# Creating an array to store URLs
urls = []

# Testing URLs:
# urls.append("https://google.com")  # 200
# urls.append("http://google.com/nothere")  # 404
# urls.append('http://api.github.com/user')  # 401

# Main Component of Program
def main():
    args, filename = get_args()
    check_args(args.singleUrl, args.version, filename)
    verify_url()

def get_args():
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
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_known_args()

def check_args(singleUrl, version, filename):
    if version is True:
        print(f"{bcolors.HEADER}Verify URL Tool {bcolors.ENDC} Version: {bcolors.BOLD}0.1{bcolors.ENDC}")
        sys.exit(1)
    elif singleUrl == "const":
        print(f"{bcolors.WARNING}⚠️ URL has not been entered, please enter a URL after the -u/--url argument to analyze.{bcolors.ENDC}")
        sys.exit(1)
    else:
        if singleUrl not in ("default", "const"):
            urls.append(singleUrl)
        elif filename:
            get_urls(filename)

def get_urls(filename):
    if filename[0].endswith(".html"):
        try:
            with open(filename[0], "r") as local_html:
                source = local_html.read()
                soup = bs.BeautifulSoup(source, "lxml")
            for url in soup.find_all("a"):
                urls.append(url.get_text("href"))
        except FileNotFoundError:
            print(f"{bcolors.WARNING}⚠️ File not found. Please enter a valid HTML file.{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}⚠️ File should be in HTML format, for single URLs please use the -u/--url arguments before the URL.{bcolors.ENDC}")

def verify_url():     
    for url in urls:
        status_color = bcolors.BOLD
        message = 'Unknown Return Code ⚠️'
        try:
            url_req = requests.get(url, timeout=5)
            if url_req.status_code in successCode:
                status_color = bcolors.OKGREEN
                message = 'Success, this site exists! ✔️'
            elif url_req.status_code in errorCode:
                status_color = bcolors.FAIL
                message = 'Failed to reach this site. ❌'
            elif url_req.status_code in redirectCode:
                status_color = bcolors.OKBLUE
                message = 'This site will redirect you. ↩'
            elif url_req.status_code in serverErrorCode:
                status_color = bcolors.ORANGEWARNING
                message = 'Encountered a server error. 🚫'
            elif url_req.status_code in informationalCode:
                status_color = bcolors.INFOCYAN
                message = 'Informational return code ℹ️'
            print_status(url, url_req.status_code, status_color, message)
        except requests.exceptions.Timeout:
            print_status('Read Timed Out', bcolors.FAIL, 'Failed to reach this site. Read Timed Out. ❌')
        except requests.exceptions.ConnectionError:
            print_status('Connection refused', bcolors.FAIL, 'Failed to reach this site. Connection Refused. ❌')
        except requests.exceptions.RequestException as req_error:
            raise SystemExit(req_error)
        except:
            print("Unexpected Error")

def print_status(url, status_code, status_color, message):
    print(f"{bcolors.WARNING}Status Code:{status_color}{bcolors.BOLD}{status_code}{bcolors.ENDC}{status_color} - {message}{bcolors.ENDC} {bcolors.BOLD}URL:{bcolors.ENDC} {bcolors.OKBLUE}{url}{bcolors.ENDC}")

# adding ability to add arguments
if __name__ == "__main__":
    main()
