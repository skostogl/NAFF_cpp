#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/math/tools/minima.hpp>
#include <boost/math/constants/constants.hpp>

#include "NAFF.h"
#include "signal.h"

BOOST_PYTHON_MODULE(NAFF)
{
  using namespace boost::python;

  class_<std::vector<Tfloat>>("Vec_cpp")
	.def(vector_indexing_suite<std::vector<Tfloat>>())
  ;	 

  class_<NAFF>("NAFF")
	.def("get_f1",&NAFF::get_f1)
 	.def("get_f",&NAFF::get_f)
        .def("set_window_parameter",&NAFF::set_window_parameter)
        .def("get_window_parameter",&NAFF::get_window_parameter)
        .def("set_merit_function",&NAFF::set_merit_function)
        .def("set_upsampling",&NAFF::set_upsampling)
        .def("set_interpolation",&NAFF::set_interpolation)
        .def_readwrite("fmax",&NAFF::fmax)
  ;

}


