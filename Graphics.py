import pygame
from Board import King

colors = {"SUMMER_SUN": (255, 196, 56),
          "BRIGHT_SUMMER_SUN": (255, 228, 196),
          "EARLY_ESPRESSO": (80, 57, 49),
          "MUSTARD": (205, 133, 63),
          "PACIFIC": (1, 128, 181),
          "BRIGHT_PACIFIC": (75, 198, 213),
          "BLACK": (19, 27, 29),
          "CHERRY": (165, 30, 44),
          "NIGHT_OF_NAVY": (33, 64, 95),
          "GREEN": (197, 244, 66)
          }


class SetupWindow:
    def __init__(self):
        self.__displayWidth = 800
        self.__displayHeight = 600
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.__displayWidth, self.__displayHeight))
        pygame.display.set_caption("Checkers")
        self.__crashed = False

    def getDisplayHeight(self):
        return self.__displayHeight

    def getDisplayWidth(self):
        return self.__displayWidth

    def setCrashed(self, value):
        self.__crashed = value

    def getCrashed(self):
        return self.__crashed


class Graphics(SetupWindow):
    def __init__(self):
        super().__init__()
        self.__squareSize = (self.getDisplayHeight() / 8) - 8
        self.__pieceSize = self.__squareSize / 2
        self.__message = False
        self.__boardSize = self.__squareSize * 8

    def getBoardSize(self):
        return self.__boardSize

    def drawBoardSquares(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].color == '1':
                    colour = colors["EARLY_ESPRESSO"]
                else:
                    colour = colors["MUSTARD"]
                pygame.draw.rect(self.screen, colour, (x * self.__squareSize, y * self.__squareSize + self.__squareSize, self.__squareSize, self.__squareSize))

    def highlightMoves(self, moves):
        for x in range(8):
            for y in range(8):
                if (x, y) in moves:
                    pygame.draw.rect(self.screen, colors['GREEN'], (x * self.__squareSize, y * self.__squareSize + self.__squareSize, self.__squareSize, self.__squareSize))

    def drawPieceCircles(self, board):
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant is not None:
                    if board.matrix[x][y].occupant.color == 'W':
                        colour = colors["SUMMER_SUN"]
                        pygame.draw.circle(self.screen, colour, (int(x * self.__squareSize + self.__pieceSize), int(y * self.__squareSize + self.__pieceSize + self.__squareSize)), int(self.__pieceSize))
                        if board.matrix[x][y].occupant.selected is True:
                            if isinstance(board.location((x, y)).occupant, King) is True:
                                self.message_display('[Bd]', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_SUMMER_SUN"])
                            else:
                                self.message_display('[B]', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_SUMMER_SUN"])
                        else:
                            if isinstance(board.location((x, y)).occupant, King) is True:
                                self.message_display('Bd', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_SUMMER_SUN"])
                            else:
                                self.message_display('B', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_SUMMER_SUN"])
                    else:
                        colour = colors["PACIFIC"]
                        pygame.draw.circle(self.screen, colour, (int(x * self.__squareSize + self.__pieceSize), int(y * self.__squareSize + self.__pieceSize + self.__squareSize)), int(self.__pieceSize))
                        if board.matrix[x][y].occupant.selected is True:
                            if isinstance(board.location((x, y)).occupant, King) is True:
                                self.message_display('[Cd]', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_PACIFIC"])
                            else:
                                self.message_display('[C]', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_PACIFIC"])
                        else:
                            if isinstance(board.location((x, y)).occupant, King) is True:
                                self.message_display('Cd', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_PACIFIC"])
                            else:
                                self.message_display('C', 30, x * self.__squareSize + self.__pieceSize, y * self.__squareSize + self.__pieceSize + self.__squareSize, colors["BRIGHT_PACIFIC"])

    def text_objects(self,text,font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, text_size, text_orientation_w, text_orientation_h, color):
        menuText = pygame.font.Font('freesansbold.ttf', text_size)
        textSurf, textRect = self.text_objects(text, menuText, color)
        textRect.center = (text_orientation_w, text_orientation_h)
        self.screen.blit(textSurf, textRect)

    def boardCoord(self, coord):
        return int(coord[0] / self.__squareSize), int(coord[1] / self.__squareSize) - 1
