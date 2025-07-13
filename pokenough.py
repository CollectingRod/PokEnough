import random
from collections import defaultdict

SET_CONFIG = {
    'cards_in_set': 244,
    'cards_per_pack': 10,
    'rarities_in_set': {
        'Common': 85,
        'Uncommon': 62,
        'Rare': 18,
        'Double Rare': 17,
        'Ultra Rare': 22,
        'Illustration Rare': 23,
        'Special Illustration Rare': 11,
        'Hyper Rare': 6,
    },
    'final_card_slot_probabilities': {
        'Hyper Rare': 1 / 149,
        'Special Illustration Rare': 1 / 94,
        'Ultra Rare': 1 / 16,
        'Illustration Rare': 1 / 12,
        'Double Rare': 1 / 5,
        'Rare': 1.0,  # Fallback if no other rarity is rolled
    },
    'fixed_card_slots': {
        'Common': 5,
        'Uncommon': 4
    }
}

SIMULATIONS = 1000

def generate_rarity_card_id_ranges() -> dict:
    """
    Card IDs go from 0 to total_cards_in_set - 1.
    Each rarity has a range of IDs based on the number of cards in that rarity.
    """
    rarity_ranges = {}
    start_id = 0
    for rarity, count in SET_CONFIG['rarities_in_set'].items():
        rarity_ranges[rarity] = (start_id, start_id + count)
        start_id += count
    return rarity_ranges

def roll_final_slot(rarity_id_ranges: dict) -> tuple:
    """
    Roll for the final slot in a booster pack based on defined probabilities.
    The roll will start with the highest rarity and work downwards.
    If no other rarity is rolled, it defaults to Rare.
    """
    for rarity, prob in SET_CONFIG['final_card_slot_probabilities'].items():
        if random.random() < prob:
            card_id = random.choice(range(*rarity_id_ranges[rarity]))
            return (rarity, card_id)

    # Fallback to Rare
    rare_id = random.choice(range(*rarity_id_ranges['Rare']))
    return ('Rare', rare_id)

def generate_pack(rarity_id_ranges: dict) -> list:
    """
    Generate a booster pack containing a fixed number of cards based on rarity.
    The pack will contain a fixed number of certain rarities and one final card
    that can be Rare or better.
    """
    pack = []

    for rarity, count in SET_CONFIG['fixed_card_slots'].items():
        # Generate fixed number of cards for each rarity
        card_ids = random.sample(range(*rarity_id_ranges[rarity]), count)
        pack += [(rarity, cid) for cid in card_ids]

    # Final slot (rare or better)
    pack.append(roll_final_slot(rarity_id_ranges))

    return pack

# --- Simulate collection and track stats ---
def simulate_collection():
    """
    Simulate the collection of cards from booster packs until the full set is completed.
    Also track the number of packs opened until the probability of drawing duplicates
    is greater than 80%.
    """

    collection = defaultdict(set)
    seen_cards = set()
    total_cards_drawn = 0
    duplicate_cards = 0
    packs_opened = 0
    packs_until_duplicate_prob_surpassed = None
    rarity_id_ranges = generate_rarity_card_id_ranges()

    while True:
        pack = generate_pack(rarity_id_ranges)
        packs_opened += 1
        for card in pack:
            total_cards_drawn += 1
            if card in seen_cards:
                duplicate_cards += 1
            else:
                seen_cards.add(card)
                collection[card[0]].add(card[1])

        completed = all(len(collection[rarity]) == SET_CONFIG["rarities_in_set"][rarity] for rarity in SET_CONFIG['rarities_in_set'])
        if completed:
            break

        if packs_until_duplicate_prob_surpassed is None:
            if duplicate_cards / total_cards_drawn > 0.7:
                packs_until_duplicate_prob_surpassed = packs_opened

    return packs_opened, packs_until_duplicate_prob_surpassed

###################
# RUN SIMULATIONS #
###################

packs_to_complete = []
packs_to_duplicate_dominance = []

for _ in range(SIMULATIONS):
    complete_packs, dup_packs = simulate_collection()
    packs_to_complete.append(complete_packs)
    if dup_packs is not None:
        packs_to_duplicate_dominance.append(dup_packs)

# --- Results ---
avg_complete = sum(packs_to_complete) / len(packs_to_complete)
avg_dup_dominance = sum(packs_to_duplicate_dominance) / len(packs_to_duplicate_dominance)

print(f"🎯 Average packs to complete full set: {avg_complete:.2f}")
print(f"📈 Average packs until 70% prob. of duplicates: {avg_dup_dominance:.2f}")
