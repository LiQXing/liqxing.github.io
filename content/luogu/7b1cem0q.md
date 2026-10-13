[$My\;blog$](https://www.cnblogs.com/LiQXing/p/17797966.html)

rp 大爆发（别一次用完就行了）。

来晚了，差点没赶上考试。

## T1

先看 T1，看上去很像一个三维偏序问题，一看数据范围 $n\le 3\times 10^7$。

打扰了。


不行，再看一眼题目，发现一句话 `请选手仔细观察给出的数据生成器，数据生成方式与解题强相关`。

阿这，原来是一道分析代码题。

看他数据生成器：

```cpp
typedef unsigned long long ull;
int n,A,B,C,u[N],v[N],w[N];
inline ull Rand(ull &k1, ull &k2){
	ull k3 = k1, k4 = k2;
	k1 = k4;
	k3 ^= (k3 << 23);
	k2 = k3 ^ k4 ^ (k3 >> 17) ^ (k4 >> 26);
	return k2 + k4;
} 
inline void GetData () {
	ull x, y;
 	cin >> n >> A >> B >> C >> x >> y;
	up(i,1,n){
 		u[i] = Rand(x, y) % A + 1;
 		v[i] = Rand(x, y) % B + 1;
 		w[i] = Rand(x, y) % C + 1;
 		if (Rand(x, y) % 3 == 0) u[i] = A;
 		if (Rand(x, y) % 3 == 0) v[i] = B;
 		if ((u[i] != A) && (v[i] != B)) w[i] = C;
 	} 
}
```

我们发现 $u_i$，$v_i$ 有三分之一的概率等于 $A$，$B$，$w_i$ 有九分之四的概率等于 $C$。

而且 $w_i$ 等于 $C$ 时，$u_i$，$v_i$ 分别不等于 $A$，$B$（大概率）。

然后我灵机一动，将操作分成两部分，第一种是 $u_i$，$v_i$ 分别等于 $A$，$B$，这个时候就只用找到$\max w_i$ 就行了，另一部分是 $w_i$ 等于 $C$ 的，然后把 $u_i$，$w_i$ 撒在二维平面，一个点代表一个矩形，求矩形面积就行了，我开始还用单调栈，写一半发现因为矩形的高度具有单调性，所以只用记录后缀最大值扫一遍就行了。

但是这有一个问题，就是有一些点没有被统计，所以我们可以 把所有的 $\max<w_i\le C$ 都进行一次如下操作~ ，桥豆麻袋，这样复杂度不就 $n^2$ 了吗？

哎呀~，观察最大的样例，我们发现这个 $\max \approx C$，而且数据纯随机，自信。

复杂度 $O(玄学)$。

```cpp
signed main(){
	GetData();
	int maxl=0;
	up(i,1,n){
		if(u[i]==A&&v[i]==B){
			maxl=max(maxl,w[i]);
			if(w[i]==C){
				i128 t=(i128)A*B*C;
				write(t);
				return 0;
			}	
		}
	}
	ans+=(i128)A*B*maxl;	
	i128 sq=0,pre=0;
	dn(H,C,maxl+1){
		up(i,1,n){
			if(w[i]==H){
				suf[u[i]]=max(suf[u[i]],v[i]);
			}
		}
		sq=0;
		for(int i=A;i>=1;i--){
			suf[i]=max(suf[i],suf[i+1]);
			sq+=suf[i];
		} 
		ans+=(i128)(H-maxl)*(sq-pre);
		pre=sq; 
	}
	write(ans);
	//cout<<ans<<endl;
	return 0;
}

```

## T2

出去洗了把脸看 T2，是期望不是很会的样子。

与前两天的 At_abc_E 类似，

把最后要求的东西看成 $\sum_{i=1}^{n} i*p_i$。

所以我们只用把每一个数留到最后的概率求出来。

然后快速写了个状压求概率。

然后考虑进一步优化。

这个 DP 可不可以用更简单的形式表达出来呢？

对于每一个数，我们似乎只用关心他前面有多少个数就行了，最后的状态就是他排名为 $1$，的情况，想到了这个，这道题就基本想出来了，接下来就只有代码实现问题（然后我在实现上卡了一个小时）。

```cpp
int n,p[N];
int ans=0;
signed main(){	
	n=read();
	up(i,1,n-1){
		p[i]=read();
	}
	up(w,1,n){
		memset(dp,0,sizeof dp);
		dp[1][w]=1;
		up(i,2,n){
			up(j,1,n){
				if(j<=n-i+1)dp[i][j]=(dp[i][j]+dp[i-1][j]*ksm((1-p[i-1]+mod)%mod,j))%mod; 
				if(j!=1)dp[i][j-1]=(dp[i][j-1]+dp[i-1][j]*(1-ksm((1-p[i-1]+mod),j-1)+mod)%mod)%mod;
			}
		}
		ans=(ans+w*dp[n][1])%mod;
	}
	cout<<ans;
	return 0;
}

```

## T3

看着不是很会，于是写了 $15$，分的 $n^3$ 暴力加上输出 $0$ 骗分。

luogu 竟然能的 $35$ 分。

暴力就不放了，没意义。

## T4

题都没看。