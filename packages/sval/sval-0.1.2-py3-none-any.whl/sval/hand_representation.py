# -*- coding: utf-8 -*-
import numpy as np

from numba import jit

CARD_NAMES = np.asarray(
    [
        "2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s",
        "5c", "5d", "5h", "5s", "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s",
        "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s", "Tc", "Td", "Th", "Ts",
        "Jc", "Jd", "Jh", "Js", "Qc", "Qd", "Qh", "Qs", "Kc", "Kd", "Kh", "Ks",
        "Ac", "Ad", "Ah", "As"
    ],
    dtype='str')
CARD_VALUES = {k: v for k, v in zip(CARD_NAMES, range(52))}

ENCODED_CARD_VALUES = np.asarray([2**n for n in range(52)], dtype=np.int64)

UNICODE_CARD_VALUES = [
    '🃒', '🃂', '🂲', '🂢', '🃓', '🃃', '🂳', '🂣', '🃔', '🃄', '🂴', '🂤', '🃕', '🃅', '🂵',
    '🂥', '🃖', '🃆', '🂶', '🂦', '🃗', '🃇', '🂷', '🂧', '🃘', '🃈', '🂸', '🂨', '🃙', '🃉',
    '🂹', '🂩', '🃚', '🃊', '🂺', '🂪', '🃛', '🃋', '🂻', '🂫', '🃝', '🃍', '🂽', '🂭', '🃞',
    '🃎', '🂾', '🂮', '🃑', '🃁', '🂱', '🂡'
]


def string_to_card(s):
    return CARD_VALUES[s]


def encode_cards(s):
    '''
    Encode a string to cards (int64).
    '''
    r = 0
    for i in range(0, len(s), 2):
        c = string_to_card(s[i:i + 2])
        r |= 0x1 << c
    return r


@jit(nopython=True)
def cards_to_string(cards):
    '''
    Cards (int64) to string.
    '''
    s = ''
    for i in range(51, -1, -1):
        if (cards & (0x1 << i)) != 0:
            s += CARD_NAMES[i]
    return s


@jit(nopython=True)
def cards_to_unicode(cards):
    '''
    Cards (int64) to unicode characters.
    '''
    s = ''
    for i in range(51, -1, -1):
        if (cards & (0x1 << i)) != 0:
            s += UNICODE_CARD_VALUES[i]
    return s
