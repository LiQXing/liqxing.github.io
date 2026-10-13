```
既不会DP，又不会优化
```
斜率优化指转移方程有以下的形式：

$$dp[i]=\min/\max(a[i]\times b[j]+c[i]+d[j]+C)$$

可以使用斜率优化。

 [$T1$](https://www.luogu.com.cn/problem/T345410)

显然有
$$f[i]=\min(f[j]+(sum[i]-sum[j])^2+m)\quad j<i$$
$$f[i]=f[j]+sum[i]^2+sum[j]^2-2sum[i]sum[j]+m$$
$$2sum[i]sum[j]+f[i]-sum[i]^2-m=f[j]+sum[j]^2$$
令

 1. $k=2sum[i]$
 2. $x=sum[j]$
 3. $b=f[i]-sum[i]^2-m$
 4. $y=f[j]+sum[j]^2$
$$y=kx+b$$

求最大的$b$。

因为$k$单增,所以只用维护下凸包就行了。
```cpp
int n,m;
int a[N],sum[N];
int q[N];
int dp[N];
inline int Y(int i){
	return dp[i]+sum[i]*sum[i];
}
inline int X(int i){
	return sum[i];
}
inline db slope(int i,int j){
	if(X(i)==X(j))return 1e18;
	return 1.0*(Y(i)-Y(j))/(X(i)-X(j));
}
signed main(){
    n=read();m=read();
	up(i,1,n)a[i]=read(),sum[i]=sum[i-1]+a[i];
	int h=1,t=1;
	up(i,1,n){
		while(h<t&&slope(q[h],q[h+1])<=2*sum[i])h++;
		int j=q[h];
		dp[i]=dp[j]+(sum[i]-sum[j])*(sum[i]-sum[j])+m;
		while(h<t&&slope(q[t],q[t-1])>=slope(q[t-1],i))t--;
		q[++t]=i;
	}
	cout<<dp[n];
	return 0;
}
```


[$T2$](https://www.luogu.com.cn/problem/P3195)

暴力非常好想。
```cpp
	up(i,1,n){
		up(j,0,i-1){
			int len=sum[i]-sum[j]+i-j-1;
			f[i]=min(f[i],f[j]+(len-l)*(len-l));
		}
	}

```

$$f[i]=\min(f[j]+(sum[i]-sum[j]+i-j-1-l)^2)$$

另 $sum[i]+i=a[i]，sum[i]+i+l+1=b[i]$ 则原式为 
$$f[i]=\min(f[j]+(a[i]-b[j])^2)$$

$$f[i]=f[j]+a[i]^2-2a[i]\times b[j]+b[j]^2$$

$$2a[i]\times b[j]+f[i]-a[i]^2=f[j]+b[j]^2$$

 - $k=2a[i]$
 - $x=b[j]$
 - $b=f[i]-a[i]^2$
 - $y=f[j]+b[j]^2$
 
 
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

int f[N],sum[N];
int q[N];
int n,l;
inline int a(int i){return sum[i]+i;}
inline int b(int i){return a(i)+l+1;}
inline int X(int i){return b(i);}
inline int Y(int i){return f[i]+b(i)*b(i);}
inline db slope(int i,int j){return 1.0*(Y(i)-Y(j))/(X(i)-X(j));}
signed main(){
	n=read();l=read();
	up(i,1,n){
		sum[i]=read();
		sum[i]+=sum[i-1];
	}
	memset(f,0x3f,sizeof f);
	f[0]=0;
	int h=1,t=1;
	up(i,1,n){
		while(h<t&&slope(q[h],q[h+1])<=2*a(i)) ++h;
        f[i]=f[q[h]]+(a(i)-b(q[h]))*(a(i)-b(q[h]));
        while(h<t&&slope(i,q[t-1])<=slope(q[t-1],q[t]))--t;
        q[++t]=i;
	}
	cout<<f[n];
	return 0;
}
```
[$T3$](https://www.luogu.com.cn/problem/P3628)

这道题与前面两道题不同的是这道题求的是上凸包.

```cpp
int n;
int a,b,c;
int f[N],x[N],sum[N],q[N];
inline int clac(int x){
	return a*x*x+b*x+c;
}
#define k(A) (2*a*sum[A])
#define x(A) sum[A]
#define b(A) (f[A]-a*sum[A]*sum[A]-b*sum[A]-c)
#define y(A) (f[A]+a*sum[A]*sum[A]-b*sum[A])
double slope(int i,int j){
    return 1.0*(y(i)-y(j))/(x(i)-x(j));
}
signed main(){
	n=read();
	a=read();b=read();c=read();
	up(i,1,n){
		x[i]=read();
		sum[i]=sum[i-1]+x[i];
	}
	memset(f,-0x3f,sizeof f);
	f[0]=0;
	int h=0,t=0;
	up(i,1,n){
		while(h<t&&slope(q[h],q[h+1])>=2*a*sum[i])h++;
        f[i]=-(k(i)*x(q[h])-y(q[h])-a*sum[i]*sum[i]-b*sum[i]-c);
        while(h<t&&slope(q[t-1],q[t])<=slope(q[t],i))t--;
        q[++t]=i;
	}
	cout<<f[n];
	return 0;
}
```