import sys
import time

from config import PAUSE_BETWEEN
from driver import init_driver
from scraper import search_official_site
from excel_handler import load_excel, save_excel


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage : python main.py <fichier_input.xlsx> <fichier_output.xlsx>")
        sys.exit(1)

    fichier_input = sys.argv[1]
    fichier_output = sys.argv[2]

    df = load_excel(fichier_input)

    print("Demarrage de Chrome headless pour scraper Bing...")
    driver = init_driver()

    total = len(df)

    for idx, raw_name in enumerate(df["Raison Sociale"], start=1):
        company = raw_name.strip() if isinstance(raw_name, str) else ""
        print(f"[{idx}/{total}] Recherche Bing pour '{company}' ...", end=" ")

        if not company:
            df.at[idx - 1, "Site officiel"] = ""
            print("vide -> aucune URL")
        else:
            url = search_official_site(driver, company)
            df.at[idx - 1, "Site officiel"] = url
            print(url if url else "aucun lien valide trouve")

        save_excel(df, fichier_output)

        time.sleep(PAUSE_BETWEEN)

    driver.quit()
    print(f"\nTraitement termine. Fichier enregistre sous '{fichier_output}'.")


if __name__ == "__main__":
    main()