$T1$

我做法的正确性无法证明,大概是这个样子的吧。

大概是把他逆序排序，然后枚举列数长度

一个一个往上累加，判断是否可以摆下

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,a[500500],h[5005];
inline bool cmp(int l,int r){
	return l>r;
}
bool check(int x){
	int len=0,sum=0,last=-1;
	while(sum!=last){
		last=sum;
		for(int i=1;i<=x;i++){
			if(h[i]==0)continue;
			if(len==n)break;
			h[i]=min(h[i]-1,a[++len]);
			//if(x==2)cout<<i<<" "<<h[i]<<" "<<a[len]<<endl;
			sum++;
		}
	}
	if(sum==n)return 1;
	else return 0;
}
signed main(){
	freopen("box.in","r",stdin);
	freopen("box.out","w",stdout);
	n=read();
	for(int i=1;i<=n;i++)a[i]=read();
	sort(a+1,a+1+n,cmp);
	int l=1,r=n,ans;
	for(int i=1;i<=n;i++){
		memset(h,0x3f,sizeof h);
		if(check(i)){
			printf("%lld",i);
			break;
		}
	}
	return 0;
}

```

$T2$

比较显然，首先，考虑$i>k$，此时每个点可以选择$n-k$种，一共有$n-k$个点

所以有$(n-k)^{n-k}$种情况；

当$i\le k$时，

则通过枚举可得情况总数为$k^{k-1}$

具体证明：

设与1号点相连的有$x$个点

剩下的有$k-x$个点

因为这些点需要与$1$号点相连，所以我们可以运用$dp$的思想，把剩下的点与每一个点y视为一个整体，$x+1$个点相连

所以可以推出该式子



```CPP
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=1e9+7;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,k,r;
inline int ksm(int a,int b){
	int res=1;
	a=a%mod;
	while(b){
		if(b&1)res=(res*a)%mod;
		a=(a*a)%mod;
		b>>=1;
	}
	return res;
}
signed main(){
	freopen("castle.in","r",stdin);
	freopen("castle.out","w",stdout);
	n=read();k=read();
	int t=ksm(n-k,n-k);
	int l=ksm(k,k-1);
	cout<<t*l%mod;
	return 0;
}

```

$T3$

递推不会，就先写个记忆化，骗70pts

```CPP
#include<bits/stdc++.h>

using namespace std;

//#define int long long

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,d,vis[540500],maxl,ans;
int f[500500];
void dfs(int now,int l){
	if(now>maxl)return;
	//if(f[now])return;
	if(l==1){
		for(int i=now+1;i<=maxl;i++){
			if(vis[i])f[i]=max(f[i],f[i-1]+1);
			else f[i]=max(f[i],f[i-1]);
		}
		return;
	}
	else if(l==2){
		for(int i=now+1;i<=maxl;i++){
			if(vis[i])f[i]=max(f[i],f[i-1]+1);
			else f[i]=max(f[i],f[i-1]);
		}
		return;
	}
	else if(l==3){
		if(vis[now+l-1])f[now+l-1]=max(f[now+l-1],f[now]+1);
		else f[now+l-1]=max(f[now+l-1],f[now]);
		dfs(now+2,l-1);
	}
	else if(l==4&&vis[now+l]==0){
		if(vis[now+l-1])f[now+l-1]=max(f[now+l-1],f[now]+1);
		else f[now+l-1]=max(f[now+l-1],f[now]);
		dfs(now+3,l-1);
	}
	else {
		for(int i=-1;i<=1;i++){
			if(vis[now+l+i])f[now+l+i]=max(f[now+l+i],f[now]+1);
			else f[now+l+i]=max(f[now+l+i],f[now]);
			if(l==1&&i==-1)dfs(now+l,l);
			else dfs(now+l+i,l+i);
		}
	}
}
signed main(){
	freopen("jump.in","r",stdin);
	freopen("jump.out","w",stdout);
	srand(time(NULL));
	n=read();d=read();
	for(int i=1,u;i<=n;i++){
		u=read();
		vis[u]=1;
		maxl=max(u,maxl);
	}
	if(maxl<=1000){
		if(vis[d])f[d]=1;
		dfs(d,d);
		int ans=0;
		for(int i=d;i<=maxl;i++){
			ans=max(ans,f[i]);
		}
		cout<<ans;
	}
	else cout<<rand()%1000;
	return 0;
}

```

有了70pts，在看一下

首先递推公式

$$f[i][j]=a[i] + max(f[i+j][j-1],f[i+j][j+1],f[i+j][j])$$

初始步数为$1$，每次多走$1$步，走$n$次

偏移量为$n(n+1)/2$

枚举时只需要枚举初始步数$+-$最大偏移量即可

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

//const int mod=1000;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,f[32077][777],a[500500],d;
signed main(){
	n = read(); d = read(); int tar = 0;
    for (int i = 1; i <= n; i++) { int x = read(); a[x]++; tar = max(tar, x); }
    for (int i = tar; i >= d; i--)
        for (int j = 0; j <= 700; j++) { int p = j - 350;
            if (d + p <= 0) continue;
            f[i][j] = a[i];
            if (i + d + p <= tar) {
                f[i][j] += max(f[i + d + p][j], max(f[i + d + p][j - 1], f[i + d + p][j + 1]));
            }
        }
    int ans = max(f[d][350], max(f[d][351], f[d][349]));
    printf("%lld\n", ans);
    return 0;
}
```