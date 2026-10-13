[题目](https://www.luogu.com.cn/problem/P3225)

------------

## 大意：
将某一个点删去。设图中原来有$k$个联通块，如果删掉割点，那么现在就有了$k+1$个联通块，如果不是割点，联通块数目不变。因此我们可以看出，割去任一个割点，割点两边的联通块都需要设一个逃生口。

------------

故 如果没有割点，至少需要建立两个出口，从任意非割点的地方选择两个点建立;如果这个分组只有一个割点,只需要在分组内设立一个出口,可以设立在任意一个非割点的地方;如果有两个及以上个割点，则无需建立，可以直接到达其他联通块
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
