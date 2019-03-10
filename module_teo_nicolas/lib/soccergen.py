import soccersimulator as soc
from utils.json import encode_json, decode_json

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

    def to_dict(self):
        return self.__dict__

if __name__ == "__main__":
    d = DiscretizedTerrain.getInstance()
    pos = soc.Vector2D(149, 89)
    print(d.FromPositionToCase(pos))
    encode_json(d.to_dict(), "test")
    data = decode_json("test")
    print(data["WIDTH"])