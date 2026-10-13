## [P1292](https://www.luogu.com.cn/problem/P1292)

简单题，答案为$a,b$ 的 $\gcd$。

然后解方程 $by\equiv 1\mod (a)$

$by-ax=1$

```cpp
inline void exgcd(int a,int b,int& d,int& x,int& y){
	int t;
	if(b==0){d=a;x=1;y=0;}
	else{
		exgcd(b,a%b,d,x,y);
		t=x;x=y;y=t-(a/b)*y;
	}
}
int a,b;
signed main(){
    a=read();b=read();
    int gcd=__gcd(a,b);
    cout<<gcd<<endl;
    a/=gcd;b/=gcd;
    int x,y,d;
    exgcd(a,b,d,x,y);
    while(x>0||y<=0){
        x-=b;y+=a;
    }
    while(x+b<=0&&y-a>0)x+=b,y-=a;
    cout<<-x<<" "<<y<<endl;
    return 0;
}
```

## [T2](https://www.luogu.com.cn/problem/U91572)


猜出来的结论题。

自己用数据模拟了下，感觉是根据点的权值由大到小一个个删除的。

其实把点删完，等价于把边删完。

删一条边 $[u,v]$ 的权值等于$\min(a[u],a[v])$。

所以删最大点一定最优。

所以只用把点的权值从大往小删除就行了。

```cpp
int n,m;
struct node{
	int v,w,id;
}a[N];
vector<int>g[N];
inline bool cmp(node x,node y){
	return x.v>y.v;
}
unordered_map<int,int>mp;
signed main(){
	n=read();m=read();
	up(i,1,n)a[i].v=read(),a[i].id=i;
	int u,v;
	up(i,1,m){
		u=read();v=read();
		g[u].push_back(v);
		g[v].push_back(u);
	}
	up(i,1,n){
		for(auto v:g[i]){
			a[i].w+=a[v].v;
		}
	}
	sort(a+1,a+1+n,cmp);
	up(i,1,n){
		mp[a[i].id]=i;
	}
	int ans=0;
	up(i,1,n){
		int u=a[i].id;
		ans+=a[i].w;
		for(auto v:g[u]){
			a[mp[v]].w-=a[i].v;
		}
	}
	cout<<ans;
	return 0;
}
```

## [T3](https://www.luogu.com.cn/problem/U189721#submit)

就是暴力bfs+暴力dfs。

```cpp
#include<bits/stdc++.h>

using namespace std;

//#define int long long
#define ull unsigned long long
#define ldb long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1
#define fi first
#define se second

const int N=1e6+100,M=2e6+100;
const int mod=45989;
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
int n,m,s;
int a[350][350];
int sx,sy;
struct node{
    int x,y;
}p[N];
int t;
bool vis[20][350][350];
int dis[20][350][350];
int sum[350][350];
int dx[]={0,1,-1,0,0},dy[]={0,0,0,1,-1};
int tg[20][350][350];
int siz[50];
inline bool check(int x,int y,int r){
    if(x+r>n||x-r<=0||y+r>m||y-r<=0)return 0;
    if(sum[x+r][y+r]-sum[x+r][y-r-1]-sum[x-r-1][y+r]+sum[x-r-1][y-r-1]==0)return 1;
    return 0;
}
inline void bfs(int k,int sx,int sy){
    queue<node>q;
    memset(dis[k],0x3f,sizeof dis[k]);
    dis[k][sx][sy]=0;
    q.push({sx,sy});
    int l=0,r=s,w=0;
    while(l<=r){
        int mid=(l+r)>>1;
        if(check(sx,sy,mid)){
            l=mid+1;w=mid;
        }
        else r=mid-1;
    }
    tg[k][sx][sy]=w;
    siz[k]=w;
    while(q.size()){
        node u=q.front();q.pop();
        up(i,1,4){
            int tx=u.x+dx[i],ty=u.y+dy[i];
            if(tx<=0||ty<=0||tx>n||ty>m)continue;
            if(a[tx][ty]==1)continue;
            l=0,r=s,w=0;
            while(l<=r){
                int mid=(l+r)>>1;
                if(check(tx,ty,mid)){
                    l=mid+1;w=mid;
                }
                else r=mid-1;
            }
            if(dis[k][tx][ty]==dis[k][u.x][u.y]+1){
                tg[k][tx][ty]=max(tg[k][tx][ty],tg[k][u.x][u.y]+w);   
            }
            if(dis[k][tx][ty]>dis[k][u.x][u.y]+1){
                dis[k][tx][ty]=dis[k][u.x][u.y]+1;
                tg[k][tx][ty]=max(tg[k][tx][ty],tg[k][u.x][u.y]+w);   
                q.push({tx,ty});
            }
        }
    }
}
map<int,pii>mp;
int d[50][50];
int val[50][50];
int ans1=inf,sumtg;
bool book[25];
inline bool check2(){
    up(i,1,t)if(book[i]==0)return 0;
    return 1;
}
inline void dfs(int u,int mindis,int maxtg){
    if(mindis>ans1)return;
	if(check2()){
        if(ans1>mindis){
            ans1=mindis;
            sumtg=maxtg;
        }
        else{
            sumtg=max(sumtg,maxtg);
        }
        return;
    }
    up(i,1,t){
        if(!book[i]){
            book[i]=1;
            dfs(i,mindis+d[u][i],maxtg+val[u][i]-siz[u]);
			book[i]=0;
        }
    }
}
signed main(){
	n=read();m=read();s=read();
    up(i,1,n){
        up(j,1,m){
            a[i][j]=read();
            sum[i][j]=sum[i-1][j]+sum[i][j-1]-sum[i-1][j-1]+a[i][j];
        }
    }
    p[0].x=read()+1;p[0].y=read()+1;
    mp[0]={p[0].x,p[0].y};
    t=read();
    up(i,1,t){
        p[i].x=read()+1;
        p[i].y=read()+1;
        mp[i]={p[i].x,p[i].y};
    }
    up(i,0,t){
        bfs(i,p[i].x,p[i].y);
    }
    if(t==1){
        int ans=inf,ans2=0;
        up(i,1,t){
            if(ans>=dis[0][p[i].x][p[i].y]){
                ans=dis[0][p[i].x][p[i].y];
                ans2=max(ans2,tg[0][p[i].x][p[i].y]);
            }
        }
        cout<<ans<<" "<<ans2;
        return 0;
    }
    up(i,0,t){
        up(j,0,t){
            d[i][j]=dis[i][mp[j].first][mp[j].second];
            val[i][j]=tg[i][mp[j].first][mp[j].second];
        }
    }
    dfs(0,0,siz[0]);
	cout<<ans1<<" "<<sumtg<<endl;
    return 0;
}

```

