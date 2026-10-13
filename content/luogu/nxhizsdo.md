### [Lovely Matrix](https://www.luogu.com.cn/problem/CF274D)

非常妙的一道题。

首先，我们可以把每一列看成一个点，由小数向大数连边，跑拓扑排序。

然而由于边数太多，会超时，考虑虚点连边优化，相同的数连向一个虚点。

```cpp
int n,m,cnt;
vector<int>g[N];
int deg[N];
queue<int>q;
vector<int>top;
inline void topu(){
    up(i,1,cnt){
        if(!deg[i])q.push(i);
    }
    while(q.size()){
        int u=q.front();q.pop();
        top.push_back(u);
        for(auto v:g[u]){
            if(!--deg[v])q.push(v);
        }
    }
}
signed main(){
    ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    vector<vector<pii> >a(n+1,vector<pii>(m+1));
    up(i,1,n){
        up(j,1,m){
            cin>>a[i][j].first;
            a[i][j].second=j;
        }
    }
    cnt=m;
    up(i,1,n){
        sort(a[i].begin()+1,a[i].end());
        vector<pii>h;
        for(int l=1,r;l<=m;l=r+1){
			r=l;while(r+1<=m&&a[i][r+1].first==a[i][l].first)r++;
			h.push_back({l,r});
		}
        for(int j=0;j+1<h.size();j++){ 
			int l1=h[j].first,r1=h[j].second,l2=h[j+1].first,r2=h[j+1].second;
			if(a[i][l1].first==-1)continue;
			cnt++;
			up(k,l1,r1)g[a[i][k].second].push_back(cnt),deg[cnt]++; 
			up(k,l2,r2)g[cnt].push_back(a[i][k].second),deg[a[i][k].second]++; 
		}
    }
    topu();
    if(top.size()<cnt)puts("-1");
	else for(auto v:top)if(v<=m)cout<<v<<" ";
    return 0;
}
```

### [Tanya and Password](https://www.luogu.com.cn/problem/CF508D)

就是跑欧拉路。

```cpp

map<int,int>mp;
int cnt;
vector<int>g[N];
int in[N],out[N];
int s,t;
inline bool check(){
	for(int i=1;i<=cnt;i++){
		if(in[i]!=out[i]){
			if(in[i]==out[i]+1){
				if(t)return 0;
				t=i;
			}
			else if(in[i]+1==out[i]){
				if(s)return 0;
				s=i;
			}
			else return 0;
		}
	}
	if(!s)s=t=1;
	return 1;
}
stack<int>st;
int del[500500];
inline void dfs(int u){
	for(int i=del[u];i<g[u].size();i=del[u]){
		del[u]=i+1;
		dfs(g[u][i]);
	}
	st.push(u);
}
map<int,string>mp2;
signed main(){
    cin>>n;
    up(i,1,n){
        string s;
        cin>>s;
        if(!mp[s[0]*300+s[1]])mp[s[0]*300+s[1]]=++cnt,mp2[cnt]=s.substr(0,2);
        if(!mp[s[1]*300+s[2]])mp[s[1]*300+s[2]]=++cnt,mp2[cnt]=s.substr(1,2);
        g[mp[s[0]*300+s[1]]].push_back(mp[s[1]*300+s[2]]);
        in[mp[s[1]*300+s[2]]]++,out[mp[s[0]*300+s[1]]]++;
    }
	if(!check()){
		cout<<"NO"<<"\n";
		return 0;
	}
    
	for(int i=1;i<=n;i++){
		sort(g[i].begin(),g[i].end());
	}
	dfs(s);
    bool flag=1;
    if(st.size()!=n+1){
        cout<<"NO"<<"\n";
        return 0;
    }
	cout<<"YES"<<"\n";
    while(!st.empty()){
		if(flag)cout<<mp2[st.top()],flag=0;
        else cout<<mp2[st.top()][1];
		//cout<<st.top()<<endl;
        st.pop();
    }
    return 0;
}
```
### [Love Triangles](https://www.luogu.com.cn/problem/CF553C)

又是神仙题。

对于一个连通块来说，里面的边是全部确定的，这很显然。

对于多个连通块，他们的边可能是爱边，也可能是恨边。

