import gzip
import numpy as np

from numba import jit
from pkg_resources import resource_filename

from . import hand_representation as hrp

RANKS = 0x1111111111111
LOOKUP_SIZE = 0x1 << 18
QUADS = 0x4444444444444
FLUSH = 111541
REDUCE = np.asarray(
    [
        248844, 344509, 578436, 1006297, 1049810, 1537951, 1627467, 2077693,
        2185318, 2557799, 2785929, 2922336, 3334005, 3411511, 3690340, 4129348,
        4333610, 4593825, 4863681, 5008913, 5489331, 5728048, 5791243, 6279771,
        6503942, 6765490, 6822030, 7296176, 7361105, 7762452, 7999853, 8324112,
        8546647, 8844882, 9137396, 9228405, 9648941, 9747526, 10147779,
        10344751, 10662433, 10823273, 11151028, 11441832, 11638513, 11998481,
        12240373, 12517381, 12589624, 13082003, 13144746, 13502680, 13824205,
        13924060, 14405355, 14620367, 14845254, 15120896, 15307881, 15601796,
        15922340, 16193284, 16422142, 16715797
    ],
    dtype='int32')


def __load_rank_lookup():

    f_string = resource_filename(__name__, 'lookup7card.dat.gz')
    f = gzip.open(f_string,
                  'rb')
    lookup = np.zeros(LOOKUP_SIZE, dtype='int16')
    for i in range(len(lookup)):
        b = f.read(2)
        lookup[i] = ((b[0] & 0xFF) | (b[1] & 0xFF) << 8)
    f.close()
    return lookup


@jit(nopython=True)
def calculate_index(cards):
    '''
    Calculate the index for the lookup table.
    :cards: The 7-cards for which to calculate the rank (int64).
    :return: The index to lookup the correct rank.
    '''
    t = 0
    r = 0
    f = 0

    for i in range(4):
        if f != 0:
            break
        t = cards >> i & RANKS
        f = t & (t - 1)
        f &= f - 1
        f &= f - 1
        f &= f - 1
        r += t

    if f != 0:
        t |= t >> 26
        t |= t >> 13
        return FLUSH ^ (t & 0x1FFF)

    t = r & QUADS
    if t != 0:
        t = t >> 1 | ((r | r >> 1) & RANKS)
        res = (~(t | t >> 26) & 0x1FFFFFF) >> 1
    else:
        res = ((r | r >> 26) & 0x0FFFFFF)

    return res ^ REDUCE[res >> 18 & 0x3F]


CARDS = hrp.ENCODED_CARD_VALUES
PAIRS = np.asarray(
    [(CARDS[c1] | CARDS[c2]) for c1 in range(52) for c2 in range(c1 + 1, 52)],
    dtype=np.int64)

rank_lookup = __load_rank_lookup()
