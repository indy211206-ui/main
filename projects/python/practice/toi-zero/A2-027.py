student = int(input())
scores = []
for _ in range(student):
    score = int(input())
    scores.append(score)
max_score = max(scores)
count = scores.count(max_score)
print(max_score)
print(count)
