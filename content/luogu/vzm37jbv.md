其实是个简单模拟题，我写的可能有些复杂。

对于一个点 $x$，答案的情况分为两个部分，儿子和其他点。

对于儿子，可以暴力硬求，枚举第 $k$ 层最小的儿子和最大的儿子，然后进行判断。

其他节点，你可以一步一步向上爬，如果该点是右儿子，那么查找左儿子，反之亦然。
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int i128
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
const int mod=998244353;
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
int n,k;
inline int ksm(int a,int b){
    int res=1;
    while(b){
        if(b&1)res=res*a;
        a=a*a;
        b>>=1;
    }
    return res;
}
int len,dep;
inline int clac(int x,int pos){
    if(x==0)return 1;
    x--;
    int u=pos*2+1;
    int l=u,r=u;
    if(x>=62)return 0;
    up(i,1,x){
        l=l*2;
        r=r*2+1;
    }
    if(r<=n)return (r-l+1);
    if(l>n)return 0;
    return n-l+1;
}
inline int clac2(int x,int pos){
    if(x==0)return 1;
    x--;
    int u=pos<<1;
    int l=u,r=u;
    if(x>=62)return 0;
    up(i,1,x){
        l=l*2;
        r=r*2+1;
    }
    if(r<=n)return (r-l+1);
    if(l>n)return 0;
    return n-l+1;
}
int x;
signed main() {
    //ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0); 
    int T;
    T=read();
    while(T--){
        n=read();x=read();k=read();
        len=0,dep=0;//len表示这棵树有多少层是满二叉树，dep表示在第几层
        up(i,0,63){
            if((1ll<<i)-1<n&&(1ll<<(i+1))-1>=n){
                len=i;
            }
            if((1ll<<i)-1<x&&(1ll<<(i+1))-1>=x){
                dep=i+1;
            }
        }
        if(k==0){
            cout<<1<<endl;
            continue;
        }
        int upp=0,down=0;//upp表示x点上方有多少个节点距离为k，down表示下方有多少个点距离为k
        int w=k,pos=x,pre=x;
        while(pos!=1){//不停的升到父亲节点，如果该点是右儿子，那么查找左儿子，反之亦然
            pos/=2;w--;
            if(w<0)break;
            if(pre==pos*2)upp+=clac(w,pos);
            else if(pre==pos*2+1)upp+=clac2(w,pos);
            pre=pos;
        }
        int l=x,r=x;
        if(k>=62){
            down=0;
            goto F;
        }
        up(i,1,k){
            l=l*2;
            r=r*2+1;
        }
        if(r<=n)down=(r-l+1);
        else if(l>n)down=0;
        else down=n-l+1;
        F:;
        write(upp+down,1);    
    }
    return 0;
}
```