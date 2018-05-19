class Square:
    def __init__(self, color, occupant=None):
        self.color = color
        self.occupant = occupant


class Piece:
    def __init__(self):
        self.color = None
        self.selected = False


class BasicPiece(Piece):
    def __init__(self, color):
        super().__init__()
        self.color = color


class King(Piece):
    def __init__(self, color):
        super().__init__()
        self.color = color


class Board:
    def __init__(self):
        self.matrix = self.newBoard()
        self.jumpAvailablePieces = []
        self.jump = []

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
            self.matrix[4][1].occupant = BasicPiece('W')
            self.matrix[0][1].occupant = BasicPiece('B')
            self.matrix[1][2].occupant = BasicPiece('B')
            self.matrix[2][3].occupant = BasicPiece('B')
            self.matrix[3][4].occupant = BasicPiece('B')
            self.matrix[3][2].occupant = BasicPiece('B')
            self.matrix[2][1].occupant = BasicPiece('B')
            self.matrix[4][3].occupant = BasicPiece('B')
            #pass # tu dodac te ustawiania
        elif test == "g":
            self.matrix[4][1].occupant = BasicPiece('W')
            self.matrix[4][5].occupant = BasicPiece('B')
            self.matrix[6][5].occupant = BasicPiece('B')
            #self.matrix[5][2].occupant = BasicPiece('B')
            self.matrix[2][5].occupant = BasicPiece('B')
            self.matrix[2][3].occupant = BasicPiece('B')
            self.matrix[4][3].occupant = BasicPiece('B')

        elif test == "h":
            for x in range(8):
                for y in range(3):
                    if self.matrix[x][y].color == '1':
                        self.matrix[x][y].occupant = BasicPiece('B')
        else:
            for x in range(8):
                for y in range(3):
                    if self.matrix[x][y].color == '1':
                        self.matrix[x][y].occupant = BasicPiece('B')
                for y in range(5, 8):
                    if self.matrix[x][y].color == '1':
                        self.matrix[x][y].occupant = BasicPiece('W')

    def blindLegalMoves(self, coord):  #uwaga tu gdzies dodac wyjaki
        (x, y) = coord
        blindLegalMoves = []
        if self.matrix[x][y].occupant is not None and isinstance(self.location((x, y)).occupant, King) is False:
            blindLegalMoves = [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]
        elif self.matrix[x][y].occupant is not None and isinstance(self.location((x, y)).occupant, King) is True:
            blindLegalMoves.extend([(x - i, y - i) for i in range(1, 8) if self.isOnBoard((x - i, y - i))])
            blindLegalMoves.extend([(x + i, y - i) for i in range(1, 8) if self.isOnBoard((x + i, y - i))])
            blindLegalMoves.extend([(x - i, y + i) for i in range(1, 8) if self.isOnBoard((x - i, y + i))])
            blindLegalMoves.extend([(x + i, y + i) for i in range(1, 8) if self.isOnBoard((x + i, y + i))])
        return blindLegalMoves

    def legalMoves(self, coord, jump=False): #uwaga tu gdzies dodac wyjaki
        (x, y) = coord
        legalMoves = []
        tempLegalMoves = []
        state = None
        blindLegalMoves = self.blindLegalMoves(coord)
        if jump is False: #and isinstance(self.location((x, y)).occupant, King) is False
            for move in blindLegalMoves:
                if self.isOnBoard(move):
                    if self.location(move).occupant is None and isinstance(self.location((x, y)).occupant, King) is False:
                        if self.location((x, y)).occupant.color == 'W' and move in [(x-1, y-1), (x+1, y-1)]:
                            legalMoves.append(move)
                        elif self.location((x, y)).occupant.color == 'B' and move in [(x-1, y+1), (x+1, y+1)]:
                            legalMoves.append(move)
                    elif (self.location(move).occupant is None and isinstance(self.location((x, y)).occupant, King) is True
                            and self.checkColision(coord, move) is None):
                        legalMoves.append(move)
                    elif (self.location(move).occupant is not None and self.location(move).occupant.color != self.location((x, y)).occupant.color and #bicie pionami
                            self.isOnBoard((move[0] + (move[0] - x), move[1] + (move[1] - y))) and
                            self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None
                            and isinstance(self.location((x, y)).occupant, King) is False):
                        state = 1
                        self.jump.append((x, y))
                        tempLegalMoves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
                    elif isinstance(self.location((x, y)).occupant, King) and self.checkColision(coord, move):
                        colisionPiece = self.checkColision(coord, move)
                        if self.checkDirection(coord, move) == "SOUTHEAST":
                            if self.isOnBoard((colisionPiece[0]+1, colisionPiece[1]+1)) and self.location((colisionPiece[0]+1, colisionPiece[1]+1)).occupant is None:
                                if self.location((colisionPiece[0], colisionPiece[1])).occupant.color != self.location((x, y)).occupant.color:
                                    state = 1
                                    self.jump.append((x, y))
                                    tempLegalMoves.append((colisionPiece[0]+1, colisionPiece[1]+1))
                        elif self.checkDirection(coord, move) == "SOUTHWEST":
                            if self.isOnBoard((colisionPiece[0]-1, colisionPiece[1]+1)) and self.location((colisionPiece[0]-1, colisionPiece[1]+1)).occupant is None:
                                if self.location((colisionPiece[0], colisionPiece[1])).occupant.color != self.location((x, y)).occupant.color:
                                    state = 1
                                    self.jump.append((x, y))
                                    tempLegalMoves.append((colisionPiece[0]-1, colisionPiece[1]+1))
                        elif self.checkDirection(coord, move) == "NORTHEAST":
                            if self.isOnBoard((colisionPiece[0]+1, colisionPiece[1]-1)) and self.location((colisionPiece[0]+1, colisionPiece[1]-1)).occupant is None:
                                if self.location((colisionPiece[0], colisionPiece[1])).occupant.color != self.location((x, y)).occupant.color:
                                    state = 1
                                    self.jump.append((x, y))
                                    tempLegalMoves.append((colisionPiece[0]+1, colisionPiece[1]-1))
                        else:
                            if self.isOnBoard((colisionPiece[0]-1, colisionPiece[1]-1)) and self.location((colisionPiece[0]-1, colisionPiece[1]-1)).occupant is None:
                                if self.location((colisionPiece[0], colisionPiece[1])).occupant.color != self.location((x, y)).occupant.color:
                                    state = 1
                                    self.jump.append((x, y))
                                    tempLegalMoves.append((colisionPiece[0]-1, colisionPiece[1]-1))
        else:
            if isinstance(self.location((x, y)).occupant, King) is False:
                for move in blindLegalMoves:
                    if self.isOnBoard(move) and self.location(move).occupant is not None:
                        if self.location(move).occupant.color != self.location((x, y)).occupant.color and self.isOnBoard((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None:
                            legalMoves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
            else:
                for move in [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]:
                    if self.isOnBoard(move) and self.location(move).occupant is not None:
                        if self.location(move).occupant.color != self.location((x, y)).occupant.color and self.isOnBoard((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant is None:
                            legalMoves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        if state == 1:
            return tempLegalMoves
        else:
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

    def adjacent(self, coord):
        (x, y) = coord
        return [(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]

    def removePiece(self, coord):
        (x, y) = coord
        self.matrix[x][y].occupant = None

    def movePiece(self, startCoord, endCoord):
        (start_x, start_y) = startCoord
        (end_x, end_y) = endCoord
        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.removePiece((start_x, start_y))
        self.king((end_x, end_y))

    def jumpAvailable(self, color):
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].color == '1' and self.matrix[x][y].occupant is not None and self.matrix[x][y].occupant.color == color:
                    self.legalMoves((x, y))
                    for hop in self.jump:
                        if hop not in self.jumpAvailablePieces:
                            self.jumpAvailablePieces.append(hop)

    def checkDirection(self, startCoord, moveCoord):
        (start_x, start_y) = startCoord
        (move_x, move_y) = moveCoord
        if start_y < move_y:
            if start_x < move_x:
                return "SOUTHEAST"
            else:
                return "SOUTHWEST"
        else:
            if start_x < move_x:
                return "NORTHEAST"
            else:
                return "NORTHWEST"

    def checkColision(self, startCoord, moveCoord):
        (start_x, start_y) = startCoord
        (move_x, move_y) = moveCoord
        moves = []
        direction = self.checkDirection(startCoord, moveCoord)
        if direction == "SOUTHEAST":
            while True:
                start_x += 1
                start_y += 1
                moves.append((start_x, start_y))
                if (start_x, start_y) == (move_x, move_y):
                    break
            for move in moves:
                if self.location(move).occupant is not None:
                    return move
        elif direction == "SOUTHWEST":
            while True:
                start_x -= 1
                start_y += 1
                moves.append((start_x, start_y))
                if (start_x, start_y) == (move_x, move_y):
                    break
            for move in moves:
                if self.location(move).occupant is not None:
                    return move
        elif direction == "NORTHEAST":
            while True:
                start_x += 1
                start_y -= 1
                moves.append((start_x, start_y))
                if (start_x, start_y) == (move_x, move_y):
                    break
            for move in moves:
                if self.location(move).occupant is not None:
                    return move
        elif direction == "NORTHWEST":
            while True:
                start_x -= 1
                start_y -= 1
                moves.append((start_x, start_y))
                if (start_x, start_y) == (move_x, move_y):
                    break
            for move in moves:
                if self.location(move).occupant is not None:
                    return move
        return None

    def king(self, coord):
        (x, y) = coord
        if self.location((x, y)).occupant is not None:
            if (self.location((x, y)).occupant.color == 'W' and y == 0) or (self.location((x, y)).occupant.color == 'B' and y == 7): #ewentualnie tu szukac bledu!!!!
                color = self.location((x, y)).occupant.color
                self.location((x, y)).occupant = King(color)
