#pragma once
#include "pybind11.hpp"
#include <functional>

void get_pixel_shuffle_index_i64(py::array_t<int64_t> index);
