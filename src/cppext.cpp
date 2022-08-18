#include "block_shuffle.hpp"
#include "pybind11.hpp"

#define STRINGIFY(x)       #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

PYBIND11_MODULE(cppext, m) {
  m.doc() = R"pbdoc(
        Pybind11 plugin
        -----------------------
        .. currentmodule:: pyutils.cppext
        .. autosummary::
           :toctree: _generate
    )pbdoc";

  // block_shuffle.hpp
  m.def("get_pixel_shuffle_index_i64", &get_pixel_shuffle_index_i64);

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
