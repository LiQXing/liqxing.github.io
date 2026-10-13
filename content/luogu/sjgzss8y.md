# 一种优雅的暴力——分块

众所周知，线段树是将一个数组放在二叉树上，每次查询，修改的复杂度是$logn$,空间复杂度是$4N$。而分块则是一种$O(n\sqrt n )$,空间$O(n)$的算法。由于常熟极小，在1e5的范围内跑的比线段树快多了。

给出线段树1的分块代码。

### code
```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long

const int mod=1e8;

inline int read(){
	int u=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){u=u*10+ch-48;ch=getchar();}
	return u*f;
}
int n,m;
int st[50050],ed[50050],pos[500500],sum[50050],add[50050],a[500500];
void init(){
	int block=sqrt(n);
	int t=n/block;
	if(n%block)t++;
	for(int i=1;i<=t;i++){
		st[i]=(i-1)*block+1;
		ed[i]=i*block;
	}
	ed[t]=n;
	for(int i=1;i<=n;i++){
		pos[i]=(i-1)/block+1;
	}
	for(int i=1;i<=t;i++){
		for(int j=st[i];j<=ed[i];j++){
			sum[i]+=a[j];
		}
	}
}
void change(int l,int r,int d){
	int p=pos[l],q=pos[r];
	if(p==q){
		for(int i=l;i<=r;i++)a[i]+=d;
		sum[p]+=d*(r-l+1);
	}
	else{
		for(int i=p+1;i<=q-1;i++)add[i]+=d;
		for(int i=l;i<=ed[p];i++)a[i]+=d;
		sum[p]+=d*(ed[p]-l+1);
		for(int i=st[q];i<=r;i++)a[i]+=d;
		sum[q]+=d*(r-st[q]+1);
	}
}
inline int ask(int l,int r){
	int p=pos[l],q=pos[r];
	int ans=0;
	if(p==q){
		for(int i=l;i<=r;i++)ans+=a[i];
		ans+=add[p]*(r-l+1);
	}
	else{
		for(int i=p+1;i<=q-1;i++)ans+=sum[i]+add[i]*(ed[i]-st[i]+1);
		for(int i=l;i<=ed[p];i++)ans+=a[i];
		ans+=add[p]*(ed[p]-l+1);
		for(int i=st[q];i<=r;i++)ans+=a[i];
		ans+=add[q]*(r-st[q]+1);
	}
	return ans;
}
signed main(){
	n=read();m=read();
	for(int i=1;i<=n;i++)a[i]=read();
	init();
	int op,l,r,k;
	while(m--){
		op=read();
		if(op==1){
			l=read();r=read();k=read();
			change(l,r,k);
		}
		if(op==2){
			l=read();r=read();
			printf("%lld\n",ask(l,r));
		}
	}
    return 0;
}
```

## 教主的魔法
```cpp
```cpp
#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>

const int N=1e6+5000;
const int mod=998244353;
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
int n,m,block,tot;
int a[N],b[N],st[N],ed[N],pos[N],add[N];
inline bool cmp(int x,int y){
	return x>y;
}
inline void init(){
	block=sqrt(n);
	tot=n/block;
	if(n % block)tot++;
	up(i,1,tot){
		st[i]=(i-1)*block+1;
		ed[i]=i*block;
	}
	ed[tot]=n;
	up(i,1,n){
		pos[i]=(i-1)/block+1;
	}
	up(i,1,tot)sort(b+st[i],b+ed[i]+1,cmp);
}
inline void change(int l,int r,int w){
	int p=pos[l],q=pos[r];
	if(p==q){
		up(i,l,r)a[i]+=w;
		up(i,st[p],ed[p])b[i]=a[i];
		sort(b+st[p],b+ed[p]+1,cmp);
	}
	else{
		up(i,l,ed[p])a[i]+=w;
        up(i,st[p],ed[p])b[i]=a[i];
        sort(b+st[p],b+ed[p]+1,cmp);
        up(i,st[q],r)a[i]+=w;
        up(i,st[q],ed[q])b[i]=a[i];
        sort(b+st[q],b+ed[q]+1,cmp);
        up(i,p+1,q-1)add[i]+=w;
	}
}
inline int ask(int l,int r,int w){
	int p=pos[l],q=pos[r],ans=0;
	if(p==q){
		up(i,l,r)if(a[i]+add[p]>=w)ans++;
		return ans;
	}
	else{
		up(i,l,ed[p])if(a[i]+add[p]>=w)ans++;
		up(i,st[q],r)if(a[i]+add[q]>=w)ans++;
		up(i,p+1,q-1){
			ans+=(upper_bound(b+st[i],b+ed[i]+1,w-add[i],cmp)-b-st[i]);
		}
		return ans;
	}
}
signed main(){
	n=read();m=read();
	up(i,1,n){
		a[i]=read();
		b[i]=a[i];
	}
	init();
	char s[5];
	int l,r,w;
	while(m--){
		scanf("%s",s);
		if(s[0]=='M'){
			l=read();r=read();w=read();
			change(l,r,w);
		}	
		if(s[0]=='A'){
			l=read();r=read();w=read();
			write(ask(l,r,w),1);
		}
	}
    return 0;
}
```
# 莫队——基于分块的离线暴力



```cpp
#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>

