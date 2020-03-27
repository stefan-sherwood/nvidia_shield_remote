# Distributed under the terms of the GNU General Public License v2

EAPI=6
PYTHON_COMPAT=( python{3_6,3_7} )

inherit distutils-r1 git-r3

DESCRIPTION="Python ADB + Fastboot implementation"
HOMEPAGE="https://github.com/google/python-adb"
EGIT_REPO_URI="https://github.com/google/python-adb.git"

LICENSE="BSD"
SLOT="0"
KEYWORDS="~amd64 ~arm ~ppc ~x86"
IUSE=""

DEPEND="virtual/libusb:=
	dev-python/setuptools[${PYTHON_USEDEP}]
	dev-python/m2crypto
	dev-python/libusb1"

RDEPEND="${DEPEND}"
