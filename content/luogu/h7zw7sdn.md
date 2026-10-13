
[原题](https://www.luogu.com.cn/problem/P1505)


------------
码量极大，十分毒瘤，这里我采用的是结构体线段树+vector边权转点权（vector万岁！！！）
思路其他题解已经很详细了，这里就不多赘述，直接上代码（以后边权转点权的模板）；
~~~cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,cnt,m,a[500500],b[500500],id[500500],fa[500500];
int siz[500500],son[500500],dep[500500],top[500500];
vector<int>vec[500500];
struct edge{
	int u,v,w;
}e[500500];
struct node{
	int l,r,maxl,minl,sum,tag;
}tr[500500<<2];
void dfs1(int u,int from){
	dep[u]=dep[from]+1;
	son[u]=0;siz[u]=1;
	for(auto v:vec[u]){
		if(v==from) continue;
		fa[v]=u;
		dfs1(v,u);
		siz[u]+=siz[v];
		if(siz[son[u]]<siz[v]) son[u]=v;
	}
}
void dfs2(int u,int tp){
	top[u]=tp;id[u]=++cnt;
	a[cnt]=b[u]; 
	if(son[u])dfs2(son[u],tp);//我是个傻逼，在判断条件前加了个！
	for(auto v:vec[u]){
		if(v==fa[u]||v==son[u])continue;
		dfs2(v,v);
	}
}
void push_up(int k){
	tr[k].maxl=max(tr[k<<1].maxl,tr[k<<1|1].maxl);
	tr[k].minl=min(tr[k<<1].minl,tr[k<<1|1].minl);
	tr[k].sum=tr[k<<1].sum+tr[k<<1|1].sum;
}
void push_down(int k){
	if(tr[k].tag!=0){
		tr[k<<1].tag^=1;tr[k<<1|1].tag^=1;
		tr[k<<1].sum=-tr[k<<1].sum;tr[k<<1|1].sum=-tr[k<<1|1].sum;
		tr[k<<1].maxl=-tr[k<<1].maxl;tr[k<<1|1].maxl=-tr[k<<1|1].maxl;
		tr[k<<1].minl=-tr[k<<1].minl;tr[k<<1|1].minl=-tr[k<<1|1].minl;
		swap(tr[k<<1].maxl,tr[k<<1].minl);
		swap(tr[k<<1|1].maxl,tr[k<<1|1].minl);
		tr[k].tag=0;
	}
}
void build(int k,int l,int r){
	tr[k].l=l;tr[k].r=r;
	if(l==r){
		tr[k].maxl=tr[k].minl=tr[k].sum=a[l];
		return;
	}
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
	push_up(k);
}
void change(int k,int x,int v){
	if(tr[k].l==tr[k].r){
		tr[k].sum=tr[k].maxl=tr[k].minl=v;
		return;
	}
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(x<=mid)change(k<<1,x,v);
	if(x>mid)change(k<<1|1,x,v);
	push_up(k);
}
void update(int k,int l,int r){
	if(tr[k].l>=l&&tr[k].r<=r){
		tr[k].tag^=1;
		tr[k].sum=-tr[k].sum;
		tr[k].maxl=-tr[k].maxl;
		tr[k].minl=-tr[k].minl;
		swap(tr[k].maxl,tr[k].minl);
		return;
	}
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(l<=mid) update(k<<1,l,r);
	if(r>mid)  update(k<<1|1,l,r);
	push_up(k);
}
void change2(int x,int y){
	while(top[x]!=top[y]){
		if(dep[top[x]]<dep[top[y]]) swap(x,y);
		update(1,id[top[x]],id[x]);
		x=fa[top[x]];
	}
	if(dep[x]>dep[y]) swap(x,y);
	if(x!=y) update(1,id[x]+1,id[y]);
}
int sum(int k,int l,int r){
	int res=0;
	if(tr[k].l>=l&&tr[k].r<=r) return tr[k].sum;
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(l<=mid) res+=sum(k<<1,l,r);
	if(r>mid)  res+=sum(k<<1|1,l,r);
	push_up(k);
	return res;
}
int qsum(int x,int y){
	int res=0;
	while(top[x]!=top[y]){
		if(dep[top[x]]<dep[top[y]]) swap(x,y);
		res+=sum(1,id[top[x]],id[x]);
		x=fa[top[x]];
	}
	if(dep[x]>dep[y]) swap(x,y);
	if(x!=y) res+=sum(1,id[x]+1,id[y]);
	return res;
}
int max1(int k,int l,int r){
	int res=-1e14;
	if(l<=tr[k].l&&tr[k].r<=r) return tr[k].maxl;
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(l<=mid) res=max(res,max1(k<<1,l,r));
	if(r>mid)  res=max(res,max1(k<<1|1,l,r));
	push_up(k);
	return res;
}
int qmax(int x,int y){
	int res=-1e14;
	while(top[x]!=top[y]){
		if(dep[top[x]]<dep[top[y]]) swap(x,y);
		res=max(res,max1(1,id[top[x]],id[x]));
		x=fa[top[x]];
	}
	if(dep[x]>dep[y]) swap(x,y);
	if(x!=y) res=max(res,max1(1,id[x]+1,id[y]));
	return res;
}
int min1(int k,int l,int r){
	int res=1e14;
	if(l<=tr[k].l&&tr[k].r<=r) return tr[k].minl;
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(l<=mid) res=min(res,min1(k<<1,l,r));
	if(r>mid)  res=min(res,min1(k<<1|1,l,r));
	push_up(k);
	return res;
}
int qmin(int x,int y){
	int res=1e14;
	while(top[x]!=top[y]){
		if(dep[top[x]]<dep[top[y]]) swap(x,y);
		res=min(res,min1(1,id[top[x]],id[x]));
		x=fa[top[x]];
	}
	if(dep[x]>dep[y]) swap(x,y);
	if(x!=y) res=min(res,min1(1,id[x]+1,id[y]));
	return res;
}
signed main(){
    //freopen("1.txt","r",stdin);
    n=read();
    int x,y,z;
    for(int i=1;i<n;i++){
    	e[i].u=read()+1;e[i].v=read()+1;e[i].w=read();
    	vec[e[i].u].push_back(e[i].v);
    	vec[e[i].v].push_back(e[i].u);	
    }
    m=read();
    dfs1(1,0);
    for(int i=1;i<n;i++){
    	if(dep[e[i].u]>dep[e[i].v])b[e[i].u]=e[i].w;
    	else b[e[i].v]=e[i].w;
    }
    dfs2(1,1);
    build(1,1,n);
    char s[10];
    //for(int i=1;i<=cnt;i++) cout<<id[i]<<endl;
    //cout<<tr[1].sum<<" "<<tr[1].maxl<<" "<<tr[1].minl<<endl;
	while(m--){
		scanf("%s ",s);
		if(s[0]=='C'){
			x=read();z=read();
			y=e[x].v;x=e[x].u;
			dep[x]>dep[y]?change(1,id[x],z):change(1,id[y],z);
		}
		else if(s[0]=='N'){
			x=read()+1;y=read()+1;
			change2(x,y);
		}
		else if(s[0]=='S'){
			x=read()+1;y=read()+1;
			printf("%lld\n",qsum(x,y));
		}
		else if(s[0]=='M'&&s[1]=='A'){
			x=read()+1;y=read()+1;
			printf("%lld\n",qmax(x,y));
		}
		else if(s[0]=='M'&&s[1]=='I'){
			x=read()+1;y=read()+1;
			printf("%lld\n",qmin(x,y));
		}
	}
    return 0;
}