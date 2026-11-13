
"""Download the public-domain paintings for the rosary's opening and closing prayers.

Run once:   python download_opening_closing.py

Saves them as full\\opening.jpg and full\\closing.jpg in the Rosary project's
docs\\_static\\rosary-images folder (skipping any already there).
"""
import time
import urllib.request
from pathlib import Path

TARGET = Path(r"C:\Users\gmccarthy\Documents\PC_RTD_GITHUB_resources\Rosary\docs\_static\rosary-images\full")

PAINTINGS = {
    # Masaccio, The Holy Trinity (c. 1427), Santa Maria Novella, Florence
    "opening": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/16/Masaccio%2C_Holy_Trinity%2C_1425-28%2C_Santa_Maria_Novella%2C_Florence.jpg/960px-Masaccio%2C_Holy_Trinity%2C_1425-28%2C_Santa_Maria_Novella%2C_Florence.jpg",
    # Piero della Francesca, Madonna della Misericordia (c. 1445-62), Museo Civico, Sansepolcro
    "closing": "https://upload.wikimedia.org/wikipedia/commons/7/75/Piero_della_Francesca_-_Polyptych_of_the_Misericordia_-_Madonna_of_Mercy_-_WGA17449.jpg",
}

HEADERS = {"User-Agent": "RosaryDocs/1.0 (classroom resource; Python urllib)"}


def fetch(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    for name, url in PAINTINGS.items():
        out = TARGET / (name + ".jpg")
        if out.exists():
            print("already there:", out.name)
            continue
        try:
            data = fetch(url)
            out.write_bytes(data)
            print("saved %-12s %4d KB" % (out.name, len(data) // 1024))
        except Exception as e:
            print("FAILED", name, "-", e)
        time.sleep(1)
    print("\nDone - tell Claude so it can crop them for the rosary.")
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
