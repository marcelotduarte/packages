# Maintainer: Marcelo Duarte https://github.com/marcelotduarte
# makepkg-mingw -sCLf

_name=cx_Freeze
_realname=cx-freeze
pkgbase=mingw-w64-python-${_realname}
pkgname=("${MINGW_PACKAGE_PREFIX}-python-${_realname}")
pkgver=7.3.0
pkgrel=1
pkgdesc="Creates standalone executables from Python scripts, with the same performance (mingw-w64)"
arch=('any')
mingw_arch=('mingw32' 'mingw64' 'ucrt64' 'clang64')
url="https://github.com/marcelotduarte/cx_Freeze/"
msys2_references=(
  'pypi: cx-Freeze'
)
license=('spdx:PSF-2.0')
depends=(
    "${MINGW_PACKAGE_PREFIX}-python"
    "${MINGW_PACKAGE_PREFIX}-python-packaging"
    "${MINGW_PACKAGE_PREFIX}-python-pip"
    "${MINGW_PACKAGE_PREFIX}-python-setuptools"
    "${MINGW_PACKAGE_PREFIX}-python-cx-logging"
)
if [ "${MINGW_ARCH}" != "mingw32" ]; then
    depends+=("${MINGW_PACKAGE_PREFIX}-python-lief")
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
    "${MINGW_PACKAGE_PREFIX}-python-pytest-datafiles"
    "${MINGW_PACKAGE_PREFIX}-python-pytest-mock"
    "${MINGW_PACKAGE_PREFIX}-python-pytest-timeout"
    "${MINGW_PACKAGE_PREFIX}-python-pytest-xdist"
)
options=(!strip)
source=()
sha256sums=()

prepare() {
  echo "pwd: $(pwd)" 
  echo "srcdir: ${srcdir}"
  rm -Rf "${srcdir}"/python-${_realname}-${MSYSTEM}
  mkdir -p "${srcdir}"/python-${_realname}-${MSYSTEM}
  if [ -d ../cx_Freeze ]; then
    cp -a ../cx_Freeze/* "${srcdir}"/python-${_realname}-${MSYSTEM}
  else
    cp -a ../../cx_Freeze/* "${srcdir}"/python-${_realname}-${MSYSTEM}
  fi

  cd "${srcdir}"/python-${_realname}-${MSYSTEM}
  # ignore version check for setuptools
  sed -i 's/"setuptools>=.*"/"setuptools"/' pyproject.toml
}

pkgver() {
  cd python-${_realname}-${MSYSTEM}
  grep "__version__ = " cx_Freeze/__init__.py | sed 's/-/./' | awk -F\" '{print $2}'
}

build() {
  cd python-${_realname}-${MSYSTEM}
  ${MINGW_PREFIX}/bin/python -m build --wheel --skip-dependency-check --no-isolation
}

check() {
  cd python-${_realname}-${MSYSTEM}
  ${MINGW_PREFIX}/bin/pip install cx_Freeze -f dist --no-deps --no-index
  ${MINGW_PREFIX}/bin/pytest -nauto --cov="cx_Freeze"
}

package() {
  cd python-${_realname}-${MSYSTEM}
  MSYS2_ARG_CONV_EXCL="--prefix=" \
    ${MINGW_PREFIX}/bin/python -m installer --prefix=${MINGW_PREFIX} \
    --destdir="${pkgdir}" dist/*.whl
  install -Dm644 LICENSE.md "${pkgdir}${MINGW_PREFIX}/share/licenses/python-${_realname}/LICENSE.md"
}
