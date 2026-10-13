## [Bath Queue](https://www.luogu.com.cn/problem/CF28C)

很有意思的期望DP。

  
我们令$dp[i][j][k]$为前$i$个房间去$j$个人，最长队列**恰好**为$k$的方案数，转移为当前房间进入$l$个人，由$i−1$转移而来。

因为人是不一样的，所以我们要从剩下的$n−j$人中选出$l$个人来，所以要乘上$C_{n−j}^l$。

```cpp
int n,m;
int a[N];
db fac[N];
inline void init(){
	fac[0]=1;
	up(i,1,50)fac[i]=fac[i-1]*i;
}
inline db C(int i,int j){
	if(i<j)return 0;
	return fac[i]/(fac[j]*fac[i-j]);
}
db dp[60][60][60],T,ans;
signed main(){
	n=read();m=read();
	init();
	up(i,1,m)a[i]=read();
	dp[0][0][0]=1;
	up(i,1,m){
		up(j,0,n){
			up(k,0,j){
				up(l,0,n-j){
					dp[i][j+l][max(((l+a[i]-1)/a[i]),k)] += dp[i-1][j][k]*C(n-j,l);
				}
			}
		}
	}
	up(i,0,n)T += dp[m][n][i];
	up(i,1,n)ans += i * dp[m][n][i] / T;
	printf("%.10f",ans);
	return 0;
}
```
​
## [Sequence of points](https://www.luogu.com.cn/problem/CF24C)

对称$2n$次之后坐标不变，所以只用观察这$2n$次的值就行了。

## [Deletion of Repeats](https://www.luogu.com.cn/problem/CF19C)

## [Jeremy Bearimy](https://www.luogu.com.cn/problem/CF1280C)

最小值：

对于最小值，即每条边的使用次数最小，那么对于以$u$为根节点的一棵树,设$v$是与它相连的子树的根，那么可以得到： **当子树的size为偶数时，我们完全可以让子树自己内部消化，而当子树的size为奇数时，则边$(u,v)$,一定会被经过**,所以我们可以得到对于最小值的计算方法。

最大值：
**那么，对于边$(u,v)$,我们的最多经过$min(size[v],n−size[v])$，换成语言说明即为这条边连接的两个子树的size最小值** 既然知道最多贡献次数了之后，那么其对于答案的贡献就为$min(size[v],n−size[v])∗e[i].val$。

## [Underground Lab](https://www.luogu.com.cn/problem/CF780E)

因为有 $2n$ 个点，可以看做dfs入和出两种情况。

```cpp

int n,m,k;
vector<int>g[N];
int dfn[N*3],tot;
bool vis[N];
inline void dfs(int u,int from){
	dfn[++tot]=u;
	vis[u]=1;
	for(auto v:g[u]){
		if(vis[v])continue;
		dfs(v,u);
		dfn[++tot]=u;
	}
}
vector<int>ans[N];
signed main(){
	n=read();m=read();k=read();
	int u,v;
	up(i,1,m){
		u=read();v=read();
		g[u].push_back(v);
		g[v].push_back(u);
	}
	dfs(1,0);
	int len=2*n/k+((2*n)%k!=0);
	up(i,1,tot)ans[i/len+1].push_back(dfn[i]);
	up(i,1,k){
		if(ans[i].size()==0)ans[i].push_back(1);
		write(ans[i].size(),0);
		for(auto v:ans[i]){
			write(v,0);
		}
		printf("\n");
	}
	return 0;
}
```






