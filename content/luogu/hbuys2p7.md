### [Love Triangles](https://www.luogu.com.cn/problem/CF553C)

又是神仙题。

对于一个连通块来说，里面的边是全部确定的，这很显然。

对于多个连通块，他们的边可能是爱边，也可能是恨边。

所以只用求出有多少个连通块就可以了。

至于判断无解的情况，假设爱边为 $1$，恨边为 $-1$，一个合法的三元环乘积为 $1$，记录到每一个点的答案，如果冲突，则无解。


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