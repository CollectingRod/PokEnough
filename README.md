# PokEnough

I made this little script to try to find out how many packs someone would need to open to complete a Destined Rivals Complete Set. It also calculates how many packs a person would need to open before switching to singles.

## **DISCLAIMER**

This script is pretty scrappy and makes a lot of assumptions that are not true, but help make the problem more manageable. Those assumptions are as follow:

1. In a pack of 10 cards, all cards will be different.
2. In a pack of 10 cards, only the last card of the pack can be rare or higher.
3. Pull rates are an approximation, and have been obtained from TCG Player.
4. A complete set is defined as having one of each card, not counting holos and reverse holos. In other words, the result of this script refer to "Complete Sets" and not "Master Sets".

Besides that, my logic might be flawed! Please, feel free to make any corrections and submit a PR where we can discuss the change.

# How Does the Script Works?

This script runs multiple simulations of opening packs until all cards in the set have been pulled, and then provides a result based on the average of each of those simulations. It has three main stages.

## Pack Creation
1. Generate unique, numeric IDs for all cards in the set.
2. Based on those IDs and how many cards each type of rarity has, assign the correct number of unique IDs to each rarity bracket.
3. Include a fixed number of common/uncommon cards in a pack, and then, based on pull rate information for each rarity, fill the last slot of said pack. If none of the higher rarities have been selected, fall back to a 'rare' card.

## Complete Set Pack Calculation
Run N simulations that include:
1. Create packs.
2. 'Opening' packs and keep track of new cards, duplicates, packs that have been opened so far and how many cards have been drawn in total.
3. Keep running the simulation until all cards for all rarities have been pulled.
4. Return the amount of packs it took to obtain all the cards.
5. Compute the average of packs it takes to complete the set for all simulations.

## Packs Until Singles Calculation
For each simulation:
1. Calculate the observed probability in which any card from a new pack has a higher chance of being a duplicate than being new. I have set this probability threshold to 70%, meaning that if there is a 70% chance of a new card being a duplicate, at that point no more packs should be opened.
2. Compute the average number of packs it takes before switching to singles for all simulations. 

## Running the Script

The project doesn't use any external dependencies, and it should be able to run in most computers by running the following command in a terminal:

```
python pokenough.py
```

If this fails, try:

```
python3 pokenough.py
```

Bear in mind that by default, the project is running 1000 simulations, so it might take a while to finish. This can be modified in the `pokenough.py` file by changing the `SIMULATIONS` value.

After a few seconds, you should get a result similar to this (results may vary as this is a probabilistic process):

```
🎯 Average packs to complete full set: 3518.58
📈 Average packs until 80% prob. of duplicates: 59.12
```

If you are curious about other sets, you can also change the rarities and pull rates in `SET_CONFIG`.


## Contributing

Anyone is welcome to submit changes to the project.

The only condition for now, is to keep the code as simple as possible so that non-tech people can run it if they want to.

