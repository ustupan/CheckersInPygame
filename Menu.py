#MENU MODULE...

import pygame

colors = {"SUMMER_SUN": (255, 196, 56),
          "BRIGHT_SUMMER_SUN": (255, 228, 196),
          "EARLY_ESPRESSO": (80, 57, 49),
          "MUSTARD": (205, 133, 63),
          "BLACK": (19, 27, 29)
          }

class SetupWindow:
    def __init__(self):
        self.displayWidth = 800
        self.displayHeight = 600
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        pygame.display.set_caption("Checkers")
        self.crashed = False


class Menu(SetupWindow):
    def __init__(self):
        super().__init__()
        self.buttonSize = [300, 50]
        self.menuText = ['GRAJ', 'ZASADY', 'WYJSCIE', 'MENU']

    def text_objects(self,text,font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, text_size, text_orientation):
        menuText = pygame.font.Font('freesansbold.ttf', text_size)
        textSurf, textRect = self.text_objects(text, menuText, colors["SUMMER_SUN"])
        textRect.center = (self.displayWidth/2, text_orientation)
        self.screen.blit(textSurf, textRect)

    def rules_loop(self, file):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    self.terminate_game()
            self.screen.fill(colors["EARLY_ESPRESSO"])
            self.menuButtons(self.menuText[3],40, self.displayWidth/2-self.buttonSize[0]-100,
                             self.displayHeight/40, self.buttonSize[0]-100, self.buttonSize[1],
                             colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], self.menuText[3])
            self.message_display('Zasady:', 50, self.displayHeight/20)
            i = 80
            with open(file, 'r') as text:
                lines = text.readlines()
                for line in lines:
                    line = line[0:len(line)-1]
                    if line != '\n':
                        self.message_display(line, 12, i)
                        i += 20
            pygame.display.update()
            self.clock.tick(15)


    def menuButtons(self, msg, msg_size, x, y, w, h, ic, ac, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            colour = ac
            if click[0] == 1 and action != None:
                if action == self.menuText[0]:
                    pass # tu dodac moj game loop
                elif action == self.menuText[1]:
                    self.rules_loop('rules.txt')
                elif action == self.menuText[3]:
                    self.menuLoop()
                else:
                    self.terminate_game()

        else:
            colour = ic
        pygame.draw.rect(self.screen, colour, (x,y,w,h))
        smallText = pygame.font.Font("freesansbold.ttf", msg_size)
        textSurf, textRect = self.text_objects(msg, smallText, colors["MUSTARD"])
        textRect.center = ((x + (w/2)), (y + (h/2))+5)
        self.screen.blit(textSurf, textRect)

    def menuLoop(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    self.terminate_game()
            self.screen.fill(colors["EARLY_ESPRESSO"])
            self.message_display('Warcaby', 80, self.displayHeight/10)
            for i in range(200,500,100):
                self.menuButtons(self.menuText[int(i/100)-2], 60, self.displayWidth/2-self.buttonSize[0]/2,
                                 i, self.buttonSize[0], self.buttonSize[1],
                                 colors["SUMMER_SUN"], colors["BRIGHT_SUMMER_SUN"], self.menuText[int(i/100)-2])
            pygame.display.update()
            self.clock.tick(15)

    def terminate_game(self):
        pygame.quit()
        quit()


menu = Menu()
menu.menuLoop()









