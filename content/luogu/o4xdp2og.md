边双连通分量


概念


与强连通分量相似，指删掉一条边后仍连通的联通块

性质

$1.$ 删掉一条边对联通块的连通性没有影响

$2.$ 边双联通分量内的每一条边必定在一个环内

$3.$ 边双联通分量是上任意两点间至少2条路径（因为断了一条边之后连通性不变）

```cpp
#include <bits/stdc++.h>

using namespace std;

#define pii pair<int,int>

inline int read(){
    int x=0,f=1;char ch=getchar();
    while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
    while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
    return x*f;
}
vector<pii>g[1550500];
int n,m;
int dfn[1500500],low[1500500],t;
bool bri[4500500];
int c[1500500],cnt,colornum;
stack<int>s;
vector<int>ans[500500];
inline void tarjan(int u, int from) {
    dfn[u] = low[u] = ++t;
    s.push(u);
    for(auto i:g[u]) {
        int v = i.first, it = i.second;
        if (!dfn[v]) {
            tarjan(v,it);
            low[u] = min(low[u], low[v]);
            if (dfn[u] < low[v]) bri[it] = bri[it^ 1] =1;
        }
        else if(it!=(from^1))low[u] = min(low[u], dfn[v]);
    }
    if(dfn[u] == low[u]) {
        int v;
        colornum ++;
        do {
            v =s.top();s.pop();
            c[v] = colornum;
            ans[colornum].push_back(v);
        } while(u != v);
    }
    return;
}

int main() {
    n=read();m=read();
    for (int i = 1,u,v; i <= m; i++){
        u=read();v=read();
        g[u].push_back({v,2*i});
        g[v].push_back({u,2*i+1});
    }
    for (int i = 1; i <= n; i++) if (!dfn[i]) tarjan(i, 0);
    cout<<colornum<<endl;
    for(int i = 1; i <= colornum; i ++) {
        cout <<ans[i].size()<<" ";
        for(auto v:ans[i]) {
            cout <<v <<" ";
        }
        cout <<endl;
    }
    return 0;
}
```

点双联通分量：

除了一种比较特殊的点双，其他的点双都满足：任意两点间都存在至少两条点不重复路径。

比较特殊的点双：只有两个点相连。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define N 500500

inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}

int n,m,cnt,dfn[N],low[N],cut,dcccnt;
vector<int>vec[N];
stack<int>s;
vector<int>dcc[N];

inline void tarjan(int u,int from){
	low[u]=dfn[u]=++cnt;
	s.push(u);
	int son=0;
	for(auto v:vec[u]){
		if(v==from)continue;
		son++;
		if (!dfn[v]){
            tarjan(v,u);
            low[u]=min(low[u],low[v]);
            if (low[v]>=dfn[u]){   
                ++dcccnt;
                int p; 
                do{
                	p=s.top();s.pop();
                    dcc[dcccnt].push_back(p);
                } while(p!=v);    
                dcc[dcccnt].push_back(u); 
            }
        }
        low[u] = min(low[u],dfn[v]);
	}
	if (!son&&from==u)  dcc[++dcccnt].push_back(u);
}
signed main(){
	n=read();m=read();
	for(int i=1,u,v;i<=m;i++){
		u=read();v=read();
		vec[u].push_back(v);
		vec[v].push_back(u);
	}
	for(int i=1;i<=n;i++)if(!dfn[i])tarjan(i,i);
	printf("%d\n",dcccnt);
	for(int i=1;i<=dcccnt;i++){
		printf("%lld ",dcc[i].size());
		for(auto v:dcc[i]){
			printf("%d ",v);
		}
		printf("\n");
	}
    return 0;
}



