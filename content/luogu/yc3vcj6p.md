$T1$

树状数组求逆序对。

数组开大点。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

const int mod=1e9+7;
const int N=100500;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,k;
inline int ksm(int a,int b,int p){
	int res=1;
	while(b){
		if(b&1)res=(res*a)%p;
		a=(a*a)%p;
		b>>=1;
	}
	return res;
}
int a[N],f[N],g[N];
int tr[N*4];
inline int lowbit(int x){return x&(-x);}
inline void add(int x){
	for(;x<=N*2;x+=lowbit(x))tr[x]++;
}
inline int ask(int x){
	int res=0;
	x--;
	if(x==0)return 0;
	for(;x>=1;x-=lowbit(x)){
		res+=tr[x];
	}
	return res;
}
int rkf[N],rkg[N];
vector<int>e;
signed main(){
	freopen("math.in","r",stdin);
	freopen("math.out","w",stdout);
	n=read();k=read();
	for(int i=1;i<=n;i++){
		a[i]=read();
		f[i]=ksm(i,a[i],k);
		g[i]=ksm(a[i],i,k);
	}
	for(int i=1;i<=n;i++){
		e.push_back(f[i]);
		e.push_back(g[i]);
	}
	sort(e.begin(),e.end());
	e.erase(unique(e.begin(),e.end()),e.end());
	for(int i=1;i<=n;i++){
		rkf[i]=lower_bound(e.begin(),e.end(),f[i])-e.begin()+1;
		rkg[i]=lower_bound(e.begin(),e.end(),g[i])-e.begin()+1;
	}
	//for(int i=1;i<=n;i++){cout<<rkf[i]<<" "<<rkg[i]<<endl;}
	int ans=0;
	for(int i=n;i>=1;i--){
		ans+=ask(rkf[i]);
		//cout<<i<<" "<<ask(f[i])<<endl;
		add(rkg[i]);
	}
	cout<<ans;
	return 0;
}

```

$T2$

求最小值最大，想到二分。

考虑二分答案。若 $a[x]<mid$,则贪心后面$2*r+1$都加上，看可不可行。

我们可以巧妙的用差分来维护修改后的值。

当然也可以用线段树。

```cpp

#include<bits/stdc++.h>

using namespace std;

#define int long long
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

const int mod=1e9+7;
const int N=500500;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int a[N],cf[N],n,r,k,sum[N];
bool check(int x, int tot = 0) {
	for (int i = 1; i <= n; ++i) {
		cf[i] = a[i] - a[i - 1];
	}
	int now = 0;
	for (int i = 1; i <= n; ++i) {
		now += cf[i];
		if (now < x) {
			if (tot + x - now > k) return false;
			int stop = min(n + 1, i + r + r + 1);
			tot += x - now, cf[stop] -= x - now, now += x - now;
		}
	}
	return tot <= k;
}
int maxl=0;
signed main() {
	n=read();r=read();k=read();
	for (int i = 1; i <= n; ++i) {
		a[i]=read();
		sum[i] = sum[i - 1] + a[i];
		maxl = max(maxl, a[i]);
	}
	for (int i = 1; i <= n; ++i) {
		int ll=max(0ll, i - r - 1);
		int rr = min(n, i + r);
		a[i] = sum[rr] - sum[ll];
	}
	int l = 0, r = k * 2 + maxl * 3;
	while(l <= r) {
		int mid = (l + r) >> 1;
		if (check(mid)) l = mid + 1;
		else r = mid - 1;
	}
	printf("%lld\n", r);
	return 0;
}
```

$T3$

由于询问和值域有关，不妨离线，把询问按 
 $k $ 值升序排序

这样就等效于是一步步把边加入图中，正好这是个无向图，直接带权并查集维护即可

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

const int mod=9959495;
const int N=500500;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
struct edge {
	int u, v, w;
	bool operator <(const edge &tmp) const {
		return w < tmp.w;
	}
} e[N*2];
int fa[N],n,m,q,ans[N],up,siz[N];
inline int find(int x) {return fa[x] == x ? x : fa[x] = find(fa[x]);}
signed main(){
	n=read();m=read();q=read();
	for(int i = 1; i <= n; i ++) {
		cin >>e[i].u >>e[i].v >>e[i].w;
		up = max(up, e[i].w);
		fa[i] = i;
	}
	sort(e + 1, e + 1 + m);
	int pos = 1;
	for(int i = 0; i <= up; i ++) {
		while(pos <= m && e[pos].w <= i) {
			int u=find(e[pos].u),v=find(e[pos].v);
			if(u != v) {
				fa[v] = u;
				siz[u] += siz[v];
			}
			siz[u] += e[pos].w;
			ans[i] = max(ans[i], max(siz[u], ans[i - 1]));
			pos ++;
		}
		ans[i] = max(ans[i], ans[i - 1]);
	} 
	while(q --) {
		int x; cin >>x;
		if(x >= up) {
			cout <<ans[up] <<endl;
			continue;
		}
		cout <<ans[x] <<endl;
	}
	return 0;
}
```