当然，如果想快点，可以状压。

```cpp

    up(i,0,t){
        bfs(i,p[i].x,p[i].y);
    }
    up(i,0,t){
        up(j,0,t){
            d[i][j]=dis[i][mp[j].first][mp[j].second];
            val[i][j]=tg[i][mp[j].first][mp[j].second];
        }
    }
    t++;
    memset(dp,0x3f,sizeof dp);
    dp[1][0]=0;
	int all=(1<<t)-1;
	for(int s=1;s<=all;s++){
		for(int j=0;j<t;j++){
			if((s>>j)&1){
				for(int k=0;k<t;k++){
					if(s^(1<<j)>>k&1){
                        if(dp[s][j]>dp[s^(1<<j)][k]+d[k][j]){
                            dp[s][j]=dp[s^(1<<j)][k]+d[k][j];
                            f[s][j]=f[s^(1<<j)][k]+val[k][j];
                        }
                        else if(dp[s][j]==dp[s^(1<<j)][k]+d[k][j]){
                            f[s][j]=max(f[s^(1<<j)][k]+val[k][j],f[s][j]);
                        }
					}
				}
			}
		}
	}
	int ans=inf,ans2=0;
	for(int i=1;i<t;i++){
        if(ans>=dp[all][i]){
            if(ans>dp[all][i])ans2=f[all][i];
            else ans2=max(ans2,f[all][i]);
            ans=min(ans,dp[all][i]);
        }
	}
	cout<<ans<<" "<<ans2+siz[0]<<endl;;
    return 0;
}

```

注意每个超市的情况不要算两次。

然后因为特判，挂了20.


## [T4](https://www.luogu.com.cn/problem/T145393)

数据非常小，所以可以直接暴力拆点跑最短路。

$dis[u][i]$ 表示到了节点 $u$ ,$\gcd$ 为 $i$ 的最短路。  
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ull unsigned long long
#define ldb long double
#define db double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1
#define fi first
#define se second

const int N=1e6+100,M=2e6+100;
const int mod=1000;
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
struct node{
	int to,g,w;
};
vector<node>g[1005][505];
inline void add(int u,int v,int w){
	up(i,0,500){
		int x=__gcd(w,i);
		g[u][x].push_back({v,i,w/x});
		g[v][x].push_back({u,i,w/x});
	}
}
bool vis[1005][505];
int dis[1005][505];
inline void spfa(){
	queue<pii>q;
	memset(dis,0x3f,sizeof dis);
	up(i,0,500){
		q.push({n,i});
		dis[n][i]=0;
		vis[n][i]=1;
	}
	while(q.size()){
		pii u=q.front();q.pop();
		int ux=u.first,uy=u.second;
		vis[ux][uy]=0;
		for(auto [vx,vy,w]:g[ux][uy]){
			if(dis[vx][vy]>dis[ux][uy]+w){
				dis[vx][vy]=dis[ux][uy]+w;
				if(!vis[vx][vy]){
					vis[vx][vy]=1;
					q.push({vx,vy});
				}
			}
		}
	}
}
signed main(){
	n=read();m=read();
	int u,v,w;
	up(i,1,m){
		u=read();v=read();w=read();
		add(u,v,w);
	}
	spfa();
	int t=read();
	up(i,1,t) {
		u=read();
		write(dis[u][0],1);
	}
	return 0;
}

```