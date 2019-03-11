import soccersimulator as soc

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

    def FromPositionToCase(self, position):
        """
        Prend un Vector2D
        """
        x, y = position.x, position.y
        X = int(x / self.TAILLE_CASE_WIDTH)
        Y = int(y / self.TAILLE_CASE_HEIGHT)

        return (X, Y)

    def getDimension(self):
        return (self.NOMBRE_CASES_WIDTH, self.NOMBRE_CASES_HEIGHT)

    def AllPossibleCoords(self):
        coords = [(x, y) for x in range(self.NOMBRE_CASES_WIDTH) for y in range(self.NOMBRE_CASES_HEIGHT)]
        return coords