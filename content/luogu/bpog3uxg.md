[$My\;blog$](https://www.cnblogs.com/LiQXing/p/17795596.html)

好久没打 abc 了，久违的 rated 一场比赛，结果被 D 创飞了。

$9$ 分钟把 ABC 题切掉，然后看 D 题，觉得是个简单的模拟，错了 $5$ 次，直接把我人整懵了，一看题目 `字符a,b,c只出现一次`，我以为是 `字符a,b,c至少出现一次`，妈妈生的。

## [E](https://atcoder.jp/contests/abc326/tasks/abc326_e "E")

求期望，有个很显然的东西，就是 $ans=\sum_{i=1}^{n} a_i\times p_i$，$p_i$ 是丢骰子丢到 $i$ 的期望次数。
而且 $p_i=\dfrac{1}{n}\sum_{j=0}^{i-1}p_j$。

这个东西是可以线性求的。

```cpp
int n,a[N];
inline int ksm(int a,int b){
    int res=1;
    while(b){
        if(b&1)res=res*a%mod;
        a=a*a%mod;
        b>>=1;
    }
    return res;
}
signed main(){
    n=read();
    up(i,1,n)a[i]=read();
    int p=ksm(n,mod-2);
    int res=0;
    up(i,1,n){
        res=(res+p*a[i])%mod;
        p=(p+p*ksm(n,mod-2))%mod;
    }
    cout<<res;
    return 0;
}
```
## [F](https://atcoder.jp/contests/abc326/tasks/abc326_f "F")

一道搜索好题。

一眼就可以看到 $n\le 80$，看起来直接暴搜不是很能过的样子，考虑优化。

因为每一次都要转向，所以可以可以考虑把 $x$ 轴和 $y$ 轴分开计算。

这样，时间复杂度就是 $2\times 2^{40}$。

还是不够，继续优化，因为直到初始状态和最终状态，所以可以考虑双向搜索优化。

最后输出答案需要注意，我们记录的信息是 $x$ 和 $y$ 的正负，转化成 `LR` 需要记录前一位的信息。

```cpp
int n,sx,sy;
map<int,string>mpx;
map<int,string>mpy;
map<int,int>mp;
int a[500];
vector<int>x,y;
inline void dfsx(int i,int pos,string s){
    if(i==x.size()/2){
        mpx[pos]=s;
        return;
    }
    dfsx(i+1,pos+x[i],s+"1");
    dfsx(i+1,pos-x[i],s+"0");
}
bool fl=0;
inline void dfsx2(int i,int pos,string s){
    if(i==x.size()){
        if(!mpx.count(sx-pos))return;
        mpx[sx]=mpx[sx-pos]+s;
		fl=1;
		return;
    }
	dfsx2(i+1,pos+x[i],s+"1");
    if(fl)return;
    dfsx2(i+1,pos-x[i],s+"0");
    if(fl)return;
}
inline void dfsy(int i,int pos,string s){
    if(i==y.size()/2){
        mpy[pos]=s;
        return;
    }
    dfsy(i+1,pos+y[i],s+"1");
    dfsy(i+1,pos-y[i],s+"0");
}
inline void dfsy2(int i,int pos,string s){
    if(i==y.size()){
        if(!mpy.count(sy-pos))return;
        mpy[sy]=mpy[sy-pos]+s;
		fl=1;
		return;
    }
	dfsy2(i+1,pos+y[i],s+"1");
    if(fl)return;
    dfsy2(i+1,pos-y[i],s+"0");
    if(fl)return;
}
inline void print(){
    puts("Yes");
    vector<int>ans;
    int i=0,j=0;
    while(i<mpy[sy].size()||j<mpx[sx].size()){
        if(i<mpy[sy].size())ans.push_back(mpy[sy][i]-'0'),i++;
        if(j<mpx[sx].size())ans.push_back(mpx[sx][j]-'0'),j++;
    }
    int la=0;
	 up(i,0,ans.size()-1) {
		if (ans[i]) {
			if (la==0) cout<<"L",la=1;
			else if (la==1) cout<<"R",la=0;
			else if (la==2) cout<<"R",la=1;
			else if (la==3) cout<<"L",la=0; 
		}
		else {
			if (la==0) cout<<"R",la=3;
			else if (la==1) cout<<"L",la=2;
			else if (la==2) cout<<"L",la=3;
			else if (la==3) cout<<"R",la=2; 
		}
	}
}
signed main(){
	n=read();sx=read();sy=read();
    up(i,1,n){
        a[i]=read();
        if(i&1)y.push_back(a[i]);
        else x.push_back(a[i]);
    }
    dfsx(0,0,"");
    dfsx2(x.size()/2,0,"");
    fl=0;
    dfsy(0,0,""); 
    dfsy2(y.size()/2,0,"");
    if(mpx.count(sx)&&mpy.count(sy))print();
    else puts("No");
    return 0;
}
```

## [G](https://atcoder.jp/contests/abc326/tasks/abc326_g "G")

看上去就很网络流。

因为 $L_{i,j}\le 5$ 所以我们需要的点数很少。

我们先把所有的价值都加进去，然后求最小割，这个网络流的图是很容易建的，但是有几个细节地方要注意，如果当前节点不满足，那么比这个节点等级高的点同样不满足，所以之间可以连一条 $inf$ 的边，
同样的，如果一个条件不满足而获得了这个成就的价值，那么同样的要连一条权值为 $inf$ 的边。

```cpp
int n,m;
int c[N],a[N];
struct Dinic{
	struct edge{
		int u,v,cap,flow;
	};
	vector<edge>edges;
	vector<int>g[N];
	int cur[N],d[N];
	bool vis[N];
	inline void add(int u,int v,int cap){
		edges.push_back({u,v,cap,0});
		edges.push_back({v,u,0,0});
		int t=edges.size();
		g[u].push_back(t-2);
		g[v].push_back(t-1);
	}
	inline bool bfs(int s,int t){
		memset(vis,0,sizeof vis);
		queue<int>q;
		q.push(s);
		d[s]=0;vis[s]=1;
		while(q.size()){
			int u=q.front();q.pop();
			for(auto i:g[u]){
				auto e=edges[i];
				if(!vis[e.v]&&e.cap>e.flow){
					vis[e.v]=1;
					d[e.v]=d[u]+1;
					q.push(e.v);
				}
			}
		}
		return vis[t];
	}
	inline int dfs(int u,int a,int t){
		if(u==t||a==0)return a;
		int flow=0,f;
		for(int &i=cur[u];i<g[u].size();i++){
			auto& e=edges[g[u][i]];
			if(d[u]+1==d[e.v]&&(f=dfs(e.v,min(a,e.cap-e.flow),t))>0){
				e.flow+=f;
				edges[g[u][i]^1].flow-=f;
				flow+=f;
				a-=f;
				if(a==0)break;
			}
		}
		return flow;
	}
	inline int maxflow(int s,int t){
		int flow=0;
		while(bfs(s,t)){
			memset(cur,0,sizeof cur);
			flow+=dfs(s,inf,t);
		}
		return flow;
	}
}E;
int ans=0;
signed main(){
	n=read();m=read();
    int s=5*n+m,t=5*n+m+1;
    up(i,0,n-1) {
        int c=read();
        up(j,0,3){
            E.add(5*i+j,5*i+j+1,c*j);
            E.add(5*i+j+1,5*i+j,inf);
        } 
        E.add(5*i+4,t,c*4);
    }
    up(i,1,m)a[i]=read(),ans+=a[i];
    int x;
    up(i,0,m-1){
        up(j,0,n-1){
            x=read()-1;
            E.add(5*n+i,5*j+x,inf);
        }
        E.add(s,5*n+i,a[i+1]);
    }
    ans-=E.maxflow(s,t);
    cout<<ans;
    return 0;
}
```