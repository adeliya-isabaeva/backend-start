from itertools import*
ans=[]
m=0
for s in range(1000,10000):
    s=str(s)
    f=[int(p) for p in s]
    comb=list(permutations(f,2))
    sp=[]
    for c in comb:
        n=''.join(map(str,c))
        sp+=[int(n)]
    a=set(sp)
    k=len(a)
    maxi=max(a)
    mini=min(a)
    h=maxi-mini
    ans.append([k,h])
print(ans)
