from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import db_operations

class Oferta:
    link = ""
    
    lokacja = ""
    cena = ""
    cena_m2 = ""
    
    # Może?
    szacowana_rata_kredytu = ""
    wklad_wlasny = ""
    okres_splaty = ""
    
    # HOSTORIC:
    #   powieszchnia - srednia
    #                - przedzialy   
    #   cena m2      - 
    #
    #
    #
    #   top 30 lokacji
    #   cena m2
    #   powieszchnia
    #   czynsz
    
    # Szczegóły ogłoszenia
    powierzchnia = ""
    liczba_pokoi = ""
    pietro = ""
    czynsz = ""
    forma_wlasnosci = ""
    stan_wykonczenia = ""
    balkon_ogrod_taras = ""
    miejsce_parkingowe = ""
    ogrzewanie = ""
    certyfikat_energetyczny = ""
    
    # Informacje dodatkowe
    rynek = ""
    typ_ogloszeniodawcy = ""
    dostepne_od = ""
    rok_budowy = ""
    rodzaj_zabudowy = ""
    okna = ""
    winda = ""
    media = ""
    zabezpieczenia = ""
    wyposazenie = ""
    informacje_dodatkowe = ""
    material_budynku = ""

class Bot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('log-level=3')
        options.add_argument('--incognito')
        options.add_argument('--pageLoadStrategy=eager')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=NetworkService')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-default-apps')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-remote-fonts')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-component-extensions-with-background-pages')
        options.add_argument("--disable-javascript")

        self.bot = webdriver.Chrome(options=options)
        self.bot.current_site_num = 1
        url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?page=' + str(self.bot.current_site_num)
        self.bot.get(url)
        self.bot.maximize_window()
        
        self.bot.sites_count = ""
        self.bot.linki_do_ofert = []
    
    def accept_cookies(self):
        try:
            button = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            button.click()
        except Exception as e:
            print("Error in accept_cookies: ", e)
            pass
    
    def get_num_of_sites(self):
        #self.bot.sites_count = 2
        try:
            ul = self.bot.find_element(By.CSS_SELECTOR,'ul[data-testid="frontend.search.base-pagination.nexus-pagination"].css-1vdlgt7')
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            last_item = li_elements[-2]
            numer_stron_sesji = last_item.get_attribute("innerHTML")
            self.bot.sites_count = int(numer_stron_sesji)
        except Exception as e:
            print("Error in get_num_of_sites: ", e)
            pass
    
    
    def get_links_to_offers(self):
        while self.bot.current_site_num < self.bot.sites_count:
            try:
                div = self.bot.find_element(By.CSS_SELECTOR, 'div[data-cy="search.listing.organic"]')
                uls = div.find_elements(By.TAG_NAME, 'ul')
                lis = []
                for ul in uls:
                    lis.extend(ul.find_elements(By.TAG_NAME, "li"))

                unique_links = set()
                for li in lis:
                    try:
                        link_element = li.find_element(By.CSS_SELECTOR, 'a[data-cy="listing-item-link"][href^="/pl/oferta/"].css-16vl3c1.e1njvixn0')
                        href = link_element.get_attribute("href")
                        if href not in unique_links:
                            self.bot.linki_do_ofert.append(href)
                            unique_links.add(href)
                    except:
                        pass
                self.bot.current_site_num +=1
                url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?page=' + str(self.bot.current_site_num)
                self.bot.get(url)
            except:
                pass
    
    def get_data_from_links_to_offers(self):
        
        oferta = Oferta()
        
        for link in self.bot.linki_do_ofert:
            self.bot.get(link)
            #lokacja
            try:
                element = self.bot.find_element(By.CSS_SELECTOR, 'a[aria-label="Adres"].e1w8sadu0.css-1helwne.exgq9l20').text
                oferta.lokacja = element.split(",")[1].strip()
            except:
                pass
            #cena
            try:
                Cena_div = self.bot.find_element(By.CSS_SELECTOR, 'strong[data-cy="adPageHeaderPrice"][aria-label="Cena"]')
                oferta.cena = Cena_div.get_attribute("innerHTML").split("z")[0].strip().replace(" ", "")
            except:
                oferta.cena = 0
                pass
            #cena_m2
            try:
                element = self.bot.find_element(By.CSS_SELECTOR, 'div[aria-label="Cena za metr kwadratowy"].css-1h1l5lm.efcnut39').text
                oferta.cena_m2 = element.split("z")[0].strip().replace(" ", "")
            except:
                oferta.cena_m2 = 0
                pass
            
            
            # Get szczegóły ogłoszenia
            szczeguly_div = self.bot.find_element(By.CSS_SELECTOR, 'div.css-2vlfd7.e10umaf20')
            #powierzchnia
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Powierzchnia"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.powierzchnia = text.split()[0].strip().replace(" ", "").replace(",", ".")
            except:
                pass
            #forma_wlasnosci
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Forma własności"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.forma_wlasnosci = text.split()[0].strip()
            except:
                pass
            #liczba_pokoi
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Liczba pokoi"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.find_element(By.CSS_SELECTOR, '[data-cy="ad-information-link"]').text
                text = text.split("z")[0]
                oferta.liczba_pokoi = text.replace(" ", "")
            except :
                oferta.liczba_pokoi = 0
                pass
            #stan_wykonczenia
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Stan wykończenia"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.stan_wykonczenia = text
            except:
                pass
            #pietro
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Stan wykończenia"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.pietro = text
            except:
                pass
            #balkon_ogrod_taras
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Balkon / ogród / taras"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.balkon_ogrod_taras = text
            except:
                pass
            #czynsz
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Czynsz"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.czynsz = text.split("z")[0].replace(" ", "")
            except:
                pass
            #miejsce_parkingowe
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Miejsce parkingowe"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.miejsce_parkingowe = text
            except:
                pass
            #ogrzewanie
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Ogrzewanie"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.ogrzewanie = text
            except:
                pass
            #certyfikat_energetyczny
            try:
                div = szczeguly_div.find_element(By.CSS_SELECTOR, 'div[aria-label="Certyfikat energetyczny"][role="region"].css-1ivc1bc.enb64yk1')
                element = div.find_element(By.CSS_SELECTOR, 'div.css-1wi2w6s.enb64yk5')
                text = element.get_attribute("innerHTML")
                oferta.certyfikat_energetyczny = text
            except:
                pass
            
            
            # Informacje dodatkowe
            inf_dodatkowe_div = self.bot.find_element(By.CSS_SELECTOR, 'div.css-1yvps34.e10umaf20')
            #rynek 
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-market"].css-1wi2w6s.enb64yk5').text
                oferta.rynek = element.strip()
            except:
                pass
            #typ_ogloszeniodawcy 
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-advertiser_type"].css-1wi2w6s.enb64yk5').text
                oferta.typ_ogloszeniodawcy = element.strip()
            except:
                pass
            #dostepne_od
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-free_from"].css-1wi2w6s.enb64yk5').text
                oferta.dostepne_od = element.strip()
            except:
                pass
            #rok_budowy 
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-build_year"].css-1wi2w6s.enb64yk5').text
                oferta.rok_budowy = element.strip()
            except:
                pass
            #rodzaj_zabudowy 
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-building_type"].css-1wi2w6s.enb64yk5').text
                oferta.rodzaj_zabudowy = element.strip()
            except:
                pass
            #okna
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-windows_type"].css-1wi2w6s.enb64yk5').text
                oferta.okna = element.strip()
            except:
                pass
            #winda 
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-lift"].css-1wi2w6s.enb64yk5').text
                oferta.winda = element.strip()
            except:
                pass
            #media
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-media_types"].css-1wi2w6s.enb64yk5').text
                oferta.media = element.strip()
            except:
                pass
            #zabezpieczenia
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-security_types"].css-1wi2w6s.enb64yk5').text
                oferta.zabezpieczenia = element.strip()
            except:
                pass
            #wyposazenie
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-equipment_types"].css-1wi2w6s.enb64yk5').text
                oferta.wyposazenie = element.strip()
            except:
                pass
            #informacje_dodatkowe
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-extras_types"].css-1wi2w6s.enb64yk5').text
                oferta.informacje_dodatkowe = element.strip()
            except:
                pass
            #material_budynku
            try:
                element = inf_dodatkowe_div.find_element(By.CSS_SELECTOR, 'div[data-testid="table-value-building_material"].css-1wi2w6s.enb64yk5').text
                oferta.material_budynku = element.strip()
            except:
                pass
                         
            #TODO: fix formating in some variables in oferta
            # Here insert to database
            try:
                db_operations.insert_data(oferta)
            except Exception as e:
                print("Error in insert_data: ", e)
                pass

if __name__ == "__main__":
    bot = Bot()

    bot.accept_cookies()
    
    bot.get_num_of_sites()
    bot.get_links_to_offers()
    
    bot.get_data_from_links_to_offers()
    
    input("end of program")
