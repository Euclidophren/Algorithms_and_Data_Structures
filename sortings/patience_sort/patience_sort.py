import bisect
import heapq


def find_pile(top_cards, n):
    pos = bisect.bisect_right(top_cards, n)
    if pos == len(top_cards):
        top_cards.append(n)
        return -1
    else:
        top_cards[pos] = n
        return pos


def patience_sort(a):
    top_cards, piles = [], []
    for i in a:
        pile_id = find_pile(top_cards, i)
        if pile_id == -1:
            pile = [i]
            piles.append(pile)
        else:
            piles[pile_id].append(i)
    heap = [(pile.pop(), pile_id) for pile_id, pile in enumerate(piles)]
    sorted_a = []
    while heap:
        i, pile_id = heapq.heappop(heap)
        sorted_a.append(i)
        pile = piles[pile_id]
        if len(pile) > 0:
            i = pile.pop()
            heapq.heappush(heap, (i, pile_id))
    return sorted_a


if __name__ == '__main__':
    print(patience_sort([3, 4, 5, 7, 7, 1, -4, -5]))
