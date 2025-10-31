#ifndef MISC_HPP
#define MISC_HPP

#include <stdfloat>
#include <cstddef>

// Для удобства реализации и проверки на разных типах float: f8, f16, f32, f64
#ifdef CUSTOM_FLOAT_T16
using dataType = std::float16_t;
#endif

#ifdef CUSTOM_FLOAT_T32
using dataType = std::float32_t;
#endif

#ifdef CUSTOM_FLOAT_T64
using dataType = std::float64_t;
#endif

#ifndef CUSTOM_FLOAT_T16
#ifndef CUSTOM_FLOAT_T32
#ifndef CUSTOM_FLOAT_T64
using dataType = std::float32_t;
#endif
#endif
#endif

// Так просто короче XD
using iT = size_t;

#endif
