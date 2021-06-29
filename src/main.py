def __bsf(n):
	o=0
	while (not (n&1)):
		n>>=1
		o+=1
	return o



def __popcnt(n):
	o=0
	while (n):
		if (n&1):
			o+=1
		n>>=1
	return o



def __parity(n):
	o=0
	while (n):
		if (n&1):
			o^=1
		n>>=1
	return o



def reed_muller(r,m):
	if (m<=r):
		raise RuntimeError
	k=1
	for i in range(1,r+1):
		v=m
		for j in range(m-1,i+1,-1):
			v*=j
		for j in range(2,m-i):
			v//=j
		k+=v
	n=1<<m
	vl=[None for _ in range(0,m)]
	for i in range(0,m):
		j=1<<(m-i-1)
		v=((1<<j)-1)<<j
		off=j<<1
		o=0
		for l in range(0,1<<i):
			o=(o<<off)|v
		vl[i]=o
	il=[None for _ in range(0,r+1)]
	mx=[None for _ in range(0,n)]
	vr=[None for _ in range(0,k)]
	vr[0]=[None for _ in range(0,n)]
	for i in range(0,n):
		mx[i]=1
		vr[0][i]=1<<i
	mx_m=2
	for i in range(1,r+1):
		v=vl[0]
		il[0]=0
		for j in range(1,i):
			v&=vl[j]
			il[j]=j
		print(list(range(i,m)))
		while (v):
			mx[__bsf(v)]|=mx_m
			v&=v-1
		mx_m<<=1
		while (True):
			nxt=False
			for j in range(i-1,-1,-1):
				if (il[j]!=m-i+j):
					il[j]+=1
					for l in range(j+1,i):
						il[l]=il[l-1]+1
					v=vl[il[0]]
					vm=1<<il[0]
					for l in range(1,i):
						v&=vl[il[l]]
						vm|=1<<il[l]
					vm=((1<<m)-1)&(~vm)
					print(bin(vm))
					while (v):
						mx[__bsf(v)]|=mx_m
						v&=v-1
					mx_m<<=1
					nxt=True
					break
			if (not nxt):
				break
	idx_l=[None for _ in range(0,r+1)]
	idx_l[0]=1
	for i in range(1,r+1):
		v=m-i
		for j in range(2,m-i):
			v*=j
		for j in range(2,i+1):
			v//=j
		idx_l[i]=idx_l[i-1]+v
	s=(1<<(m-r-1))-1
	return (r,m,k,n,s,mx,idx_l,vr)



def encode(rm,dt):
	o=0
	for i in range(rm[3]-1,-1,-1):
		o=(o<<1)|__parity(dt&rm[5][i])
	return o



def decode(rm,dt):
	o=0
	m=1
	for i in range(rm[0],-1,-1):
		a=(0 if i==0 else rm[6][i-1])
		b=rm[6][i]
		for j in range(a,b):
			v=0
			for k in range(0,len(rm[7][j])):
				v+=__parity(dt&rm[7][j][k])
			if (v==rm[2]):
				return None
			if (v>(rm[2]>>1)):
				o|=m
			m<<=1s
		n=1
		for j in range(0,rm[3]):
			if (__parity(((o&rm[5][j])>>a)&((1<<(b-a))-1))):
				dt^=n
			n<<=1
	return o



rm=reed_muller(2,4)
print(rm)
print(bin(encode(rm,0b10101001011)),"0b100100001111011")
# print(bin(decode(rm,encode(rm,0b10101001011))),"0b10101001011")
