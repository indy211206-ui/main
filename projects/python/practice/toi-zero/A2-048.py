n_student = int(input())
line = input().split()
scores = []
for x in line:
    scores.append(int(x))

# Line 1: student list
students = ''
for i in range(n_student):
    if i > 0:
        students += ' '
    students += 'Student' + str(i+1)
print('Student: ' + students)

if n_student == 0:
    print('Highest score: ')
    print('Lowest score: ')
    print('Average score: ')
    print('Students who scored above average:')
else:
    # Find max, min manually
    h_score = scores[0]
    l_score = scores[0]
    total = 0
    for s in scores:
        if s > h_score:
            h_score = s
        if s < l_score:
            l_score = s
        total += s

    av_score = total / n_student

    print('Highest score: ' + str(h_score))
    print('Lowest score: ' + str(l_score))
    print('Average score: ' + ('%.1f' % av_score))
    print('Students who scored above average:')
    for i in range(n_student):
        if scores[i] > av_score:
            print('Student ' + str(i+1))
