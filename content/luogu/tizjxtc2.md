$T2$

考场代码
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=1e9+7;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9') {x=(x<<1)+(x<<3)+ch-'0';ch=getchar();}
	return x*f;
}
int n,a[100500],ans,f[100500];
inline int ksm(int a,int b){
	int res=1;
	while(b){
		if(b&1)res=(res*a)%mod;
		a=(a*a)%mod;
		b>>=1;
	}
	return res;
}
inline int work(int i,int j){
	int k;
	k=f[i];
	if(n-j==0)return k;
	return f[i]*f[n-j]%mod;
}
inline void init(){
	for(int i=0;i<=n;i++){
		if(i==0||i==1)f[i]=2;
		else f[i]=ksm(2,i);
	}
}
signed main(){
	n=read();
	for(int i=0;i<=n;i++)a[i]=read();
	init();
	for(int i=0;i<=n;i++){
		for(int j=i+1;j<=n;j++){
			ans=(ans+(a[i]*a[j]%mod)*work(i,j))%mod;
		}
	}
	printf("%lld",ans);
	return 0;
}
```
有两个$SB$的点

$1.$求$2$的次幂用快速幂

$2.$for循环里可以简化

```cpp
for(int i=0;i<=n;i++){
		for(int j=i+1;j<=n;j++){
			ans=(ans+(a[i]*a[j]%mod)*work(i,j))%mod;
		}
	}
```
简化一下,$po$是$2$的次幂

```cpp
for(int i=0;i<n;i++){
		for(int j=i+1;j<=n;j++){
			ans=(ans+a[i]*f[i]*a[j]*po[n-j])%mod;
		}
	}
```
在提一下公约数

```cpp
for(int i=0;i<n;i++){
		int tmp=a[i]*f[i]%mod,k=0;
		for(int j=i+1;j<=n;j++)k=(k+a[j]*po[n-j])%mod;
		ans=(ans+k*tmp)%mod;
	}
```
于是可以求出前缀和，快速求$k$;
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=1e9+7;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9') {x=(x<<1)+(x<<3)+ch-'0';ch=getchar();}
	return x*f;
}
int n,a[100500],ans,f[100500],po[100500],s[100500],sum[500500];
inline int ksm(int a,int b){
	int res=1;
	while(b){
		if(b&1)res=(res*a)%mod;
		a=(a*a)%mod;
		b>>=1;
	}
	return res;
}
inline int work(int i,int j){
	int k;
	k=f[i];
	if(n-j==0)return k;
	return f[i]*f[n-j]%mod;
}
inline void init(){
	f[0]=2;f[1]=2;
	po[0]=1;po[1]=2;
	for(int i=2;i<=n;i++){
		f[i]=2*f[i-1]%mod;
		po[i]=f[i];
	}
}
signed main(){
	//freopen("num.in","r",stdin);
	//freopen("num.out","w",stdout);
	n=read();
	sum[n+1]=1;
	for(int i=0;i<=n;i++)a[i]=read();
	init();
	for(int i=1;i<=n;i++){
		s[i]=a[i]*po[n-i]%mod;
	}
	sum[0]=1;
	for(int i=1;i<=n;i++)sum[i]=(sum[i-1]+s[i])%mod;
	for(int i=0;i<n;i++){
		int tmp=a[i]*f[i]%mod;
		int k=((sum[n]-sum[i])%mod+mod)%mod;
		ans=(ans+k*tmp)%mod;
	}
	printf("%lld",ans);
	return 0;
}
```
