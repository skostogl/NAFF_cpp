#include "NAFF.h"
#include "signal.h"

int main() {
  std::vector<double> t;
  std::vector<double> data;
  std::vector<double> data_prime;
  for( double i = 0.0; i <= 1000; i++ ) {
    t.push_back(i);
    data.push_back(40.0*cos(2*pi*0.31*i)+60.0);
    data_prime.push_back(0.0);
  }
  NAFF naff;
  double tunes = naff.get_f1(data,data_prime);
  std::cout<<std::setprecision(15)<<tunes<<std::endl;
  return 0;
}
