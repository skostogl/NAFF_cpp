#include "spline_interpolation.h"
#include <complex>
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include <numeric>
#include <cmath>
#include <math.h>

void solve(double& k0, double &k1, double &k2, const float&a,const float&b,const float&c,const float&d,const float&l,const float&m,const float&n,const float&k,const float&p,const float&q,const float&r, const float&s)
{
 float D = (a*m*r+b*p*n+c*l*q)-(a*n*q+b*l*r+c*m*p);
 k0 = ((b*r*k+c*m*s+d*n*q)-(b*n*s+c*q*k+d*m*r))/D;
 k1 = ((a*n*s+c*p*k+d*l*r)-(a*r*k+c*l*s+d*n*p))/D;
 k2 = ((a*q*k+b*l*s+d*m*p)-(a*m*s+b*p*k+d*l*q))/D;
}

std::complex<double> spline (const double& t, const std::vector<std::complex<double>>& data) {
  double a11, a12, a21, a22, a23, a32, a33, b1, b2, b3, k0, k1, k2, a_2, b_2, x0, y0, x1, y1, x2, y2;
  //if ((t>1) && t<data.size()-1){
  x0 = (int)(t)-1;
  y0 = data[x0].real();
  x1 = (int)(t);
  y1 = data[x1].real();
  x2 = (int)(t)+1;
  y2 = data[x2].real();
  a11 = 2.0/(x1-x0);
  a12 = 1.0/(x1-x0);
  a21 = a12;
  a22 = 2.0*(1.0/(x1-x0)+ 1.0/(x2-x1));
  a23 = 1.0/(x2-x1);
  a32 = a23;
  a33 = 2.0/(x2-x1);
  b1 = 3.0*((y1-y0)/pow((x1-x0),2));
  b2 = 3.0*((y1-y0)/pow((x1-x0),2)+(y2-y1)/pow((x2-x1),2));
  b3 = 3.0*((y2-y1)/pow((x2-x1),2));
  size_t ccounter=0;
  solve(k0, k1, k2, a11, a12, 0.0, -b1, a21, a22 , a23, -b2, 0.0, a32, a33, -b3);
  a_2 =  k1*(x2-x1)-(y2-y1);
  b_2 = -k2*(x2-x1)+(y2-y1);
  auto q2 = [&x1,&x2,&y1,&y2,&a_2,&b_2,&ccounter](double x) {
    double t = (x-x1)/(x2-x1);
    return (1-t)*y1+t*y2+t*(1.0-t)*(a_2*(1.0-t)+b_2*t);
  }; 
  return std::complex<double>(q2(t),0.0); 
  // }
  //else
  //  return data[int(t)]; 
}


