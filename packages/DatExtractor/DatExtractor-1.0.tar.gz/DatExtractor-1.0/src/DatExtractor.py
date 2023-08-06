import re
from datetime import datetime

def date_parser(text, date_format = None ):   
    text = text.replace("&nbsp;", " ")
    cleanr = re.compile('<([\\w|\\W]*?)>')
    cleantext = re.sub(cleanr, ' ', text)
    cleanr = re.compile('{.*?}')
    cleantext = re.sub(cleanr, ' ', cleantext)
    cleantext = re.sub(chr(160), ' ', cleantext)
    date_ext = re.findall("\d+[-/]\d+[-/]\d+", text)
    #print(len(date_ext))
    if len(date_ext) == 0:
        return "No date found, please see that the date in the text is delimeted [./-] by the following."
    pattern = ["%m/%d/%Y", "%Y/%m/%d","%d/%m/%Y","%Y/%d/%m","%m-%d-%Y","%Y-%m-%d","%d-%m-%Y","%Y-%d-%m"]
    date_result = []
    if date_format is None:
        date_format = "%m/%d/%Y"
    for i in range(0, len(date_ext)):
        date = date_ext[i]
        for x in pattern:
            try:
                date = datetime.strptime(date,x).strftime(date_format)
                date_result.append(date)                    
            except:
                pass
    #print(date_result)
    return date_result

