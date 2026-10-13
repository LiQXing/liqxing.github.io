## [Maximum Submatrix 2](https://www.luogu.com.cn/problem/CF375B)

很巧妙的一道题。

行是可以随便换的，因此从第 $m$ 列到第 $1$ 列递推，每次只与当前列右边第一串 $1$ 的个数有关，这样每次就可以从第 $i+1$ 列递推到第 $i$ 列，就记一下极长的 $1$ 个数，然后逆序排序统计答案即可。


## [Counting Rectangles is Fun](https://www.luogu.com.cn/problem/CF372B)

看一下数据，是一道$O(n^4)$ 的题。
$f[i][j][k][l]$  表示以 $(i,j)$ 为左上角，$(k,l)$ 为右下角的个数。

$dp[i][j][k][l]$ 为答案。

```cpp
inline bool clac(int i,int j,int k,int l){
    return sum[k][l]-sum[k][j-1]-sum[i-1][l]+sum[i-1][j-1]==0;
}
int q;
signed main(){
    n=read();m=read();q=read();
    up(i,1,n){
        up(j,1,m){
            scanf("%1lld",&a[i][j]);
            sum[i][j]=sum[i-1][j]+sum[i][j-1]-sum[i-1][j-1]+a[i][j];
        }
    }
    up(i,1,n){
        up(j,1,m){
            up(k,i,n){
                up(l,j,m){
                    f[i][j][k][l]=f[i][j][k-1][l]+f[i][j][k][l-1]-f[i][j][k-1][l-1]+clac(i,j,k,l);
                }
            }
        }
    }

    dn(i,n,1){
        dn(j,m,1){
            dn(k,n,i){
                dn(l,m,j){
                    dp[i][j][k][l]=dp[i+1][j][k][l]+dp[i][j+1][k][l]-dp[i+1][j+1][k][l]+f[i][j][k][l];
                }
            }
        }
    }
    while(q--){
        int a=read(),b=read(),c=read(),d=read();
        write(dp[a][b][c][d],1);
    }
	return 0;
}
```
## [Game with Strings ](https://www.luogu.com.cn/problem/CF354B)
假设已经走了$x$歩，那么我们可以发现，此时可能的位置的范围是在一条对角线的位置，一条对角线长度最多只有20，利用状压的思想，可以用一组二进制数来表示走这条对角线的位置是否是等价的，那么通过这个就可以向下推导下一步的情况。
```cpp
char a[55][55];
int dp[40][1<<20],n;
bool vis[40][1<<20];
inline int dfs(int step,int st){
	if(vis[step][st])return dp[step][st];
	int&res=dp[step][st];
	vis[step][st]=1;
	if(step==n*2-2)res=0;
	else{
		if(step&1)res=-inf;
		else res=inf;
		int mask[30];
		memset(mask,0,sizeof mask);
		int cnt=0;
		for(int j=0;j<=step+1;j++){
			int x=step+1-j;
			int y=j;
			if(x>=n||y>=n)continue;
			mask[a[x][y]-'a']|=(1<<cnt);
			cnt++;
		}
		up(i,0,25){
			if(mask[i]){
				int x;
				if(step+1<n)x=(st|(st<<1))&mask[i];
				else x=(st|(st>>1))&mask[i];
				if(x==0)continue;
				int tmp=0;
				if(i==0)tmp=1;
				else if(i==1)tmp=-1;
				if(step&1)res=max(res,tmp+dfs(step+1,x));
				else res=min(res,tmp+dfs(step+1,x));
			}
		}
	}
	if(step==0){
		if(a[0][0]=='a')res++;
		else if(a[0][0]=='b')res--;
	}
	return res;
	
}

signed main(){
	n=read();
	up(i,0,n-1){
		scanf("%s",a[i]);
	}
	memset(vis,0,sizeof vis);
	int res=dfs(0,1);
	if(res==0)cout<<"DRAW";
	else if(res>0)cout<<"FIRST";
	else cout<<"SECOND";
	return 0;
}
```
