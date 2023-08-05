# Fast Python Seven Card Hand Evaluation

Hand evaluator for 7 card hands using a 512kb lookup table (2^18 shorts).
An evaluation consists of calculating the index plus a single lookup.
This is a Python port of the 7 card hand evaluator used by 
[Hold\'em Resources Calculator](https://www.holdemresources.net/]).


## Installation
The library can be installed straight from [PyPI](https://pypi.org/).

```
pip install sval
``` 

The only dependencies are `numpy` and `numba` and the library should work 
with all Python versions >= 3.6.

## Hand format:
The evaluation methods take a single long to represent the hand using the
lowest 52 bits.

bits 0-3: 2s2h2d2c
bits 4-7: 3s3h3d3c
etc.

The library supports encoding strings such as '2s2h' as longs. However,
avoid using all encoding/decoding methods for performance critical code and 
work with the longs directly.

```python
>>> import sval
>>> sval.encode_cards('2s2h')
12
>>> sval.cards_to_string(12)
'2s2h'
``` 

This allows to check for board collision or to combine cards with simple bit 
arithmetic.

```python
>>> sval.cards_to_string(sval.encode_cards('2s2h') & sval.encode_cards('2hAs'))
'2h'
>>> sval.cards_to_string(sval.encode_cards('2s2h') | sval.encode_cards('2hAs'))
'As2s2h'
``` 

## Seven Card Evaluation
Given a set of seven cards, we can lookup it's rank by calculating it's index.
Higher ranks are better.

```python
>>> hand_1 = sval.encode_cards('As5h')
>>> hand_2 = sval.encode_cards('Ad2d')
>>> board_1 = sval.encode_cards('Ah3d5hTsKd')
>>> value_1 = sval.calculate_index(hand_1 | board_1)
>>> value_2 = sval.calculate_index(hand_2 | board_1)
>>> sval.rank_lookup[value_1]
4117
>>> sval.rank_lookup[value_2]
4114
```

We can then easily calculate the hand strength, i.e. the percentage the hand is
better than all other opponents hands, by comparing the hand vs all other 
possible hands. 
Effective hand strength is defined as (2 * ahead + tied)/(ahead + tied + behind) 
([EHS Wikipedia](https://en.wikipedia.org/wiki/Poker_Effective_Hand_Strength_(EHS)_algorithm)).

## Development

Using `nix-shell default.nix` drops you in a development shell with all 
dependencies already installed.
