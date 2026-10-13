
var code = "ba24a35e-a10e-4174-9cb9-94a61c421806"
## [Bus Routes](https://vjudge.csgrandeur.cn/problem/URAL-1137)

题意：找出欧拉回路。

```cpp
vector<int>g[N];
stack<int>st;
int del[N],n,m;
inline void dfs(int u){
	for(int i=del[u];i<g[u].size();i=del[u]){
		del[u]=i+1;
		dfs(g[u][i]);
	}
	st.push(u);
}
signed main(){
	n=read();
    int sum=0;
    up(i,1,n){
        m=read();
        sum+=m;
        int u=read(),v;
        up(j,1,m){
            v=read();
            g[u].push_back(v);
            u=v;
        }
    }
    dfs(1);
    if(sum!=st.size()-1)printf("0\n");
    else{
        cout<<st.size()-1<<" ";
        while(!st.empty()){
            cout<<st.top()<<" ";
            st.pop();
        }    
    }
	return 0;
}
	
```

## [Labyrinth - URAL 1033](https://vjudge.csgrandeur.cn/problem/URAL-1033)

题意：找出从原点能到达的边缘个数。

坑点：两边可能不连通。

```cpp
int n,m;
char a[550][550];
int dx[]={1,-1,0,0},cnt,dy[]={0,0,1,-1};
bool vis[550][550];
bool inc[550][550];
inline void bfs(){
    queue<pii>q;
    q.push({1,1});
    vis[1][1]=1;
    while(!q.empty()){
        pii u=q.front();q.pop();
        int ux=u.fi,uy=u.se;
        up(i,0,3){
            int tx=ux+dx[i],ty=uy+dy[i];
            if(vis[tx][ty])continue;
            if(tx<1||ty<1||tx>n||ty>n||a[tx][ty]=='#'){
                cnt++;
                continue;
            }
            vis[tx][ty]=1;
            q.push({tx,ty});
        }
    }
}
inline void bfs2(){
    queue<pii>q;
    q.push({n,n});
    vis[n][n]=1;
    while(!q.empty()){
        pii u=q.front();q.pop();
        int ux=u.fi,uy=u.se;
        up(i,0,3){
            int tx=ux+dx[i],ty=uy+dy[i];
            if(vis[tx][ty])continue;
            if(tx<1||ty<1||tx>n||ty>n||a[tx][ty]=='#'){
                cnt++;
                continue;
            }
            vis[tx][ty]=1;
            q.push({tx,ty});
        }
    }
}
signed main(){ 
	n=read();
    up(i,1,n){
        scanf("%s",a[i]+1);
    }
    bfs();
    if(!vis[n][n]){
        bfs2();
    }
    if(vis[1][1])cnt-=2;
    if(vis[n][n])cnt-=2;
    cout<<cnt*9<<endl;
    return 0;
}
```

## [Knight - URAL 1298](https://vjudge.csgrandeur.cn/problem/URAL-1298)

经典马走棋盘问题。

```cpp
const int dx[]={1,1,2,2,-1,-1,-2,-2};
const int dy[]={2,-2,1,-1,2,-2,1,-1};

int n,cnt[10][10];
bool vis[10][10];
pair<int,int> pre[maxn][maxn];
vector<pair<int,int> > v;

inline bool ok(){
	rep(i,n) rep(j,n) if(!vis[i][j]) return 0;
	return 1;
}

inline void print(int x,int y){
	if(pre[x][y].fs!=-1) print(pre[x][y].fs,pre[x][y].sc);
	printf("%c%c\n",char(x+'a'),char(y+'1'));
}

inline bool cmp(pair<int,int> x,pair<int,int> y){
	return cnt[x.fs][x.sc]<cnt[y.fs][y.sc];
}

inline void dfs(int x,int y){
	vis[x][y]=1;
	if(ok()){
		print(x,y);
		exit(0);
	}
	vector<pair<int,int> > w;w.clear();
	rep(i,8){
		int cx=x+dx[i],cy=y+dy[i];
		if(cx>=0&&cx<n&&cy>=0&&cy<n&&!vis[cx][cy]) w.push_back({cx,cy});
	}
	sort(All(w),cmp);
	repV(i,w){
		int cx=i.fs,cy=i.sc;
		pre[cx][cy]={x,y};
		dfs(cx,cy);
	}
	vis[x][y]=0;
}
signed main(){
	n=read();
	up(i,n) 
		rep(j,n){
			v.push_back({i,j});
			rep(k,8){
				int ci=i+dx[k],cj=j+dy[k];
				if(ci>=0&&ci<n&&cj>=0&&cj<n) cnt[i][j]++;
			}
		}
	sort(All(v),cmp);
	repV(it,v) {
		int i=it.fs,j=it.sc;
		MC(vis);
		MC(pre);
		pre[i][j]={-1,-1};
		dfs(i,j);
	}
	puts("IMPOSSIBLE");
	return 0;
}
```

