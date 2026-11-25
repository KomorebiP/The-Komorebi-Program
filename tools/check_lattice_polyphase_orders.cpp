// Author: Komorebi P.
// C++17, exact modular lower bounds for the recurrence order.
#include <cassert>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
using u64=uint64_t;
constexpr u64 P=1000000007;
u64 power(u64 a,u64 n){u64 b=1;while(n){if(n&1)b=b*a%P;a=a*a%P;n>>=1;}return b;}
vector<u64> strips(int w,int H){vector<int> masks;for(int i=0;i<(1<<w);i++)if(!(i&(i<<1)))masks.push_back(i);int d=masks.size();vector<vector<int>> edges(d);for(int i=0;i<d;i++)for(int j=0;j<d;j++)if(!(masks[i]&masks[j])&&!((masks[i]<<1)&masks[j]))edges[i].push_back(j);vector<u64> v(d),z(d),out{1};v[0]=1;for(int h=1;h<=H;h++){fill(z.begin(),z.end(),0);for(int i=0;i<d;i++)for(int j:edges[i]){z[j]+=v[i];if(z[j]>=P)z[j]-=P;}v.swap(z);u64 s=0;for(auto a:v)s=(s+a)%P;out.push_back(s);}return out;}
vector<u64> bm(const vector<u64>& a){vector<u64>C{1},B{1};int L=0,m=1;u64 bi=1;for(int n=0;n<(int)a.size();n++){u64 delta=a[n];for(int j=1;j<=L;j++)delta=(delta+C[j]*a[n-j])%P;if(!delta){m++;continue;}u64 f=delta*bi%P;bool inc=2*L<=n;vector<u64> T;if(inc)T=C;if(C.size()<B.size()+m)C.resize(B.size()+m);for(int j=0;j<(int)B.size();j++)C[j+m]=(C[j+m]+P-f*B[j]%P)%P;if(inc){L=n+1-L;B.swap(T);bi=power(delta,P-2);m=1;}else m++;}C.resize(L+1);return C;}
void arrays(){for(auto row:vector<vector<int>>{{3,30},{4,27},{5,165},{6,135},{7,1040},{8,652},{9,6448},{10,3627}}){int W=row[0],D=row[1],N=2*D+8,H=(N+2)/2+2;auto a=strips(W/2,H),b=strips((W+1)/2,H);vector<u64> y;for(int n=1;n<=N;n++){int h=(n+2)/2,k=(n+3)/2;y.push_back(a[h]*a[k]%P*b[h]%P*b[k]%P);}auto C=bm(y);u64 tr2=C.size()>2?(C[1]*C[1]%P+2*P-2*C[2])%P:0;long long signedtrace=tr2>P/2?(long long)tr2-P:tr2;const int expected[]={30,27,165,134,1040,652,6376,3445};const int traces[]={-3,5,-19,10,-99,13,-397,59};assert(C.size()==expected[W-3]+1&&signedtrace==traces[W-3]);cout<<W<<" "<<D<<" "<<C.size()-1<<" "<<signedtrace<<"\n"<<flush;}}
void infinite_family(){
 vector<int> D={1,3,4,7,9,10};
 for(int k=2;k<=6;k++){
  int a=1,b=1;long long hprod=1,tprod=1;
  for(int j=0;j<k;j++){a*=3;b*=2;hprod*=1+D[j];tprod*=1+2*D[j];}
  int R=2*a-b,N=2*R+8,H=N/2+2;vector<u64> u(H+1,1);
  for(int j=0;j<k;j++){vector<u64> f{2,1};for(int m=2;m<=H;m++)f.push_back((f[m-1]+D[j]*f[m-2])%P);for(int m=0;m<=H;m++)u[m]=u[m]*f[m]%P;}
  vector<u64> y;for(int n=0;n<N;n++)y.push_back(u[n/2]*u[(n+1)/2]%P);
  auto C=bm(y);assert(C.size()==R+1);u64 tr2=(C[1]*C[1]%P+2*P-2*C[2])%P;long long t=tr2>P/2?(long long)tr2-P:tr2;assert(t==2*hprod-tprod&&t<0);
  cout<<"factors="<<k<<" order="<<R<<" trace2="<<t<<" min_vertices="<<R+1<<"\n";
 }
}
int main(){arrays();infinite_family();}
