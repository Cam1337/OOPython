class TileValues(object):
    def __init__(self):
        self.values = {
            "a":1,
            "e":1,
            "i":1,
            "l":1,
            "n":1,
            "o":1,
            "r":1,
            "s":1,
            "t":1,
            "u":1,
            
            "d":2,
            "g":2,
            
            "b":3,
            "c":3,
            "m":3,
            "p":3,
            
            "f":4,
            "h":4,
            "v":4,
            "w":4,
            "y":4,
            
            "k":5,
            
            "j":8,
            "x":8,
            
            "q":10,
            "z":10
            }
    
    def get(self, letter):
        return self.values.get(letter.lower(),0)

class ScrabbleBoard(object):
    def __init__(self, allowNeighbors):
        self.allowNeighbors = allowNeighbors
        self.tileScores = TileValues()
        self.multipliers = [
                "500200050002005",
                "040003000300040",
                "004000202000400",
                "200400020004002",
                "000040000040000",
                "030003000300030",
                "002000202000200",
                "500200040002005",
                "002000202000200",
                "030003000300030",
                "000040000040000",
                "200400020004002",
                "004000202000400",
                "040003000300040",
                "500200050002005"]
                
        self.values = [
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ', 
                '               ']
        
        self.tileOwners = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                    
        
    def display(self):
        """
        Print out the board in a human readable way :)
        """
        for tileRow in range(len(self.multipliers)):
            scoresRow = self.multipliers[tileRow]
            valuesRow = self.values[tileRow]
            line = "|"
            for score,value in zip(scoresRow, valuesRow):
                line += "{0} ".format(value)
            print line + "|"

    def getLetterScore(self, coordinate, player):
        """
        ]coordinate = (x,y) coordinates (tuple)
        ]player = player object (player class)
        Return the value for one tile on any given space. 
        Calculates tile's value and any multiplier on the space below it. 
        Does not calculate word multipliers.
        """
        x,y = coordinate
        
        value = self.getLetterValue(coordinate)
        
        multiplier = int(self.multipliers[y][x])
        tileScore  = self.tileScores.get(value)
        
        if multiplier in [2,3]:
            return tileScore * multiplier
        return tileScore
        
    def getLetterValue(self, coordinate):
        """
        ]coordinate = (x,y) coordinates (tuple)
        Return the letter of the tile for a given x,y coordinate.
        """
        x,y = coordinate        
        value = self.values[y][x]
        return value
    
    def setValue(self, coordinate, value, player):
        """
        ]coordinate = (x,y) coordinates (tuple)
        ]value = letter of tile (string)
        ]player = player object (player class)
        Set the value of a given coordinate and store which player "played" that tile.
        """
        x,y = coordinate
        if self.values[y][x] != " ":
            return False
        self.values[y] = self.values[y][:x] + value + self.values[y][x+1:]
        self.tileOwners[y][x] = player
        return True
        #return self.getLetterScore(coordinate, player)
    
    def getPathFromCoordinates(self, x0, y0, x1, y1):
        """
        Python Bresehnam's Line Algorithm implementation
        Computationally this algorithm is built for computers
        """
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0,y0,x1,y1 = y0,x0,y1,x1

        if x0 > x1:
            x0,x1, y0, y1 = x1, x0, y1, y0

        ystep = [-1,1][y0 < y1]


        dx = x1 - x0
        dy = abs(y1 - y0)
        error = -dx / 2
        y = y0

        path = []    
        for x in range(x0, x1 + 1):
            if steep: path.append((y,x))
            else:     path.append((x,y))

            error = error + dy
            if error > 0:
                y = y + ystep
                error = error - dx
        return path
        
    def checkValidWord(self, word):
        """
        Implement this if you want to include a dictionary to check for word validity.
        """
        return True
    
    def checkNeighbors(self, path):
        if self.allowNeighbors:
            return True
        createNine = lambda x,y: [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
        for x,y in path:
            if self.values[y][x] != " ":
                continue
            surrounding = createNine(x,y)
            surrounding = [coord for coord in surrounding if coord not in path]
            for x2,y2 in surrounding:
                if self.values[y2][x2] != " ":
                    return False
        return True
        
    def canPlaceWord(self, word, start, end):
        """
        Runs a series of tests against the word and coordinates and proposed playing line.
        If the word does not pass every single test, it will not be played.
        - Test 1: are all of the coordinates in the board's limits?
        - Test 2: is the range of coordinates equal to the length of the word?
        - Test 3: are the coordinates given integers? (whole numbers)
        - Test 4: are we dealing with a straight line? (do the coords suggest a diagonal)
        - Test 5: are all of the places we are going to put tiles free or overlapping letters?
        - Test 6: are we allowing neighbors? -> if not, check that there are no bad neighbors.
        """
        isdgt = lambda i: str(i).isdigit()
        sx,sy = start
        ex,ey = end
        lw1   = len(word) - 1 # coordinates are offset by -1
        
        test1 = ((-1 < ex < 16) and (-1 < ey < 16) and (-1 < sx < 16) and (-1 < sy < 16))
        test2 = (abs(ex - sx) == lw1 or abs(ey - sy) == lw1)
        test3 = (isdgt(ex) and isdgt(ey) and isdgt(sx) and isdgt(sy))
        test4 = (ey == sy or ex == sx)
        
        if not test2: return False
        
        tilePath = self.getPathFromCoordinates(sx,sy,ex,ey)
        tileSafe = [self.values[v[1]][v[0]] in [" ",word[i]] for i,v in enumerate(tilePath)]

        test5 = all(tileSafe)
        
        test6 = self.checkNeighbors(tilePath)
        
        # return true if all of the tests are passed
        return test1 and test2 and test3 and test4 and test5 and test6
        
        
    def setWord(self, word, start, end, player):
        """
        ]word = word to play (string)
        ]start = (x,y) coordinate (tuple)
        ]end = (x,y) coordinate (tuple)
        ]player = player object (player class)
        Main word playing logic. Includes safeguards:
            - Word too long
            - Tiles in the way
            - Is a valid word [dictionary not implemented]
        """
        _wordScore = 0
        wordMultipliers = []
        
        # This is where the main logic for adding words is
        if (self.canPlaceWord(word,start,end) and self.checkValidWord(word)):
            path = self.getPathFromCoordinates(start[0], start[1], end[0], end[1])
            for letter,coord in zip(word,path):
                didSet = self.setValue(coord,letter,player)
                if didSet: # Are we using someone elses letter or what?
                    possibleWordMult = int(self.multipliers[coord[1]][coord[0]])
                    if possibleWordMult != 0 and possibleWordMult not in [2,3]:
                        wordMultipliers.append(int(self.multipliers[coord[1]][coord[0]]))
                    _wordScore += self.getLetterScore(coord, player)
            for mult in wordMultipliers:
                _wordScore = _wordScore * {5:3,4:2}[mult]
            player.addScore(word, _wordScore)
            print "[+]Word '{0}' played by {2} for {1} points.".format(word, _wordScore, player.name)
        else:
            print "[-]Word '{0}' unable to be played by {1}".format(word, player.name)

class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hash = hash(self)
        self.words = []
        self.scores = []
    def addScore(self, word, score):
        self.words.append(word)
        self.scores.append(score)
        self.score += score
    def __repr__(self):
        return self.name



def playGame():
    player1 = Player("John")
    player2 = Player("Elisa")
    
    scorePrint = lambda pl: "{0}'s score is {1} with {2} words played.".format(pl.name, pl.score, len(pl.words))
    
    board = ScrabbleBoard(allowNeighbors=False)
    
    board.setWord("corn",  (4,5),(7,5),  player1)
    board.setWord("porn",  (4,4),(7,4), player1)
    board.setWord("pants", (7,3),(7,7),  player2)
    board.setWord("star",  (7,7),(10,7), player1)
    board.setWord("apple", (9,7),(9,11), player2)
    board.setWord("airplane", (2,11),(9,11), player1)
    
    board.display()
    
    print scorePrint(player1)
    print scorePrint(player2)
    
    

if __name__ == "__main__":
    playGame()