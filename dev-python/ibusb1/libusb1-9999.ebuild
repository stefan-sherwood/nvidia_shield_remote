# Distributed under the terms of the GNU General Public License v2

EAPI=6
PYTHON_COMPAT=( python{3_6,3_7} )

inherit distutils-r1 git-r3

DESCRIPTION="Python ctype-based wrapper around libusb1"
HOMEPAGE="https://github.com/vpelletier/python-libusb1"
EGIT_REPO_URI="https://github.com/vpelletier/python-libusb1.git"

LICENSE="BSD"
SLOT="0"
KEYWORDS="~amd64 ~arm ~ppc ~x86"
IUSE=""

DEPEND="virtual/libusb:=
	dev-python/setuptools[${PYTHON_USEDEP}]"
RDEPEND="${DEPEND}"
