非常毒瘤的一道题

首先考虑如何求出全局最大正方形。

令 $f[i][j]$ 为以 $(i,j)$ 为正方形右下角顶点的边长。

显然 $f[i][j]=\min(f[i-1][j],f[i-1][j-1],f[i][j-1])+1$ 。

如果是多次询问不同的区间呢？

尝试用二维 RMQ 来维护这一区间 dp 的最大值，然后再二分长度。




```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define ull unsigned long long
#define ldo long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=2e5+100;
const int mod=1e9+7;
const int inf=0x3f3f3f3f;

namespace IO{
	inline int read(){
		char c=getchar();int x=0,fh=0;
        while(c<'0'||c>'9'){fh|=c=='-';c=getchar();}
        while(c>='0'&&c<='9'){x=(x<<1)+(x<<3)+(c^48);c=getchar();}
        return fh?-x:x;
	}
	inline void wt(int x){
		if(x<0){x=-x;putchar('-');}
		if(x>9)wt(x/10);
		putchar((x%10)^48);
	}
	inline void write(int x,bool op){
		wt(x);
		putchar(op?'\n':' ');
	}
}using namespace IO;
int n,m;
int a[1020][1020];
int f[11][11][1020][1020];
int lg[1020];
inline void init(){	
	up(i,2,1000){
		lg[i]=lg[i>>1]+1;
	}
	up(i,1,n){
		for(int k=1;(1<<k)<=m;k++){
			for(int j=1;j+(1<<k)-1<=m;j++){
				f[0][k][i][j]=max(f[0][k-1][i][j],f[0][k-1][i][j+(1<<(k-1))]);
			}
		}
	}
	for(int k=1;(1<<k)<=n;k++){
		for(int i=1;i+(1<<k)-1<=n;i++){
			for(int q=0;(1<<q)<=m;q++){
				for(int j=1;j+(1<<q)-1<=m;j++){
					f[k][q][i][j]=max(f[k-1][q][i][j],f[k-1][q][i+(1<<(k-1))][j]);
				}
			}
		}
	}
}
inline bool check(int x1,int y1,int x2,int y2,int x){
	int k1=lg[x2-x1+1],k2=lg[y2-y1+1];
	x2=x2-(1<<k1)+1;
	y2=y2-(1<<k2)+1;
	int y=max(max(f[k1][k2][x1][y1],f[k1][k2][x1][y2]),max(f[k1][k2][x2][y1],f[k1][k2][x2][y2]));
	return y>=x;
}
signed main(){
	n=read();m=read();
	up(i,1,n){
		up(j,1,m){
			a[i][j]=read();
			if(!a[i][j]) f[0][0][i][j]=0;
			else f[0][0][i][j]=min(f[0][0][i][j-1],min(f[0][0][i-1][j],f[0][0][i-1][j-1]))+1;
		}
	}
	init();
	int T=read();
	while(T--){
		int x1=read(),y1=read(),x2=read(),y2=read();
		int l=0,r=min(x2-x1,y2-y1)+1;
		while(l<r){
			int mid=(l+r+1)>>1;
			if(check(x1+mid-1,y1+mid-1,x2,y2,mid))l=mid;
			else r=mid-1;
		}
		write(l,1);
	}
	return 0;
}

```

[$T2$](https://www.luogu.com.cn/problem/CF677D)

这道题还是比较巧妙的。

把两种暴力混合在一起就成了正解。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ull unsigned long long
#define ldo long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=1e6+500;
const int mod=1e9+7;
const int inf=0x3f3f3f3f;

namespace IO{
	inline int read(){
		char c=getchar();int x=0,fh=0;
        while(c<'0'||c>'9'){fh|=c=='-';c=getchar();}
        while(c>='0'&&c<='9'){x=(x<<1)+(x<<3)+(c^48);c=getchar();}
        return fh?-x:x;
	}
	inline void wt(int x){
		if(x<0){x=-x;putchar('-');}
		if(x>9)wt(x/10);
		putchar((x%10)^48);
	}
	inline void write(int x,bool op){
		wt(x);
		putchar(op?'\n':' ');
	}
}using namespace IO;
int n,m,p;
int a[350][350];
vector<pii>g[350*300];

int dis[350][350];
inline int dist(pii a,pii b){
	return abs(a.first-b.first)+abs(a.second-b.second);
}
inline void refresh(int lev){
	for(auto u:g[lev]){
		int ux=u.first,uy=u.second;
		for(auto v:g[lev+1]){
			int vx=v.first,vy=v.second;
			dis[vx][vy]=min(dis[vx][vy],dis[ux][uy]+dist(u,v));
		}
	}
}

const int dx[4]={0,1,0,-1},dy[4]={1,0,-1,0};
int dis2[350][350],vis[350][350];
inline void bfs(int lev){
	memset(dis2,0x3f,sizeof(dis2));
	queue<pii>q;
	for(auto u:g[lev]){
		int ux=u.first,uy=u.second;
		dis2[ux][uy]=dis[ux][uy];
		q.push(u);
		vis[ux][uy]=1;
	}
	while(!q.empty()){
		int ux=q.front().first,uy=q.front().second;q.pop();
		vis[ux][uy]=0;
		up(i,0,3){
			int vx=ux+dx[i],vy=uy+dy[i];
			if(vx<=0||vx>n||vy<=0||vy>m)continue;
			if(dis2[vx][vy]>dis2[ux][uy]+1){
				dis2[vx][vy]=dis2[ux][uy]+1;
				if(!vis[vx][vy]){
					q.push({vx,vy});
					vis[vx][vy]=1;
				}
			}
		}
	}
	for(auto v:g[lev+1]){
		int ux=v.first,uy=v.second;
		dis[ux][uy]=dis2[ux][uy];
	}
}
signed main(){
	n=read();m=read();p=read();
	up(i,1,n){
		up(j,1,m){
			a[i][j]=read();
			g[a[i][j]].push_back({i,j});
		}
	}
	memset(dis,0x3f,sizeof(dis));
	for(int i=0;i<g[1].size();++i){
		int ux=g[1][i].first,uy=g[1][i].second;
		dis[ux][uy]=dist(g[1][i],{1,1});
	}
	up(lev,1,p-1){
		if(g[lev].size()*g[lev+1].size()<n*m)refresh(lev);
		else bfs(lev);
	}
	int res=0x3f3f3f3f;
	for(auto u:g[p]){
		int ux=u.first,uy=u.second;
		res=min(res,dis[ux][uy]);
	}
	write(res,1);
	return 0;
}

```

$$