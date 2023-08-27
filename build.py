import os
import sys
import shutil
import platform
import argparse
import subprocess
import multiprocessing

PLATFORM_IS_WINDOWS = platform.system() == "Windows"
PLATFORM_IS_LINUX = platform.system() == "Linux"
PLATFORM_IS_MAC = platform.system() == "Darwin"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_path",
        required=True,
        help="The path to the top SuiteSparse source folder, which "
        "contains src/, scripts/, CMakeLists.txt, etc.",
    )

    parser.add_argument(
        "--build_path",
        required=True,
    )

    parser.add_argument(
        "--toolchain_file",
        required=True,
        help="The path of cmake tool chain file.",
    )

    parser.add_argument(
        "--install_path",
        default="",
        help="The path to install path SuiteSparse.",
    )

    parser.add_argument(
        "--build_type",
        default="Release",
        help="Build type, e.g., Debug, Release, RelWithDebInfo",
    )

    parser.add_argument(
        "--bla_vendor",
        default="All",
        help="CMake generator, e.g., All, OpenBLAS, Intel10_64ilp, "
        "Intel10_64lp, Apple, Arm_mp, IBMESSL_SMP, Generic",
    )

    parser.add_argument(
        "--cmake_generator",
        default="",
        help="CMake generator, e.g., Visual Studio 17 2022",
    )

    parser.add_argument("--build_shared", dest="build_shared", action="store_true")

    parser.add_argument("--with_cuda", dest="with_cuda", action="store_true")
    parser.add_argument(
        "--cuda_path",
        default="",
        help="The path to the folder containing CUDA, "
        "e.g., under Windows: C:/Program Files/NVIDIA GPU "
        "Computing Toolkit/CUDA/v8.0",
    )
    parser.add_argument(
        "--cuda_archs",
        default="Auto",
        help="List of CUDA architectures for which to generate "
        "code, e.g., all, all-major, native, 50, 75, etc.",
    )

    parser.add_argument("--with_demo", dest="with_demo", action="store_true")
    parser.add_argument(
        "--blas_underscore", dest="blas_underscore", action="store_true"
    )

    parser.set_defaults(build_shared=False)
    parser.set_defaults(with_cuda=False)
    parser.set_defaults(with_demo=False)
    parser.set_defaults(blas_underscore=True)

    args = parser.parse_args()

    args.cmake_config_args = []

    if args.install_path:
        args.cmake_config_args.append(
            "-DCMAKE_PREFIX_PATH={}".format(args.install_path)
        )
        args.cmake_config_args.append(
            "-DCMAKE_INSTALL_PREFIX={}".format(args.install_path)
        )
        args.cmake_config_args.append("-DLOCAL_INSTALL=OFF")
    else:
        args.cmake_config_args.append("-DLOCAL_INSTALL=ON")

    if args.toolchain_file:
        args.cmake_config_args.append(
            "-DCMAKE_TOOLCHAIN_FILE={}".format(args.toolchain_file)
        )

    args.cmake_config_args.append("-DCMAKE_BUILD_TYPE={}".format(args.build_type))

    if args.cmake_generator:
        args.cmake_config_args.append(
            "-DCMAKE_GENERATOR={}".format(args.cmake_generator)
        )

    if PLATFORM_IS_WINDOWS:
        args.cmake_config_args.append("-DCMAKE_GENERATOR_PLATFORM=x64")

    if args.bla_vendor:
        args.cmake_config_args.append("-DBLA_VENDOR={}".format(args.bla_vendor))

    if args.build_shared:
        args.cmake_config_args.append("-DNSTATIC=ON")
    else:
        args.cmake_config_args.append("-DNSTATIC=OFF")

    if args.with_cuda:
        args.cmake_config_args.append("-DENABLE_CUDA=ON")
    else:
        args.cmake_config_args.append("-DENABLE_CUDA=OFF")

    if args.with_demo:
        args.cmake_config_args.append("-DDEMO=ON")
    else:
        args.cmake_config_args.append("-DDEMO=OFF")

    if args.blas_underscore:
        args.cmake_config_args.append("-DBLAS_UNDERSCORE=ON")
    else:
        args.cmake_config_args.append("-DBLAS_UNDERSCORE=OFF")

    args.cmake_build_args = ["--"]
    if PLATFORM_IS_WINDOWS:
        # Assuming that the build system is MSVC.
        args.cmake_build_args.append(
            "/maxcpucount:{}".format(multiprocessing.cpu_count())
        )
    else:
        # Assuming that the build system is Make.
        args.cmake_build_args.append("-j{}".format(multiprocessing.cpu_count()))

    return args


def mkdir_if_not_exists(path):
    assert os.path.exists(os.path.dirname(os.path.abspath(path)))
    if not os.path.exists(path):
        os.makedirs(path)


def copy_file_if_not_exists(source, destination):
    if os.path.exists(destination):
        return
    shutil.copyfile(source, destination)


def build_cmake_project(
    args, build_path, extra_config_args=[], extra_build_args=[], source_path=".."
):
    mkdir_if_not_exists(build_path)

    cmake_command = (
        ["cmake", "-S", source_path, "-B", build_path]
        + args.cmake_config_args
        + extra_config_args
    )
    return_code = subprocess.call(cmake_command, cwd=build_path)
    if return_code != 0:
        print("Command failed:", " ".join(cmake_command))
        sys.exit(1)

    cmake_command = (
        [
            "cmake",
            "--build",
            build_path,
            "--target",
            "install",
            "--config",
            args.build_type,
        ]
        + args.cmake_build_args
        + extra_build_args
    )
    return_code = subprocess.call(cmake_command, cwd=build_path)
    if return_code != 0:
        print("Command failed:", " ".join(cmake_command))
        sys.exit(1)


def main():
    args = parse_args()

    BUILD_LIBS = "SuiteSparse_config:Mongoose:AMD:BTF:CAMD:CCOLAMD:COLAMD:CHOLMOD:CXSparse:LDL:KLU:UMFPACK:RBio:SuiteSparse_GPURuntime:GPUQREngine:SPQR:GraphBLAS:SPEX"

    mkdir_if_not_exists(args.build_path)

    libs = BUILD_LIBS.split(":")
    for lib in libs:
        if not lib:
            continue
        source_path = os.path.join(args.source_path, lib)
        build_dir = os.path.join(args.build_path, lib)
        mkdir_if_not_exists(build_dir)
        build_path = os.path.join(build_dir, "build")
        extra_config_args = []
        build_cmake_project(
            args,
            build_path,
            extra_build_args=extra_config_args,
            source_path=source_path,
        )


if __name__ == "__main__":
    main()
