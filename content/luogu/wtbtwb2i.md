### F

我们把每个人对应的所有区间都存起来，然后贪心的枚举每个区间的端点。

```cpp
int n;
int x[N],L[N];
vector<int>s;
signed main(){
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n;
    up(i,1,n)cin>>x[i];
    up(i,1,n)cin>>L[i];
    up(i,1,n){
        up(j,1,n){
            s.push_back(x[i]+L[j]);
            s.push_back(x[i]-L[j]-1);
        }
    }
    sort(s.begin(),s.end());
    int ans=0;
    up(i,0,s.size()-1){
        vector<int>d;
        up(j,1,n){
            d.push_back(abs(x[j]-s[i]));
        }
        sort(d.begin(),d.end());
        bool flag=0;
        up(j,1,n){
            if(d[j-1]>L[j]){
                flag=1;
                break;
            }
        }
        if(!flag)ans+=s[i+1]-s[i];
    }
    cout<<ans;
    return 0;
}
```

### G

考虑网络瘤。

每个点只能经过一次，所以考虑拆点。

从原点向 $B$ 连 $2$ 个流量，$A,C$ 向汇点分别连一个流量，跑最大流，判断最后的流量是否是 $2$。

```cpp

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
int n,m,a,b,c;
int in[N],out[N];
signed main(){
	ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n>>m>>a>>b>>c;
    int cnt=0;
    up(i,1,n){
        in[i]=++cnt;
        out[i]=++cnt;
        E.add(in[i],out[i],1);
        //E.add(out[i],in[i],1);
    }
    int u,v;
    up(i,1,m){
        cin>>u>>v;
        E.add(out[u],in[v],1);
        E.add(out[v],in[u],1);
    }
    E.add(0,out[b],2);
    int t=cnt+10;
    E.add(out[a],t,1);E.add(out[c],t,1);
    if(E.maxflow(0,t)==2)puts("Yes");
    else puts("No");
    return 0;
}
```