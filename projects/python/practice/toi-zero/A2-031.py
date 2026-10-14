n = int(input())

chrom1 = input().split()
chrom2 = input().split()

mutations = int(input())

for _ in range(mutations):
    parts = input().split()
    strand = int(parts[0])
    pos = int(parts[1])
    gene = parts[2]

    if strand == 1:
        chrom1[pos] = gene
    else:
        chrom2[pos] = gene

print(" ".join(chrom1))
print(" ".join(chrom2))

mismatches = 0
for i in range(n):
    a = chrom1[i]
    b = chrom2[i]
    if not ((a == 'A' and b == 'T') or (a == 'T' and b == 'A') or
            (a == 'C' and b == 'G') or (a == 'G' and b == 'C')):
        mismatches += 1

print(mismatches)
