from bs4 import BeautifulSoup
import requests
from typing import Literal

WRS_150_URL = "https://mkwrs.com/mk8dx/wrs.php"
WRS_200_URL = "https://mkwrs.com/mk8dx/wrs_200.php"

def fetch_wrs(cc: str, items: str) -> list:
    if items == "Shrooms":
        return fetch_wrs_shrooms(cc)
    elif items == "NITA":
        return fetch_wrs_nita(cc)
    else:
        raise ValueError(f"Item type is not recognised: {items}")

def fetch_wrs_shrooms(cc: Literal["150cc", "200cc"] = "150cc") -> list:
    url = WRS_150_URL if cc == "150cc" else WRS_200_URL
    # Should probably put a try-except
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    wr_table = soup.find_all("table")[1]
    wr_times = []
    for row in wr_table.find_all("tr")[1:]:
        col = row.find_all("td")
        track = col[0].text.strip()
        time = col[1].text.strip()

        if "*" not in time:
            # Change format: M'SS"mmm -> M:SS.mmm
            time = time.replace("'", ":").replace('"', ".")
            wr_times.append((track, time))

    return wr_times

def fetch_wrs_nita(cc: Literal["150cc", "200cc"] = "150cc") -> list:
    raise NotImplementedError()