```



[$problem.1$](https://loj.ac/p/10098)

大意：给出一个无向图，求至少添加几条边后，改图可以变为边双连通分量。

要点：

$1.$ 边双连通分量 $\Longleftrightarrow$ 每两个点至少有两条相互分离的路径。

$2.$添加的边数$\Longleftrightarrow$缩点后出度为1的点的一半向上取整
```cpp
#include <bits/stdc++.h>
using namespace std;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
vector<pair<int,int> >vec[55000];
int n, m;
int u[25000], v[25000];
int dfn[25000],low[25000],t;
bool bri[2 * 25000];
int color[25000], cnt, deg[2*25000], ans;
void tarjan(int u, int fa) {
	dfn[u] = low[u] = ++t;
	for(auto i : vec[u]) {
		int v = i.first, it = i.second;
		if (v == fa) continue;
		if (!dfn[v]) {
			tarjan(v, u);
			low[u] = min(low[u], low[v]);
			if (dfn[u] < low[v]) bri[it] = bri[it^ 1] =1;
		}
		else low[u] = min(low[u], dfn[v]);
	}
	return;
}
inlnie void dfs(int u) {
	color[u] = cnt;
	for (auto i:vec[u]) {
		int v = i.first,it = i.second;
		if (color[v] || bri[it]) continue;
		dfs(v);
	}
	return;
}
int main() {
	n=read();m=read();
	for (int i = 1; i <= m; i++){
		u[i]=read();v[i]=read();
		vec[u[i]].emplace_back(v[i], 2 * i);
		vec[v[i]].emplace_back(u[i], 2 * i + 1);
	}
	for (int i = 1; i <= n; i++) if (!dfn[i]) tarjan(i, 0);
	for (int i = 1; i <= n; i++) if (!color[i]) ++cnt, dfs(i);
	for (int i = 1; i <= m; i++) 
		if (color[u[i]] != color[v[i]]) 
		deg[color[u[i]]]++, deg[color[v[i]]]++;
	for (int i = 1; i <= cnt; i++) 
		if (deg[i] == 1) 
		ans++;
	printf("%d",(ans+1)/2);
	return 0;
}
```


$T2$

 大意：
将某一个点删去。设图中原来有$k$个联通块，如果删掉割点，那么现在就有了$k+1$个联通块，如果不是割点，联通块数目不变。因此我们可以看出，割去任一个割点，割点两边的联通块都需要设一个逃生口。

------------

故 如果没有割点，至少需要建立两个出口，从任意非割点的地方选择两个点建立;如果这个分组只有一个割点,只需要在分组内设立一个出口,可以设立在任意一个非割点的地方;如果有两个及以上个割点，则无需建立，可以直接到达其他联通块
```cpp
```cpp
#include<bits/stdc++.h>
#define int long long
using namespace std;
int head[505],dfn[505],low[505],vis[505],stack[505];
bool cut[505];
int n,m,cnt,num,t,color,ans1,ltk,cases,root,top;
int ans2;
vector<int>vec[25000];
inline void clear(){
    memset(dfn,0,sizeof(dfn));
    memset(low,0,sizeof(low));
    memset(cut,0,sizeof(cut));
    memset(vis,0,sizeof(vis));
    int i=1;
    for(int i=0;i<=n;i++){
    	vec[i].clear();
    }
    top=cnt=t=n=ans1=ltk=0;ans2=1;
    color=0;
}
inline int read(){
    int x=0,f=1; char c=getchar();
    while (c<'0'||c>'9'){if(c=='-')f=-1;c=getchar();}
    while (c>='0'&&c<='9'){x=x*10+c-'0';c=getchar();}
    return x*f;
}
void Tarjan(int u,int fa) {
    dfn[u]=low[u]=++t;
    for(auto v:vec[u]){
            if(!dfn[v]){
                Tarjan(v,u);
                low[u]=min(low[u],low[v]);
                if(low[v]>=dfn[u]){
                    if(u==root) color++;
                    else cut[u]=true;
                }
            }
            else if(v!=fa) low[u]=min(low[u],dfn[v]);
        }
}
void dfs(int x){
    vis[x]=ltk;
    if(cut[x]) return;
    cnt++;
    for(auto v:vec[x]){
        if(cut[v]&&vis[v]!=ltk) num++,vis[v]=ltk;
        if(!vis[v])dfs(v);
    }
}
signed main()
{
    m=read();
    while (m){
        clear();
        for (int i=1;i<=m;i++){
            int u=read(),v=read();
            n=max(n,max(u,v)); 
            vec[u].push_back(v);
            vec[v].push_back(u);
        }
        for (int i=1;i<=n;i++){
            if(!dfn[i]){
            	root=i;
            	Tarjan(i,0);	
            }
            if(color>=2) cut[root]=1;
            color=0;
        }
        for (int i=1;i<=n;i++)
            if (!vis[i]&&!cut[i]){
                ltk++; cnt=num=0;
                dfs(i);
                if (!num) ans1+=2,ans2*=cnt*(cnt-1)/2;
                if (num==1) ans1++,ans2*=cnt;
            }
        printf("Case %lld: %lld %lld\n",++cases,ans1,ans2);
        m=read();
    }
    return 0;
}


```
$T3$

求割点模板。

