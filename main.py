import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime


def scrap_albums():
    """
    Scrape les albums des années 1960s à 2020s depuis besteveralbums.com
    100 pages par décennie = ~1000 albums/décennie = ~7000 albums total
    """

    # ========================================
    # FONCTIONS D'EXTRACTION
    # ========================================

    def get_titre(title_row):
        """Extrait le titre de l'album"""
        titre_link = title_row.find("a", class_="nav2emph bigger")

        if titre_link:
            return titre_link.text.strip()

        return None

    def get_artiste(title_row):
        """Extrait le nom de l'artiste"""
        all_links = title_row.find_all("a", class_="nav2emph bigger")

        if len(all_links) >= 2:
            return all_links[1].text.strip()

        return None

    def get_year(stats_div):
        """Extrait l'année de sortie"""
        if not stats_div:
            return None

        labels = stats_div.find_all("div", class_="chartstring")
        metrics = stats_div.find_all("div", class_="chart-stats-metric")

        for index in range(len(labels)):
            label_text = labels[index].text.strip()

            if label_text == "Year of Release:":
                if index < len(metrics):
                    year_text = metrics[index].text.strip()

                    digits = ""
                    for character in year_text:
                        if character.isdigit():
                            digits = digits + character
                        if len(digits) == 4:
                            return int(digits)

        return None

    def get_overall_rank(stats_div):
        """Extrait le classement global (Overall Rank)"""
        if not stats_div:
            return None

        labels = stats_div.find_all("div", class_="chartstring")
        metrics = stats_div.find_all("div", class_="chart-stats-metric")

        for index in range(len(labels)):
            label_text = labels[index].text.strip()

            if label_text == "Overall Rank:":
                if index < len(metrics):
                    rank_link = metrics[index].find("a")

                    if rank_link:
                        rank_text = rank_link.text.strip()
                        rank_text = rank_text.replace(",", "")

                        digits = ""
                        for character in rank_text:
                            if character.isdigit():
                                digits = digits + character

                        if digits:
                            return int(digits)

        return None

    def get_pays(title_row):
        """Extrait le pays depuis le drapeau"""
        if not title_row:
            return None

        flag_img = title_row.find("img", class_="flag-mini")

        if flag_img:
            pays = flag_img.get("title") or flag_img.get("alt")
            return pays

        return None

    def get_number_of_charts(stats_div):
        """Extrait le nombre de charts où l'album apparaît"""
        if not stats_div:
            return None

        labels = stats_div.find_all("div", class_="chartstring")
        metrics = stats_div.find_all("div", class_="chart-stats-metric")

        for index in range(len(labels)):
            label_text = labels[index].text.strip()

            if label_text == "Appears in:":
                if index < len(metrics):
                    metric_text = metrics[index].text.strip()

                    digits = ""
                    for character in metric_text:
                        if character.isdigit():
                            digits = digits + character

                    if digits:
                        return int(digits)

        return None


    def get_rank_by_year(stats_div):
        """Extrait le rang de l'album pour son année de sortie"""
        if not stats_div:
            return None

        labels = stats_div.find_all("div", class_="chartstring")
        metrics = stats_div.find_all("div", class_="chart-stats-metric")

        for index in range(len(labels)):
            label_text = labels[index].text.strip()

            if label_text.startswith("Rank in") and label_text.endswith(":"):
                year_in_label = ""
                for character in label_text:
                    if character.isdigit():
                        year_in_label = year_in_label + character

                if len(year_in_label) == 4:
                    if index < len(metrics):
                        metric_text = metrics[index].text.strip()

                        digits = ""
                        for character in metric_text:
                            if character.isdigit():
                                digits = digits + character

                        if digits:
                            return int(digits)

        return None


    def get_rank_by_decade(stats_div):
        """Extrait le rang de l'album pour sa décennie"""
        if not stats_div:
            return None

        labels = stats_div.find_all("div", class_="chartstring")
        metrics = stats_div.find_all("div", class_="chart-stats-metric")

        for index in range(len(labels)):
            label_text = labels[index].text.strip()

            if label_text.startswith("Rank in") and label_text.endswith("s:"):
                if index < len(metrics):
                    metric_text = metrics[index].text.strip()

                    digits = ""
                    for character in metric_text:
                        if character.isdigit():
                            digits = digits + character

                    if digits:
                        return int(digits)

        return None


    # ========================================
    # CONFIGURATION
    # ========================================

    base_url = "https://www.besteveralbums.com/topratedstats.php"

    cookies = {
        "bea3_data": "YTowOnt9",
        "bea3_sid": "013323156478d07ba0ac248c3030b61b",
        "_gid": "GA1.2.1231774226.1770906771",
        "_ga": "GA1.1.1916262177.1770906771",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    decades = {
        "1960s": 196,
        "1970s": 197,
        "1980s": 198,
        "1990s": 199,
        "2000s": 200,
        "2010s": 201,
        "2020s": 202,
    }

    all_albums = []
    max_pages = 100

    # ========================================
    # SCRAPING
    # ========================================

    for decade_name, decade_code in decades.items():
        print(f"{'=' * 50}")
        print(f":musical_note: {decade_name}...")
        print(f"{'=' * 50}")

        for page_number in range(1, max_pages + 1):
            print(f"  Page {page_number:2}/{max_pages}...", end=" ", flush=True)

            params = {
                "o": "album",
                "d": str(decade_code),
                "y": str(decade_code),
                "r": "10",
                "orderby": "Rank",
                "sortdir": "asc",
                "page": str(page_number),
            }

            try:
                response = requests.get(
                    base_url,
                    params=params,
                    cookies=cookies,
                    headers=headers,
                    timeout=10,
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")

                    all_rows = []
                    all_rows.extend(soup.find_all("div", class_="chartrow"))
                    all_rows.extend(soup.find_all("div", class_="chartrow2"))

                    albums_count = 0

                    for index in range(0, len(all_rows), 4):
                        if index + 3 >= len(all_rows):
                            break

                        title_row = all_rows[index]
                        stats_row = all_rows[index + 3]
                        stats_div = stats_row.find("div", class_="chart-stats")

                        album = {
                            "decade": decade_name,
                            "album": get_titre(title_row),
                            "artiste": get_artiste(title_row),
                            "annee": get_year(stats_div),
                            "rang": get_overall_rank(stats_div),
                            "country": get_pays(title_row),
                            "charts": get_number_of_charts(stats_div),
                            "rang_par_annee": get_rank_by_year(stats_div),
                            "rang_par_decennie": get_rank_by_decade(stats_div)
                        }

                        if album["album"]:
                            all_albums.append(album)
                            albums_count += 1

                    print(f":white_check_mark: {albums_count} albums")
                    time.sleep(2)

                else:
                    print(f":x: Erreur {response.status_code}")
                    break

            except Exception as error:
                print(f":x: {error}")
                break

        print(f":white_check_mark: {decade_name} terminée\n")
        time.sleep(3)

    return all_albums


# ========================================
# SAUVEGARDE JSON
# ========================================

if __name__ == "__main__":
    resultats = scrap_albums()

    print("\n" + "=" * 70)
    print(":floppy_disk: SAUVEGARDE DES DONNÉES")
    print("=" * 70)

    # Créer un dictionnaire avec métadonnées
    data_complete = {
        "metadata": {
            "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "besteveralbums.com",
            "nombre_albums": len(resultats),
            "nombre_decennies": 7,
            "pages_par_decennie": 100,
        },
        "albums": resultats,
    }

    # Sauvegarder en JSON
    filename = f"albums_bestever_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_complete, f, ensure_ascii=False, indent=2)

    print(f":white_check_mark: Fichier JSON créé : {filename}")
    print(f":bar_chart: {len(resultats)} albums sauvegardés")

    # Aperçu des 5 premiers albums
    print("\n" + "=" * 70)
    print(":clipboard: APERÇU DES DONNÉES")
    print("=" * 70)

    for index, album in enumerate(resultats[:5], 1):
        print(
            f"{index}. {album['album']} - {album['artiste']} ({album['annee']}) - Rang: {album['rang']}"
        )

    print(f"\n... et {len(resultats) - 5} autres albums")

    print("\n:tada: TERMINÉ !")