const int N=1e6+5000;
const int mod=998244353;
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
int a[N],pos[N];
struct node{
	int l,r,k;
}q[N];
int block;
inline bool cmp(node x,node y){
	if(pos[x.l]!=pos[y.l])return pos[x.l]<pos[y.l];
	if(pos[x.l]&1)return x.r>y.r;
	return x.r<y.r;
}
int cnt[N],ans[N],tot;
inline void del(int x){
	cnt[a[x]]--;
	if(!cnt[a[x]])tot--;
}
inline void add(int x){
	cnt[a[x]]++;
	if(cnt[a[x]]==1)tot++;
}
signed main(){
	n=read();
	up(i,1,n)a[i]=read();
	block=sqrt(n);
	up(i,1,n)pos[i]=(i-1)/block+1;
	m=read();
	up(i,1,m){
		q[i].l=read();
		q[i].r=read();
		q[i].k=i;
	}
	sort(q+1,q+1+m,cmp);
    int l=1,r=0;
    up(i,1,m){
    	while(l<q[i].l)del(l),l++;
    	while(r>q[i].r)del(r),r--;
    	while(l>q[i].l)l--,add(l);
    	while(r<q[i].r)r++,add(r);
		ans[q[i].k]=tot;
	}
	up(i,1,m){
		write(ans[i],1);
	}
	return 0;
}
```

# 带修莫队

##  [数颜色](https://www.luogu.com.cn/problem/P1903)

着重讲一下，如果没有修改，就是一个基础的莫队算法。一个查询的左右端点为`[L,R]`,加上修改后，一个查询为`[L,R,t]`,t 表示在查询`[L,R]`前经过了t次修改。

从一个查询移动到另一个查询，除了`L,R`的变化，还要考虑 $t$ 的变化。如果两次查询的 $t$ 相同，说明处于相同的序列，如果不同，就暴力补上变化。

莫队的重点在排序，带修莫队的排序应为：

 1. 左端点`L`的块排序
 2. 右端点`R`的块排序
 3. 时间 $t$ 排序
 由数学计算，当块长为 $n^{\frac{3}{2}}$,时间复杂度为$O(n^{\frac{5}{3}})$,最优。
 
```cpp
#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>

const int N=1e6+5000;
const int mod=998244353;
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
int a[N],pos[N];
int block;
int cnt[N],ans[N],tot;
struct node{
	int l,r,t,k;
}q[N];
struct change{
	int pos,col;
}c[N];
inline void add(int x){
	tot+=!cnt[x]++;
}
inline void del(int x){
	tot-=!--cnt[x];
}
int cntq,cntc;
inline bool cmp(node x,node y){
	if(pos[x.l]!=pos[y.l])return pos[x.l]<pos[y.l];
	if(pos[x.r]!=pos[y.r])return pos[x.r]<pos[y.r];
	return x.t<y.t;
}
inline void upd(int x, int t){
	if (q[x].l<=c[t].pos&&c[t].pos<=q[x].r){
		del(a[c[t].pos]);
		add(c[t].col);
	} 
	swap(a[c[t].pos],c[t].col);
}
signed main(){
	n=read();m=read();
	block=pow(n,0.6666);
	up(i,1,n)a[i]=read(),pos[i]=(i-1)/block+1;
	char op[5];
	up(i,1,m){
		scanf("%s",op);
		if(op[0]=='Q'){
			q[++cntq].l=read();
			q[cntq].r=read();
			q[cntq].t=cntc;
			q[cntq].k=cntq;
		}
		else{
			c[++cntc].pos=read();
			c[cntc].col=read();
		}
	}
	sort(q+1,q+1+cntq,cmp);
	int l=1,r=0,t=0;
	up(i,1,cntq){
		while (l>q[i].l) add(a[--l]);
		while (l<q[i].l) del(a[l++]);
		while (r>q[i].r) del(a[r--]);
		while (r<q[i].r) add(a[++r]);
		while (t<q[i].t) upd(i, ++t);
		while (t>q[i].t) upd(i, t--);
		ans[q[i].k] =tot;
	}
	up(i,1,cntq)write(ans[i],1);
	return 0;
}
```
