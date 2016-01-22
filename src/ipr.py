#!/usr/bin/env python
import sys
from src.annotation import Annotation

#this functions takes an ipr file and returns a list of annotations. 3 types of annotations are retrieved based on the following keys: "Dbxref", "GO" and "InterPro"
#Note: when pulling data from the input file, we always use ".strip()" to remove any whitespace padding
#Note: this algorithm assumes that if the column exists then the supposed type of value is there (e.g. if column #11 exists, then it has IPR information)
def read_ipr(io_buffer, whitelist=None):
    """Returns a list of lists, each containing mrna_id, "Dbxref" and annotation."""
    ipr_list = []
    for line in io_buffer:
        columns = line.split("\t") #columns are assumed to be tab-separated
        #if column exists and dbxref is in whitelist (aside from whitespace padding and caps)
        if (len(columns)>3 and (columns[3].strip().lower() in whitelist)) or\
		 (len(columns)>3 and not whitelist): 
	    ipr_list.append(Annotation(columns[0].strip(), "Dbxref", columns[3].strip().upper()+":"+columns[4].strip()))
        #if column exists (we don't care about the whitelist for GO annotations)
        if len(columns)>13 and columns[13].find("GO:") != -1: 
            ipr_list.append(Annotation(columns[0].strip(), "Dbxref", columns[13].strip()))
        #if column exists (we don't care about the whitelist for IPR annotations)
        if len(columns)>11 and columns[11].find("IPR") != -1: 
            ipr_list.append(Annotation(columns[0].strip(), "Dbxref", "InterPro:"+columns[11].strip()))
	if len(columns)>14 :  #if column exists 
            list_col_14=columns[14].split('|')
            for element in list_col_14:
                db_current=element.rsplit(':', 1)[0]
                if db_current.strip().lower() in whitelist:
                    ipr_list.append(Annotation(columns[0].strip(), "Dbxref", element.strip()))

    #this alg removes duplicates
    ipr_list = sorted(ipr_list)
    ipr_list = [ipr_list[i] for i in range(len(ipr_list)) if i== 0 or ipr_list[i] != ipr_list[i-1]]

    return ipr_list
