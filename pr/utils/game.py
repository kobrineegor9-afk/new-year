import random
from typing import List,Dict,Any
from database.crude import  set_target

def start_game(partipicants: List[Dict[str,Any]]):
    shuffled = partipicants.copy()
    random.shuffle(shuffled)

    for i, p in enumerate(shuffled):
        target = shuffled[(i + 1) % len(shuffled)]
        set_target(p['id'], target['id'])

