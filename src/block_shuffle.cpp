#include "block_shuffle.hpp"

#include <algorithm>
#include <execution>
#include <random>
#include <vector>

using std::vector;

template <typename T>
vector<T> randomperm(int n) {
  std::mt19937 g(static_cast<unsigned int>(rand()));
  auto vec = vector<T>(n);
  std::iota(vec.begin(), vec.end(), 0);
  std::shuffle(vec.begin(), vec.end(), g);
  return vec;
}

void get_pixel_shuffle_index_i64(py::array_t<int64_t> index) {
  if (index.ndim() != 2)
    throw std::runtime_error("number of dimensions must be 2");
  auto r = index.mutable_unchecked<2>(); // must be a 2-dimensional array
  std::mt19937 g(static_cast<unsigned int>(rand()));
  auto temp = vector<int64_t>(r.shape(0));
  std::iota(temp.begin(), temp.end(), 0);

  for (int j = 0; j < r.shape(1); ++j) {
    std::shuffle(temp.begin(), temp.end(), g);
    for (int i = 0; i < r.shape(0); ++i) {
      r(i, j) = temp[i];
    }
  }
}
