## T1

树的直径.

## T2

非常有意思的一道题

考试的时候想了一个假的贪心，认为用质数拼凑起来的数一定最优，考后才发现一个反例，如 $56=2\times2\times2\times7=7\times8$ 。后者显然优于前者。

不过正解思路与这个贪心有相似之处，首先我们可以晒出 $k$ 以内的质数，然后求出$[l,r]$ 区间中有多少是可以用这些数来表示的。

考虑 DP。$f[i]=min(f[i-1]+1+f[i/j]+1)$。

```cpp
#include<bits/stdc++.h>

using namespace std;

#define LL long long
#define ull unsigned long long
#define db double
#define pii pair<int,int>
#define ldb long double 
#define lc k<<1
#define rc k<<1|1
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)

const int N=2e5,M=3e6;
const int inf=1e9;

inline int read(){
	int x=0,f=1;char ch=getchar();
	while(ch<'0'||ch>'9'){if(ch=='-')f=-1;ch=getchar();}
	while(ch>='0'&&ch<='9'){x=x*10+ch-48;ch=getchar();}
	return x*f;
}
int x=1,y=0,l,r;
bool vis[500];
vector<int>pri;
int f[M];
bool c[M];
int k;
inline void init(){
	up(i,2,k){
		if(vis[i])continue;
		pri.push_back(i);
		for(int j=2;j*i<=105;j++) {
			vis[j*i]=1;
		}
	}
}
int n,ans;
int a[M];
signed main(){
	l=read();r=read();k=read();
	init();
	a[++n]=1;f[n] = 0;
	for(auto v:pri) {
		for(int j = 1;j<=n;++j){
			if ((LL)a[j]*v<=(LL)r)a[++n]=a[j]*v,f[n]=inf;
		}
	}
	sort(a+1,a+1+n);
	f[1]=0;
	up(i,2,k) {
		int x=1;
		up(j,1,n)
			if(a[j]%i==0){
				if(f[x]+1<f[j]&&a[x]*i==a[j])f[j]=f[x]+1;
				if(i+f[j]<=k&&!c[j]&&a[j]>=l)++ans,c[j] = 1;
				++x;
		}
	}
	cout<<ans;
	return 0;
}

```

## T3

你肯定能够想到用 5 个堆来实现这个反悔贪心。

但是太麻烦了。

于是你考虑在连续选两个一个的和直接选一个两个的之间进行比较就可只用两个堆来实现这道提了。

```cpp
int n,w;
int a[N],b[N];
bool vis[N];
priority_queue<pii,vector<pii>,greater<pii> >q1,q2;
int star[N];
signed main(){
    n=read();w=read();
    up(i,0,n-1){
        a[i]=read();
        a[i+n]=read();
        a[i+n]-=a[i];
        q1.push({a[i],i});
        q2.push({a[i]+a[i+n],i});
    }
    int ans=0;
    while(w--){
        while(q1.size()&&vis[q1.top().se])q1.pop();
        while(q2.size()&&vis[q2.top().se])q2.pop();
        int i=q1.top().second;q1.pop();
        while(q1.size()&&vis[q1.top().se])q1.pop();
        if(w&&q2.size()&&q1.size()&&q1.top().first+a[i]>=q2.top().first){
            q1.push({a[i],i});
            i=q2.top().second;
            q2.pop();
        }
        i<n&&(q1.push({a[i+n],i+n}),1);
        ans+=a[i];
        star[i%n]++;
        vis[i]=1;
        //cout<<ans<<endl;
    }
    cout<<ans<<endl;
    up(i,0,n-1) cout<<star[i];
    return 0;
}
```