所以只用求出有多少个连通块就可以了。

至于判断无解的情况，假设爱边为 $1$,恨边为 $-1$,一个合法的三元环乘积为 $1$，记录到每一个点的答案，如果冲突，则无解。


```cpp

int n,m;
inline int ksm(int a,int b){
	int res=1;
	while(b){
		if(b&1)res=res*a%mod;
		a=a*a%mod;
		b>>=1;
	}
	return res;
}
int vis[N];
vector<pii>g[N];
int col[N];
inline void dfs(int u,int from,int tp){
	vis[u]=1;col[u]=tp;
	for(auto [v,w]:g[u]){
		if(v==from)continue;
		if(vis[v]){
	        if(col[v]!=(w?tp:-tp)){
		         cout<<"0"<<endl;
		         exit(0);
	        }
	        continue;
	    }
		dfs(v,u,(w?tp:-tp));
	}
}
signed main(){
	cin>>n>>m;
	int u,v,w;
    up(i,1,m){
        cin>>u>>v>>w;
        g[u].push_back({v,w});
        g[v].push_back({u,w});
    }
    int ans=0;
	up(i,1,n)if(!vis[i])ans++,dfs(i,0,1);
	cout<<ksm(2,ans-1);
	return 0;
}
```

### [Mr. Kitayuta's Technology](https://www.luogu.com.cn/problem/CF505D)

告诉你一些点的连通性，求出至少需要多少条有向边。

对于一个没有环的联通块，可以用拓扑序排成一个链，用 $n-1$ 条边，因为联通 $n$ 个点至少需要 $n-1$ 条边，所以这是最优的。

如果有环呢？

那么你可以加一条边，让所有这个连通块的点连成一个大环。

这样可以保证所有点可以互相到达且花费最少。

```cpp
int n,m;
vector<int>g[N];
int deg[N],fa[N];
inline int find(int x){
    if(x==fa[x])return x;
    return fa[x]=find(fa[x]);
}
int vis[N];
queue<int>q;
signed main(){
	ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    int u,v;
    up(i,1,n)fa[i]=i;
    up(i,1,m){
        cin>>u>>v;
        g[u].push_back(v);
        //g[v].push_back(u);
        deg[v]++;
        fa[find(u)]=find(v);
    }
    int ans=n;
    up(i,1,n){
        if(fa[i]==i){
            ans--;
            vis[i]=1;
        }
    }
    up(i,1,n)if(!deg[i])q.push(i);
    while(q.size()){
        int u=q.front();q.pop();
        for(auto v:g[u]){
            if(!--deg[v])q.push(v);
        }
    }
    up(i,1,n){
        if(deg[i]){
            ans+=vis[find(i)],vis[find(i)]=0;
        }
    }
    cout<<ans;
    return 0;
}
```

### [Population Size](https://www.luogu.com.cn/problem/CF416D)

有一个非常显然的贪心，一个数如果能够放在前一个等差数列里，那么就要放在那个等差数列里。

大体的思路有了，然后是一些细节，比如所有的数都是正整数，所以要判断那个数列会不会小于 $0$。

```cpp
int n,m;
int a[N];
signed main(){
	ios_base::sync_with_stdio(0);
    cin.tie(0);cout.tie(0);
    cin>>n;
    up(i,1,n)cin>>a[i];
    int u=1,ans=0;
    while(u<=n){
        ans++;
        int d,sx=0,mx=0,nxt=0;
        up(i,u,n){
            if(a[i]==-1)continue;
            if(sx==0)sx=i;
            else{
                nxt=i;
                break;
            }
        }
        if(nxt==0)break;
        if((a[nxt]-a[sx])%(nxt-sx)!=0){
            u=nxt; 
            continue;
        }
        d=(a[nxt]-a[sx])/(nxt-sx);
        if(a[sx]-(sx-u)*d<=0){
            u=nxt;
            continue;
        }
        int last=a[nxt];
		u=nxt+1;
		while(u<=n){
			if(last+d<=0)break;
			if(a[u]==-1||a[u]==last+d)last+=d;
			else break;
			++u;
		}
    }
    cout<<ans;
    return 0;
}
```