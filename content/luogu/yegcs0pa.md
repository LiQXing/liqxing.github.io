
[题目](https://www.luogu.com.cn/training/244301#problems)

## $e$

这道题 n 很小， W 很大，V却很小。

把重量 w 和价值 v 颠倒，来求

计算完所有状态的值后，只需要选取满足重量上限的最大价值即可。

## $i$

比较典型的期望 DP 。

$f[i][j]$ 指抛第 $i$ 个硬币有 $j$ 个正面朝上。

$f[i][j]=f[i-1][j-1]*p+f[i-1][j]*(i-p)$

## $j$

因为是任选盘子，不用考虑顺序。

$f[i][j][k][l]$  分别表示有 $i$ 个空盘子，$j$  个一个寿司  $k$  个两个寿司，$l$  个三个寿司的盘子。

$$f[i][j][k][l]=1+\frac{i}{n}f[i][j][k][l]+\frac{j}{n}f[i+1][j-1][k][l]+\frac{k}{n}f[i][j+1][k-1][l]+\frac{l}{n}f[i][j][k+1][l-1]$$

$$f[i][j][k][l]=\frac{n}{j+k+l}+\frac{j}{j+k+l}f[i+1][j-1][k][l]+\frac{k}{j+k+l}f[i][j+1][k-1][l]+\frac{l}{j+k+l}f[i][j][k+1][l-1]$$

但是这样空间会炸掉。

因为知道一共有多少个盘子，所以可以压掉一维。

$$f[j][k][l]=\frac{n}{j+k+l}+\frac{j}{j+k+l}f[j-1][k][l]+\frac{k}{j+k+l}f[j+1][k-1][l]+\frac{l}{j+k+l}f[j][k+1][l-1]$$

```cpp
signed main(){
	n=read();
	up(i,1,n){
		a[i]=read();
		cnt[a[i]]++;
	}
	up(k,0,n){
		up(j,0,n){
			up(i,0,n){
				if(!i&&!j&&!k)continue;
				if(i)f[i][j][k]+=f[i-1][j][k]*i/(i+j+k);
				if(j)f[i][j][k]+=f[i+1][j-1][k]*j/(i+j+k);
				if(k)f[i][j][k]+=f[i][j+1][k-1]*k/(i+j+k);
				f[i][j][k]+=(double)n/(i+j+k);
			}
		}
	}
	printf("%.10LF",f[cnt[1]][cnt[2]][cnt[3]]);
	return 0;
}
```

##  $l$

可以一眼看出，这是一道区间 DP。

这道题的做法其实还是挺巧妙的。

另 `dp[l][r]` 带表一个区间`[l,r]`可获得的最大值，那么另一个人获得的价值就是 `sum[r]-sum[l-1]-dp[l][r]`

$$dp[i][j]=\max(sum[j]-sum[i-1]-dp[i+1][j],sum[j]-sum[i-1]-dp[i][j-1])$$

## $m$

经典的 **dp + 前缀和优化**。

看题一眼，一个 $nk^2$ 的 dp 就出来了。



```cpp
	dp[0][0]=1;
	up(i,1,n){
		up(j,0,m){
			up(l,0,a[i]){
				if(j-l<0)break;
				dp[i][j]+=dp[i-1][j-l];
			}
		}
	}
	cout<<dp[n][m];
```

观察代码，我们发现对于每一个`dp[i][j]` , 其加上的都是`[dp[i-1][0],dp[i-1][a[i]]]`，这些的区间和。

所以可以前缀和优化。

```cpp
int n,num;
int dp[105][N],a[N],sum[N],s[N];
inline int getsum(int l,int r){
	return (l==0?s[r]:(s[r]+mod-s[l-1])%mod);
}
signed main(){
	n=read();num=read();
	dp[0][0]=1;
	up(i,1,n)a[i]=read(),sum[i]=sum[i-1]+a[i];
	up(i,1,n){
		s[0]=dp[i-1][0];
		up(k,1,num)s[k]=(s[k-1]+dp[i-1][k])%mod;
		up(j,0,num){
			dp[i][j]=getsum(max(0ll,j-a[i]),j);
		}
	}
	cout<<dp[n][num]<<endl;
	return 0;
}
```

## $n$ 

石子合并。

## $p$

树上 DP。

对于点 $u$

$$dp[u][0]=\prod dp[v][1],dp[u][1]=\prod (dp[v][1]+dp[v][0])$$

## $q$

求权值最大上升子序列。

经典的 DS 优化 dp

dp 方程很一眼。

$$f[i]=\max(f[j]+a[i])\quad h[j]<h[i]$$

那么如何快速求出最大的 $f[j]$。

我们可以考虑用树状数组。
```cpp
inline int lowbit(int x){
	return x&(-x);
}
inline void add(int pos,int w){
	for(int i=pos;i<=N;i+=lowbit(i)){
		tr[i]=max(tr[i],w);
	}
}
inline int ask(int pos){
	int res=0;
	for(int i=pos;i>0;i-=lowbit(i)){
		res=max(res,tr[i]);
	}
	return res;
}
signed main(){
	n=read();
	up(i,1,n)a[i].h=read();
	up(i,1,n)a[i].w=read();
	f[0]=0;
	up(i,1,n){
		f[i]=ask(a[i].h-1)+a[i].w;
		add(a[i].h,f[i]);
	}
	int ans=0;
	up(i,1,n){
		ans=max(ans,f[i]);
	}
	cout<<ans;

```

## $s$

数位 DP 水题。

```cpp
inline int dfs(int pos,int sum,int lead,int lim){
	if(!pos)return sum%d==0;
	if(f[pos][sum]!=-1&&!lim&&!lead)return f[pos][sum]%mod;
	int ret=0,res=lim?num[pos]:9;
	up(i,0,res){
		if(lead&&!i)ret+=dfs(pos-1,(sum+i)%d,lead&!i,lim&(i==res));
		else ret+=dfs(pos-1,(sum+i)%d,lead&!i,lim&(i==res));
	}
	ret%=mod;
	if(!lim&&!lead)f[pos][sum]=ret;
	return ret;
}
string a;
inline int dp(string x){
	len=0;
	memset(f,-1,sizeof f);
	int slen=x.size();
	dn(i,slen-1,0)num[++len]=x[i]-'0';
	return dfs(len,0,1,1);
}
```

## $t$

直接DP会超时。

考虑前缀和优化。

```cpp
	dp[1][1]=1;
	up(i,2,n){
		if(s[i-2]=='<'){
			up(j,1,i)dp[i][j]=(dp[i][j-1]+dp[i-1][j-1])%mod;
		}
		else{
			dn(j,i-1,1)dp[i][j]=(dp[i][j+1]+dp[i-1][j])%mod;
		}
	}
	up(i,1,n)ans=(ans+dp[n][i])%mod;
	cout<<ans<<endl;
```

## $u$

看数据范围，状压DP非常明显。

直接状压就行了。

## $w$

对于这种区间的命令，一种常见的做法是**化区间为点**。

具体来说，就是按照右端点排序，当**访问到某个区间的右边界时才计算其贡献**。

$dp[i][j]$ 表示考虑到第 $i$ 个位置，上一个 0 在 $j$ 处的最大分数。

$O(n^3)$ 暴力就出来了。

考虑优化，把每次修改都丢线段树上去。

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

const int N=5e5+5000;
const int mod=1e9+7;

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
struct node{
	int l,r,w;
}a[N];
int n,m;
vector<node>g[N];
struct SegmentTree{
	int maxn[N<<2],tag[N<<2];
    void change(int p,int k){
        maxn[p]+=k;tag[p]+=k;
    }
    void push_down(int p){
        if(!tag[p]) return ;
        change(p<<1,tag[p]);
        change(p<<1|1,tag[p]);
        tag[p]=0;
    }
    void change(int p,int l,int r,int x,int y,int k){
        if(x<=l&&r<=y){change(p,k);return ;}
        push_down(p);
		int mid=(l+r)>>1;
        if(x<=mid) change(p<<1,l,mid,x,y,k);
        if(y>mid) change(p<<1|1,mid+1,r,x,y,k);
        maxn[p]=max(maxn[p<<1],maxn[p<<1|1]);
    }
}T;
signed main(){
	n=read();m=read();
	int l,r,w;
	up(i,1,m){
		l=read();r=read();w=read();
		a[i]={l,r,w};
		g[r].push_back(a[i]);
	}
	for(int i=1;i<=n;i++){
        T.change(1,1,n,i,i,max(T.maxn[1],0ll));
        for(auto it:g[i])T.change(1,1,n,it.l,i,it.w);
    }
    cout<<max(T.maxn[1],0ll)<<'\n';
	return 0;
}
```
## $x$

非常奇怪的一道贪心题。

使用贪心的思想。对于两个箱子 $i,j$，第 $i$ 个箱子若要比第 $j$ 个箱子优先考虑，显然应令 $i$ 上方除 $j$ 以外能放的箱子总质量 $s_i​−w_j$​ 大于 $j$ 上方除 $i$ 以外能放的箱子总质量 $s_j​−w_i$​。

所以可以以此来排序。

```cpp
int n;
struct node{
	int w,s,v;
}a[N];
int f[N];
inline bool cmp(node x,node y){
	return x.s+x.w<y.s+y.w;
}
signed main(){
	n=read();
	up(i,1,n){
		a[i].w=read();
		a[i].s=read();
		a[i].v=read();
	}
	memset(f,-0x3f,sizeof f);
	f[0]=0;
	sort(a+1,a+1+n,cmp);
	up(i,1,n){
		dn(j,a[i].s,0){
			f[j+a[i].w]=max(f[j+a[i].w],f[j]+a[i].v);
		}
	}
	int ans=0;
	up(i,0,20000)ans=max(ans,f[i]);
    write(ans,1);
	return 0;
}

```

## $y$

挺水的，就是暴力判断影响。

## $z$

很水的斜率优化。

```cpp
int f[N],sum[N];
int q[N],a[N];
int n,l;
inline int X(int i){return a[i];}
inline int Y(int i){return f[i]+a[i]*a[i];}
inline db slope(int i,int j){return 1.0*(Y(i)-Y(j))/(X(i)-X(j));}
signed main(){
	n=read();l=read();
	up(i,1,n){
		a[i]=read();
	}
	memset(f,0x3f,sizeof f);
	f[1]=0;
	int h=1,t=1;q[1]=1;
	up(i,2,n){
		while(h<t&&slope(q[h],q[h+1])<=2*a[i]) ++h;
        f[i]=f[q[h]]+(a[i]-a[q[h]])*(a[i]-a[q[h]])+l;
        while(h<t&&slope(i,q[t-1])<=slope(q[t-1],q[t]))--t;
        q[++t]=i;
	}
	cout<<f[n];
	return 0;
}
```










