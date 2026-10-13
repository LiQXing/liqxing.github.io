## [Cow Program ](https://www.luogu.com.cn/problem/CF283B)

记忆化搜索。

$dp[0][u]$ 表示到达 $u$ 点进行2操作。
$dp[1][u]$ 表示到达 $u$ 点进行3操作。

此题的难点在于，如何利用以前的计算判圈

于是可用两个数组记录是否出发过，是否已回去的状态。

## [Zero Tree](https://www.luogu.com.cn/problem/CF274B)

因为是一棵树，所以有着良好的结构。

对于每一颗子树考虑变为0需要加减多少次。

就是把下面子树取 $\max$ 然后再对单点进行修改。

## [Dima and Two Sequences](https://www.luogu.com.cn/problem/CF272D)

```cpp
int n;
int a[N],b[N],ans=1;
unordered_map<int,int>mp,f,mp1;
inline int getsum(int maxn,int cnt){
	int sum=1;
	for(int i=1;i<=maxn;i++){
		if(i%2==0&&cnt) sum=sum*i/2%mod,cnt--;
		else sum=sum*i%mod;
	}
	return sum;
}
signed main(){
	n=read();
	up(i,1,n)a[i]=read();
	up(i,1,n)b[i]=read();
	mod=read();
	up(i,1,n){
		mp[a[i]]++;
		mp[b[i]]++;
		if(a[i]==b[i])f[a[i]]++;
	}
	up(i,1,n){
		if(!mp1[a[i]]){
			ans=ans*getsum(mp[a[i]],f[a[i]])%mod;
			mp1[a[i]]=1;
		}
		if(!mp1[b[i]]){
			ans=ans*getsum(mp[b[i]],f[b[i]])%mod;
			mp1[b[i]]=1;
		}
	}
	cout<<ans;
	return 0;
}
```

## [Alternating Current](https://www.luogu.com.cn/problem/CF343B)
求出最长上升子序列就行。

## [Maxim and Restaurant](https://www.luogu.com.cn/problem/CF261B)

设 $f(i,j,k)$ 表示表示已经处理完前 $i$ 个人选了 $j$ 个人占了$k$这么长的方案数，那么答案显然是：

$ans=n!\sum f(n,i,j)×i!×(n−i)!$​

对于 $f(i,j,k)$我们有两个策略，一个是选，一个是不选，得出：

$f(i,j,k)=f(i−1,j−1,k−a[i])+f(i−1,j,k)$


## [Little Elephant and Elections ](https://www.luogu.com.cn/problem/CF258B)

数位DP。
$g[i]$ 表示有 $i$ 个4或7。
```cpp
int m,f[15][15],g[15],dit[15];
inline int dp(int step,int r,int lim){
	if(step==0)return r==0;
	if(!lim&&~f[step][r])return f[step][r];
	int x=lim?dit[step]:9,res=0;
	for(int i=0;i<=x;i++){
		if(i==4||i==7){
			if(r==0)continue;
			(res+=dp(step-1,r-1,lim&&i==x))%mod;
			continue;
		}
		res+=dp(step-1,r,lim&&i==x);
	}
	if(!lim)f[step][r]=res;
	return res;
}
inline int dfs(int step,int r,int mul){
	if(step==0)return mul;
	int res=0;
	for(int i=0;i<=r;i++){
		if(g[i]){
			g[i]--;
			(res+=dfs(step-1,r-i,mul*(g[i]+1)%mod))%mod;
			g[i]++;
		}
	} 
	return res;
}
signed main(){
	memset(f,-1,sizeof f);
	m=read();
	int len=0;
	while(m)dit[++len]=m%10,m/=10;
	up(i,0,len) g[i]=dp(len,i,1);
	g[0]--;
	int ans=0;
	up(i,1,len) (ans+=g[i]*dfs(6,i-1,1)%mod);
	printf("%d\n",ans);
	return 0;
}
```
## [Mr. Bender and Square](https://www.luogu.com.cn/problem/CF255D)

简单二分题。

二分答案然后减去超出方格的部分，还要加上四角重叠的部分

## [Playing with Permutations](https://www.luogu.com.cn/problem/CF251B)

首先不考虑恰好 $k$ 次，而只考虑能否达到。可以发现给出的两次操作其实是互为逆元的（换句话说，在进行了操作一后进行操作二就相当于啥都没做），所以最后的答案一定是重复操作一或者操作二若干次而不可能同时出现操作一和操作二。

在已经进行了 $m$ 次操作的前提下，可以通过在两个操作中反复横跳的方法解决任意为偶数的剩下次数。
```cpp
int n,k;
bool flag;
int p[N],s[N],q[N],now[N],p2[N],now2[N];
inline void check(){
	up(i,1,k-1){
		up(j,1,n) now2[j]=now[p[j]];
		up(j,1,n) now[j]=now2[j];
		flag=1;
		up(j,1,k)if(now[j]!=s[j])flag=0;
		if(flag){
			printf("NO\n");
			return;
		}
	}
	up(j,1,n)now2[j]=now[p[j]];
	up(j,1,n)now[j]=now2[j];
	flag=1;
	up(j,1,k)if(now[j]!=s[j])flag=0;
	if(flag==0){printf("NO\n");return;}
	printf("YES\n");
}
signed main(){
	n=read();k=read();
	up(i,1,n)p[i]=read();
	up(i,1,n)s[i]=read();
	up(i,1,n)p2[p[i]]=i;
	up(i,1,n)now[i]=i;
	flag=1;
	up(i,1,n)if(s[i]!=now[i])flag=0;
	if(flag){
		printf("NO\n");
		return 0;
	}
	flag=1;
	for(int i=1;i<=n;i++)if(p[i]!=p2[i])flag=0;
	if(flag){
		check();
		return 0;
	}
	up(i,1,n) now[i]=i;
	up(i,1,k){
		up(j,1,n) now2[j]=now[p[j]];
		up(j,1,n) now[j]=now2[j];
		flag=1;
		up(j,1,k)if(now[j]!=s[j])flag=0;
		if(flag&&(k-i)%2==0){
			printf("YES\n");
			return 0;
		}		
	}
	up(i,1,n)now[i]=i;
	up(i,1,k) {
		up(j,1,n)now2[j]=now[p2[j]];
		up(j,1,n)now[j]=now2[j];
		flag=1;
		up(j,1,k)if(now[j]!=s[j])flag=0;
		if(flag&&(k-i)%2==0){
			printf("YES\n");
			return 0;
		}		
	}
	printf("NO\n");
	return 0;
}
```

## [Hydra](https://www.luogu.com.cn/problem/CF243B)
枚举每一条边，判断是否满足条件。



