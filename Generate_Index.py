# ===========================================================================
# FILE:         Generate_Index.py
#
# AUTHOR:       Anyi Chen; Yuqi Ma
#
# DESCRIPTION:  This file generates the index database
#
# ===========================================================================

import Index

c = Index.Index('WEBPAGES_RAW/bookkeeping.json')

c.parse_json()
c.update_list()
c.cal_tf()
c.generate_post_dict_file()

token = c.get_index()
idf = c.get_idf()
unique = c.get_dict_unique_len()
doc_len = c.get_total_doc()

dic = open("database.json", "w")
u = open("unique.txt", "w")
d = open("doclen.txt", "w")
i = open("idf.json", "w")
dic.write(str(token))
u.write(str(unique))
d.write(str(doc_len))
i.write(str(idf))
dic.close()
u.close()
d.close()
i.close()