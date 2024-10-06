def solution(A, B):
    diff = A - B
    if diff % 2 == 0:
        return (B * 2) + (diff * 2)
    else:
        return (B * 2) + (diff * 2) + 1
