%global oneapi_dir /opt/intel/oneapi

%global module_load() MODULEPATH=%{oneapi_dir}/modulefiles module load mpi/latest
%global mpi_dir %{oneapi_dir}/mpi/latest

%if (0%{?suse_version} >= 1500)
%global cmake cmake
%else
%global cmake cmake3
%endif

Name:    vpic
Version: 1.2
Release: 0%{?commit:.git%{shortcommit}}%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL:     https://github.com/LANL/vpic
Source0: https://github.com/LANL/%{name}/archive/%{version}.tar.gz

%if (0%{?suse_version} >= 1500)
BuildRequires: cmake >= 3.1
BuildRequires: lua-lmod
%else
BuildRequires: cmake3 >= 3.1
BuildRequires: Lmod
%endif
BuildRequires: intel-oneapi-mpi
Requires: intel-oneapi-mpi

%description
VPIC is a general purpose particle-in-cell simulation code for modeling kinetic
plasmas in one, two, or three spatial dimensions. It employs a second-order,
explicit, leapfrog algorithm to update charged particle positions and velocities
in order to solve the relativistic kinetic equation for each species in the
plasma, along with a full Maxwell description for the electric and magnetic
fields evolved via a second- order finite-difference-time-domain (FDTD) solve.
The VPIC code has been optimized for modern computing architectures and uses
Message Passing Interface (MPI) calls for multi-node application as well as
data parallelism using threads. VPIC employs a variety of short-vector,
single-instruction-multiple-data (SIMD) intrinsics for high performance and has
been designed so that the data structures align with cache boundaries. The
current feature set for VPIC includes a flexible input deck format capable of
treating a wide variety of problems. These include: the ability to treat
electromagnetic materials (scalar and tensor dielectric, conductivity, and
diamagnetic material properties); multiple emission models, including
user-configurable models; arbitrary, user-configurable boundary conditions for
particles and fields; user- definable simulation units; a suite of "standard"
diagnostics, as well as user-configurable diagnostics; a Monte-Carlo treatment
of collisional processes capable of treating binary and unary collisions and
secondary particle generation; and, flexible checkpoint-restart semantics
enabling VPIC checkpoint files to be read as input for subsequent simulations.
VPIC has a native I/O format that interfaces with the high-performance
visualization software Ensight and Paraview. While the common use cases for
VPIC employ low-order particles on rectilinear meshes,. a framework exists to
treat higher-order particles and curvilinear meshes, as well as more advanced
field solvers.


%package impi
Summary: vpic for IntelMPI
BuildRequires: intel-oneapi-mpi
Requires: intel-oneapi-mpi

%description impi
vpic for IntelMPI

%prep
%setup -q

%build
mkdir impi
pushd impi
module avail
echo $MODULEPATH
%module_load

%{cmake} -DCMAKE_INSTALL_PREFIX=%{mpi_dir} \
cmake   -DCMAKE_BUILD_TYPE=Release         \
        -DENABLE_INTEGRATED_TESTS=ON       \
        -DCMAKE_C_FLAGS="-rdynamic"        \
        -DCMAKE_CXX_FLAGS="-rdynamic"      \
        ..
%{make_build}
module purge
pushd bin
# create the harris.Linux binary
./vpic ../../sample/harris
popd
popd

%install
%module_load
%{make_install} -C impi
module purge
# install the harris.Linux binary
install -m 0755 impi/bin/harris.Linux ${RPM_BUILD_ROOT}%{mpi_dir}/bin

%files impi
%{mpi_dir}/*

%changelog
* Fri Jun 18 2021 Mauren Jean <maureen.jean@intel.com> - 1.2-0
- Initial version
