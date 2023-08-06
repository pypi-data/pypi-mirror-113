# pylint: disable=W0622
"""cubicweb-graphql application packaging information"""


modname = "cubicweb_graphql"
distname = "cubicweb-graphql"

numversion = (0, 2, 2)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "GraphQL for CubicWeb"
web = "https://www.cubicweb.org/project/%s" % distname

__depends__ = {
    "cubicweb": "~= 3.26",
    "six": ">= 1.12.0",
    "graphql-core": ">= 2.3, <3",
    "graphene": ">= 2.1, <3",
    "iso8601": None,
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
