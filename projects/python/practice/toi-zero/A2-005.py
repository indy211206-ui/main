W, H, M, N = map(int, input().split())
xs = list(map(int, input().split()))
ys = list(map(int, input().split()))
while len(xs) > M or len(ys) > N:
    W, H, M, N = map(int, input().split())
    xs = list(map(int, input().split()))
    ys = list(map(int, input().split()))
xs = [0] + xs + [W]
width = sorted([xs[i] - xs[i-1] for i in range(len(xs))],reverse=True)
ys = [0] + ys + [H]
height = sorted([ys[i] - ys[i-1] for i in range(len(xs))],reverse=True)
w1, w2 = width[0], width[1]
h1, h2 = height[0], height[1]

area1 = h1 * w1
area2 = max(h1 * w2, h2 * w1)
print(area1, area2)
