"""Download the 20 public-domain rosary paintings from Wikimedia Commons.

Run once:   python download_rosary_paintings.py

Saves joyful-1.jpg ... glorious-5.jpg into the Rosary project's
docs\\_static\\rosary-images folder (skipping any already there).
"""
import time
import urllib.request
from pathlib import Path

TARGET = Path(r"C:\Users\gmccarthy\Documents\PC_RTD_GITHUB_resources\Rosary\docs\_static\rosary-images")

PAINTINGS = {
    "joyful-1": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fe/Angelico%2C_prado.jpg/960px-Angelico%2C_prado.jpg",
    "joyful-2": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/82/Visitation_by_Domenico_Ghirlandaio.jpg/960px-Visitation_by_Domenico_Ghirlandaio.jpg",
    "joyful-3": "https://upload.wikimedia.org/wikipedia/commons/3/31/Giotto_di_Bondone_-_No._17_Scenes_from_the_Life_of_Christ_-_1._Nativity_-_Birth_of_Jesus_-_WGA09193.jpg",
    "joyful-4": "https://upload.wikimedia.org/wikipedia/commons/9/95/Giotto_di_Bondone_-_No._19_Scenes_from_the_Life_of_Christ_-_3._Presentation_of_Christ_at_the_Temple_-_WGA09197.jpg",
    "joyful-5": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/William_Holman_Hunt_-_The_Finding_of_the_Saviour_in_the_Temple.jpg/960px-William_Holman_Hunt_-_The_Finding_of_the_Saviour_in_the_Temple.jpg",
    "luminous-1": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5a/Piero_della_Francesca_-_Baptism_of_Christ_-_WGA17595.jpg/960px-Piero_della_Francesca_-_Baptism_of_Christ_-_WGA17595.jpg",
    "luminous-2": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a0/Giotto_di_Bondone_-_No._24_Scenes_from_the_Life_of_Christ_-_8._Marriage_at_Cana_-_WGA09202.jpg/960px-Giotto_di_Bondone_-_No._24_Scenes_from_the_Life_of_Christ_-_8._Marriage_at_Cana_-_WGA09202.jpg",
    "luminous-3": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9c/Carl_Bloch_-_The_Sermon_on_the_Mount.jpg/960px-Carl_Bloch_-_The_Sermon_on_the_Mount.jpg",
    "luminous-4": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/51/Transfiguration_Raphael.jpg/960px-Transfiguration_Raphael.jpg",
    "luminous-5": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1a/Joan_de_Joanes_-_The_Last_Supper_-_WGA12058.jpg/960px-Joan_de_Joanes_-_The_Last_Supper_-_WGA12058.jpg",
    "sorrowful-1": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/Bellini%2CGiovanni_-_Agony_in_the_Garden_-_National_Gallery.jpg/960px-Bellini%2CGiovanni_-_Agony_in_the_Garden_-_National_Gallery.jpg",
    "sorrowful-2": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0e/Caravaggio_-_La_Flagellazione_di_Cristo.jpg/960px-Caravaggio_-_La_Flagellazione_di_Cristo.jpg",
    "sorrowful-3": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/17/Titian_-_Christ_crowned_with_Thorns_-_Louvre.jpg/960px-Titian_-_Christ_crowned_with_Thorns_-_Louvre.jpg",
    "sorrowful-4": "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/61/El_Greco_-_Christ_Carrying_the_Cross_-_Google_Art_Project.jpg/960px-El_Greco_-_Christ_Carrying_the_Cross_-_Google_Art_Project.jpg",
    "sorrowful-5": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/56/Diego_Vel%C3%A1zquez_007.jpg/960px-Diego_Vel%C3%A1zquez_007.jpg",
    "glorious-1": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/eb/Piero_della_Francesca_-_Resurrection_-_WGA17609.jpg/960px-Piero_della_Francesca_-_Resurrection_-_WGA17609.jpg",
    "glorious-2": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/04/Giotto_di_Bondone_-_No._38_Scenes_from_the_Life_of_Christ_-_22._Ascension_-_WGA09226.jpg/960px-Giotto_di_Bondone_-_No._38_Scenes_from_the_Life_of_Christ_-_22._Ascension_-_WGA09226.jpg",
    "glorious-3": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d3/Pentecost%C3%A9s_%28El_Greco%2C_c._1600%29_Prado.jpg/960px-Pentecost%C3%A9s_%28El_Greco%2C_c._1600%29_Prado.jpg",
    "glorious-4": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9e/Tizian_041.jpg/960px-Tizian_041.jpg",
    "glorious-5": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b5/Diego_Vel%C3%A1zquez_-_Coronation_of_the_Virgin_-_Prado.jpg/960px-Diego_Vel%C3%A1zquez_-_Coronation_of_the_Virgin_-_Prado.jpg",
}

HEADERS = {"User-Agent": "RosaryDocs/1.0 (classroom resource; Python urllib)"}


def fetch(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:      # too many requests: wait and retry
                time.sleep(5 * (attempt + 1))
                continue
            raise


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    done = 0
    for name, url in PAINTINGS.items():
        out = TARGET / (name + ".jpg")
        if out.exists():
            print("already there:", out.name)
            done += 1
            continue
        try:
            data = fetch(url)
            out.write_bytes(data)
            print("saved %-14s %4d KB" % (out.name, len(data) // 1024))
            done += 1
        except Exception as e:
            print("FAILED", name, "-", e)
        time.sleep(1)
    print("\n%d of %d paintings in %s" % (done, len(PAINTINGS), TARGET))
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
