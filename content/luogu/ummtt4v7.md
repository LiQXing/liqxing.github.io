[$T1$](https://www.luogu.com.cn/problem/P1173)

首先，有一个非常显然的结论，答案只可能是 $-1,0,1,2$。

1. 当答案为 -1 时，只有当 $nm-c\le 1$ 或 $nm-c=2$ 剩下的两个白点相连。

1. 当答案为零时，原图不连通。

1. 当答案为 1 时，原图存在割点。

1. 否则答案为 2。

不难想到暴力做法，直接将每一个点都与之四连通的点连接起来，找割点。

然鹅，这是一定会 Tle and Mle。

再想一想， 有哪些地方会产生割点。

1. 一个黑点周围八连通的白点。

2. 四个角落的四个点。

这两处是比较显然的。

然鹅，这可以被hack

```
. . . 
. . .
. . #

```

```cpp
。. 。 
. 。。
。。#
```

中间的看起来是割点实际上并不是。

所以我们需要把四个角落的 $3\times 3$ 的矩阵全部标记。

这就结束了吗？（右京音）

看hack。


```
...
. . . 
. . #
. . .
...

```

```
...
. 。 。 
。。 #
. 。 。
...
```

中间这个点同样不是割点。

题解 1 为了解决这个问题让黑点再往外扩散一圈。

实际上只用把 黑点在边界上的投影给标记上就行了。




```cpp
int n,m,c;
struct node{
    int x,y,t;
}a[N],b[N];
int len,lenb;
inline void addblt(int x,int y){
    up(i,max(x-1,1ll),min(x+1,n)){
        up(j,max(y-1,1ll),min(y+1,m)){
            a[++len]={i,j,0};
        }
    }
}
inline void addsb(int x,int y){
    a[++len]={1,y,0};
    a[++len]={n,y,0};
    a[++len]={x,1,0};
    a[++len]={x,m,0};
}
inline void addjl(){
    up(i,1,min(3ll,n))up(j,1,min(3ll,m))a[++len]={i,j,0};
    up(i,max(1ll,n-3),n)up(j,1,min(3ll,m))a[++len]={i,j,0};
    up(i,1,min(3ll,n))up(j,max(1ll,m-3),m)a[++len]={i,j,0};
    up(i,max(1ll,n-3),n)up(j,max(1ll,m-3),m)a[++len]={i,j,0};
}
inline bool cmp1(node u,node v){
    if(u.x==v.x){
        if(u.y==v.y)return u.t<v.t;
        return u.y<v.y;
    }
    return u.x<v.x;
}
inline bool cmp2(node u,node v){
    if(u.y==v.y)return u.x<v.x;
    return u.y<v.y;
}
vector<int>g[N];
int fa[N],dfn[N],flag=0,low[N];
int tot;
inline void clear(){
    memset(dfn,0,sizeof dfn);
    memset(fa,0,sizeof fa);
    tot=0;
    flag=0;
    memset(low,0,sizeof low);
    memset(a,0,sizeof a);
    memset(b,0,sizeof b);
    len=0;lenb=0;
}
inline void tarjan(int u){
    dfn[u]=low[u]=++tot;
    int son=0;
    for(auto v:g[u]){
        if(!dfn[v]){
            fa[v]=u;
            tarjan(v);
            low[u]=min(low[u],low[v]);
            if(low[v]>=dfn[u]){
                if(fa[u])flag=1;
                else son++;
            }
        }
        else if(v!=fa[u])low[u]=min(low[u],dfn[v]);
    }
    if(son>1)flag=1;
}
signed main(){
    int T=read();
    while(T--){
        clear();
        n=read();m=read();c=read();
        int cnt=0;
        int x,y;
        up(i,1,c){
            x=read();y=read();
            addblt(x,y);
            addsb(x,y);
            a[++len]={x,y,-1};
        }
        addjl();
        sort(a+1,a+1+len,cmp1);
        node tmp={inf,inf,0};
        up(i,1,len){
            if(a[i].x!=tmp.x||a[i].y!=tmp.y){
                tmp=a[i];
                b[++lenb]=tmp;
                ///cout<<i<<endl;
            }
        }
        up(i,1,lenb)if(b[i].t!=-1)b[i].t=++cnt;
        for(int i=1;i<=cnt;i++)g[i].clear(),dfn[i]=0;
        up(i,2,lenb){
            if(b[i].x==b[i-1].x&&b[i].t!=-1&&b[i-1].t!=-1){
                g[b[i].t].push_back(b[i-1].t);
                g[b[i-1].t].push_back(b[i].t);
            }
        }
        sort(b+1,b+1+lenb,cmp2);
        up(i,2,lenb) {
            if(b[i].y==b[i-1].y&&b[i].t!=-1&&b[i-1].t!=-1){
                g[b[i].t].push_back(b[i-1].t);
                g[b[i-1].t].push_back(b[i].t);
            }
        } 
        if(cnt<=1){
            printf("-1\n");
            continue;
        }
        if(cnt==2&&g[1].size()){
            int id[2];
            up(i,1,lenb)if(b[i].t>=1&&b[i].t<=2)id[b[i].t-1]=i;
            if(abs(b[id[0]].x-b[id[1]].x)+abs(b[id[0]].y-b[id[1]].y)==1){
                printf("-1\n");
                continue;
            }
            else{
                printf("1\n");
                continue;
            }
        }
        tarjan(1);
        if(tot!=cnt)printf("0\n");
        else {
            if(flag)printf("1\n");
            else printf("2\n");
        }
    }
    return 0;
}
```
$T2$
```
 给出一张无向图，求删除一条边后此图变成二分图的所有删边种类。
```
二分图存在的充要条件是该图没有奇环。

若原图本就为二分图，显然随意删除都可行。

否则，图中存在奇环，我们需要删一条边破坏图中所有的奇环。

显然，答案是所有奇环的交集中的边。

我们先求出这张图的 dfs 树。

倘若有环，则一定是返祖边。

跑到返祖边的时候看一下当前环是奇还是偶，然后把环上的所有边的记录相应的环的种类都+1。

判定的时候，如果是dfs树上的边，直接数经过它的奇环个数是否=奇环总个数，并且不能有偶环经过否则这条边就一定不能删。

如果是dfs树上的返祖边，那它就至多有一个树上奇环经过它，判断一下它的奇环个数和总奇环个数是否都=1即可。

```cpp

#include <bits/stdc++.h>

using namespace std;

#define int long long
#define ull unsigned long long
#define i128 __int128
#define ldo long double
#define dle double
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=5e5+7;
const int mod=998244353;
const int inf=1e18;

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
int n,m;
vector<pii>g[N];
int dfn[N],dis[N],e[N],cnt,f[N],nums;
inline void dfs1(int u,int from){
    dfn[u]=1;
    for (auto [v,id]:g[u]){
        if(!dfn[v]){
            dis[v]=dis[u]^1;
            e[id]=1;
            dfs1(v,u);
        }
        else if(!e[id]){
            e[id]=1;
            if(dis[u]==dis[v]){
                cnt++;
                f[u]++;f[v]--;
                nums=id;
            }
            else {
                f[u]--;
                f[v]++;
            }
        }
    }
}
vector<int>ans;
inline void dfs2(int u,int from){
    dfn[u]=1;
    for (auto [v,id]:g[u]){
        if(!dfn[v]){
            dfs2(v,u);
            if(f[v]==cnt)ans.push_back(id);
            f[u]+=f[v];
        }
    }
}
signed main(){
	n=read();m=read();
    int u,v;
    up(i,1,m){
        u=read();v=read();
        g[u].push_back({v,i});
        g[v].push_back({u,i});
    }
    up(i,1,n)if(!dfn[i])dfs1(i,0);
    if (!cnt){
        write(m,1);
        up(i,1,m)write(i,0);
        return 0;
    }
    memset(dfn,0,sizeof dfn);
    up(i,1,n)if(!dfn[i])dfs2(i,0);
    if(cnt==1)ans.push_back(nums);
    write(ans.size(),1);
    sort(ans.begin(),ans.end());
    for(auto v:ans)write(v,0);
    return 0;
}
```

[$T3$](https://www.luogu.com.cn/problem/AT_keyence2019_e)


有 $n$ 个点排成一行，在第 $i,j$ 个点之间连边的代价为 $|i-j| \times D+A_i+A_j$，求将它们连成一棵树的最小代价。

考虑如何去掉这个绝对值，

换句话说，如何减少边数并且能建出 MST。

在求解偏序问题时，往往会分而治之，

这样原来 $ O(n^2)$的做法就能够被优化。

考虑将所有点对半折开，

左半部分和右半部分的建边分治处理，

只考虑横跨两部分的建边，

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ull unsigned long long
#define ldo long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=2e5+500;
const int mod=1e9+7;
const int inf=0x3f3f3f3f;

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
namespace DSU{
    int fa[N], siz[N];
    void init(int n) {
        up(i,1,n) fa[i] = i, siz[i] = 1;
    }
    int find(int x) {
        return fa[x] == x ? fa[x] : fa[x] = find(fa[x]);
    }
    void unionn(int x, int y) {
        int fx = find(x), fy = find(y);
		if(fx==fy)return;
        if(siz[fx] > siz[fy]) swap(fx, fy);
        fa[fx] = fy; siz[fy] += siz[fx];
    }
}using namespace DSU;

struct node{
	int x,y,w;
}e[N<<5];
int a[N],b[N],D,ans; 
int n,m;
inline bool cmp(node x,node y){
	return x.w<y.w;
}
inline void dfs(int l,int r){
    if (l==r) return;
    int mid=(l+r)>>1,t0=l,t1=r;
    up(i,l,mid)if(a[t0]>a[i]) t0=i;
    dn(i,r,mid+1)if(b[t1]>b[i])t1=i;
    up(i,l,mid)e[++m]={i,t1,a[i]+b[t1]};
	dn(i,r,mid+1)e[++m]={t0,i,a[t0]+b[i]};
    dfs(l,mid);
	dfs(mid+1,r);
}
signed main(){
    n=read();D=read();
	init(n);
    up(i,1,n){
        int x=read();
        a[i]=x-i*D,b[i]=x+i*D;
    }
    dfs(1,n);
	sort(e+1,e+1+m,cmp);
    up(i,1,m){
		int fx=find(e[i].x),fy=find(e[i].y);
        if (fx!=fy) {
			fa[fx]=fy;
			ans+=e[i].w;
		}
	}
	write(ans,1);
    return 0;
}

```

[$T4$](https://www.luogu.com.cn/problem/CF878C)

我们考虑两个选手之间的关系，如果一个选手能在某一项运动中战胜对手，那么就从他自身向对手连一条有向边。这样显然会出现很多环，于是可以大力缩点，将整张图缩成一个 $DAG$（实际实现中会变为一条链）。那么显然入度为零的环中包含的点数即为最后可能成为冠军的人数。

```cpp

#include <bits/stdc++.h>

using namespace std;

#define int long long
#define ull unsigned long long
#define i128 __int128
#define ldo long double
#define dle double
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=5e5+7;
const int mod=998244353;
const int inf=1e18;

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
int n,m;
struct node{
    int maxl[20],minl[20],sz;
    node(){
        memset(maxl,0,sizeof maxl);
        memset(minl,0x3f,sizeof minl);
        sz=0;
    }
    inline friend bool operator < (node a,node b) {
        up(i,1,m)if(a.maxl[i]>b.minl[i]) return 0;
        return 1;
    }	
}ans;
set<node>s;
signed main(){
    n=read();m=read();
    int u,v;
    up(i,1,n){
        ans.sz=1;
        up(j,1,m){
            ans.minl[j]=ans.maxl[j]=read();
        }
        auto it=s.find(ans);
        while(it!=s.end()) {
            ans.sz+=(it->sz);
            up(j,1,m){
                ans.maxl[j]=max(ans.maxl[j],it->maxl[j]);
                ans.minl[j]=min(ans.minl[j],it->minl[j]);
            }
            s.erase(it);
            it=s.find(ans);
        }
        s.insert(ans);
        write((s.rbegin())->sz,1);
    }

    return 0;
}
```
[$T5$](https://www.luogu.com.cn/problem/CF555E)

首先，如果两个点在一个边双里面，一定可以互相到达。
```cpp
#include <bits/stdc++.h>

using namespace std;

#define pii pair<int,int>

inline int read(){
    int x=0,f=1;char ch=getchar();
    while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
    while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
    return x*f;
}
int n,m;
vector<pii>g[500500];
vector<int>e[500500];
int low[500500],dfn[500500],cnt,colornum;
bool bri[500500];
int c[500500];
int col[500500];
int tot;
bool ins[500500];
stack<int>s;
inline void tarjan(int u,int from){
    dfn[u]=low[u]=++cnt;
    col[u]=tot;
    s.push(u);ins[u]=1;
    for(auto i:g[u]){
        int v=i.first,it=i.second;
        if(it==(from^1))continue;
        if(!dfn[v]){
            tarjan(v,it);
            low[u]=min(low[u],low[v]);
        }
        else if(ins[v])low[u]=min(low[u],dfn[v]);
    }
   
    if(dfn[u]==low[u]){
        colornum++;
         int t=0;
        while(t!=u){
            t=s.top();s.pop();
            c[t]=colornum;
            ins[t]=0;
        }
    }
}
int siz[500500],son[500500],fa[500500],dep[500500];
int top[500500],r,p,id[500500],idx;
int tag1[500500],tag2[500500];
int q,w[500500];
bool vis[500500];
inline void dfs1(int u,int from){
	siz[u]=1;son[u]=0;
	dep[u]=dep[from]+1;
	for(auto v:e[u]){
		if(v==from) continue;
		fa[v]=u;
		dfs1(v,u);
		if(siz[v]>siz[son[u]])son[u]=v;
		siz[u]+=siz[v];
	}
}
inline void dfs2(int u,int tp){
	top[u]=tp;id[u]=++idx;
	if(son[u]!=0) dfs2(son[u],tp);
	for(auto v:e[u]){
		if(v==fa[u]||v==son[u]) continue;
		dfs2(v,v);
	}
}
inline int lca(int u,int v){
    while(top[u] != top[v]){
        if(dep[top[u]] > dep[top[v]]) u = fa[top[u]];
        else v = fa[top[v]];
    }
    return dep[u] > dep[v] ? v : u;
}
inline void dfs3(int u){
	vis[u]=1;
	for(auto v:e[u]){
		if(v==fa[u]) continue;
		dfs3(v);
		tag1[u]+=tag1[v];
		tag2[u]+=tag2[v];
	}
}
int main() {
    n=read();m=read();q=read();
    for(int i=1,u,v;i<=m;i++){
        u=read();v=read();
        g[u].push_back({v,2*i});
        g[v].push_back({u,2*i+1});
    }
    for(int i=1;i<=n;i++){
        if(!dfn[i]){
            tot++;
            tarjan(i,0);
        }
    }
    for(int i=1;i<=n;i++){
        for(auto j:g[i]){
            int v=j.first;
            if(c[v] != c[i] ){
                e[c[v]].push_back(c[i]);
                e[c[i]].push_back(c[v]);
            }
        }
    }
    for(int i=1;i<=colornum;i++)
        if(!dep[i]){
            dfs1(i,0);
            dfs2(i,i);
        }
   // for(int i=1;i<=colornum;i++)if(!top[i])
    while(q--){
        int u=read(),v=read();
        if(col[u]!=col[v]){
            printf("NO");
            return 0;
        }
		int x=lca(c[u],c[v]);
		tag1[c[u]]++;tag1[x]--;
		tag2[c[v]]++;tag2[x]--;
    }
    for(int i=1;i<=n;i++)if(!vis[i]) dfs3(i);
	for(int i=1;i<=n;i++){
        if(tag1[i]&&tag2[i]){
			printf("No\n");
			return 0;
		}
    }
	printf("Yes\n");
    return 0;
}
```
[$T6$](https://www.luogu.com.cn/problem/CF76A)

非常妙的一道题。

但是呢，这棵树有两个量，需要同时考虑，又不能加起来算（因为要选取金币数最大再转换成图腾数，再加上银币数最大再转换成图腾数，不能先加起来再算最小生成树）所以我们要做一个类似于次小生成树的操作。

我们先对金币数量排序，然后做建边的操作，当然先把金币数小的先放进去，然后得到一个ans，之后不断地往里塞边（放进去后按银币冒泡），得到一个关于金币的次小生成树，并使银币从生成树向最小生成树过度，得到一个对于银币和金币加起来最小的树。
```cpp
#include<bits/stdc++.h>
#include <ios>

using namespace std;

#define int long long
#define ull unsigned long long
#define ldo long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=2e5+500;
const int mod=1e9+7;
const int inf=7e18;

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
namespace DSU{
    int fa[N], siz[N];
    void init(int n) {
        up(i,1,n) fa[i] = i, siz[i] = 1;
    }
    int find(int x) {
        return fa[x] == x ? fa[x] : fa[x] = find(fa[x]);
    }
    void unionn(int x, int y) {
        int fx = find(x), fy = find(y);
		if(fx==fy)return;
        if(siz[fx] > siz[fy]) swap(fx, fy);
        fa[fx] = fy; siz[fy] += siz[fx];
    }
}using namespace DSU;
int n,m;
struct node{
	int u,v,x,y;
}e[N<<3],q[5000];
inline bool cmp(node x,node y){
	return x.x<y.x;
}
int A,B;
int ans=inf;
signed main(){
	n=read();m=read();
	A=read();B=read();
	up(i,1,m){
		e[i].u=read();
		e[i].v=read();
		e[i].x=read();
		e[i].y=read();
	}
	sort(e+1,e+1+m,cmp);
	init(n);
	int t=0,s,x,y;
	up(i,1,m){
		q[++t]=e[i];
		s=0;
		for(int j=t-1;j&&q[j+1].y<q[j].y;j++)swap(q[j],q[j+1]);
		init(n);
		for(int j=1,x,y;s<n-1&&j<=t;j++){
			if((x=find(q[j].x))!=(y=find(q[j].y))) fa[x]=y,q[++s]=q[j];
		}
		if(s==n-1) ans=min(ans,A*e[i].x+1ll*B*q[s].y);
		t=s;
	}
	if(ans>=1e18)cout<<-1;
	else cout<<ans;
    return 0;
}

```

$T7$

图的绝对中心的定义可以知道，到绝对中心距离最远的结点至少有两个。

令 $d(i,j)$ 为顶点 $i,j$ 间的最短路径长，通过多源最短路算法求出所有结点的最短路。

$\textit{rk}(i,j)$ 记录点 $i$ 到其他所有结点中第 $j$ 小的那个结点。

图的绝对中心可能在某条边上，枚举每一条边 $(u,v,w)$，并且假设图的绝对中心 $c$ 就在这条边上。那么距离 $u$ 的长度为 $x(x\le w)$，距离 v 的长度就是 $w - x$。

对于图中的任意一点 $i$，图的绝对中心 $c$ 到 $i$ 的距离为 $d(c,i)=\min(d(u,i) + x, d(v,i) + (w - x))$。

```cpp
#include<bits/stdc++.h>
#include <ios>

using namespace std;

#define int long long
#define ull unsigned long long
#define ldo long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=2e5+500;
const int mod=1e9+7;
const int inf=7e18;

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
namespace DSU{
    int fa[N], siz[N];
    void init(int n) {
        up(i,1,n) fa[i] = i, siz[i] = 1;
    }
    int find(int x) {
        return fa[x] == x ? fa[x] : fa[x] = find(fa[x]);
    }
    void unionn(int x, int y) {
        int fx = find(x), fy = find(y);
		if(fx==fy)return;
        if(siz[fx] > siz[fy]) swap(fx, fy);
        fa[fx] = fy; siz[fy] += siz[fx];
    }
}using namespace DSU;
int n,m;
int val[N],rk[300][300],d[400][400];
bool cmp(int a, int b) { return val[a] < val[b]; }
struct node{
	int u,v,w;
}a[N];
void Floyd() {
	for (int k = 1; k <= n; k++)
    	for (int i = 1; i <= n; i++)
      		for (int j = 1; j <= n; j++) 
				d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
}

void solve() {
  Floyd();
  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
      rk[i][j] = j;
      val[j] = d[i][j];
    }
    sort(rk[i] + 1, rk[i] + 1 + n, cmp);
  }
  int ans = INF;
  // 图的绝对中心可能在结点上
  for (int i = 1; i <= n; i++) ans = min(ans, d[i][rk[i][n]] * 2);
  // 图的绝对中心可能在边上
  for (int i = 1; i <= m; i++) {
    int u = a[i].u, v = a[i].v, w = a[i].w;
    for (int p = n, i = n - 1; i >= 1; i--) {
      if (d[v][rk[u][i]] > d[v][rk[u][p]]) {
        ans = min(ans, d[u][rk[u][i]] + d[v][rk[u][p]] + w);
        p = i;
      }
    }
  }
  cout<<p<<endl;
}
signed main(){
	memset(d,0x3f,sizeof d);
	n=read();m=read();
	int u,v;
	up(i,1,m){
		d[v][u]=d[u][v]=read();
	}
	solve();
    return 0;
}

```

就这些吧，其他真的写不动啊！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！