#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

#include <iostream>


// fast single precision version of OpenCV'2 cvProjectPoints
// deprecated 
void __project_points(py::array_t<float> img_points, 
                    py::array_t<float> obj_points, 
                    py::array_t<float> r_mat, 
                    py::array_t<float> t_vec, 
                    py::array_t<float> camera_matrix, 
                    py::array_t<float> dist_coeffs)
{
    auto m = img_points.mutable_unchecked<2>(); 
    auto M = obj_points.unchecked<2>();
    auto R = r_mat.unchecked<2>();
    auto t = t_vec.unchecked<1>();
    auto C = camera_matrix.unchecked<2>();
    auto k = dist_coeffs.unchecked<1>();

    int count = M.shape(0);

    float Rxx = R(0,0);
    float Rxy = R(0,1);
    float Rxz = R(0,2);
    float Ryx = R(1,0);
    float Ryy = R(1,1);
    float Ryz = R(1,2);
    float Rzx = R(2,0);
    float Rzy = R(2,1);
    float Rzz = R(2,2);

    float tx = t(0);
    float ty = t(1);
    float tz = t(2);

    float fx = C(0,0);
    float fy = C(1,1);
    float cx = C(0,2);
    float cy = C(1,2);

    float k0 = k(0);
    float k1 = k(1);
    float k2 = k(2);
    float k3 = k(3);
    float k4 = k(4);

    for(int i = 0; i < count; i++)
    {
        float X = M(i,0), Y = M(i,1), Z = M(i,2);

        float x = Rxx*X + Rxy*Y + Rxz*Z + tx;
        float y = Ryx*X + Ryy*Y + Ryz*Z + ty;
        float z = Rzx*X + Rzy*Y + Rzz*Z + tz;
        float r2, r4, r6, a1, a2, a3, cdist;
        float xd, yd;

        z = z ? 1./z : 1;
        x *= z; y *= z;

        r2 = x*x + y*y;
        r4 = r2*r2;
        r6 = r4*r2;
        a1 = 2*x*y;
        a2 = r2 + 2*x*x;
        a3 = r2 + 2*y*y;
        cdist = 1 + k0*r2 + k1*r4 + k4*r6;
        xd = x*cdist + k2*a1 + k3*a2;
        yd = y*cdist + k2*a3 + k3*a1;

        m(i,0) = xd*fx + cx;
        m(i,1) = yd*fy + cy;
    }
}

// fast single precision map projection
void project_map( py::array_t<uint16_t> u_map, 
                  py::array_t<uint16_t> v_map, 
                  py::array_t<float> map3d, 
                  py::array_t<float> r_mat, 
                  py::array_t<float> t_vec, 
                  py::array_t<float> camera_matrix, 
                  py::array_t<float> dist_coeffs,
                  uint16_t img_dim0,
                  uint16_t img_dim1)
{
    auto u = u_map.mutable_unchecked<2>(); 
    auto v = v_map.mutable_unchecked<2>(); 
    auto M = map3d.unchecked<3>();
    auto R = r_mat.unchecked<2>();
    auto t = t_vec.unchecked<1>();
    auto C = camera_matrix.unchecked<2>();
    auto k = dist_coeffs.unchecked<1>();

    int dim0 = M.shape(1);
    int dim1 = M.shape(2);

    float Rxx = R(0,0);
    float Rxy = R(0,1);
    float Rxz = R(0,2);
    float Ryx = R(1,0);
    float Ryy = R(1,1);
    float Ryz = R(1,2);
    float Rzx = R(2,0);
    float Rzy = R(2,1);
    float Rzz = R(2,2);

    float tx = t(0);
    float ty = t(1);
    float tz = t(2);

    float fx = C(0,0);
    float fy = C(1,1);
    float cx = C(0,2);
    float cy = C(1,2);

    float k0 = k(0);
    float k1 = k(1);
    float k2 = k(2);
    float k3 = k(3);
    float k4 = k(4);

    for(int i = 0; i < dim0; i++)
        for(int j = 0; j < dim1; j++)
        {
            float X = M(0,i,j), Y = M(1,i,j), Z = M(2,i,j);

            float x = Rxx*X + Rxy*Y + Rxz*Z + tx;
            float y = Ryx*X + Ryy*Y + Ryz*Z + ty;
            float z = Rzx*X + Rzy*Y + Rzz*Z + tz;
            float r2, r4, r6, a1, a2, a3, cdist;
            float xd, yd;

            z = z ? 1./z : 1;
            x *= z; y *= z;

            r2 = x*x + y*y;
            r4 = r2*r2;
            r6 = r4*r2;
            a1 = 2*x*y;
            a2 = r2 + 2*x*x;
            a3 = r2 + 2*y*y;
            cdist = 1 + k0*r2 + k1*r4 + k4*r6;
            xd = x*cdist + k2*a1 + k3*a2;
            yd = y*cdist + k2*a3 + k3*a1;

            int ix = xd*fx + cx;
            int iy = yd*fy + cy;

            ix = ix < 0 ? 0 : ix;
            iy = iy < 0 ? 0 : iy;
            ix = ix > img_dim1 - 1 ? img_dim1 - 1 : ix; 
            iy = iy > img_dim0 - 1 ? img_dim0 - 1 : iy;

            v(i,j) = uint16_t(ix);
            u(i,j) = uint16_t(iy);
        }
}

