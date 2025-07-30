
import lancedb
import os

uri = "data/lancedb"

db = lancedb.connect(uri)

tbl = db.open_table("HR_kb")
#tbl.create_fts_index("text")

# table_1 = db.open_table("HR_kb")

result = tbl.search(query="objective of promotion",query_type="vector").limit(3)
result.to_pandas()