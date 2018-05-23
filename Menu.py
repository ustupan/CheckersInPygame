#MENU MODULE...
from Game import *


class Menu(SetupWindow):
    def __init__(self):
        super().__init__()
        self.__buttonSize = [300, 50]
        self.__menuText = ['GRAJ', 'ZASADY', 'WYJSCIE', 'MENU']
        self.__graphics = Graphics()
        self.__game = Game()

    def rules_loop(self, file):
        while not self.getCrashed():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.setCrashed(True)
                    self.terminate_game()
            self.screen.fill(colors["NIGHT_OF_NAVY"])
            self.menuButtons(self.__menuText[3], 40, self.getDisplayWidth() / 2 - self.__buttonSize[0] - 100,
                             self.getDisplayHeight() / 40, self.__buttonSize[0] - 100, self.__buttonSize[1],
                             colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], self.__menuText[3])
            self.__graphics.message_display('Zasady:', 50, self.getDisplayWidth() / 2, self.getDisplayHeight() / 20, colors["SUMMER_SUN"])
            i = 80
            with open(file, 'r') as text:
                lines = text.readlines()
                for line in lines:
                    line = line[0:len(line)-1]
                    if line != '\n':
                        self.__graphics.message_display(line, 12, self.getDisplayWidth() / 2, i, colors["SUMMER_SUN"])
                        i += 20
            pygame.display.update()
            self.clock.tick(15)

    def menuButtons(self, msg, msg_size, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            colour = ac
            if click[0] == 1 and action is not None:
                if action == self.__menuText[0]:
                    self.gameLoop()
                elif action == self.__menuText[1]:
                    self.rules_loop('rules.txt')
                elif action == self.__menuText[3]:
                    self.menuLoop()
                else:
                    self.terminate_game()
        else:
            colour = ic
        pygame.draw.rect(self.screen, colour, (x,y,w,h))
        smallText = pygame.font.Font("freesansbold.ttf", msg_size)
        textSurf, textRect = self.__graphics.text_objects(msg, smallText, colors["MUSTARD"])
        textRect.center = ((x + (w/2)), (y + (h/2))+5)
        self.screen.blit(textSurf, textRect)

    def menuLoop(self):
        while not self.getCrashed():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.setCrashed(True)
                    self.terminate_game()
            self.screen.fill(colors["NIGHT_OF_NAVY"])
            self.__graphics.message_display('Warcaby', 80, self.getDisplayWidth() / 2, self.getDisplayHeight() / 10, colors["SUMMER_SUN"])
            for i in range(200, 500, 100):
                    self.menuButtons(self.__menuText[int(i / 100) - 2], 60, self.getDisplayWidth() / 2 - self.__buttonSize[0] / 2,
                                     i, self.__buttonSize[0], self.__buttonSize[1],
                                     colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], self.__menuText[int(i / 100) - 2])
            pygame.display.update()
            self.clock.tick(15)

    def gameLoop(self):
        while self.__game.getBackMenu() is False:
            self.screen.fill(colors["NIGHT_OF_NAVY"])
            self.__game.eventLoopPvP()
        self.__game = Game()

    def terminate_game(self):
        pygame.quit()
        quit()


m = Menu()
m.menuLoop()

