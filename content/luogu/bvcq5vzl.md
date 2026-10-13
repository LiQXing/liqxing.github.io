# T1

并查集加点加上 $DP$.

并查集加点很巧妙。


### code
```cpp
#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>

const int N=5e5+5000;
const int mod=998244353;

namespace IO{
	inline int read(){
		char c=getchar();int x=0,fh=0;
        while(c<'0'||c>'9'){fh|=c=='-';c=getchar();}
        while(c>='0'&&c<='9'){x=(x<<1)+(x<<3)+(c^48);c=getchar();}
        return fh?-x:x;
	}
	inline void wt(int x){
		if(x<0){x=-x;putchar('-');}
		if(x>9)wt(x/10);
		putchar((x%10)^48);
	}
	inline void write(int x,bool op){
		wt(x);
		putchar(op?'\n':' ');
	}
}using namespace IO;
int n,m,fa[N];
inline int get(int x){
	if(x==fa[x])return fa[x];
	return fa[x]=get(fa[x]);
}
int f[5005][5005];
signed main(){
	n=read();
	int x,y;
	up(i,1,25000)fa[i]=i;
	up(i,1,n){
		x=read();y=read();
		fa[get(x)]=get(y+10000);
	}
	up(i,1,5000){
		up(j,1,5000){
			if(get(i)==get(j+10000))f[i][j]=f[i-1][j-1]+1;
	    	else f[i][j]=max(f[i-1][j],f[i][j-1]);
		}
	}
	printf("%d",f[5000][5000]);
    return 0;
}
```
# T2
求逆序对和正序对。
### code
```cpp

#include <bits/stdc++.h>

using namespace std;

#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>

const int N=5e5;
const int mod=998244353;
namespace IO{
	inline int read(){
		char c=getchar();int x=0,fh=0;
        while(c<'0'||c>'9'){fh|=c=='-';c=getchar();}
        while(c>='0'&&c<='9'){x=(x<<1)+(x<<3)+(c^48);c=getchar();}
        return fh?-x:x;
	}
	inline void wt(int x){
		if(x<0){x=-x;putchar('-');}
		if(x>9)wt(x/10);
		putchar((x%10)^48);
	}
	inline void write(int x,bool op){
		wt(x);
		putchar(op?'\n':' ');
	}
}using namespace IO;
int tr[N],a[N];
inline int lowbit(int x){return x&(-x);}
inline void add(int x){
	for(;x<=N;x+=lowbit(x))tr[x]++;
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
int n,rk[N];
vector<int>e;
signed main(){
	n=read();
	up(i,1,n){
		a[i]=read();
		e.push_back(a[i]);
	}
	sort(e.begin(),e.end());
	e.erase(unique(e.begin(),e.end()),e.end());
	up(i,1,n){
		rk[i]=lower_bound(e.begin(),e.end(),a[i])-e.begin()+1;
	}
	int ans=0,ans2=0;
	for(int i=n;i>=1;i--){
		ans+=ask(rk[i]);
		add(rk[i]);
	}
	memset(tr,0,sizeof tr);
	for(int i=1;i<=n;i++){
		ans2+=ask(rk[i]);
		add(rk[i]);
	}
	cout<<min(ans,ans2);
    return 0;
}
```

# T3

因为这道题特意去学习主席树。

题目大意：给你一棵树，求路径上某个数字的数量。
分析：树链剖分+主席树；
对每个颜色建一棵树。
记得用$map$

```cpp
#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>

const int N=1e5+5000;
const int mod=998244353;
namespace IO{
	inline int read(){
		char c=getchar();int x=0,fh=0;
        while(c<'0'||c>'9'){fh|=c=='-';c=getchar();}
        while(c>='0'&&c<='9'){x=(x<<1)+(x<<3)+(c^48);c=getchar();}
        return fh?-x:x;
	}
	inline void wt(int x){
		if(x<0){x=-x;putchar('-');}
		if(x>9)wt(x/10);
		putchar((x%10)^48);
	}
	inline void write(int x,bool op){
		wt(x);
		putchar(op?'\n':' ');
	}
}using namespace IO;
int n,m,s,siz[N],son[N],f[N],dep[N];
int top[N],r,p,a[N],id[N],b[N],cnt,idx,rk[N];
struct node{
	int ls,rs,w;
}tr[N<<6];
vector<int>g[N];
int t,c[N];
unordered_map<int,int>rt;
inline void dfs1(int u,int fa){
	siz[u]=1;
	dep[u]=dep[fa]+1;
	for(auto v:g[u]){
		if(v==fa) continue;
		f[v]=u;
		dfs1(v,u);
		if(siz[v]>siz[son[u]])son[u]=v;
		siz[u]+=siz[v];
	}
}
inline void dfs2(int u,int tp){
	top[u]=tp;
	id[u]=++idx;
    a[idx]=b[u];
	if(son[u]!=0) dfs2(son[u],tp);
	for(auto v:g[u]){
		if(v==f[u]||v==son[u]) continue;
		dfs2(v,v);
	}
}
inline void push_up(int u) {
    tr[u].w=tr[tr[u].ls].w+tr[tr[u].rs].w;
}
inline void update(int &p,int k,int l,int r,int val){
	if(!p) p=++cnt;
    if(l==r && l == k){
        tr[p].w=val;
        return ;
    }
    int mid=(l+r)>>1;
    if(k<=mid) update(tr[p].ls,k,l,mid,val);
    else update(tr[p].rs,k,mid+1,r,val);
	push_up(p);
}
inline int ask(int p,int l,int r,int x,int y){
    if(!p) return 0;
    if(x<=l&&r<=y)return tr[p].w;
    int mid=(l+r)>>1,ans=0;
    if(x<=mid) ans+=ask(tr[p].ls,l,mid,x,y);
    if(mid<y) ans+=ask(tr[p].rs,mid+1,r,x,y);
    return ans;
}
inline int sum1(int x,int y,int w){
    int ans=0;
    while(top[x]!=top[y]){
        if(dep[top[x]]<dep[top[y]]) swap(x,y);
        ans=(ans+ask(rt[w],1,n,id[top[x]],id[x]));
        x=f[top[x]];
    }
    if(dep[x]>dep[y]) swap(x,y);
    ans=(ans+ask(rt[w],1,n,id[x],id[y]));
    return ans;
}
signed main(){
	n=read();m=read();
	up(i,1,n){
		b[i]=read();
	}
	int op,x,y,z;
	up(i,1,n-1){
		x=read();y=read();
		g[x].push_back(y);
		g[y].push_back(x);
	}
	dfs1(1,0);
	dfs2(1,1);
	up(i,1,n)update(rt[b[i]],id[i],1,n,1);
	char opt[2];
	int last=0;
	while(m--){
		scanf("%s",opt);
		if(opt[0]=='C'){
			x=read()^last;z=read()^last;
			update(rt[b[x]],id[x],1,n,0);
			update(rt[z],id[x],1,n,1);
			b[x]=z;
		}
		else if(opt[0]=='Q'){
			x=read()^last;y=read()^last;z=read()^last;
			last=sum1(x,y,z);
			write(last,1);
		}
	}
    return 0;
}

```
# T4
```cpp

```