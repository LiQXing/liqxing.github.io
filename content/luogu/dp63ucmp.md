$T1$

傻逼爆搜。

挺简单的一道搜索，不要想复杂了。

$T2$

有意思的 DP。

$T3$

傻逼线段树。

```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define i64 long long
#define ull unsigned long long
#define ldb long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=(b);a<=(c);a++)
#define dn(a,b,c) for(int a=(b);a>=(c);a--)
#define pii pair<int,int>
#define pivi pair<int,vector<int> >
#define lc k<<1
#define rc k<<1|1
#define fi first
#define se second
#define endl '\n'
#define i16 short

const int N=2e5+100,M=2e6+100;
const int mod=2019;
const int inf=0x3f3f3f3f;
const ull uinf=1e18+14;

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
int n,q;
vector<int>g[N];
int a[N];
struct treelca{
    int siz[N],son[N],fa[N],dep[N],top[N];
    int dfn[N],cnt,idx[N];
    inline void dfs1(int u,int from){
        siz[u]=1;son[u]=0;
        dep[u]=dep[from]+1;
        for(auto v:g[u]){
            if(v==from) continue;
            fa[v]=u;dfs1(v,u);
            if(siz[v]>siz[son[u]])son[u]=v;
            siz[u]+=siz[v];
        }
    }
    inline void dfs2(int u,int tp){
        top[u]=tp;dfn[u]=++cnt;
        idx[cnt]=u;
        if(son[u])dfs2(son[u],tp);
        for(auto v:g[u]){
            if(v==fa[u]||v==son[u]) continue;
            dfs2(v,v);
        }
    }
    inline int lca(int x,int y){
        while(top[x]!=top[y]){
            if(dep[top[x]]>dep[top[y]])x=fa[top[x]];
            else y=fa[top[y]];
        }
        return dep[x]<dep[y]?x:y;
    }
    struct node{
        int l,r,sum,tag,siz;
        int num,rel;
    }tr[N<<1];
    inline void push_up(int k){
        tr[k].sum=(tr[lc].sum+tr[rc].sum)%mod;
        tr[k].siz=(tr[lc].siz+tr[rc].siz)%mod;
        tr[k].num=(tr[lc].num+tr[rc].num)%mod;
        tr[k].rel=(tr[lc].rel+tr[rc].rel)%mod;
    }
    inline void build(int k,int l,int r){
        tr[k].l=l;tr[k].r=r;
        if(l==r){
            tr[k].siz=siz[idx[l]]%mod;
            tr[k].sum=tr[k].siz*a[idx[l]]%mod;
            tr[k].num=tr[k].siz*tr[k].siz%mod;
            tr[k].rel=tr[k].num*a[idx[l]]%mod;
            return;
        }
        int mid=(l+r)>>1;
        build(lc,l,mid);
        build(rc,mid+1,r);
        push_up(k);
    }
    inline int asksum(int k,int l,int r){
        if(l>r)return 0;
        if(tr[k].l>=l&&tr[k].r<=r)return tr[k].sum;
        int mid=(tr[k].l+tr[k].r)>>1,res=0;
        push_down(k);
        if(mid>=l)res=(res+asksum(lc,l,r))%mod;
        if(mid<r)res=(res+asksum(rc,l,r))%mod;
        return res;
    }
    inline int askrel(int k,int l,int r){
        if(l>r)return 0;
        if(tr[k].l>=l&&tr[k].r<=r)return tr[k].rel;
        int mid=(tr[k].l+tr[k].r)>>1,res=0;
        push_down(k);
        if(mid>=l)res=(res+askrel(lc,l,r))%mod;
        if(mid<r)res=(res+askrel(rc,l,r))%mod;
        return res;
    }
    inline void push_down(int k){
        if(tr[k].tag){
            int w=tr[k].tag;
            tr[lc].sum=(tr[lc].sum+tr[lc].siz*w)%mod;
            tr[rc].sum=(tr[rc].sum+tr[rc].siz*w)%mod;
            tr[lc].rel=(tr[lc].rel+tr[lc].num*w)%mod;
            tr[rc].rel=(tr[rc].rel+tr[rc].num*w)%mod;
            tr[lc].tag=(tr[lc].tag+w)%mod;
            tr[rc].tag=(tr[rc].tag+w)%mod;
            tr[k].tag=0;
        }
    }
    inline void add(int k,int l,int r,int w){
        if(tr[k].l>=l&&tr[k].r<=r){
            tr[k].sum=(tr[k].sum+tr[k].siz*w)%mod;
            tr[k].rel=(tr[k].rel+tr[k].num*w)%mod;
            tr[k].tag=(tr[k].tag+w)%mod;
            return;
        }
        int mid=(tr[k].l+tr[k].r)>>1;
        push_down(k);
        if(mid>=l)add(lc,l,r,w);
        if(mid<r)add(rc,l,r,w);
        push_up(k);
    }
    inline void change(int x,int y,int w) {
        if(x==y)return;
        while(top[x]!=top[y]) {
            if(dep[top[x]]<dep[top[y]])swap(x, y);
            add(1,dfn[top[x]],dfn[x],w);
            x=fa[top[x]];
        }
        if(x==y)return;
        if(dep[x]>dep[y])swap(x, y);
        add(1,dfn[x]+1,dfn[y],w);
    }
    inline int ask(int x){
        return (asksum(1,dfn[x]+1,dfn[x]+siz[x]-1)*siz[x]%mod-askrel(1,dfn[x]+1,dfn[x]+siz[x]-1)%mod+mod)%mod;
    }
}T;
signed main(){
    n=read();q=read();
    int u,v,w;
    up(i,2,n){
        u=read();a[i]=read();
        g[u].push_back(i);
        g[i].push_back(u);
    }
    T.dfs1(1,0);
    T.dfs2(1,1);
    T.build(1,1,n);
    char s[50];
    while(q--){
        scanf("%s",s+1);
        if(s[1]=='I'){
            u=read();v=read();w=read();
            T.change(u,v,w);
        }
        if(s[1]=='A'){
            u=read();
            write(T.ask(u),1);
        }
    }
    return 0;
}
```