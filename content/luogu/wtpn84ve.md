# 前言

之前写过一篇用递推实现的数位dp的学习笔记，过了三个月，发现完全不会做。于是痛定思痛，决定磨碎道基，重修大道，以 $dfs$ 证得仙王果位。

# 数位DP能够解决的问题
首先我们要清楚数位 $dp$ 解决的是什么问题：

**求出在给定区间`[L,R] `内，符合条件 $f(i)$ 的数的个数。条件$f(i)$一般与数的大小无关，而与数的组成有关**

由于数是按位dp，**数的大小对复杂度的影响很小**

# 实现过程
## 记搜过程
从起点向下搜索，到最底层得到方案数，一层一层向上返回答案并累加，最后从搜索起点得到最终答案。

对于` [L,R]` 区间问题，我们一般把他转化为两次数位dp,即找 `[0,R]` 和 `[0,L−1]` 两段，再将结果相减就得到了我们需要的 `[L,R]`.
## 状态设计
$dfs$需要那些变量？

 1. 首先是数字位数$pos$,记录答案的$st$,最高位限制的$lim$
 2. 判断前导0的$lead$
 3. 由于数位dp解决的大多是数字组成问题，所以经常要比较当前位和前一位或前几位的关系（根据题意而定），所以一般在$dfs()$中也要记录前一位或前几位数$pre$方便比较。

 ## 细节
### 前导0

 1.如果当前位 $lead=1$ 而且当前位也是0，那么当前位也是前导0， $pos+1$ 继续搜；
 2. 如果当前位 $lead = 1$ 但当前位不是0，则本位作为当前数的最高位， $pos+1$ 继续搜；（注意这次根据题意st或其他参数可能发生变化）

### 最高位标记
为了分清这两种情况，我们引入了 limit 标记：

1.  若当前位$ limit=1$ 而且已经取到了能取到的最高位时，下一位 $limit=1$ ；

2. 若当前位 $limit=1$ 但是没有取到能取到的最高位时，下一位 $limit=0$ ；

3. 若当前位 $limit=0$ 时，下一位 $limit=0$ 。

我们设这一位的标记为 $limit$ ，这一位能取到的最大值为 $res$ ，则下一位的标记就是 `i==res && limit`
**当 `limit==1||lead==1` 时，不能记录和取用dp值！**

# 例题

## 数字游戏

大意：定义一种不降数，这种数字必须满足从左到右各位数字成小于等于的关系，如 $123$，$446$。给出区间`[L,R]`求该区间有多少不降数。
### code
```cpp

#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

const int N=5e5;
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
int num[50],len,f[50][50];
inline int dfs(int pos,int pre,int limit,int lead){
	if(!pos)return 1;
	if(f[pos][pre]!=-1&&limit==0)return f[pos][pre];
	int ret=0;
	int res=limit?num[pos]:9;
	up(i,pre,res){
		if(lead&&!i)ret+=dfs(pos-1,i,limit&&i==res,lead&&!i);
		else ret+=dfs(pos-1,i,limit&&i==res,lead&&!i);
	}
	if(!limit&&!lead)f[pos][pre] = ret;
	return ret;
}
inline int dp(int x){
	if(x==0)return 1;
	len=0;
	while(x)num[++len]=x%10,x/=10;
	memset(f,-1,sizeof f);
	return dfs(len,0,1,1);
}
signed main(){
	int l,r;
	while(cin>>l>>r){
		cout<<dp(r)-dp(l-1)<<"\n";
	}
	return 0;
}
```  
## 数字游戏 2
找到区间 `[L,R]`各位数字之和 $\mod p=0$ 的数的个数。
这种带模数的就加一个变量就行。

```cpp
#include <bits/stdc++.h>

using namespace std;

//#define int long long
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define ls k<<1
#define rs k<<1|1

const int N=5e5;
//const int mod=998244353;

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
int num[50],len,f[50][1500],mod;
inline int dfs(int pos,int sum,int limit,int lead){
	if (!pos) return sum%mod==0;
	if(f[pos][sum]!=-1&&!limit&&!lead)return f[pos][sum];
	int ret=0;
	int res=limit?num[pos]:9;
	up(i,0,res){
		if(lead&&!i)ret+=dfs(pos-1,(i+sum)%mod,limit&&i==res,lead&&!i);
		else ret+=dfs(pos-1,(i+sum)%mod,limit&&i==res,lead&&!i);
	}
	if(!limit&&!lead)f[pos][sum]=ret;
	return ret;
}
inline int dp(int x){
	//if(x==0)return 0;
	len=0;
	while(x)num[++len]=x%10,x/=10;
	memset(f,-1,sizeof f);
	return dfs(len,0,1,1);
}
signed main(){
	int l,r;
	while(cin>>l>>r>>mod){
		cout<<dp(r)-dp(l-1)<<"\n";
	}
	return 0;
}
```