## [Legendary Teams Contest - URAL 1208 ](https://vjudge.csgrandeur.cn/problem/URAL-1208)

暴力 dfs。

```cpp
map<string,int>f;
struct node{
    int a,b,c;
}p[20];
int n,maxz;
int vis[60];
int judge(node x,node y){
    if(x.a==y.b||x.a==y.a||x.a==y.c)return 0;
    if(x.b==y.b||x.b==y.a||x.b==y.c)return 0;
    if(x.c==y.b||x.c==y.a||x.c==y.c)return 0;
    return 1;
}
inline void dfs(int v,int u){
    maxz=max(maxz,v);
    if(u>n)return ;
    if(!vis[p[u].a]&&!vis[p[u].b]&&!vis[p[u].c]){
        vis[p[u].a] = vis[p[u].b] = vis[p[u].c] = 1;
        dfs(v+1,u+1);
        vis[p[u].a] = vis[p[u].b] = vis[p[u].c] = 0;
    }
    dfs(v,u+1);
}
signed main(){
    int i,g=0;
    scanf("%d",&n);
    string s1,s2,s3;
	up(i,1,n){
        cin>>s1>>s2>>s3;
        if(!f[s1])g++,f[s1]=g;
        if(!f[s2])g++,f[s2]=g;
        if(!f[s3])g++,f[s3]=g;
        p[i].a=f[s1];
        p[i].b=f[s2];
        p[i].c=f[s3];
    }
    up(i,1,n){
        vis[p[i].a] = vis[p[i].b] = vis[p[i].c] = 1;
        dfs(1,i+1);
        vis[p[i].a] = vis[p[i].b] = vis[p[i].c] = 0;
    }
    cout<<maxz;
    return 0;
}
```
## [Game with a Strip - URAL 2104](https://vjudge.csgrandeur.cn/problem/URAL-2104)

很基础的一道博弈论。

把搜索数建出来，这是一棵二叉树。

如果两个儿子中有一个是当前人的必胜态，当前人必胜。

若二者都是必败态，那么必败。

否则平局。

```cpp
int n;
char s[M];
int suma[N],sumb[N];
inline int dfs(int L,int R,int opt){     
    if((R-L+1)%2!=0)return 3;
    if(suma[R]-suma[L-1]==R-L+1)return 1; 
    if(sumb[R]-sumb[L-1]==R-L+1)return 2; 
    int mid=(L+R)/2;
    int ls=dfs(L,mid,3-opt);
    int rs=dfs(mid+1,R,3-opt);
    if(ls==opt||rs==opt)return opt;
    if(ls==rs&&ls==3-opt)return 3-opt; 
    return 3;
}
signed main(){
    n=read();
    scanf("%s",s+1);
    scanf("%s",s+1+n);
    up(i,1,2*n){
        suma[i]=suma[i-1]+(s[i]=='A');
        sumb[i]=sumb[i-1]+(s[i]=='B');
    }
    int ans=dfs(1,n+n,1);
    if(ans==1) printf("Alice\n");
    if(ans==2) printf("Bob\n");
    if(ans==3) printf("Draw\n");
	return 0;
}
```

