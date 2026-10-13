# 数据结构

## 树状数组

[$problem.1$](https://www.luogu.com.cn/problem/P5482)

解：

$ax+b>c$可化为$x>\dfrac{c-b}{a}$或$x>\dfrac{b-c}{a}$，故可化为数轴上的点，又因为$-10^6\le k \le10^6$,所以建立树状数组，从$0$到$2\times10^6$

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define inf 1e14
#define mod 1000000007
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
const int N = 1e6;
int cnt,k[N + 60],ans,sum,a,b,c,p[N + 60],num1[(N << 1) + 60],num2[(N << 1) + 60];
char op[20];
inline void add(int x, int val, int c[]){
	x += N;						
	for(; x<= (N<<1); x += x&(-x)) c[x]+=val;
	return ;
}
inline int ask(int x, int c[]){
	x += N;
	int res=0;
	for(; x; x -= x&(-x)) res += c[x];
	return res;
}
signed main(){
	int n=read();
	while(n--) {
		scanf("%s ",op);
		if(op[0] == 'A') {
			cin >>a >>b >>c;
			if(a == 0) {
				if(b > c) {
					ans++;
					k[++cnt] = 3;
				} 
				else k[++cnt] = 0;
			} 
			else if(a > 0) {
				p[++cnt] = floor((c * 1.0 - b)/a);
				k[cnt] = 1; 
				if(p[cnt] > N) k[cnt] = 0;
				else if(p[cnt] < -N){
					ans ++;
					k[cnt] = 3;
				} 
				else add(p[cnt], 1, num1);
			} 
			else {
				p[++cnt] = ceil((c * 1.0 - b)/a);
				k[cnt] = 2;
				if(p[cnt] < -N) k[cnt] = 0;
				else if(p[cnt] > N){
					ans ++;
					k[cnt] = 3;
				} 
				else add(p[cnt], 1, num2);
			}
		} 
		else if(op[0] == 'D') {
			cin >>a;
			if(k[a] == 3) ans --;
			else if(k[a] == 1) add(p[a], -1, num1);
			else if(k[a] == 2) add(p[a], -1, num2);
			k[a] = 0;
		} 
		else{
			a=read();
			cout<<ask(a-1, num1) + (ask(N, num2)- ask(a, num2))+ ans<<endl;
		}
	}
	return 0;
}
```
[$problem.2$](https://www.luogu.com.cn/problem/P5463)
```cpp
#include<bits/stdc++.h>
using namespace std;
#define int __int128
#define inf 1e14
#define mod 1000000007
#define N 1500500
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
inline void write(__int128 x){
    if(x<0){putchar('-');x=-x;}
    if(x>9)write(x/10);
    putchar(x%10+'0');
}
int a[N],b[N],c[N],m,n;
inline int lowbit(int x){
	return x&(-x);
}
inline void add(int x,int v){
    for(;x<=m;x+=lowbit(x))	c[x] +=v;
}
inline int sum(int x){
    int ans =0;
    for(;x;x-=lowbit(x))ans+=c[x];
    return ans;
}
signed main(){
	n =read();
    for(int i=1;i<=n;++i)a[i] =b[i] =read();
    sort(b+1,b+n+1);
    m = unique(b+1,b+n+1)-b-1;
    for (int i=1;i<=n;++i)a[i]=lower_bound(b+1,b+m+1,a[i])-b; 
    int ans =0;
    for(int i=1;i<=n;++i){
    	add(a[i],i);
    	ans+=(n-i+1)*(sum(m)-sum(a[i]));
    }	
    write(ans);
	return 0;
}
```

[$problem.3$](https://www.luogu.com.cn/problem/P1637)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define inf 1e14
#define mod 1000000007
#define N 500500
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
struct node{
	int num,pos;
}a[N];
struct st{
	int sum,l,r;
}tr[N<<2];
int n,f[2077][2077],ans,cnt,num[N],bigger[N],smaller[N];
bool cmp(node x,node y){return x.num<y.num;}
void build(int k,int l,int r){
	tr[k].l=l;tr[k].r=r;
	if(l==r)return;
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
}
inline void push_up(int k){
	tr[k].sum=tr[k<<1].sum+tr[k<<1|1].sum;
}
inline void update(int k,int pos){
    if(tr[k].l==tr[k].r&&tr[k].l==pos){tr[k].sum++;return;}
    int mid=(tr[k].l+tr[k].r)>>1;
    if(mid>=pos) update(k<<1,pos);
    if(mid<pos) update(k<<1|1,pos);
    push_up(k);
}
inline int ask(int k,int l,int r){
	if(tr[k].l>=l&&tr[k].r<=r)return tr[k].sum;
	int mid=(tr[k].l+tr[k].r)>>1;
	int res=0;
	if(mid>=l)res+=ask(k<<1,l,r);
	if(mid<r)res+=ask(k<<1|1,l,r);
    return res; 
}
signed main() {
	n=read();
	for(int i=1;i<=n;i++){
		a[i].num=read();
		a[i].pos=i;
	}
	sort(a+1,a+1+n,cmp);
	for(int i=1;i<=n;i++) {
        if(a[i].num>a[i-1].num) cnt++;
        num[a[i].pos]=cnt;//离散化 
    }
    build(1,1,n);
    for(int i=1;i<=n;i++){
        if(num[i]>1) smaller[i]=ask(1,1,num[i]-1);
        update(1,num[i]);
    }
    for(int i=1;i<=(n<<2);i++)tr[i].sum=0;
    for(int i=n;i>=1;i--){
        if(num[i]<n) bigger[i]=ask(1,num[i]+1,n);
        update(1,num[i]);
    }
    for(int i=1;i<=n;i++) ans+=(bigger[i]*smaller[i]);
	printf("%lld",ans);
	return 0;
}
```

$problem.4$

题意：给一颗$n$个点的树，对每一个点$x$，求有几个祖先点权小于$x$

```cpp
鸽
```

## 线段树

$problem.5$

题意：给一个长为$n$的数列，$m$次操作，操作有三种

$1.$修改数列中一个数

$2.$求数列中一段所有数两两乘积的和 $\mod1e9+7$

$3.$求数列中一段所有相邻数两两乘积的和$\mod1e9+7$

```cpp
鸽
```

[$problem.6$](https://www.luogu.com.cn/problem/P4513)

```cpp
#include<bits/stdc++.h>
#define int long long
using namespace std;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int n,m,a[500500];
struct node{
	int l,r,sum,lmax,rmax,max;
}tr[500500<<2];
inline void push_up(int k){
	tr[k].sum=tr[k*2].sum+tr[k*2+1].sum;
    tr[k].lmax=max(tr[k*2].lmax,tr[k*2].sum+tr[k*2+1].lmax);
    tr[k].rmax=max(tr[k*2+1].rmax,tr[k*2].rmax+tr[k*2+1].sum);
    tr[k].max=max(max(tr[k*2].max,tr[k*2+1].max),tr[k*2].rmax+tr[k*2+1].lmax);
}
inline void build(int k,int l,int r){
	tr[k].l=l;tr[k].r=r;
	if(l==r){tr[k].sum=tr[k].lmax=tr[k].rmax=tr[k].max=a[l];return;}
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
	push_up(k);
}
inline void change(int k,int x,int r){
	if(tr[k].l==tr[k].r){tr[k].sum=tr[k].lmax=tr[k].rmax=tr[k].max=r;return;}
	int mid=(tr[k].l+tr[k].r)>>1;
	if(mid>=x)change(k<<1,x,r);
	else change(k<<1|1,x,r);
	push_up(k);
}
node ask(int k,int l,int r){
	if(l<=tr[k].l&&tr[k].r<=r){return tr[k];}
	int mid=(tr[k].r+tr[k].l)>>1;
	if(r<=mid) return ask(k<<1,l,r);
    if(l>mid) return ask(k<<1|1,l,r);      
    node t,a=ask(k<<1,l,r),b=ask(k<<1|1,l,r);
    t.lmax=max(a.lmax,a.sum+b.lmax);
    t.rmax=max(b.rmax,a.rmax+b.sum);
    t.max=max(max(a.max,b.max),a.rmax+b.lmax);
    return t;
}
signed main(){
    n=read();m=read();
    for(int i=1;i<=n;i++) a[i]=read();
    build(1,1,n);
    int op,a,b;
    for(int i=1;i<=m;i++){
    	op=read();a=read();b=read();
    	if(op==2){
    		change(1,a,b);
    	}
    	else{
    		if(a>b)swap(a,b);
    		printf("%lld\n",ask(1,a,b).max);
    	}
    }
    return 0;
}
```

[$problem.7$](https://www.luogu.com.cn/problem/P7706)

```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define inf 1e14
#define mod 1000000007
#define N 1500500
inline int read(){
	int x=0,f=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if (ch=='-') f=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int a[N],b[N],n,m;
struct node{
	int l,r,a,b,lmx,rmx,ans;
}tr[500500<<2];
node operator + (node x,node y){
	node g;
	g.a=max(x.a,y.a);		
	g.b=min(x.b,y.b);
	g.lmx=max(x.lmx,max(y.lmx,x.a-y.b));		
	g.rmx=max(x.rmx,max(y.rmx,y.a-x.b));
	g.ans=max(x.ans,max(y.ans,max(x.lmx+y.a,x.a+y.rmx)));
	return g;
}
void push_up(int k){
	tr[k].a=max(tr[k<<1].a,tr[k<<1|1].a);
	tr[k].b=min(tr[k<<1].b,tr[k<<1|1].b);
	tr[k].lmx=max(tr[k<<1].lmx,max(tr[k<<1|1].lmx,tr[k<<1].a-tr[k<<1|1].b));
	tr[k].rmx=max(tr[k<<1].rmx,max(tr[k<<1|1].rmx,tr[k<<1|1].a-tr[k<<1].b));
	tr[k].ans=max(tr[k<<1].ans,max(tr[k<<1|1].ans,max(tr[k<<1].lmx+tr[k<<1|1].a,tr[k<<1|1].rmx+tr[k<<1].a)));	
}
void build(int k,int l,int r){
	tr[k].l=l;tr[k].r=r;
	if(l==r){
		tr[k].a=a[l];
		tr[k].b=b[l];
		tr[k].lmx=tr[k].rmx=tr[k].ans=-0x3f3f3f3f;	
		return;
	}
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
	push_up(k);
}
void changeA(int k,int x,int y){
	if(tr[k].l==tr[k].r){
		tr[k].a=y;
		return;
	}
	int mid=(tr[k].l+tr[k].r)>>1;
	if(x<=mid)changeA(k<<1,x,y);
	if(x>mid)changeA(k<<1|1,x,y);
	push_up(k);
}
inline void changeB(int k,int x,int y){
	if(tr[k].l==tr[k].r){
		tr[k].b=y;
		return;
	}
	int mid=(tr[k].l+tr[k].r)>>1;
	if(x<=mid)changeB(k<<1,x,y);
	if(x>mid)changeB(k<<1|1,x,y);
	push_up(k);
}
inline node ask(int k,int l,int r){
	if(tr[k].l>=l&&tr[k].r<=r){
		return tr[k];
	}
	int mid=(tr[k].l+tr[k].r)>>1;
	if(mid>=r)return ask(k<<1,l,r);
	if(mid<l)return ask(k<<1|1,l,r);
	return ask(k<<1,l,r)+ask(k<<1|1,l,r);
}
signed main(){
	n=read();m=read();
	for(int i=1;i<=n;i++)a[i]=read();
	for(int i=1;i<=n;i++)b[i]=read();
	build(1,1,n);
	int op,x,y,l,r;
	while(m--){
		op=read();
		if(op==1){
			x=read();y=read();
			changeA(1,x,y);
		}
		if(op==2){
			x=read();y=read();
			changeB(1,x,y);
		}
		if(op==3){
			l=read();r=read();
			printf("%lld\n",ask(1,l,r).ans);
		}
	}
	return 0;
}
```

[$problem.8$](https://www.luogu.com.cn/problem/P1471)

```cpp
#include <cstdio>
#include <iostream>
#define Maxn 300010
using namespace std;
double sega[Maxn],segb[Maxn],a[250000];
double mark[Maxn];
void pushup(int x)
{
    sega[x]=sega[x<<1]+sega[x<<1|1];
    segb[x]=segb[x<<1]+segb[x<<1|1];
}
void pushdown(int rt,int x)
{
    if (mark[rt])
    {
        segb[rt<<1]+=2*mark[rt]*sega[rt<<1]+(x-x/2)*mark[rt]*mark[rt];
        segb[rt<<1|1]+=2*mark[rt]*sega[rt<<1|1]+(x/2)*mark[rt]*mark[rt];
        sega[rt<<1]+=(x-x/2)*mark[rt];
        sega[rt<<1|1]+=(x/2)*mark[rt];
        mark[rt<<1]+=mark[rt];
        mark[rt<<1|1]+=mark[rt];
        mark[rt]=0;
    }
}
void build(int rt,int l,int r)
{
    if (l==r){
    	sega[rt]=a[l];
    	segb[rt]=a[l]*a[l];
    }
    else
    {
        int mid=(l+r)/2;
        build(rt<<1,l,mid);
        build(rt<<1|1,mid+1,r);
        pushup(rt);
    }
}
double query_a(int rt,int l,int r,int L,int R)
{
    if (l>=L && r<=R)
        return sega[rt];
    else
    {
        pushdown(rt,r-l+1);
        int mid=(r+l)/2;
        double ret=0;
        if (mid>=L)
            ret+=query_a(rt<<1,l,mid,L,R);
        if (mid<R)
            ret+=query_a(rt<<1|1,mid+1,r,L,R);
        return ret;
    }
}
double query_b(int rt,int l,int r,int L,int R)
{
    //--L--l--r--R--
    if (l>=L && r<=R)
        return segb[rt];
    else
    {
        pushdown(rt,r-l+1);
        int mid=(r+l)/2;
        double ret=0;
        if (mid>=L)
            ret+=query_b(rt<<1,l,mid,L,R);
        if (mid<R)
            ret+=query_b(rt<<1|1,mid+1,r,L,R);
        return ret;
    }
}
void update(int rt,int l,int r,int L,int R,double x)
{
    if (l>=L && r<=R)
        mark[rt]+=x,segb[rt]+=2*x*sega[rt]+x*x*(r-l+1),sega[rt]+=(r-l+1)*x;
    else
    {
        pushdown(rt,r-l+1);
        int mid=(r+l)/2;
        if (mid>=L)
            update(rt<<1,l,mid,L,R,x);
        if (mid<R)
            update(rt<<1|1,mid+1,r,L,R,x);
        pushup(rt);
    }
}
double sqr(double x)
{
    return x*x;
}
main()
{
    int n,m,x,y,c;
    double z;
    scanf("%d %d",&n,&m);
    for(int i=1;i<=n;i++) scanf("%lf",&a[i]);
    build(1,1,n);
    for (int i=1;i<=m;i++)
    {
        scanf("%d",&c);
        if (c==2)
            scanf("%d%d",&x,&y),printf("%.4lf\n",query_a(1,1,n,x,y)/(y-x+1));
        if (c==1)
            scanf("%d%d",&x,&y),cin>>z,update(1,1,n,x,y,z);
        if (c==3)
        {
            scanf("%d%d",&x,&y);
            double sum1=query_b(1,1,n,x,y)/(y-x+1),sum2=query_a(1,1,n,x,y)/(y-x+1);
            double ans=sum1-sum2*sum2;
            printf("%.4lf\n",ans);
        }
    }
}

```

[$problem.9$](https://www.luogu.com.cn/problem/P4344)

```cpp
#include <bits/stdc++.h>
using namespace std;
inline int read(){
	int x=0,opt=1;char ch=getchar();
	while (ch<'0'||ch>'9'){if(ch=='-')opt=-1;ch=getchar();}
	while (ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*opt;
}
struct node{
	int l,r,lmax,rmax,sum,tag,len,ans;
}tr[500500<<2];
int n,m,l0,r0,l1,r1,opt;
void pushup(int k){
	tr[k].sum=tr[k<<1].sum+tr[k<<1|1].sum;
	if(tr[k<<1].lmax==tr[k<<1].len)tr[k].lmax=tr[k<<1].len+tr[k<<1|1].lmax;
	else tr[k].lmax=tr[k<<1].lmax;
	if(tr[k<<1|1].rmax==tr[k<<1|1].len)tr[k].rmax=tr[k<<1|1].len+tr[k<<1].rmax;
	else tr[k].rmax=tr[k<<1|1].rmax;
	tr[k].ans=max(max(tr[k<<1].ans,tr[k<<1|1].ans),tr[k<<1].rmax+tr[k<<1|1].lmax);
}
void down1(int k){
	tr[k].ans=tr[k].lmax=tr[k].rmax=tr[k].len;
	tr[k].sum=0;
	tr[k].tag=1;
}
void down2(int k){
	tr[k].ans=tr[k].lmax=tr[k].rmax=0;
	tr[k].sum=tr[k].len;
	tr[k].tag=2;
}
void push_down(int k){
	if(tr[k].tag==1){
		down1(k<<1);down1(k<<1|1);
		tr[k].tag=0;
	}
	if(tr[k].tag==2){
		down2(k<<1);down2(k<<1|1);
		tr[k].tag=0;
	}
}
void build(int k,int l,int r){
	tr[k].tag=0;tr[k].l=l;tr[k].r=r;
	tr[k].len=r-l+1;
	if(l==r){
		tr[k].sum=1;
		tr[k].ans=tr[k].lmax=tr[k].rmax=0;
		return;
	}
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
	pushup(k);
}
void change(int k,int x,int y,int z){
	if(tr[k].l>=x&&tr[k].r<=y){
		if(z==1)down1(k);
		if(z==2)down2(k);
		return;
	}
	push_down(k);
	if(tr[k<<1].r>=x)change(k<<1,x,y,z);
	if(tr[k<<1|1].l<=y)change(k<<1|1,x,y,z);
	pushup(k);
}
int asksum(int k,int x,int y){
	if(tr[k].l>=x&&tr[k].r<=y)return tr[k].sum;
	push_down(k);
	if(tr[k<<1].r<x)return asksum(k<<1|1,x,y);
	if(tr[k<<1|1].l>y)return asksum(k<<1,x,y);
	return asksum(k<<1,x,y)+asksum(k<<1|1,x,y);
}
void work(){
	l1=read();r1=read();
	int x=asksum(1,l0,r0);
	if(x==0)return;
	change(1,l0,r0,1);
	int l=l1,r=r1+1;
	while(l+1<r){
		int mid=(l+r)>>1;
		if((mid-l1+1)-asksum(1,l1,mid)<=x)l=mid;
		else r=mid;
	}
	change(1,l1,l,2);
}
int askans(int k,int x,int y){
	if(tr[k].l>=x&&tr[k].r<=y)return tr[k].ans;
	push_down(k);
	if(tr[k<<1].r<x)return askans(k<<1|1,x,y);
	if(tr[k<<1|1].l>y)return askans(k<<1,x,y);
	return max(max(askans(k<<1,x,y),askans(k<<1|1,x,y)),min(tr[k<<1].rmax,tr[k<<1|1].l-x)+min(tr[k<<1|1].lmax,y-tr[k<<1].r));
}
void print(int k,int l,int r){
	if(l==r){
		cout<<tr[k].sum<<" ";
		return;
	}
	int mid=(l+r)>>1;
	print(k<<1,l,mid);
	print(k<<1|1,mid+1,r);
}
int main(){
	n=read();m=read();
	build(1,1,n);
	//print(1,1,n);printf("\n");
	while(m--){
		opt=read();l0=read();r0=read();
		switch(opt){
			case 0:change(1,l0,r0,1);break;
			case 1:work();break;
			case 2:printf("%d\n",askans(1,l0,r0));//print(1,1,n);printf("\n");break;
		}
	}
	return 0;
}

```

[$problem.10$](https://www.luogu.com.cn/problem/P3215)

```cpp
鸽
```



