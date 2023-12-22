import frappe
from frappe.core.doctype.file.utils import attach_files_to_document

def execute():
    query = """
        SELECT parent, COUNT(parent) AS count
        FROM `tabDocField`
        WHERE fieldtype IN ("Attach", "Attach Image")
          AND parent NOT IN (
            SELECT name
            FROM `tabDocType`
            WHERE issingle = 1
          )
        GROUP BY parent
        HAVING COUNT(parent) > 1;
        """
    
    doctypes = frappe.db.sql(query,as_dict=True)

    for doctype in doctypes:
        doctype = doctype.parent
        documents = frappe.db.get_list(doctype)

        for document in documents:
            doc = frappe.get_doc(doctype,document)
            attach_files_to_document(doc,"Patch")