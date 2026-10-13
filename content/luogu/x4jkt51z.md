这次考试有什么好写的呢？

$T1$

差分约束，但是不能一遍$spfa$直接 $ dis[i]-dis[j] $,

看n的范围$n\le200$,考虑弗洛伊德更新二维$dis$数组。

```cpp
int main(){
	ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
	cin >>n >>m;
	for(int i = 1; i <= n; i ++) {
		for(int j = 1; j <= n; j ++) {
			g[i][j] = Inf;
		}
	}
	for(int i = 1, u, v, w, op; i <= m; i ++) {
		cin >>op >>u >>v >>w;
		if(op == 0) {
			g[v][u] = min(g[v][u], (i64)w);
		}
		else if(op == 1) {
			g[u][v] = min(g[u][v], (i64)-w);
		}
		else {
			g[v][u] = min(g[v][u], (i64)w);
			g[u][v] = min(g[u][v], (i64)-w);
		}
	}
	for(int k = 1; k <= n; k ++) {
		for(int i = 1; i <= n; i ++) {
			for(int j = 1; j <= n; j ++) {
				if(g[i][k] >= Inf || g[k][j] >= Inf) continue;
				g[i][j] = min(g[i][j], g[i][k] + g[k][j]);
			}
		}
	}
	cin >>q;
	for(int i = 1, x, y; i <= q; i ++) {
		cin >>x >>y;
		if(g[y][x] >= Inf) {
			cout <<"Infinity" <<endl;
		}
		else {
			cout <<g[y][x] <<endl;
		}
	}
}
```

$T2$

没什么好讲的，$dis[u][0]$ 为进 $u $ 的距离，$dis[u][1]$ 为出$u$的距离，

$spfa$ 被卡了，所以用 $djs$ 。

```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define pii pair<int,int>

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
} 
int n,m,s,Q;
int re[250500],gr[250500];
vector<pii>g[250500];
int dis[250500][2];
bool vis[250500];
priority_queue<pii,vector<pii>,greater<pii> >q;
inline void djs(){
	memset(dis,0x3f,sizeof dis);
	dis[s][1]=re[s];
	dis[s][0]=re[s];
	q.push({dis[s][1],s});
	while(q.size()){
		int u=q.top().second;q.pop();
		if(vis[u])continue;
		vis[u]=1;
		for(auto i:g[u]){
			int v=i.first,w=i.second;
			if(dis[v][0]>dis[u][1]+w){
				dis[v][0]=dis[u][1]+w;
				if(dis[v][0]%(re[v]+gr[v])>re[v])dis[v][1]=dis[v][0];
				else dis[v][1]=dis[v][0]+re[v]-dis[v][0]%(re[v]+gr[v]);
				q.push({dis[v][1],v});
			}
		}
	}
}
signed main(){
	n=read();m=read();s=read();Q=read();
	for(int i=1;i<=n;i++){
		re[i]=read();
		gr[i]=read();
	}
	while(m--){
		int u=read(),v=read(),w=read();
		g[u].push_back({v,w});
		g[v].push_back({u,w});
	}
	djs();
	cout<<dis[Q][0];
	return 0;
}
```
$T3$

有点难度

以0为原点，n+1为汇点，建一个正图，求出最长路

再建一个反图，找到每条 $dis[u]+t[v]=dis[v]$ 的边，

有以每条边建一个新图

求割点。

显然当该点为割点时，会影响最终值
```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define pii pair<int,int>

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch>'9'||ch<'0'){if(ch=='-')f=-1;ch=getchar();}
	while(ch<='9'&&ch>='0'){x=x*10+ch-48;ch=getchar();}
	return x*f;
} 
int n,m;
int t[100500];
int c[100500];
int cnt[100500];
vector<int>g[100500];
vector<int>e[100500];
vector<int>edge[100500];
queue<int>q;
int dis[105009][2];
bool vis[105000];
inline void spfa1(){
	q.push(0);
	vis[0]=1;
	dis[0][1]=dis[0][0]=0;
	while(q.size()){
		int u=q.front();q.pop();
		for(auto v:g[u]){
			cnt[v]++;
			if(dis[v][0]<dis[u][1]){
				dis[v][0]=dis[u][1];
			}
			if(cnt[v]==c[v]){
				dis[v][1]=dis[v][0]+t[v];
				q.push(v);	
			}
		}
	}
}
inline void dfs(int u){
	if(!u)return;
	for(auto v:e[u]){
		if(dis[v][1]==dis[u][0]){
			edge[u].push_back(v);
			edge[v].push_back(u);
			dfs(v);
		}
	}
}
int dfn[155000],idx,low[155000];
bool num[155000];
vector<int>ans;
inline void dfs_cut(int u,int fa){
	dfn[u] = low[u] = ++idx;
	int child = 0;
	for(auto v:edge[u]) {
		if(!dfn[v]){
			dfs_cut(v, fa);
			low[u] = min(low[v], low[u]);
			if(low[v] >= dfn[u] && u != fa) ans.push_back(u);
			if(u == fa) child ++;
		}
		low[u] = min(low[u], dfn[v]);
	}
	if(child >= 2 && u == fa) ans.push_back(u);
}
signed main(){
	n=read();
	int x,u,s;
	for(int i=1;i<=n;i++){
		t[i]=read();
		c[i]=read();
		if(c[i]==0){
			c[i]=1;
			g[0].push_back(i);	
			e[i].push_back(0);
		}
		else for(int j=1;j<=c[i];j++){
			u=read();
			g[u].push_back(i);
			e[i].push_back(u);
		}
	}
	c[n+1]=n;
	for(int i=1;i<=n;i++){
		g[i].push_back(n+1);
		e[n+1].push_back(i);
	}
	spfa1();
	cout<<dis[n+1][0]<<endl;
	dfs(n+1);
	dfs_cut(n+1,-1);
	cout <<ans.size()-1<<endl;
	sort(ans.begin(), ans.end());
	for(int i = 0; i < (int)ans.size()-1; i ++) {
		cout <<ans[i] <<" ";
	}
	return 0;
}
```