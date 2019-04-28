import wat

d = [1, 2]
wat.d(d)
d.append(4)
d.remove(2)
wat.d(d)

for v in d:
    if v==1:
        d.append(5)
    wat.d(v)

try:
    d.remove(3)
except Exception as e:
    wat.d(str(e))

