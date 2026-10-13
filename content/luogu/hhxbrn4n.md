
比较显然的结论:

$a\Longleftrightarrow b,b\Longleftrightarrow c$，则 $a\Longleftrightarrow c$。

看一眼数据范围，肯定不能每条边都一一加上，肯定会超时。

观察，每个连通块的贡献都为 $size[x]\times(size[x]-1)$。

想到只维护连通块之间的边。

手动模拟加边情况：

加入边 $[u,v]$，如果这条边在同一个联通图，跳过。

如果 $u$ 有一条连向 $v$ 所在连通图的边，那么 $u$ 一定已经连向了 $v$ 本身，跳过。

再判断有无一条边可以从 $v$ 所在的连通图连向 $u$ 所在的连通图。

如果 $v$ 所在的连通图不能够连向 $u$ 所在的连通图，就直接记录这条边，然后答案加上 $v$ 连通块的大小。

如果能够连向，那么这两个连通块都可以合并成一个。

那么把答案中的两个连通块去掉，合并之后再加上。

把 $v$ 所在的连通图合并在 $u$ 所在的联通图上。

$v$ 连通图伸出和射入的边去掉，然后全连在 $u$ 的图上，bfs 循环加边，最后再统计答案。


```cpp

inline int clac(int u){
    return siz[u]*(siz[u]-1)+in[u].size()*siz[u];
}
inline void merge(int xx,int yy){
    queue<pii>q;
    q.push({xx,yy});
    while(q.size()){
        pii u=q.front();q.pop();
        int x=u.first,y=u.second;
        int fux=find(x),fuy=find(y);
        if(fux==fuy||in[fuy].count(x))continue;
        auto it=out[fuy].lower_bound({fux,0});
        if(it==out[fuy].end()||it->first!=fux){
            in[fuy].insert(x);
            out[fux].insert({fuy,x});
            ans+=siz[fuy];
            continue;
        }
        ans-=clac(fux)+clac(fuy);
        for(auto t:out[fuy]){
            int tx=t.first,ty=t.second;
            in[tx].erase(ty);
            if(tx==fux)continue;
            q.push({ty,tx});
            ans-=siz[tx];
        }
        for(auto t:in[fuy]){
            int ft=find(t);
            out[ft].erase({fuy,t});
            if(ft!=fux)q.push({t,fux});
        }
        fa[fuy]=fux;siz[fux]+=siz[fuy];
        ans+=clac(fux);
        in[fuy].clear();
        out[fuy].clear();
    }
}
```

然而，会超时。

考虑优化，想到启发式合并。

```cpp
	if(in[fux].size()+out[fux].size()<in[fuy].size()+out[fuy].size()){
            swap(fux,fuy);
            swap(x,y);
        }
```
时间复杂度变为 $O(n\log^2n)$。

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

const int N=1e6+7;
const int mod=59027;

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
int fa[N];
inline int find(int x){
    if(x==fa[x])return x;
    return fa[x]=find(fa[x]);
}
set<int>in[N];
set<pii>out[N];
int n,m,siz[N];
int ans;
inline int clac(int u){
    return siz[u]*(siz[u]-1)+in[u].size()*siz[u];
}
inline void merge(int xx,int yy){
    queue<pii>q;
    q.push({xx,yy});
    while(q.size()){
        pii u=q.front();q.pop();
        int x=u.first,y=u.second;
        int fux=find(x),fuy=find(y);
        if(fux==fuy||in[fuy].count(x))continue;
        auto it=out[fuy].lower_bound({fux,0});
        if(it==out[fuy].end()||it->first!=fux){
            in[fuy].insert(x);
            out[fux].insert({fuy,x});
            ans+=siz[fuy];
            continue;
        }
        if(in[fux].size()+out[fux].size()<in[fuy].size()+out[fuy].size()){
            swap(fux,fuy);
            swap(x,y);
        }
        ans-=clac(fux)+clac(fuy);
        for(auto t:out[fuy]){
            int tx=t.first,ty=t.second;
            in[tx].erase(ty);
            if(tx==fux)continue;
            q.push({ty,tx});
            ans-=siz[tx];
        }
        for(auto t:in[fuy]){
            int ft=find(t);
            out[ft].erase({fuy,t});
            if(ft!=fux)q.push({t,fux});
        }
        fa[fuy]=fux;siz[fux]+=siz[fuy];
        ans+=clac(fux);
        in[fuy].clear();
        out[fuy].clear();
    }
}
signed main(){
    int u,v;
    n=read();m=read();
    up(i,1,n)fa[i]=i,siz[i]=1;
    up(i,1,m){
        u=read();v=read();
        merge(u,v);
        write(ans,1);
    }
    return 0;
}

```







