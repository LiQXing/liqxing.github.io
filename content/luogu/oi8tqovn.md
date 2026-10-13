$T1$

解析：简单的$ gcd $

每次将$ a,b$ 两个数变成 $a-b,b$，这一过程就是辗转相除法，用欧几里得算法模拟辗转相除法即可。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

inline int  read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int sum;
inline void gcd(int a,int b){
	if(b==0)return;
	sum+=a/b;
	//cout<<sum<<endl;
	gcd(b,a%b);
}
signed main(){
	freopen("sword.in","r",stdin);
	freopen("sword.out","w",stdout);
	int T=read();
	int a,b;
	while(T--){
		sum=0;
		a=read();b=read();
		if(a<b)swap(a,b);
		gcd(a,b);
		printf("%lld\n",sum-1);
	}
	return 0;
}

```

$T2$

简单的双向搜索，警钟撅烂，注意数组下表不要让他为负数，不然会十个$Re$，

个人推荐$map$

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int ze=1e8;

inline int  read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n;
int a[6][500];
map<int,bool>mp;
inline void dfs(int step,int sum){
	if(step==3){
		mp[sum]=1;
		return ;
	}
	for(int i=1;i<=n;i++){
		dfs(step+1,sum+a[step][i]);
	}
}
inline void dfs2(int step,int sum){
	if(sum>ze*2)return;
	if(step==6){
		if(mp[-sum]){
			printf("YES");
			exit(0);
		}
		return ;
	}
	for(int i=1;i<=n;i++){
		dfs2(step+1,sum+a[step][i]);
	}
}
signed main(){
	n=read();
	for(int i=1;i<=5;i++){
		for(int j=1;j<=n;j++){
			a[i][j]=read();
		}
	}
	dfs(1,0);
	dfs2(3,0);
	printf("NO\n");
	return 0;
}
```

$T3$

首先，可以合成$2048$的数一定是$2$的幂次，将其提出

一个小推论，$2$ 的幂次和只要大于等于$2048$ 就一定能合成$2048$

一点小小的证明：

设和为$sum$

由于合并的性质，所以2的每个幂次系数要么是$0$，要么是$1$

因为sum一定可化为2进制表示

所以当$sum \ge 2048$时二进制位大于$11$位的数一定有1，

又因为给出的$a[i] \le 2048$所以当和大于$2048$时，一定可以合成$2048$

$QED.$


用一个简单的dp求出2的幂次小于$2048$的组合有多少种

再用整体减去局部可得值

因为总序列数为 $2^n$



```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=998244353;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,ans,len;
int a[500500],num[500500];
inline int ksm(int x,int y){
	int res=1;
	while(y){
		if(y&1)res=(res*x)%mod;
		x=(x*x)%mod;
		y>>=1;
	}
	return res;
}
int vis[2077];
int dp[500500];
int sum,sum2;
signed main(){
	n=read();
	int t;
	for(int i=1;i<=n;i++){
		a[i]=read();
		//vis[a[i]]++;
		t=2048;
		while(a[i]!=t&&t){
			t/=2;
		}
		if(t==0)sum++;
		else num[++len]=a[i],sum2+=a[i];
	}
	sum=ksm(2,sum);
	dp[0]=1;
	//cout<<len<<" "<<sum2<<endl;
	for(int i=1;i<=len;i++){
		for(int j=2047;j>=num[i];j--){
			dp[j]=(dp[j]+dp[j-num[i]])%mod;
		}
	}
	for(int i=0;i<=2047;i++){
		ans=(dp[i]+ans)%mod;
	}
	t=ksm(2,n);
	int l=ans*sum%mod;
	cout<<(t-l+mod)%mod<<endl;
	return 0;
}
```