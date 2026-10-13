# 图论

$01BFS:$

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
int n,m,dis[500500];
bool vis[500500];
vector<pair<int,int> >vec[500500];
deque<int>q;//常数极大，很慢
signed main(){
	memset(dis,0x3f,sizeof dis);
	n=read();m=read();
	int u,v,w;
	for(int i=1;i<=m;i++){
		u=read();v=read();w=read();
		vec[u].push_back({v,w});
	}
	dis[1]=0;
	q.push_back(1);
	while(q.size()){
		u=q.front();q.pop_front();
		if(vis[u])continue;
		vis[u]=1;
		for(auto i:vec[u]){
			v=i.first;w=i.second;
			if(dis[u]+w<dis[v]){
				dis[v]=dis[u]+w;
				if(w==0)q.push_front(v);
				else q.push_back(v);
			}
		}
	}
	for(int i=1;i<=n;i++)printf("%lld",dis[i]);
    return 0;
}


```
$problem.1$

给定一个 $n$ 个点 $m$ 条边的无向图，可以每次选两个点，并把这两个点缩起来，锁起来后两个点的相邻点集合合并，直到最后缩成一条链，求链长度最大值（$n<=1000,m<=10^5$）

提示：如果一个连通图缩成一个$s$到$t$的链，其长度一定不大于$s$到$t$最短路的距离

$problem.2$

给定一个$n$个点$m$条边的有向带权图，你可以选择一个边集$E$,并将这个边集里所有的边反向，花费的代价是边集里的边的权值最大值，求最小的代价使得该图不存在环。
$n,m<=10^5,w_i≤10^9$

提示：二分答案

```cpp
鸽
```
$problem.3$

给出一个$N$个顶点$M$条边的无向无权图，顶点编号为$1$->$N$。问从顶点$1$开始，到其他每个点的最短路有几条。

提示：如何保证走的是最短路？ 只走分层图上跨两层的边!计数$DP$

```cpp
#include<bits/stdc++.h>
using namespace std;  
int mod=100003,ans,book[1092983],f,dep[1023746],step[1234537],n;
vector<int>a[1005000];
void bfs(int k){
	int u,v;
	queue<int>que;
    que.push(1);
    book[1]=true;
    while(!que.empty()){
        u=que.front();
        que.pop();
        for(int i=0;i<a[u].size();i++){
            v=a[u][i];
            if(!book[v]){
                dep[v]=dep[u]+1;
                que.push(v);
                book[v]=1;
            }
            if(dep[v]==dep[u]+1){
            	step[v]=(step[v]+step[u])%mod;
            }
        }
    }
    for(int i=1;i<=n;i++)cout<<step[i]<<endl;
}
int main(){
	step[1]=1;
	int m,x,y;
	scanf("%d%d",&n,&m);
	for(int i=1;i<=m;i++){
		scanf("%d%d",&x,&y);
		a[x].push_back(y);
		a[y].push_back(x);
	}
	memset(book,0,sizeof book);
	bfs(1);
	return 0;
}
```

[$problem.4$](https://www.luogu.com.cn/problem/CF1765I)

注意到由于点数过多，所以不能直接建图$bfs$。

由于棋子很稀疏，所以中间一定存在很多段没有棋子的连续段，同时这些连续段只有若干行不能走，启发我们压缩棋盘。
对于每个连续段只建立左边$8$个点以及右边$8$个点，中间边加权即可。

压缩完之后在图上跑$dijkstra$求最短路即可。


```cpp
鸽
```
[$problem.5$](https://www.luogu.com.cn/problem/CF986F)

观察到对于非质数的因数一定可以拆成若干质因数的和，所以我们可以只考虑质因数。

设质因数为$p_1,p_2,,p_m$

分类讨论：

$m=0$, 此时$k=1$，无解

$m=1$, 只用判断$n$是不是$k$的倍数即可

$m=2$, 标准二元一次方程，使用扩欧求出通解。

$m\ge2$, 此时$p_1$<$10^5$, 记$d_x$表示模$p_1$余$x$，用后面质因数组成的数最小是多少，可以使用$dijkstra$计算最短路。


```cpp
鸽
```
## [次短路](https://www.luogu.com.cn/problem/P2865)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long 
inline int read(){
	register int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,dis[500500],dis2[500500];
vector<pair<int,int> >vec[500500];
priority_queue<pair<int,int>, vector<pair<int,int> >,greater<pair<int,int> > >q;
void djs(){
	//fill(dis,dis+500000,1e15);
	//fill(dis2,dis2+500000,1e15);
	memset(dis,0x3f,sizeof dis);
	memset(dis2,0x3f,sizeof dis);
	dis[1]=0;//dis2[1]=0;
	q.push({0,1});
	while(q.size()){
		int u=q.top().second,dist=q.top().first;q.pop();
		for(auto i:vec[u]){
			int v=i.second,w=i.first;
			bool flag=0;
			if(dist+w<dis[v]){
				dis[v]=dist+w;
				flag=1;
			}
			if(dist+w>dis[v]&&dist+w<dis2[v]){
				dis2[v]=dist+w;
				flag=1;
			}
			if(dis2[u]+w<dis2[v]){
				dis2[v]=dis2[u]+w;
				flag=1;
			}
			if(flag==1) q.push({dis[v],v});
		}
	}
}
signed main(){
    n=read();m=read();
    int x,y,z;
    for(int i=1;i<=m;i++){
    	x=read();y=read();z=read();
    	vec[x].push_back({z,y});
    	vec[y].push_back({z,x});
    }
    djs();
    printf("%lld",dis2[n]);
    return 0;
}


```
## 差分约束

$problem.6$

