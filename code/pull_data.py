"""Pull HOST_AFFORDABLEHOUSING layer 0 in full from Denver's ArcGIS service.
Source: https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/HOST_AFFORDABLEHOUSING/FeatureServer/0
Writes data/raw.json (immutable snapshot for this package).
"""
import json, pathlib, urllib.request
URL = ("https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/"
       "HOST_AFFORDABLEHOUSING/FeatureServer/0/query?where=1%3D1&outFields=*"
       "&returnGeometry=false&f=json&resultRecordCount=2000&resultOffset=0")
out = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw.json"
with urllib.request.urlopen(URL, timeout=30) as r:
    d = json.loads(r.read())
assert len(d["features"]) == 497, len(d["features"])
out.write_text(json.dumps(d, indent=2))
print("pulled", len(d["features"]), "features")
