from mineral import minerals
class Ore(object):
    def __init__(self, name: str, price: float, minerals: dict):
        self.name = name
        self.price = price
        self.minerals = minerals
        self.value = self.compute_minerals_value()

    def __repr__(self):
        return (f"{self.name}: price: {self.price}; minerals: {self.minerals}, "
                f"minerals value: {self.value}, times: {self.value/self.price}")

    def compute_minerals_value(self):
        value = 0
        for m,n in self.minerals.items():
            value += n*minerals[m]
        return value


    # def __str__(self):
    #     return f"{}"

# None means less store
fjs = Ore("fjs", 500, {"sthj": 249})
zsy = Ore("zsy", 600, {"sthj": 97.2, "ljtjk": 69})
xcy = Ore("xcy", 1800, {"sthj": 30.6, "ljtjk": 39, "lycjs": 58.2})
abes = {"sthj": 306, "ljtjk": 38.76, "tljht": 28.05}
sps = {"sthj": 136, "lycjs": 245, "tljht": 24.48}
gjy = {"sthj": 30.6, "ljtjk": 39, "lycjs": 58.2, "cxxnks": 15.3}
hzs = {"sthj": 30.6, "tljht": 24.48, "cxxnks": 15.3}
jsbk = None
xmft = None
twyk = None
hy = None
if __name__ == "__main__":
    print(fjs)
    print(zsy)
    print(xcy)