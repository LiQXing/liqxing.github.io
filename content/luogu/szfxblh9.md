$T1$

考虑DP，有一种非常快的方法。

已知一个点的排名，还有与他相同排名的点的个数。

把每个点的排名区段求出来，并用vector存起来。

然后把每个点都进行排序。

有一个非常显然的Dp方程。

$$dp[r]=\max (dp[r],dp[l-1]+num)$$

然后就结束了。

dp复杂度为$O(n)$,瓶颈主要在排序

一些坑点：

1.写逆推不要写正推，如果写正推的话，状态的传递会变得非常困难，要是没写好就会像我一样想出了这个方程却写挂。



```cpp

#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ldo long double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

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
int n;
int len=0;
vector<int>g[N];
int dp[N];
signed main(){
	n=read();
	int l,r;
	int cnt=0;
	up(i,1,n){
		l=read()+1;r=n-read();
		if(r<l)continue;
		g[r].push_back(l);
	}
	up(i,1,n)sort(g[i].begin(),g[i].end());
	up(i,1,n){
		dp[i]=dp[i-1];
		int num=0;
		for(int j=0;j<g[i].size();j++){
			if(j!=0)if(g[i][j]!=g[i][j-1])num=0;
			num++;
			if(num<=i-g[i][j]+1){
				dp[i]=max(dp[i],dp[g[i][j]-1]+num);	
			}	
		}
	}
	cout<<n-dp[n]<<endl;
	return 0;
}
```
$T2$

应该算的上一道期望$DP$

设

$$dp[i]=dp[i-1]+\Delta$$

当 $k=3$ 时

$\Delta=((x+1)^3-x^3)p[i]=(3x^2+3x+1)p[i]$

当 $k=2$ 时

$\Delta=((x+1)^2-x^2)p[i]=(2x+1)p[i]$

······

所以，用$x[i]$表示$x^i$

可以解决。


```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ldo long double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

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
int n,k;
int c[10][10]={
	{1,0,0,0},
	{1,1,0,0},
	{1,2,0,0},
	{1,3,3,0},
	{1,4,6,4,1}
};
ldo p[N],dp[N],x[5];
signed main(){
	n=read();k=read();
	up(i,1,n){
		scanf("%LF",&p[i]);
	}
	up(i,1,n){
		dp[i]=dp[i-1]+p[i]*(c[k][1]*x[1]+c[k][2]*x[2]+c[k][3]*x[3]+1);
		x[3]=(x[3]+3*x[2]+3*x[1]+1)*p[i];
		x[2]=(x[2]+2*x[1]+1)*p[i];
		x[1]=(x[1]+1)*p[i];
	}
	printf("%LF",dp[n]);
	return 0;
}
```
$T3$

暴力很轻松有60pts

首先很容易想到的是把每个旋转点给标记出来。

每个点都有一个优先级，这个点的优先级等于所有没有打上标记的点的乘积。

可以自己手摸几组数据

之后就简单了。

像求等价于求平衡树第k大

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ldo long double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

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
int n,k;
int c[50][50];
int r[5000],cnt;
bool vis[5050];
int g[50][50];
inline int calc(){
	int res=1;
	up(i,1,cnt){
		if(!vis[i])res*=r[i];
	}
	return res;
}
signed main(){
	n=read();k=read();
	k=(1ll<<(n*n/2))-k+1;
	int x,y;
	up(i,1,n){
		up(j,1,n){
			if(!c[i][j]){
				r[++cnt]=4;
				x=i;y=j;
				up(i,1,4){
					c[x][y]=cnt;
					x=n-x+1;
					swap(x,y);
				}
			}
		}
	}
	int tmp;
	up(i,1,n){
		up(j,1,n){
			if(!vis[c[i][j]]){
				vis[c[i][j]]=1;
				tmp=calc();
				if(tmp>=k)g[i][j]=1;
				else{
					k-=tmp;
					r[c[i][j]]--;
					vis[c[i][j]]=0;
				}
			}
		}
	}
	up(i,1,n){
		up(j,1,n){
			printf("%lld",g[i][j]);
		}
		printf("\n");
	}
	return 0;
}
```