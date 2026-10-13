## [原题](https://www.luogu.com.cn/problem/P2486)

lc指左端点颜色，rc指右端点颜色，num为颜色种数

------------

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
int n,m,id[500500],top[500500],cnt,fa[500500],siz[500500];
int son[500500],dep[500500],a[500500],b[500500],lc,rc;
vector<int>vec[500500];
struct node{
	int l,r,lc,rc,num,tag;
}tr[500500<<2];
void dfs1(int u,int from){
	dep[u]=dep[from]+1;
	son[u]=0;siz[u]=1;
	for(auto v:vec[u]){
		if(v==from)continue;
		fa[v]=u;
		dfs1(v,u);
		siz[u]+=siz[v];
		if(siz[son[u]]<siz[v])son[u]=v;
	}
}
void dfs2(int u,int tp){
	top[u]=tp;id[u]=++cnt;
	a[cnt]=b[u];
	if(son[u]) dfs2(son[u],tp);
	for(auto v:vec[u]){
		if(v==fa[u]||v==son[u])continue;
		dfs2(v,v);
	}
}
void push_up(int k){
	tr[k].num=tr[k<<1].num+tr[k<<1|1].num;
    if(tr[k<<1].rc==tr[k<<1|1].lc) tr[k].num--;
    tr[k].lc=tr[k<<1].lc;
    tr[k].rc=tr[k<<1|1].rc;
}
void push_col(int k,int col){
	tr[k].lc=tr[k].rc=col;
    tr[k].num=1;tr[k].tag=col;
}
void push_down(int k){
	if(tr[k].tag) {
        push_col(k<<1,tr[k].tag);
        push_col(k<<1|1,tr[k].tag);
        tr[k].tag=0;
    }
}
void build(int k,int l,int r){
	tr[k].l=l;tr[k].r=r;
	if(l==r){
		tr[k].lc=tr[k].rc=a[l];
		tr[k].num=1;
		return;
	}
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
	push_up(k);
}
void update(int k,int l,int r,int v){
	if(tr[k].l>=l&&tr[k].r<=r){
		push_col(k,v);
		return;
	}
	int mid=(tr[k].l+tr[k].r)>>1;
	push_down(k);
	if(l<=mid)update(k<<1,l,r,v);
	if(r>mid) update(k<<1|1,l,r,v);
	push_up(k);
}
void add(int x,int y,int v){
	while(top[x]!=top[y]){
		if(dep[top[x]]<dep[top[y]]) swap(x,y);
		update(1,id[top[x]],id[x],v);
		x=fa[top[x]];
	}
	if(dep[x]>dep[y]) swap(x,y);
	update(1,id[x],id[y],v);
}
int qnum(int k,int l,int r){
	if(tr[k].l>=l&&tr[k].r<=r){
		if(l==tr[k].l)lc=tr[k].lc;
		if(r==tr[k].r)rc=tr[k].rc;
		return tr[k].num;
	}
	push_down(k);//不要掉了
	int mid=(tr[k].l+tr[k].r)>>1;
	if(r<=mid) return qnum(k<<1,l,r);
	if(l>mid) return qnum(k<<1|1,l,r);
	int res=qnum(k<<1,l,r)+qnum(k<<1|1,l,r);
	if(tr[k<<1].rc==tr[k<<1|1].lc)res--;
	return res;
}
int ask(int x,int y){
	int res=0,pos1=0,pos2=0;
	while(top[x]!=top[y]){
		if(dep[top[x]]<dep[top[y]]) swap(x,y),swap(pos1,pos2);
		res+=qnum(1,id[top[x]],id[x]);
		if(rc==pos1)res--;
		pos1=lc;x=fa[top[x]];
	}
	if(id[x]>id[y]) swap(x,y),swap(pos1,pos2);
	res+=qnum(1,id[x],id[y]);
	if(lc==pos1)res--;
	if(rc==pos2)res--;
	return res;
}
signed main(){
	n=read();m=read();
	for(int i=1;i<=n;i++)b[i]=read();
	int x,y,z;
	for(int i=1;i<n;i++){
		x=read();y=read();
		vec[x].push_back(y);
		vec[y].push_back(x);
	}
	dfs1(1,0);
	dfs2(1,1);
	build(1,1,n);
	char op;
	while(m--){
		cin>>op;
		if(op=='Q'){
			x=read();y=read();
			printf("%lld\n",ask(x,y));
		}
		else{
			x=read();y=read();z=read();
			add(x,y,z);
		}
	}
    return 0;
}

