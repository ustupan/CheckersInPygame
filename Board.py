class Square:
    def __init__(self, color, occupant=None):
        self.color = color
        self.occupant = occupant

class Piece: #ewentualnie zrobic go basic i cos potem zmienic...
    def __init__(self, color, king=False):
        self.color = color
        self.king = king
        self.selected = False


class Board:
    def __init__(self):
        self.matrix = self.newBoard()

    def newBoard(self):
        matrix = [[Square('1') if ((x % 2 != 0) and (y % 2 == 0) or (x % 2 == 0) and (y % 2 != 0)) else Square('0') for x in range(8)] for y in range(8)]
        return matrix

    def initializePieces(self, test=None):
        """
        test == [d,e,f,g,h] special testing composition
        """
        if test == "d":
            pass  #tu dodac te ustawienia
        elif test == "e":
            pass #tu dodac te ustawienia
        elif test == "f":
            pass # tu dodac te ustawiania
        elif test == "g":
            pass #tu dodac te ustawiania
        elif test == "h":
            pass #tu dodac te ustawiania
        else:
            for x in range(8):
                for y in range(3):
                    if self.matrix[x][y].color == '1':
                        self.matrix[x][y].occupant = Piece('B')
                for y in range(5, 8):
                    if self.matrix[x][y].color == '1':
                        self.matrix[x][y].occupant = Piece('W')

#uwaga tu gdzies dodac wyjaki
    def blindLegalMoves(self, coord):
        (x, y) = coord
        if self.matrix[x][y].occupant is not None:
            if self.matrix[x][y].occupant.king is False and self.matrix[x][y].occupant.color == 'W':
                blindLegalMoves = [(x-1, y-1), (x+1, y-1)]
            elif self.matrix[x][y].occupant.king is False and self.matrix[x][y].occupant.color == 'B':
                blindLegalMoves = [(x-1, y+1), (x+1, y+1)]
            else:
                blindLegalMoves = [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
        else:
            blindLegalMoves = []
        return blindLegalMoves

#uwaga tu gdzies dodac wyjaki
    def legalMoves(self, coord, jump = False):
        (x, y) = coord
        legalMoves = []
        blindLegalMoves = self.blindLegalMoves(coord)
        if jump is False:
            for move in blindLegalMoves:
                if self.isOnBoard(move):
                    if self.location(move).occupant is None:
                        legalMoves.append(move)
                    elif (self.location(move).occupant.color != self.location((x, y)).occupant.color and
                          self.isOnBoard((move[0] + (move[0] - x), move[1] + (move[1] - y))) and
                          self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None):
                        legalMoves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
        else:
            for move in blindLegalMoves:
                if self.isOnBoard(move) and self.location(move).occupant is not None:
                    if (self.location(move).occupant.color != self.location((x, y)).occupant.color and
                            self.isOnBoard((move[0] + (move[0] - x), move[1] + (move[1] - y))) and
                            self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None):
                        legalMoves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
        return legalMoves

    def location(self, coord):
        (x, y) = coord
        return self.matrix[x][y]

    def isOnBoard(self, coord):
        (x, y) = coord
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        else:
            return True

    def removePiece(self, coord):
        (x, y) = coord
        self.matrix[x][y].occupant = None

    def movePiece(self, startCoord, endCoord):
        (start_x, start_y) = startCoord
        (end_x, end_y) = endCoord
        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.removePiece((start_x, start_y))
        self.king((end_x, end_y))


    def king(self, coord):
        (x, y) = coord
        if self.location((x, y)).occupant is not None:
            if (self.location((x, y)).occupant.color == 'W' and y == 0) or (self.location((x, y)).occupant.color == 'B' and y == 7): #ewentualnie tu szukac bledu!!!!
                self.location((x, y)).occupant.king = True