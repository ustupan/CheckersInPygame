import pygame

colors = {"SUMMER_SUN": (255, 196, 56),
          "BRIGHT_SUMMER_SUN": (255, 228, 196),
          "EARLY_ESPRESSO": (80, 57, 49),
          "MUSTARD": (205, 133, 63),
          "PACIFIC": (1, 128, 181),
          "BRIGHT_PACIFIC": (75, 198, 213),
          "BLACK": (19, 27, 29),
          "CHERRY": (165, 30, 44),
          "NIGHT_OF_NAVY": (33, 64, 95)
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


class Graphics(SetupWindow):
    def __init__(self):
        super().__init__()
        self.squareSize = (self.displayHeight/8)-8
        self.pieceSize = self.squareSize / 2
        self.message = False
        self.boardSize = self.squareSize * 8

    def drawBoardSquares(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].color == '1':
                    colour = colors["EARLY_ESPRESSO"]
                else:
                    colour = colors["MUSTARD"]
                pygame.draw.rect(self.screen, colour, (x * self.squareSize, y * self.squareSize + self.squareSize, self.squareSize, self.squareSize))

    def drawPieceCircles(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None:
                    if board.matrix[x][y].occupant.color == 'W':
                        colour = colors["SUMMER_SUN"]
                        pygame.draw.circle(self.screen, colour, (int(x * self.squareSize + self.pieceSize), int(y * self.squareSize + self.pieceSize + self.squareSize)), int(self.pieceSize))
                        if board.matrix[x][y].occupant.selected is True:
                            if board.location((x, y)).occupant.king is True:
                                self.message_display('[Bd]', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_SUMMER_SUN"])
                            else:
                                self.message_display('[B]', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_SUMMER_SUN"])
                        else:
                            if board.location((x, y)).occupant.king is True:
                                self.message_display('Bd', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_SUMMER_SUN"])
                            else:
                                self.message_display('B', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_SUMMER_SUN"])
                    else:
                        colour = colors["PACIFIC"]
                        pygame.draw.circle(self.screen, colour, (int(x * self.squareSize + self.pieceSize), int(y * self.squareSize + self.pieceSize + self.squareSize)), int(self.pieceSize))
                        if board.matrix[x][y].occupant.selected is True:
                            if board.location((x, y)).occupant.king is True:
                                self.message_display('[Cd]', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_PACIFIC"])
                            else:
                                self.message_display('[C]', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_PACIFIC"])
                        else:
                            if board.location((x, y)).occupant.king is True:
                                self.message_display('Cd', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_PACIFIC"])
                            else:
                                self.message_display('C', 30, x * self.squareSize + self.pieceSize, y * self.squareSize + self.pieceSize + self.squareSize, colors["BRIGHT_PACIFIC"])

    def text_objects(self,text,font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, text_size, text_orientation_w, text_orientation_h, color):
        menuText = pygame.font.Font('freesansbold.ttf', text_size)
        textSurf, textRect = self.text_objects(text, menuText, color)
        textRect.center = (text_orientation_w, text_orientation_h)
        self.screen.blit(textSurf, textRect)

    def boardCoord(self, coord):
        return int(coord[0]/self.squareSize), int(coord[1]/self.squareSize)-1
