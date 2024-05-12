import pygame
import sys
from MyUtils import blit_line,Bordered_blit_line
from MyColours import *
from Buttons import EasyButton,create_buttons
from Textboxes import Textbox
from Validation import paswordcheck, Lencheck
from game import Game
import os

class BasicPage:
    def __init__(self, name, system, returning=False):
        pygame.display.set_caption('Pages')
        self.screen = pygame.display.set_mode((700, 500))
        self.clock = pygame.time.Clock()
        self.System = system
        self.Return = EasyButton("Back", (150, 390), activecol=orange)
        self.Quit = EasyButton("Quit", (450, 390), activecol=red)
        self.Buttons = [self.Quit] if not returning else [self.Quit, self.Return]
        self.name = name
        self.Titlefont = pygame.font.SysFont("Arial", 32)
        self.Title = self.Titlefont.render(self.name, False, (0, 0, 0))
        self.Title_rect = self.Title.get_rect(center=(self.screen.get_width() / 2, 60))
        self.Menu_bar = pygame.Rect(100, 40, 3 * self.screen.get_width() / 4, self.screen.get_height() - 100)
        self.next = ""
        self.returning = returning

    def Returnhandler(self, change=-1):
        if self.Return.isClicked:
            self.System.Changepage(change)

    def Handle_Event(self, event):
        for button in self.Buttons:
            button.handle_events(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def Quithandler(self):
        if self.Quit.isClicked:
            pygame.quit()
            sys.exit()

    def UpdateDisplay(self):
        self.screen.fill(white)
        self.screen.blit(self.Title, self.Title_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.Menu_bar, 1, 25)
        self.Quithandler()
        for button in self.Buttons:
            button.draw(self.screen)
        self.Returnhandler()

    def run(self):
        while True:
            for event in pygame.event.get():
                self.Handle_Event(event)

            self.UpdateDisplay()
            pygame.display.update()
            self.clock.tick(60)




class Start(BasicPage):
    def __init__(self, system):
        super().__init__(name="Levels", system=system, returning=True)
        self.new = create_buttons()
        self.Buttons.extend(self.new)


    def Returnhandler(self):
        super().Returnhandler(-1)

    def CLicked(self):
        for button in self.new:
            if button.isClicked:
                os.environ['SDL_VIDEO_CENTERED'] = "1"
                self.System.Game.level = int(button.name[-1])
                self.System.Game.PlayerSpawners = False
                self.screen = pygame.display.set_mode((1280, 720))
                self.System.Game.run()

    def UpdateDisplay(self):
        super().UpdateDisplay()
        self.Playername = self.System.Login.Username.savetext
        pagefont = pygame.font.SysFont("Arial", 15, bold=True)
        blit_line(self.screen, [f"User: {self.Playername}"], (110, 70), color=black, font=pagefont)
        self.CLicked()




class PagesSystem:
    def __init__(self):
        self.Pages = [Start(self)]
        self.Game = Game(self)
        self.Current_Page = self.Pages[self.Pageindex]

    def Changepage(self, increase):
        for button in self.Current_Page.Buttons:
            if not button.toggle:
                button.isClicked = False
        self.Pageindex += increase
        self.Pageindex %= len(self.Pages)
        self.Current_Page = self.Pages[self.Pageindex]
        for button in self.Current_Page.Buttons:
            if not button.toggle:
                button.isClicked = False
        self.run()

    def run(self):
        self.Current_Page.run()



PagesSystem().run()