// bounding box projection
void project_bounding_box(  py::array_t<uint16_t> u_map, 
                            py::array_t<uint16_t> v_map, 
                            py::array_t<int64_t> bounding_box)
{
    auto u = u_map.unchecked<2>(); 
    auto v = v_map.unchecked<2>(); 
    auto bb = bounding_box.mutable_unchecked<2>();

    uint16_t top = bb(0, 0);
    uint16_t left = bb(1, 0);
    uint16_t bottom = bb(0, 1);
    uint16_t right = bb(1, 1);

    int64_t new_top;
    int64_t new_left;
    int64_t new_bottom;
    int64_t new_right;

    uint16_t dim0 = u.shape(0);
    uint16_t dim1 = u.shape(1);

    uint16_t epsilon = 1;

    // first pass left - right

    int64_t count_left = 0, count_right = 0;
    int64_t value_left = 0, value_right = 0;

    for(uint16_t i = 0; i < dim0; i++)
        for(uint16_t j = 0; j < dim1; j++)
        {
            uint16_t val = v(i,j);
            if(val >= left - epsilon && val <= left - epsilon)
            {
                value_left += j;
                count_left++;
            }
            if(val >= right - epsilon && val <= right - epsilon)
            {
                value_right += j;
                count_right++;
            }
        }

    new_left = value_left / count_left;
    new_right = value_right / count_right;
    new_left = new_left < 0 ? 0 : new_left;
    new_right = new_right > dim1 ? dim1 : new_right;

    // first pass top - bottom

    int64_t count_top = 0, count_bottom = 0;
    int64_t value_top = 0, value_bottom = 0;

    for(uint16_t i = 0; i < dim0; i++)
        for(uint16_t j = new_left; j < new_right; j++)
        {
            uint16_t val = u(i,j);
            if(val >= top - epsilon && val <= top - epsilon)
            {
                value_top += i;
                count_top++;
            }
            if(val >= bottom - epsilon && val <= bottom - epsilon)
            {
                value_bottom += i;
                count_bottom++;
            }
        }

    new_top = value_top / count_top;
    new_bottom = value_bottom / count_bottom;
    new_top = new_top < 0 ? 0 : new_top;
    new_bottom = new_bottom > dim0 ? : new_bottom;

    // second pass left - right

    count_left = 0; count_right = 0;
    value_left = 0; value_right = 0;

    for(uint16_t i = new_top; i < new_bottom; i++)
        for(uint16_t j = 0; j < dim1; j++)
        {
            uint16_t val = v(i,j);
            if(val >= left - epsilon && val <= left - epsilon)
            {
                value_left += j;
                count_left++;
            }
            if(val >= right - epsilon && val <= right - epsilon)
            {
                value_right += j;
                count_right++;
            }
        }

    new_left = value_left / count_left;
    new_right = value_right / count_right;
    new_left = new_left < 0 ? 0 : new_left;
    new_right = new_right > dim1 ? dim1 : new_right;

    // return

    bb(0, 0) = new_top;
    bb(1, 0) = new_left;
    bb(0, 1) = new_bottom;
    bb(1, 1) = new_right;

}

