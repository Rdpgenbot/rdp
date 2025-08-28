import requests
from bs4 import BeautifulSoup

# --- CONFIG ---
BASE_URL = "https://cdms.police.gov.bd/cdms/"
LOGIN_URL = BASE_URL + "wwv_flow.accept"
USERNAME = "8403040326"
PASSWORD = "Nsna1234@"

# --- SESSION SETUP ---
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})

def fetch_login_tokens():
    """GET করে hidden token গুলো আনা (SSL verify bypass করা হয়েছে)"""
    r = session.get(BASE_URL, verify=False)  # SSL bypass
    if r.status_code != 200:
        raise Exception("Failed to load login page")

    soup = BeautifulSoup(r.text, "html.parser")
    tokens = {}

    for hidden in soup.find_all("input", {"type": "hidden"}):
        if hidden.get("name") and hidden.get("value"):
            tokens[hidden["name"]] = hidden["value"]

    return tokens

def login():
    try:
        tokens = fetch_login_tokens()

        # form data বানানো
        payload = {
            "p_flow_id": tokens.get("p_flow_id"),
            "p_flow_step_id": tokens.get("p_flow_step_id"),
            "p_instance": tokens.get("p_instance"),
            "p_request": "LOGIN",
            "p_arg_names": ["USERNAME", "PASSWORD"],
            "p_arg_values": [USERNAME, PASSWORD]
        }

        r = session.post(LOGIN_URL, data=payload, allow_redirects=True, verify=False)  # SSL bypass

        if "Logout" in r.text or "Dashboard" in r.text:
            print("✅ Login success")
        else:
            print("❌ Login failed!")
            # Debugging output (first 500 chars)
            print(r.text[:500])

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    login()