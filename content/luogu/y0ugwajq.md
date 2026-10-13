# 题目
![题目](https://cdn.luogu.com.cn/upload/image_hosting/6pgu7des.png)

------------
考场思路：线段树+区间修改+区间推平+单点求值
```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
int mod=1e9+7;
inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int a[1000050];
int inf=1145141919810,n;
struct node{
	int l,r,sum,tag1,tag2;
};
node tr[1000050<<2];
inline void push_up(int k){tr[k].sum=(tr[k<<1].sum+tr[k<<1|1].sum)%mod;}
inline void build(int k,int l,int r){
	tr[k].l=l;tr[k].r=r;tr[k].sum=tr[k].tag1=0;
	tr[k].tag2=inf;
	if(l==r){
		tr[k].sum=a[l];
		return ;
	}
	int mid=(l+r)>>1;
	build(k<<1,l,mid);
	build(k<<1|1,mid+1,r);
	push_up(k);
	//tr[k].sum=max(tr[k<<1].sum,tr[k<<1|1].sum);
}
inline void push_down(int k){
    if(tr[k].tag2!=inf){
        tr[k<<1].tag1=0;
        tr[k<<1].tag2=tr[k].tag2;
        tr[k<<1].sum=(tr[k].tag2*(tr[k<<1].r-tr[k<<1].l+1))%mod;
        tr[k<<1|1].tag1=0;
        tr[k<<1|1].tag2=tr[k].tag2;
        tr[k<<1|1].sum=(tr[k].tag2*(tr[k<<1|1].r-tr[k<<1|1].l+1))%mod;
        tr[k].tag2=inf;
    }
    if(tr[k].tag1){
        tr[k<<1].tag1+=tr[k].tag1;
        tr[k<<1].sum+=(tr[k].tag1*(tr[k<<1].r-tr[k<<1].l+1))%mod;
        tr[k<<1|1].tag1+=tr[k].tag1;
        tr[k<<1|1].sum+=(tr[k].tag1*(tr[k<<1|1].r-tr[k<<1|1].l+1))%mod;
        tr[k].tag1=0;
    }
}
inline void change(int k,int l,int r,int x){
	if(l<=tr[k].l&&tr[k].r<=r){
		tr[k].tag1=0;tr[k].tag2=x;
		tr[k].sum=x*(tr[k].r-tr[k].l+1)%mod;
		return;
	}
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(l<=mid) change(k<<1,l,r,x);
	if(r>mid) change(k<<1|1,l,r,x);
	push_up(k);
	//tr[k].sum=max(tr[k<<1].sum,tr[k<<1|1].sum);
}
inline void change2(int k,int l,int r,int x){
	if(l<=tr[k].l&&tr[k].r<=r){
		tr[k].tag1+=x;
		tr[k].sum+=x*(tr[k].r-tr[k].l+1)%mod;
		return;
	}
	push_down(k);
	int mid=(tr[k].l+tr[k].r)>>1;
	if(l<=mid) change2(k<<1,l,r,x);
	if(mid<r)change2(k<<1|1,l,r,x);
	push_up(k);
	//tr[k].sum=max(tr[k<<1].sum,tr[k<<1|1].sum);
}
inline int ask(int k,int l,int r){
	if(l<=tr[k].l&&tr[k].r<=r){
		return tr[k].sum;
	}
	int res=0;
	int mid=(tr[k].l+tr[k].r)>>1;
	push_down(k);
	if(l<=mid) res=(res+ask(k<<1,l,r))%mod;
	if(mid<r)res=(res+ask(k<<1|1,l,r))%mod;
	return res;
}
int ksm(int a,int p){
	int rel=1;
	while(p){
		if(p%2==1)rel=(rel*a)%mod;
		a=(a*a)%mod;
		p>>=1;
	}
	return rel%mod;
}
signed main(){
	n=read();
   	int q=read(),op,x,t,l,ans=0,r;
   	for(int i=1;i<=n;i++) a[i]=read();
   	build(1,1,n);
	while(q--){
		op=read();
		if(op==2){
			l=read();r=read();x=read();
			change(1,l,r,x);
		}
		else if(op==1){
			l=read();r=read();x=read();
			change2(1,l,r,x);
		}
		else{
			l=read();r=read();x=read();
			if(x==0)printf("%lld\n",r-l+1);
			else if(x==1)printf("%lld\n",ask(1,l,r));
			else {
				ans=0;
				for(int i=l;i<=r;i++){
					t=ask(1,i,i);
					ans+=ksm(t,x);
					ans%=mod;
				}
				printf("%lld\n",ans);
			}
		}
	}  	
    return 0;
}
```
考场写挂了，后来按思路，写了40

------------
然后发现k值较小，把sum改为sum[15],  幂次和可以都求出来，再加上二项式展开

****正解
------------
```cpp