// image points projection
// TODO better (with a tree for instance)
void project_image_points(  py::array_t<uint16_t> u_map, 
                            py::array_t<uint16_t> v_map, 
                            py::array_t<uint16_t> u_inv_map, 
                            py::array_t<uint16_t> v_inv_map, 
                            py::array_t<double> image_points)
{
    auto u = u_map.unchecked<2>(); 
    auto v = v_map.unchecked<2>(); 
    auto u_inv = u_inv_map.mutable_unchecked<2>();
    auto v_inv = v_inv_map.mutable_unchecked<2>();
    auto points = image_points.mutable_unchecked<2>();

    uint16_t dim0 = u.shape(0);
    uint16_t dim1 = u.shape(1);

    const uint16_t no_point = 65535;

    // inverse maps

    for(uint16_t i = 0; i < dim0; i++)
        for(uint16_t j = 0; j < dim1; j++)
        {
            u_inv(i,j) = no_point;
            v_inv(i,j) = no_point;
        }

    for(uint16_t i = 0; i < dim0; i++)
        for(uint16_t j = 0; j < dim1; j++)
        {
            int u_index = u(i, j);
            int v_index = v(i, j);

            u_inv(u_index, v_index) = i;
            v_inv(u_index, v_index) = j;
        }

    // remap points

    int num_points = points.shape(0);

    for(int p = 0; p < num_points; p++)
    {
        int p_u = int(points(p,0));
        int p_v = int(points(p,1));

        p_u = p_u < 0 ? 0 : p_u;
        p_v = p_v < 0 ? 0 : p_v;

        p_u = p_u >= dim0 ? dim0 - 1 : p_u;
        p_v = p_v >= dim0 ? dim0 - 1 : p_v;

        const int max_iteration = 100;

        double new_p_u;
        double new_p_v;
        int count;

        for(int i = 0; i < max_iteration; i++)
        {
            int u_min = p_u - i;
            int u_max = p_u + i;
            int v_min = p_v - i;
            int v_max = p_v + i;

            u_min = u_min < 0 ? 0 : u_min;
            v_min = v_min < 0 ? 0 : v_min;
            u_max = u_max >= dim0 ? dim0 - 1 : u_max;
            v_max = v_max >= dim1 ? dim1 - 1 : v_max;

            new_p_u = 0.0;
            new_p_v = 0.0;
            count = 0;

            for(int iu = u_min; iu < u_max; iu++)
                for(int iv = v_min; iv < v_max; iv++)
                {
                    uint16_t i_p_u = u_inv(iu, iv);
                    uint16_t i_p_v = v_inv(iu, iv);

                    if(i_p_u != no_point)
                    {
                        new_p_u += double(i_p_u);
                        new_p_v += double(i_p_v);
                        count++;
                    }
                }

            if(count != 0)
                break;
        }

        if(count != 0)
        {
            points(p, 0) = new_p_u/double(count);
            points(p, 1) = new_p_v/double(count);
        }
        else
        {
            points(p, 0) = 0.0;
            points(p, 1) = 0.0; 
        }
    }
}


// remapping kernels
void remap_uint8(   py::array_t<uint8_t> img_src, 
                    py::array_t<uint8_t> img_dst, 
                    py::array_t<uint16_t> u_map, 
                    py::array_t<uint16_t> v_map) 
{
    auto dst = img_dst.mutable_unchecked<3>(); 
    auto src = img_src.unchecked<3>();
    auto _u_map = u_map.unchecked<2>();
    auto _v_map = v_map.unchecked<2>();

    for(int c = 0; c < src.shape(0); c++)
      for(int u = 0; u < _u_map.shape(0); u++)
        for(int v = 0; v < _v_map.shape(1); v++)
          dst(c, u, v) = src(c, _u_map(u,v), _v_map(u,v));
}

void remap_uint16(  py::array_t<uint16_t> img_src, 
                    py::array_t<uint16_t> img_dst, 
                    py::array_t<uint16_t> u_map, 
                    py::array_t<uint16_t> v_map) 
{
    auto dst = img_dst.mutable_unchecked<3>(); 
    auto src = img_src.unchecked<3>();
    auto _u_map = u_map.unchecked<2>();
    auto _v_map = v_map.unchecked<2>();

    for(int c = 0; c < src.shape(0); c++)
      for(int u = 0; u < _u_map.shape(0); u++)
        for(int v = 0; v < _v_map.shape(1); v++)
          dst(c, u, v) = src(c, _u_map(u,v), _v_map(u,v));
}

void remap_float64( py::array_t<double> img_src, 
                    py::array_t<double> img_dst, 
                    py::array_t<uint16_t> u_map, 
                    py::array_t<uint16_t> v_map) 
{
    auto dst = img_dst.mutable_unchecked<3>(); 
    auto src = img_src.unchecked<3>();
    auto _u_map = u_map.unchecked<2>();
    auto _v_map = v_map.unchecked<2>();

    for(int c = 0; c < src.shape(0); c++)
      for(int u = 0; u < _u_map.shape(0); u++)
        for(int v = 0; v < _v_map.shape(1); v++)
          dst(c, u, v) = src(c, _u_map(u,v), _v_map(u,v));
}


// bindings
PYBIND11_MODULE(_library, m) 
{
   m.doc() = "reprojection";
   m.def("project_map", &project_map);
   m.def("project_bounding_box", &project_bounding_box);
   m.def("project_image_points", &project_image_points);
   // order matters
   m.def("remap", &remap_uint8, "");
   m.def("remap", &remap_uint16, "");
   m.def("remap", &remap_float64, "");
}

