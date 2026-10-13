## [F](https://atcoder.jp/contests/abc326/tasks/abc326_f "F")

一道搜索好题。

一眼就可以看到 $n\le 80$，看起来直接暴搜不是很能过的样子，考虑优化。

因为每一次都要转向，所以可以可以考虑把 $x$ 轴和 $y$ 轴分开计算。

这样，时间复杂度就是 $2\times 2^{40}$。

还是不够，继续优化，因为直到初始状态和最终状态，所以可以考虑双向搜索优化。

最后输出答案需要注意，我们记录的信息是 $x$ 和 $y$ 的正负，转化成 `LR` 需要记录前一位的信息。

```cpp
int n,sx,sy;
map<int,string>mpx;
map<int,string>mpy;
map<int,int>mp;
int a[500];
vector<int>x,y;
inline void dfsx(int i,int pos,string s){
    if(i==x.size()/2){
        mpx[pos]=s;
        return;
    }
    dfsx(i+1,pos+x[i],s+"1");
    dfsx(i+1,pos-x[i],s+"0");
}
bool fl=0;
inline void dfsx2(int i,int pos,string s){
    if(i==x.size()){
        if(!mpx.count(sx-pos))return;
        mpx[sx]=mpx[sx-pos]+s;
		fl=1;
		return;
    }
	dfsx2(i+1,pos+x[i],s+"1");
    if(fl)return;
    dfsx2(i+1,pos-x[i],s+"0");
    if(fl)return;
}
inline void dfsy(int i,int pos,string s){
    if(i==y.size()/2){
        mpy[pos]=s;
        return;
    }
    dfsy(i+1,pos+y[i],s+"1");
    dfsy(i+1,pos-y[i],s+"0");
}
inline void dfsy2(int i,int pos,string s){
    if(i==y.size()){
        if(!mpy.count(sy-pos))return;
        mpy[sy]=mpy[sy-pos]+s;
		fl=1;
		return;
    }
	dfsy2(i+1,pos+y[i],s+"1");
    if(fl)return;
    dfsy2(i+1,pos-y[i],s+"0");
    if(fl)return;
}
inline void print(){
    puts("Yes");
    vector<int>ans;
    int i=0,j=0;
    while(i<mpy[sy].size()||j<mpx[sx].size()){
        if(i<mpy[sy].size())ans.push_back(mpy[sy][i]-'0'),i++;
        if(j<mpx[sx].size())ans.push_back(mpx[sx][j]-'0'),j++;
    }
    int la=0;
	 up(i,0,ans.size()-1) {
		if (ans[i]) {
			if (la==0) cout<<"L",la=1;
			else if (la==1) cout<<"R",la=0;
			else if (la==2) cout<<"R",la=1;
			else if (la==3) cout<<"L",la=0; 
		}
		else {
			if (la==0) cout<<"R",la=3;
			else if (la==1) cout<<"L",la=2;
			else if (la==2) cout<<"L",la=3;
			else if (la==3) cout<<"R",la=2; 
		}
	}
}
signed main(){
	n=read();sx=read();sy=read();
    up(i,1,n){
        a[i]=read();
        if(i&1)y.push_back(a[i]);
        else x.push_back(a[i]);
    }
    dfsx(0,0,"");
    dfsx2(x.size()/2,0,"");
    fl=0;
    dfsy(0,0,""); 
    dfsy2(y.size()/2,0,"");
    if(mpx.count(sx)&&mpy.count(sy))print();
    else puts("No");
    return 0;
}
```