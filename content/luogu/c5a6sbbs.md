### [Tavas and Malekas](https://www.luogu.com.cn/problem/CF535D)

正难则反，考虑如果没有限制条件，那么一共有 $26^k$种。

那么可以考虑写 $z$ 函数，求出最长公共后缀即可

```cpp
inline int ksm(int a,int b){
	int res=1;
	while(b){
		if(b&1)res=res*a%mod;
		a=a*a%mod;
		b>>=1;
	}
	return res;
}
int n,m,z[N];
char b[N];
bool a[N];
signed main(){
	n=read();m=read();
	scanf("%s",b+1);
	int lenb=strlen(b+1);
    z[1]=lenb;
    for(int i=2,l=0,r=0;i<=lenb;i++) {
        z[i]=i>r?0:min(z[i-l+1],r-i+1);
        while(b[1+z[i]]==b[i+z[i]])z[i]++;
        if(i+z[i]-1>r)l=i,r=i+z[i]-1;
    }
	int x,y;
	while(m--){
		x=read();
		a[x]=true;
	}
	x=y=0;
	up(i,1,n) {
		if(x){
			if(a[i]){
				if(z[lenb-x+1]>=x)x=lenb;
				else{
					printf("0");
					return 0;
				}
			}
		}
		else{
			if(a[i])x=lenb;
			else ++y;
		}
		if(x)--x;
	}
	x=ksm(26,y);
	printf("%lld",x);
	return 0;
}
```

### [Not Assigning](https://www.luogu.com.cn/problem/CF1627C)

只有在链的情况是存在的。

### [Painting Fence](https://www.luogu.com.cn/problem/CF448C)
分治，每个区间比较横着刷和纵向那种情况更优。
```cpp
int n;
int a[N];
inline int merge(int l,int r){
	if(l<1||r<1)return 0;
	if(l>r)return 0;
	if(l==r)return min(a[l],1ll);
	int m=inf,w=0;
	up(i,l,r){
		if(a[i]<m){
			m=a[i];
			w=i;
		}
	}
	int j=a[w];
	up(i,l,r)a[i]-=j;
	int lco=merge(l,w-1);
	int rco=merge(w+1,r);
	return min(j+lco+rco,r-l+1);
}
```

### [Lipshitz Sequence](https://www.luogu.com.cn/problem/CF601B#submit)

很有意思，首先有一个结论，k 一定在相邻的数里面。

所以我们考虑一个数所贡献的区间。

```cpp
int n,q,h[N],a[N],l[N],r[N],st[N];
signed main(){
	n=read();q=read();
	up(i,1,n)h[i]=read();
	up(i,1,n-1)a[i]=abs(h[i+1]-h[i]);
	while(q--){
		int L,R;
		scanf("%lld%lld",&L,&R);
		R--;
		memset(l,0,sizeof l);
		memset(r,0,sizeof r);
		int ans=0;
		for(int i=L,j=1;i<=R;++i,++j)a[j]=abs(h[i+1]-h[i]);
		int len=R-L+1;
		int top=0;
		for(int i=1;i<=len;++i){
			while(top&&a[st[top]]<a[i]){
				r[st[top]]=i-st[top];
				top--;
			}
			l[i]=i-st[top];
			st[++top]=i;
		}
		while(top)r[st[top]]=len+1-st[top],top--;
		up(i,1,len)ans+=a[i]*l[i]*r[i];
		printf("%lld\n",ans);
	}
	return 0;
}
```

### [Moodular Arithmetic](https://www.luogu.com.cn/problem/CF603B)

个人觉得这题不应该是绿。

第一眼看上去没有任何思路。

然后打开题解：

由于 $p$ 是质数。所以，$k^{p-1}$ 一定是模 $p$ 余 $1$ 的。所以我们只要所以这个 $m$，$m$ 是一个循环节，一定是 $p−1$ 的因数。于是，答案即为

$k=0$, $ans=p^{p-1}$

$k=1$, $ans=p^{p-1}$

$ans=p^{(p-1)/m}$
```cpp
inline int ksm(int a,int b){
	int ret=1;
	while(b){
		if(b&1)ret=ret*a%mod;
		a=a*a%mod;
		b>>=1;
	}
	return ret;
}
int p,k;
signed main(){
	p=read();k=read();
	if(k==0)write(ksm(p,p-1),1),exit(0);
	if(k==1)write(ksm(p,p),1),exit(0);
	int m=1;
	int x=k;
	while(x!=1)m++,x=x*k%p;
	write(ksm(p,(p-1)/m),1);
	return 0;
}
```
### [Edgy Trees ](https://www.luogu.com.cn/problem/CF1139C)

就是反着算。
```cpp
int n;
int fa[N];
inline int find(int x){
	if(x==fa[x])return x;
	return fa[x]=find(fa[x]);
}
inline int ksm(int a,int b){
	int res=1;
	while(b){
		if(b&1)res=res*a%mod;
		a=a*a%mod;
		b>>=1;
	}
	return res;
}
int k,ans;
int cnt[N];
signed main(){
	n=read();k=read();
	up(i,1,n)fa[i]=i;
	int u,v,w;
	up(i,1,n-1) {
		u=read();v=read();w=read();
		if(w==0)fa[find(u)]=find(v);
		
	}
	up(i,1,n){
		cnt[find(i)]++;
	}
	up(i,1,n){
		if(fa[i]==i){
			ans=(ans+ksm(cnt[i],k))%mod;
		}
	}
	cout<<(ksm(n,k)-ans+mod)%mod;
	return 0;
}
```