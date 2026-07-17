f=open("C:/Users/Аделия/Downloads/10_5363.docx")
cnt=0
for s in f:
    a=[x for x in s.split()]
    for i in range(len(a)):
        if ('в' in a[i] or 'В' in a[i]) and ('а' not in a[i] and 'А' not in a[i]) and ('о' not in a[i] and 'О' not in a[i]):
            cnt+=1
print(cnt)
