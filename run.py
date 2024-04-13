import csv
import glob

NOUPDATE = 1
BOOLEAN = ("True", "False")
ERP_HEADER = """<?xml version="1.0"?>
<odoo>
    <data noupdate="%s">"""

ERP_FOOTER = """
    </data>
</odoo>
"""


def convert_relationnal_field2xml(tag, value):
    mytag = tag
    for elm in ["/ids", "/id", ":id"]:
        mytag = mytag.replace(elm, "")
    if tag[-6:] == "ids/id":
        line = '%s" eval="[(6, 0, [%s])]"/>\n' % (mytag, value)
    else:
        line = '%s" ref="%s"/>\n' % (mytag, row[i])
    return line


for csv_file in glob.glob("*.csv"):
    no_update = NOUPDATE
    xml_file = csv_file.replace(".", "_").replace("_csv", ".xml")
    csv_data = csv.reader(open(csv_file))
    xml_data = open(xml_file, "w")
    xml_data.write(ERP_HEADER % NOUPDATE + "\n\n\n")
    row_num = 0
    for row in csv_data:
        if row_num == 0:
            tags = row
            for i in range(len(tags)):
                tags[i] = tags[i].replace(" ", "_")
            print(tags)
        else:
            for i in range(len(tags)):
                char = False
                if tags[i][-5:] == "|char":
                    char = True
                numeric = False
                begin = '    <field name="'
                try:
                    float(row[i])
                    numeric = True
                except Exception:
                    pass
                if tags[i] in ["id", "ID"]:
                    line = '<record id="%s" model="%s">\n' % (row[i], csv_file[:-4])
                elif "/" in tags[i] or ":" in tags[i]:
                    xml_suffix = convert_relationnal_field2xml(tags[i], row[i])
                    line = "%s%s" % (begin, xml_suffix)
                elif char:
                    line = '%s%s">%s</field>\n' % (begin, tags[i][:-5], row[i])
                elif numeric or row[i] in BOOLEAN:
                    line = '%s%s" eval="%s"/>\n' % (begin, tags[i], row[i])
                else:
                    line = '%s%s">%s</field>\n' % (begin, tags[i], row[i])
                if row[i] or tags[i] == "id":
                    xml_data.write(line)
            xml_data.write("</record>" + "\n\n")
        row_num += 1
    xml_data.write(ERP_FOOTER)
    xml_data.close()
