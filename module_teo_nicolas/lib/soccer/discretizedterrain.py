import soccersimulator as soc
import random

class DiscretizedTerrain:
    terrain = None

    def __init__(self):
        """
        Singleton to get some data about the terrain such as its width, height, center, the goals etc.
        """
        self.WIDTH = soc.settings.GAME_WIDTH
        self.HEIGHT = soc.settings.GAME_HEIGHT

        self.NOMBRE_CASES_WIDTH = 2
        self.NOMBRE_CASES_HEIGHT = 2 

        self.TAILLE_CASE_WIDTH = self.WIDTH / self.NOMBRE_CASES_WIDTH
        self.TAILLE_CASE_HEIGHT = self.HEIGHT / self.NOMBRE_CASES_HEIGHT

    @staticmethod
    def getInstance():
        if not DiscretizedTerrain.terrain :
            DiscretizedTerrain.terrain = DiscretizedTerrain()
        return DiscretizedTerrain.terrain

    def clamp(self, value, mini, maxi):
        if value < mini :
            return mini

        if value > maxi :
            return maxi

        return value

    def FromPositionToCase(self, position):
        """
        Prend un Vector2D
        """
        x, y = position.x, position.y
        X = x // self.TAILLE_CASE_WIDTH
        Y = y // self.TAILLE_CASE_HEIGHT

        X = self.clamp(X, 0, self.NOMBRE_CASES_WIDTH - 1)
        Y = self.clamp(Y, 0, self.NOMBRE_CASES_HEIGHT - 1)

        return (int(X), int(Y))

    def FromCaseToPosition(self, case_coord):
        x, y = case_coord
        assert x >= 0 and x < self.NOMBRE_CASES_WIDTH
        assert y >= 0 and y < self.NOMBRE_CASES_HEIGHT

        minX = self.TAILLE_CASE_WIDTH * x
        minY = self.TAILLE_CASE_HEIGHT * y

        maxX = minX + self.TAILLE_CASE_WIDTH - 1
        maxY = minY + self.TAILLE_CASE_HEIGHT - 1

        X = random.uniform(minX, maxX)
        Y = random.uniform(minY, maxY)

        return soc.Vector2D(X, Y)
        

    def getDimension(self):
        return (self.NOMBRE_CASES_WIDTH, self.NOMBRE_CASES_HEIGHT)

    def AllPossibleCoords(self):
        coords = [(x, y) for x in range(self.NOMBRE_CASES_WIDTH) for y in range(self.NOMBRE_CASES_HEIGHT)]
        return coords


if __name__ == "__main__":
    d = DiscretizedTerrain.getInstance()
    coords = d.AllPossibleCoords()
    for coord in coords :
        print(d.FromCaseToPosition(coord))