$A$国一天有$N$个小时，某座工厂每天每个小时都有生产任务，第$i$小时至少需要$a_i$个工人，$A$国规定每个工人每天只能正好工作$c$小时且每个工人每天的开工时间是固定的。现在工厂举行招聘，来应聘的工人有$b_i$个人的开工时间是????时，即这些人会从每天的????时开始连续工作????个小时(注意这些人结束工作的时间可能已经是第二天了)，为了完成生产任务，至少需要招聘多少工人。

$C≤N≤700,a_i,b_i\le10^9$

解：

设在第$1,2,...i$个小时开工的人有$x_i$个

则在第$C$个小时开工的人数为$x_i-x_{i-1}$

则有限制：$x_i-x_{i-1}\le b_i$

由于让人数尽可能小，变成大于号：$x_i-x_{i-1}\ge -b_i$

第$C$小时开工的人数，若这些人都在同一天，则有：$x_i-x_{i-c}\ge a_i$.

否则:$C-(x_{i-C+n-1}-x_{i-1})\ge   a_i$

其中$C$为总人数，注意到$C$越大限制越松，我们可以二分$C$,用差分约束判定是否存在负环。


```cpp
鸽
```

$problem.7$

给出一个$mn$矩阵，问是否存在 $n$ 个数 $a_1,a_2,...a_n$以及$m$个数$b_1,b_2,...,b_n$,使矩阵的第$i$行的元素乘上$a_i$，第$j$列的元素乘上$b_j$，使得操作后矩阵中的每个元素都在$[L,R]$范围内。

注意选择的$a$和$b$可以是任意正实数。

$n,m\le400$,$1\le L\le R \le 10^4$

解：

限制可以写成：$L_{i,j}\le a_ib_j\le R_{i,j}$

取对数，令$A_i=loga_i,B_i=-logb_j$

则$logL_{i,j}\le A_i-B_i\le logR_{i,j}$

即为差分约束标准模型。

```cpp
鸽
```
## 最小生成树

### $Kruskal$

扩展$1$：最小瓶颈生成树

即边权最大值最小的生成树

易证最小生成树一定是最小瓶颈生成树

最小瓶颈生成树不一定为最小生成树

扩展$2$：$Kruskal$重构树

[$problem.7$](https://loj.ac/p/137)

```cpp
鸽
```
[$problem.8$](https://www.luogu.com.cn/problem/P4768)

$Kruskal$重构树

一个点能走到的点集为 $Kruskal$ 重构树上的一个子树，可以通过倍增求出这个子树的根。

预处理$1$号点到所有点的最短路，和每个子树的最短路最小值即可在线回答询问

```cpp
鸽
```
[$problem.9$](https://www.luogu.com.cn/problem/P2573)

题目是有特殊性质的最小树形图问题。

改进$Kruskal$: 首先求出能走到的节点集合，然后以有向边终点高度为第一关键字从大到小，边权从小到大为第二关键字, 使用$Kruskal$ 求最小生成树。

如果按照高度从高到低将点排成一排，那么生成树的每个前缀的导出子图也一定是树，所以贪心的正确性能够保证。

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define inf 1e14
#define mod 10000007
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,ans,tot,cnt;
int h[1500500],fa[1500500];
struct node{
	int u,v,w;
}e[1500500];
int find(int x){
	if(x==fa[x])return x;
	return fa[x]=find(fa[x]);
}
void merge(int x,int y){
	fa[find(x)]=find(y);
}
bool cmp(node x,node y){
	return x.w<y.w;
}
vector<pair<int,int> >vec[500500];
void kruskal(){
	sort(e+1,e+1+cnt,cmp);
	for(int i=0;i<=n;i++)fa[i]=i;
	for(int i=1;i<=cnt;i++){
		if(find(e[i].u)!=find(e[i].v)){
			ans+=e[i].w;
			merge(e[i].u,e[i].v);
			cout<<ans<<endl;
		}
	}
}
queue<int>q;
bool vis[500500];
void bfs(){
	q.push(1);vis[1]=1;
	while(q.size()){
		int u=q.front();q.pop();
		for(auto i:vec[u]){
			int v = i.first,w = i.second;
			e[++cnt]=node{u,v,w};
			//cout<<e[cnt].v<<endl;
			if (!vis[v]){
				vis[v]=1;
				q.push(v);
				tot++;	
			}
		}
	}
}

signed main() {
	n=read();m=read();
	for(int i=1;i<=n;i++)h[i]=read();
	for(int i=1,u,v,w;i<=m;i++){
		u=read();v=read();w=read();
		if(h[u]>=h[v])vec[u].push_back({v,w});
		if(h[u]<=h[v])vec[v].push_back({u,w});
	}
	bfs();
	printf("%lld \n",tot+1);
	kruskal();
	printf("%lld",ans);
	return 0;
}
```
[$problem.10$](https://www.luogu.com.cn/problem/CF1508C)

注意到在最优解里面，没有填长度的边只有一个非零的值。这是因为如果$MST$里面包含所有没填的边，那么把所有权值分配到一条边上一定不会变得更差。如果$MST$里面不包含所有每填的边，那么把一条没有填的边设置成$x$，其他设置成$0$就得到了一个不会更差的生成树。

对已经分配了权值的边有三类：
1. 一定存在于$MST$里的边
2. 一定不存在于$MST$里的边
3. 其他的边

对于没有分配权值的边，如果它们存在环，那么直接把环上一个边设置成$x$，其他设置成$0$。
如果不存在环，那么最优解就是用最小的第三类边替换这个$x$,因为第三类边加入之后一定能构成一个包含未分配权值边的环。

```cpp
鸽
```
[$problem.11$](https://www.luogu.com.cn/problem/CF1515F)

```cpp
鸽
```