因为是任选盘子，不用考虑顺序。

$f[i][j][k][l]$  分别表示有 $i$ 个空盘子，$j$  个一个寿司  $k$  个两个寿司，$l$  个三个寿司的盘子。

$$f[i][j][k][l]=1+\frac{i}{n}f[i][j][k][l]+\frac{j}{n}f[i+1][j-1][k][l]+\frac{k}{n}f[i][j+1][k-1][l]+\frac{l}{n}f[i][j][k+1][l-1]$$

$$f[i][j][k][l]=\frac{n}{j+k+l}+\frac{j}{j+k+l}f[i+1][j-1][k][l]+\frac{k}{j+k+l}f[i][j+1][k-1][l]+\frac{l}{j+k+l}f[i][j][k+1][l-1]$$

但是这样空间会炸掉。

因为知道一共有多少个盘子，所以可以压掉一维。

$$f[j][k][l]=\frac{n}{j+k+l}+\frac{j}{j+k+l}f[j-1][k][l]+\frac{k}{j+k+l}f[j+1][k-1][l]+\frac{l}{j+k+l}f[j][k+1][l-1]$$

```cpp
#include<bits/stdc++.h>

using namespace std;

#define int long long
#define ull unsigned long long
#define ldo long double
#define i128 __int128
#define up(a,b,c) for(int a=b;a<=c;a++)
#define dn(a,b,c) for(int a=b;a>=c;a--)
#define pii pair<int,int>
#define lc k<<1
#define rc k<<1|1

const int N=5e5+5000;
const int mod=1e9+7;

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
int n,k;
int a[3050];
ldo f[305][305][305];
int cnt[50];
signed main(){
	n=read();
	up(i,1,n){
		a[i]=read();
		cnt[a[i]]++;
	}
	up(k,0,n){
		up(j,0,n){
			up(i,0,n){
				if(!i&&!j&&!k)continue;
				if(i)f[i][j][k]+=f[i-1][j][k]*i/(i+j+k);
				if(j)f[i][j][k]+=f[i+1][j-1][k]*j/(i+j+k);
				if(k)f[i][j][k]+=f[i][j+1][k-1]*k/(i+j+k);
				f[i][j][k]+=(double)n/(i+j+k);
			}
		}
	}
	printf("%.10LF",f[cnt[1]][cnt[2]][cnt[3]]);
	return 0;
}
```
