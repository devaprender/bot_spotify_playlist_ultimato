from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random


class PlaylistUltimato:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-BR")
        self.driver = webdriver.Chrome(executable_path=r"./chromedriver.exe",chrome_options=options)
        self.wait = WebDriverWait(
            self.driver,
            10,
            poll_frequency=1,
            ignored_exceptions=[  
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
            ],
        )
        self.email = "email@hotmail.com"
        self.senha = "senha123456"
        self.link_spofity = "https://open.spotify.com/"
        self.DeveUsarLoginFacebook = True

    def Start(self):
        self.driver.get(self.link_spofity)
        self.LoginSpotify()
        if self.DeveUsarLoginFacebook == True:
            self.LogarComFacebook()
        else:
            self.LogarComEmail()
        self.GerarPlaylist()

    def LoginSpotify(self):
        print("Loggando no Spotify")
        login_button = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//button[text()="Entrar"]')
            )
        )
        login_button.click()

    def LogarComEmail(self):
        campo_email = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//input[@name="username"]')))
        campo_senha = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//input[@name="password"]')))
        botao_entrar = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//button[text()="Entrar"]')))

        campo_email.send_keys(self.email)
        time.sleep(2)
        campo_senha.send_keys(self.senha)
        time.sleep(2)
        botao_entrar.click()

    def LogarComFacebook(self):
        print("logando no facebook")
        botao_logar_com_facebook = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//a[text()="Entrar com o Facebook"]')
            )
        )
        botao_logar_com_facebook.click()
        self.InserirDadosLoginFacebook()

    def InserirDadosLoginFacebook(self):
        campo_email = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//input[@name="email"]')))
        campo_senha = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//input[@name="pass"]')))
        botao_login = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH,'//button[@name="login"]')))

        campo_email.clear()
        self.digite_como_uma_pessoa(self.email, campo_email)
        time.sleep(random.randint(1, 3))
        campo_senha.clear()
        self.digite_como_uma_pessoa(self.senha, campo_senha)
        time.sleep(random.randint(1, 3))
        botao_login.click()
        time.sleep(random.randint(4, 7))

    def GerarPlaylist(self):
        lists_dos_artistas = self.ObterLinksDosArtistas()
        for link_do_artista in lists_dos_artistas:
            self.NavegarParaAlbumAtual(link_do_artista)
            self.ObterLinksDosAlbunsDesteArtista()
            self.NavegarParaCadaAlbumDesteArtista(self.links_dos_albuns)
        self.driver.quit()

    def NavegarParaAlbumAtual(self, link_do_artista):
        time.sleep(random.randint(2, 4))
        self.driver.get(link_do_artista)
        self.wait.until(
            CondicaoExperada.visibility_of_element_located(
                (By.XPATH, '//h1[text()="Álbuns"]')
            )
        )
        time.sleep(random.randint(2, 3))


    def NavegarParaCadaAlbumDesteArtista(self, links_do_album):
        for link_album in links_do_album:
                try:
                    self.driver.get(link_album)
                    print('adicionando album: '+ link_album)
                    time.sleep(1)
                    self.AddAlbumParaPlaylist(link_album)
                except:
                    print('não foram encontrados albuns para este artista')
                    pass

    def ClicarNoMenuOpcoesDoAlbum(self):
        try:
            self.actions = ActionChains(self.driver)
            self.wait.until(
                CondicaoExperada.element_to_be_clickable(
                    (By.XPATH, '//button[@class="btn btn-transparent btn--narrow"]')
                )
            )
            menu_opcoes_do_album = self.driver.find_elements_by_xpath(
                '//button[@class="btn btn-transparent btn--narrow"]'
            )
            time.sleep(random.randint(1, 2))
            self.actions.context_click(menu_opcoes_do_album[1]).perform()
        except:
            pass

    def AddAlbumParaPlaylist(self, album_link):
        self.driver.get(album_link)
        self.ClicarNoMenuOpcoesDoAlbum()
        self.ClicarEmAdicionarParaPlaylist()
        self.ClicarNaPlaylistASerAdicionada(album_link)

    def DescerPagina(self, elemento_referencia, quantidade_de_descidas):
        for descida in range(1, quantidade_de_descidas):
            time.sleep(random.randint(1, 3))
            elemento_referencia.send_keys(Keys.PAGE_DOWN)
            time.sleep(random.randint(1, 3))

    def ClicarNaPlaylistASerAdicionada(self, album_link):
        time.sleep(random.randint(3, 4))
        thumbnail_playlist = self.wait.until(
            CondicaoExperada.visibility_of_any_elements_located(
                (By.XPATH, '//div[@class="mo-coverArt-hoverContainer"]')
            )
        )
        time.sleep(random.randint(4, 6))
        thumbnail_playlist[0].click()
        print('Clicando em "Adicionar a Playlist"')
        time.sleep(random.randint(2, 4))

    def ClicarEmAdicionarParaPlaylist(self):
        add_to_playlist_button = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (
                    By.XPATH,
                    '//nav[@class="react-contextmenu react-contextmenu--visible"]/div[@class="react-contextmenu-item" and text()="Adicionar à playlist"]',
                )
            )
        )
        time.sleep(random.randint(1, 2))
        add_to_playlist_button.click()

    def ObterLinksDosArtistas(self):
        print("Encontrando artistas para este perfíl")
        self.driver.get("https://open.spotify.com/collection/artists")
        first_artist_element = self.wait.until(
            CondicaoExperada.visibility_of_element_located(
                (By.XPATH, '//*[text()="Red"]')
            )
        )
        self.DescerPagina(first_artist_element, 10)
        time.sleep(3)
        somentes_hrefs = []
        somente_links_de_artistas = []
        todos_links_na_pagina = self.driver.find_elements_by_tag_name('a')
        for elemento in todos_links_na_pagina:
            somentes_hrefs.append(elemento.get_attribute("href"))
    
        for link in somentes_hrefs:
            try:
                if link.index('/artist/') != -1:
                    somente_links_de_artistas.append(link)
            except:
                pass
        return list(dict.fromkeys(somente_links_de_artistas))

    def CarregarMaisAlbuns(self):
        try:
            self.botao_carregar_mais_albuns = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//section[@class=" artist-albums"]//*[text()="MOSTRAR MAIS"]')
            )
            )
            self.botao_carregar_mais_albuns.click()
            time.sleep(random.randint(1, 2))
            self.botao_carregar_mais_albuns = None
            self.botao_carregar_mais_albuns = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//section[@class=" artist-albums"]//*[text()="MOSTRAR MAIS"]')
            )
            )
            if self.botao_carregar_mais_albuns is not None:
                self.botao_carregar_mais_albuns.click()
                print("Carregando mais albuns")
                self.CarregarMaisAlbuns()
        except:
            print("Todos albuns foram carregados")
            pass
        

    def ObterLinksDosAlbunsDesteArtista(self):
        somente_hrefs = []
        links_dos_albuns = []
        links_unicos_dos_albuns = []

        try:
            self.CarregarMaisAlbuns()
        except:
            print("Carregado todos albuns desta página")
            pass

        elemento_secao_album = self.driver.find_elements_by_xpath(
            '//section[@class=" artist-albums"]//a'
        )
        for elemento in elemento_secao_album:
            somente_hrefs.append(elemento.get_attribute("href"))

        for link in somente_hrefs:
            try:
                if link.index("/album/") != -1:
                    links_dos_albuns.append(link)
            except:
                pass

        for link in links_dos_albuns:
            links_unicos_dos_albuns.append(link)
        self.links_dos_albuns = list(dict.fromkeys(links_unicos_dos_albuns))

    @staticmethod
    def digite_como_uma_pessoa(frase, campo_input_unico):
        print("Digitando...")
        for letra in frase:
            campo_input_unico.send_keys(letra)
            time.sleep(random.randint(1, 5) / 30)


bot = PlaylistUltimato()
bot.Start()