```cpp
inline void Tarjan(int u,int fa){
    dfn[u]=low[u]=++dfn_id;
    int ch=0;
    for(auto v:g[u]){
        if(!dfn[v]){
            Tarjan(v,fa);
            low[u]=min(low[u],low[v]);
            if(low[v]>=dfn[u]&&u!=fa) cut[u]=1;
            if(u==fa) ch++;
        }
        low[u]=min(low[u],dfn[v]);

    }
    if(ch>=2&&u==fa) cut[u]=1;
}
```

$T4$

同$T3$.

$T5$

找割边模板

```cpp
inline void dfs(int u,int from) {
	dfn[u] = low[u] = ++cnt;
	for(auto v:g[u]) {
		if(v==from)continue;
		if (!dfn[v]) {
			dfs(v,u);
			low[u] = min(low[u], low[v]);
			if(low[v]>dfn[u])vis[u] = true, num++;
		}
		else low[u] = min(low[u], dfn[v]);
	}
	return;
}
```

$T6$

题意：求一个无向图图删除一个点之后，连通块最多有多少。

显然只有是割点的情况，连通图数量会增加。

每删一个割点，增加联通块个数等于其儿子个数.

注意考虑图可能不联通。

```cpp
inline void tarjan(int u){
	low[u]=dfn[u]=++idx;
	int son=0;
	for(auto v:g[u]){
		if(!dfn[v]){
			tarjan(v);
			low[u]=min(low[u],low[v]);
			if(dfn[u] <= low[v]) son++;
        }
		else low[u] = min(low[u], dfn[v]);
	}
	if(u!=root)son++;
	ans=max(ans,son);
}
```

$T7$

大意：请你对于每个节点 $i$ 求出，把与节点 $i$ 关联的所有边去掉以后（不去掉节点 $i$ 本身），无向图有多少个有序点 $(x,y)$，满足 $x$ 和 $y$ 不连通。

解析：

假如 $i$ 不是割点,那么这个图只有 $i$ 是独立在外面的，由于求的是有序点对，所以点对数为 $2(n-1)$

假如 $ i$是割点，那么会把图分为 $a$ 个连通块以及 $i$ 本身,由于 $tarjan$ 在求割点的过程中是一棵搜索树往下遍历，所以除了它和它的子树外，还会有其他剩余点共同构成另一个连通块, 设 $i$ 所有子树的和为$sum$,第 $i$ 个子树的节点总数为 $t[i]$，点对的数量便为
$$t[1](n-t[1])+t[2](n-t[2])+\cdots+t[a](n-t[a])+(n-1)+(1+sum)(n-sum-1)$$

所以在求割点的过程中每遇到一个$low[v]\ge dfn[u]$ 便把对数加上$t[i]*(n-t[i])$最后假如不是割点那直接把对数更新为$2*(n-1)$ 是割点则加上$n-1$+$(n-sum-1)(sum+1)n$−$1+(n−sum−1)(sum+1)$  最后遍历输出答案即可

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
vector<int>vec[125000];
int t,n,m,dfn[125000],ans[125000],low[125000],root,Size[125000];
bool cnt[125000];
void dfs(int u,int fa){
	dfn[u]=low[u]=++t;
	int child=0;
	Size[u]=1;
	int sum=0;
	for(int i=0;i<vec[u].size();i++){
		int v=vec[u][i];
		if(v==fa)continue;
		if(!dfn[v]){
			dfs(v,u);
			Size[u]+=Size[v];
			low[u]=min(low[u],low[v]);
			//if(u==root&&child>1) cnt[u]=1;
			if(low[v]>=dfn[u]){
				ans[u]+=Size[v]*(n-Size[v]);
				sum+=Size[v];
				child++;
				if(child>1||u!=root)cnt[u]=1;
			} 
		}
		else low[u]=min(low[u],dfn[v]);
	}
    ans[u]+=(n-sum-1)*(sum+1)+(n-1);
}
signed main(){
    n=read();m=read();
    int x,y;
    for(int i=1;i<=m;i++){
    	x=read();y=read();
    	vec[x].push_back(y);
    	vec[y].push_back(x);
    }
    for(int i=1;i<=n;i++){
    	if(!dfn[i]){
    		root=i;
    		dfs(i,0);
    	}
    }
    for(int i=1;i<=n;i++){
    	if(cnt[i]){
    		printf("%lld\n",ans[i]);
    	}
    	else printf("%lld\n",2*n-2);
    }
    return ~~(0-0);
}

```