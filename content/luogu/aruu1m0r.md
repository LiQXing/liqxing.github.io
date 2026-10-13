原题：[P1099树网的核](https://www.luogu.com.cn/problem/P1099)

少有的有思路的紫题；

大意：给定一棵带边权无根树，在其直径上求出一段长度不超过s的路径F，使得离路径距离最远的点到路径的距离最短。
二分+树的直径
~~~cpp
#include<bits/stdc++.h>
#define M 500005
using namespace std;
int n,m,x,y,z,k,id,top,ans=2e9;
int dis[M],fa[M],head[M];
bool mark[M];
vector<pair<int,int> >vec[500500];
void dfs1(int f,int x){
    fa[x]=f;
    if(dis[x]>dis[k])k=x;
    for(auto v:vec[x]){
        int y=v.first;
        if(y==f||mark[y])continue;
        dis[y]=dis[x]+v.second;
        dfs1(x,y);
    }
}
int main(){
    scanf("%d%d",&n,&m);
    int x,y,z;
    for(int i=1;i<n;i++){
        scanf("%d%d%d",&x,&y,&z);
        vec[x].push_back({y,z});
        vec[y].push_back({x,z});
    }
    dis[1]=1,dfs1(0,1);
    dis[k]=0,dfs1(0,k);
    top=k;
    for(int i=top,j=top,l=1,r=0;i;i=fa[i]){
        while(dis[j]-dis[i]>m)j=fa[j];
        x=max(dis[top]-dis[j],dis[i]);
        ans=min(ans,x);
    }
    for(int i=top;i;i=fa[i])mark[i]=1;
    for(int i=top;i;i=fa[i]){
        k=i,dis[k]=0;
        dfs1(fa[i],i);
    }
    for(int i=1;i<=n;i++)
        ans=max(ans,dis[i]);
    printf("%d\n",ans);
    return 0;
}