## [Longest k-Good Segment](https://www.luogu.com.cn/problem/CF616D)

用莫队思想去做。

```cpp
int n,m;
int a[N];
int maxl=-1;
int L,R;
int cnt[M],sum;
inline void add(int x){
    cnt[x]++;
    if(cnt[x]==1)sum++;
}
inline void del(int x){
    cnt[x]--;
    if(cnt[x]==0)sum--;
}
signed main(){
    n=read();m=read();
    up(i,1,n)a[i]=read();
    int l=1,ans=0;
    up(r,1,n){
        add(a[r]);
        while(sum>m)del(a[l++]);
        if(ans<r-l+1){
            L=l;R=r;
            ans=r-l+1;
        }
    }
    cout<<L<<" "<<R<<endl;
    return 0;
}
```
## [Professor GukiZ and Two Arrays](https://www.luogu.com.cn/problem/CF620D)

对于 $k=0$ 的情况，直接相减。
对于 $k=1$ 的情况，直接暴力。
对于 $k=2$ 的情况，把 a 数组预处理出来，然后二分查询。

```cpp
int n,m;
int a[N],b[N];
int suma,sumb;
int ans;
int del[2050][2050];
struct node{
	int v,x,y;
	bool operator < (const node &b) const{
		if(v==b.v && x==b.x) return y<b.y;
		if(v==b.v) return x<b.x;
		return v<b.v;
	}
};
set<node>s;
int c[20];
int flag=0;
signed main(){
    n=read();
    up(i,1,n)a[i]=read(),suma+=a[i];
    m=read();
    up(i,1,m)b[i]=read(),sumb+=b[i];
    ans=abs(suma-sumb);
    up(i,1,n){
        up(j,1,m){
            if(ans>abs(suma+b[j]-a[i]-(sumb+a[i]-b[j]))){
                ans=abs(suma+b[j]-a[i]-(sumb+a[i]-b[j]));
                c[0]=i;c[1]=j;
                flag=1;
            }
        }
    }
    up(i,1,m-1){
        up(j,i+1,m){
            s.insert({b[i]+b[j],i,j});
        }
    }    
    up(i,1,n){
        up(j,i+1,n){
            if(s.empty())continue;
            int x=suma-sumb,y=a[i]+a[j];
			auto it=s.lower_bound({y-x/2,0,0});
            if(it==s.end()) it--;
			int t=abs(suma+2*((*it).v)-sumb-2*y);
			if(t<ans){
				ans=t;flag=2;
				c[0]=i;c[1]=(*it).x;
				c[2]=j;c[3]=(*it).y;
			}
			if(it!=s.begin()) it--;
			t=abs(suma+2*((*it).v)-sumb-2*y);
			if(t<ans){
				ans=t;flag=2;
				c[0]=i;c[1]=(*it).x;
				c[2]=j;c[3]=(*it).y;
			}
        }
    }
    cout<<ans<<endl<<flag<<endl;
	if(flag==1) cout<<c[0]<<" "<<c[1]<<endl;
	if(flag==2) cout<<c[0]<<" "<<c[1]<<endl<<c[2]<<" "<<c[3]<<endl;
    return 0;
}
```
## [Foe Pairs](https://www.luogu.com.cn/problem/CF652C)
好题。

对于每一个点，判断其向左最多可以扩展多少。

如果经过标记点更新左端点。
```cpp
int n,m;
int a[N],pos[N];
int to[N];
int L[N];
signed main(){
    n=read();m=read();
    up(i,1,n)a[i]=read(),pos[a[i]]=i;
    int u,v;
    up(i,1,m){
        u=read();v=read();
        int l=pos[u],r=pos[v];
        if(l>r)swap(l,r);
        L[r]=max(L[r],l+1);
    }
    int ans=0;
    int x=1;
    up(i,1,n){
        x=max(x,L[i]);
        ans+=(i-x+1);
    }   
    cout<<ans;
    return 0;
}
```