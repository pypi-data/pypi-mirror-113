"""Queries the NASA Exoplanet Archive's TAP API."""

from numpy import NaN
import pyvo as vo
from ..util import get_label_list

_CLIENT_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP"
# _DEFAULT_COLUMNS = ["pl_name",
#     "hostname",
#     "disc_year",
#     "discoverymethod",
#     "pl_orbper",
#     "pl_orbsmax",
#     "pl_orbeccen",
#     "pl_rade",
#     "pl_masse",
#     "pl_bmasse",
#     "st_met",
#     "st_teff",
#     "st_metratio",
#     "st_mass"]
_DEFAULT_COLUMNS = get_label_list()
_DEFAULT_DB = "ps"

# Database to query. View databases at https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html
_QUERY_FORMAT = lambda columns, db: "SELECT " + ",".join(columns) + " FROM " + db# + " WHERE " # need to add constraint

def query(**kwargs):
    """
    Queries NASA Exoplanet TAP interface to retrieve data.
    Returns a list of dictionaries in format {column: data}
    """
    defaultKwargs = {
        "query_columns": _DEFAULT_COLUMNS,
        "query_db": _DEFAULT_DB,
        "do_not_process": False
    }
    kwargs = { **defaultKwargs, **kwargs }
    columns = kwargs["query_columns"]
    db = kwargs["query_db"]
    do_not_process = kwargs["do_not_process"]

    print("RETRIEVING DATA")

    service = vo.dal.TAPService(_CLIENT_URL)
    result = service.search(_QUERY_FORMAT(columns, db))

    print("DATA RETRIEVED")
    if do_not_process:
        return result
    else:
        print("PROCESSING DATA")

        # restructure data into a list of planets
        pl_list = []
        used_names = []
        for row in result:
            if row["pl_name"] in used_names:
                dict = pl_list[used_names.index(row["pl_name"])]
                for columnLabel in columns:
                    val = row[columnLabel]
                    dict[columnLabel] = val or NaN
            else:
                dict = {}
                for columnLabel in columns:
                    val = row[columnLabel]
                    dict[columnLabel] = val or NaN
                pl_list.append(dict)
                used_names.append(row["pl_name"])

        print("PROCESSED DATA")

        print("Exoplanet Entries:", len(pl_list))
        return pl_list