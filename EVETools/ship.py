from EVETools.ore import Ore
from mineral import minerals
from planet_material import pm
from ore import fjs, zsy, xcy


class Ship(object):
    def __init__(self, name: str, price: float, minerals: dict, pm: dict, blueprint: float):
        self.name = name
        self.price = price

        self.minerals = minerals
        self.pm = pm
        self.blueprint = blueprint

        self.cost_minerals = self.compute_cost_minerals()
        self.cost_pm = self.compute_cost_pm()
        self.cost_blueprint = self.blueprint

        self.cost = self.cost_minerals + self.cost_pm + self.cost_blueprint

    def __repr__(self):
        return (f"{self.name}: price: {self.price}, cost: {self.cost}, profit: {self.price - self.cost};\n"
                f"minerals cost: {self.cost_minerals}, planet materials cost {self.cost_pm}, "
                f"blueprint cost {self.cost_blueprint};\n"
                f"minerals: {self.minerals};\nplanet materials: {self.pm}")

    def compute_cost_minerals(self):
        cost = 0
        for m, n in self.minerals.items():
            cost += n * minerals[m]
        return cost

    def compute_cost_pm(self):
        cost = 0
        for m, n in self.pm.items():
            cost += n * pm[m]
        return cost

    def compute_cost_ore(self, ores_priority: list[Ore], minerals_priority: list[str] = None):
        minerals_cache = self.minerals.copy()
        ores_num = {}
        cost = 0

        if minerals_priority is None:
            minerals_priority = minerals.keys()
            minerals_priority = list(minerals_priority)
            minerals_priority.reverse()

        for mineral in minerals_priority:
            candidates = []
            for ore in ores_priority:
                if mineral in ore.minerals:
                    candidates.append(ore)
            if len(candidates) > 0:
                selected_ore = candidates[0]
                ms = selected_ore.minerals
                num = minerals_cache[mineral]/ms[mineral]
                cost += num*selected_ore.price
                ores_num[selected_ore.name] = num
                for m, n in ms.items():
                    if m in minerals_cache:
                        minerals_cache[m] -= num * n
                # print(minerals_cache)
                pop_cache = []
                for k, r in minerals_cache.items():
                    if r <= 0:
                        pop_cache.append(k)
                for k in pop_cache:
                    minerals_cache.pop(k)
                print(minerals_cache)
                ores_priority.remove(selected_ore)
            # print(ores_priority)

        for m, n in minerals_cache.items():
            cost += n * minerals[m]
        for m, n in self.pm.items():
            cost += n * pm[m]
        cost += self.blueprint
        return cost, ores_num





nhjhjx = Ship("nhjhjx", 135000000 * 0.87,
              {"sthj": 1618709, 'ljtjk': 458816, 'lycjs': 143813, 'twjht': 24589, 'cxxnks': 5856},
              {'sghj': 8801, 'gzhj': 8745, 'dyfhw': 9972, 'gjs': 9972, 'fyjs': 2480}, 10000000)

jnjswx = Ship("jnjswx", 180000000 * 0.87,
              {"sthj": 4043965, 'ljtjk': 1031413, 'lycjs': 340964, 'twjht': 53003, 'cxxnks': 14427,'jzsyhy':5094},
              {'sghj': 12062, 'jmhj': 10709, 'dyfhw': 13666, 'gjs': 13666, 'fyjs': 3399}, 10000000)


# good > 2000
hnjynx = Ship("nhjhjx", 280000000 * 0.87,
              {"sthj": 3980447, 'ljtjk': 1015212, 'lycjs': 335609, 'twjht': 52171, 'cxxnks': 14201,'jzsyhy':5015},
              {'sghj': 11873, 'jmhj': 10541, 'dyfhw': 13452, 'gjs': 13452, 'fyjs': 3345}, 20000000)
jnj = Ship("jnj", 140000000 * 0.87,
              {"sthj": 1590353, 'ljtjk': 450779, 'lycjs': 141294, 'twjht': 24159, 'cxxnks': 5754},
              {'sghj': 8647, 'gzhj': 8592, 'dyfhw': 9797, 'gjs': 9797, 'fyjs': 2436}, 10000000)
if __name__ == "__main__":
    ores_priority = [xcy,zsy,fjs]
    minerals_priority = ['lycjs','ljtjk','sthj']
    print(nhjhjx)
    print(nhjhjx.compute_cost_ore(ores_priority.copy(), minerals_priority.copy()))
    print(jnjswx)
    print(jnjswx.compute_cost_ore(ores_priority.copy(), minerals_priority.copy()))
    print(jnj)
    print(jnj.compute_cost_ore(ores_priority.copy(), minerals_priority.copy()))
