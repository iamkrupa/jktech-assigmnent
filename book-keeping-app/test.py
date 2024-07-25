lst1=[10,20,30]

lst2=["a","b","c"]



tup=tuple(lst1)
tup2=tuple(lst2)


print(f"{tup} : {tup2}")
d={}

d[lst2[0]]=lst1[0]


d=dict(zip(lst1, lst2))

print(d)



[y*2 for y in range(10)] #==[0,2,4,6]

result=(y*3 for y in range(10)) 
print(result)

for i in result:
    print(i)

#(0,3,6,9)