一道诈骗题。

------------
题意：

给定一个长度为 $n$ 的序列 $\{a_n\}$，对于每个 $i\in [1,n]$ ，求出一个最小的非负整数 $p$ ，使得 $\forall j\in[1,n]$，都有 $a_j\le a_i+p-\sqrt{|i-j|}$

$1 \le n \le 5\times 10^{5}$，$0 \le a_i \le 10^{9}$ 。


------------

看起来是相当的不可做，题解里大部分都是决策单调性DP。

然而，因为 $ n \le 5\times 10^{5} $, 所以 $\sqrt{i-j}\le710$。

能够对答案造成影响的只有 $\max a_i-\sqrt{n}\le a_i\le \max a_i$。

其实最多只有 710 个不同的数。

又有一个显然的结论，多个相同的数，只有两端的数会对答案造成影响，所以最多不过记录 1420 个数。

然而如果就这么硬写的话，会 Tle 掉一个点。

考虑到两个相同的数，左端点影响右边的数，右端点影响左边的数，所以考虑分开来计算。

常数直接变成一半。

还有一个小坑点，就是这道题要向上取整。

```cpp

#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define ldo long double
#define dle double
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=5e5+7;
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
int n;
int a[N];
int hmax;
vector<pii>g;
bool vis[N];
unordered_map<int,bool>mp;
dle ans[N];
signed main(){
    n=read();
    up(i,1,n)a[i]=read(),hmax=max(hmax,a[i]);
    int lim=hmax-sqrt(n)-1;
    up(i,1,n){
        if(a[i]>=lim&&!mp.count(a[i])){
            mp[a[i]]=1;
            vis[i]=1;
            g.push_back({a[i],i});
        }
    }
    mp.clear();
    dn(i,n,1){
        if(vis[i])continue;
        if(a[i]>=lim&&!mp.count(a[i])){
            mp[a[i]]=1;
            g.push_back({a[i],i});
        }
    }
    sort(g.begin(),g.end());
    g.push_back({-1,0});
    up(i,0,g.size()-2){
        int w=g[i].first,nxt=g[i+1].first;
        if(w!=nxt){
            int pos=g[i].second;
            up(j,1,n){
                ans[j]=max(ans[j],(dle)sqrt(abs(pos-j))+a[pos]-a[j]);
            }
        }  
        else {
            int pos1=g[i].second,pos2=g[i+1].second;
            int mid=(pos1+pos2)>>1;
            up(j,1,mid){
                ans[j]=max(ans[j],(dle)sqrt(abs(pos2-j))+a[pos2]-a[j]);
            }
            up(j,mid,n){
                ans[j]=max(ans[j],(dle)sqrt(abs(pos1-j))+a[pos2]-a[j]);
            }
            i++;
        }
    }
    up(i,1,n)write((int)ceil(ans[i]),1);
    return 0;
}
```