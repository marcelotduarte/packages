# Maintainer: Marcelo Duarte https://github.com/marcelotduarte
# makepkg-mingw -sCLf

_name=cx_Freeze
_realname=cx-freeze
pkgbase=mingw-w64-python-${_realname}
pkgname=("${MINGW_PACKAGE_PREFIX}-python-${_realname}")
pkgver=8.2.0
pkgrel=1
pkgdesc="Creates standalone executables from Python scripts, with the same performance (mingw-w64)"
arch=('any')
mingw_arch=('mingw32' 'mingw64' 'ucrt64' 'clang64' 'clangarm64')
url="https://github.com/marcelotduarte/cx_Freeze/"
msys2_references=(
  'pypi: cx-Freeze'
)
license=('spdx:PSF-2.0')
depends=(
  "${MINGW_PACKAGE_PREFIX}-python"
  "${MINGW_PACKAGE_PREFIX}-python-filelock"
  "${MINGW_PACKAGE_PREFIX}-python-packaging"
  "${MINGW_PACKAGE_PREFIX}-python-pip"
  "${MINGW_PACKAGE_PREFIX}-python-setuptools"
  "${MINGW_PACKAGE_PREFIX}-python-cx-logging"
)
if [ "${MINGW_ARCH}" != "mingw32" ]; then
  depends+=(
    "${MINGW_PACKAGE_PREFIX}-python-lief"
    "${MINGW_PACKAGE_PREFIX}-python-cabarchive"
    "${MINGW_PACKAGE_PREFIX}-python-striprtf"
  )
fi
makedepends=(
  "${MINGW_PACKAGE_PREFIX}-python-build"
  "${MINGW_PACKAGE_PREFIX}-python-installer"
  "${MINGW_PACKAGE_PREFIX}-cc"
  "${MINGW_PACKAGE_PREFIX}-tools"
)
checkdepends=(
  "${MINGW_PACKAGE_PREFIX}-python-pytest"
  "${MINGW_PACKAGE_PREFIX}-python-pytest-cov"
  "${MINGW_PACKAGE_PREFIX}-python-pytest-mock"
  "${MINGW_PACKAGE_PREFIX}-python-pytest-timeout"
  "${MINGW_PACKAGE_PREFIX}-python-pytest-xdist"
)
options=(!strip)
if [ "$CI" == "true" ]; then
  source=("file://$startdir/${_realname/-/_}-${pkgver}.tar.gz")
  sha256sums=(SKIP)
else
  source=()
  sha256sums=()
fi

prepare() {
  if ! [ "$CI" == "true" ]; then
    # Local
    cd ../../cx_Freeze
    pkgver=$(grep "__version__ = " cx_Freeze/__init__.py | sed 's/-dev./.dev/' | awk -F\" '{print $2}')
    ${MINGW_PREFIX}/bin/python -m build -s -x -n -o "$startdir"
    cd "${srcdir}"
    echo "Extract tar archive"
    ${MINGW_PREFIX}/bin/bsdtar -x -v -f "$startdir/${_realname/-/_}-${pkgver}.tar.gz"
  fi

  cd "${srcdir}"/${_name}-${pkgver}
  # ignore version check for setuptools
  sed -i 's/"setuptools>=.*"/"setuptools"/' pyproject.toml
  if [ "${MINGW_ARCH}" == "mingw32" ]; then
    sed -i 's/"cabarchive>=.*"/#"cabarchive"/' pyproject.toml
    sed -i 's/"striprtf>=.*"/#"striprtf"/' pyproject.toml
  fi

  rm -Rf "${srcdir}"/python-${_realname}-${MSYSTEM}
  cp -a "${srcdir}"/cx_Freeze-${pkgver} "${srcdir}"/python-${_realname}-${MSYSTEM}
}

pkgver() {
  cd python-${_realname}-${MSYSTEM}
  grep "__version__ = " cx_Freeze/__init__.py | sed 's/-dev./.dev/' | awk -F\" '{print $2}'
}

build() {
  cd python-${_realname}-${MSYSTEM}
  ${MINGW_PREFIX}/bin/python -m build --wheel --skip-dependency-check --no-isolation
}

check() {
  cd python-${_realname}-${MSYSTEM}
  ${MINGW_PREFIX}/bin/pip install cx_Freeze -f dist --no-deps --no-index

  mkdir -p "${srcdir}/python-test"
  cp pyproject.toml "${srcdir}/python-test/"
  cp -a samples "${srcdir}/python-test/samples/"
  cp -a tests "${srcdir}/python-test/tests/"

  cd "${srcdir}/python-test"
  ${MINGW_PREFIX}/bin/python -m pytest -nauto --cov="cx_Freeze"
}

package() {
  cd python-${_realname}-${MSYSTEM}
  MSYS2_ARG_CONV_EXCL="--prefix=" \
    ${MINGW_PREFIX}/bin/python -m installer --prefix=${MINGW_PREFIX} \
    --destdir="${pkgdir}" dist/*.whl
  install -Dm644 LICENSE.md "${pkgdir}${MINGW_PREFIX}/share/licenses/python-${_realname}/LICENSE.md"
}
