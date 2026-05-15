import random
from typing import List,Dict,Any
from database.crude import set_target

def start_game(partipicants: List[Dict[str,Any]]):
    partip2 = partipicants.copy()
    random.shuffle(partip2)

    for i, p in enumerate(partip2):
        target = partip2[(i + 1) % len(partip2)]
        set_target(p['id'], target['id'])

