import frappe
from frappe.model.document import Document

class DocumentSettings(Document):
	def on_update(self):
		custom_fields = frappe.db.get_all('Custom Field',{'module':'Document Manager','options':'Document','fieldtype':'Table'},['name','dt','insert_after'])
		setting_fields = self.assigned_doctypes
		cf_to_delete = [f.name for f in custom_fields if f.dt not in [f.dt for f in setting_fields]]
		sb_to_delete = [f.name for f in frappe.db.get_all('Custom Field',{'module':'Document Manager','fieldtype':'Section Break','fieldname':'related_documents_section'})]
		cf_to_add = [f for f in setting_fields if f.dt not in [f.dt for f in custom_fields]]
		for f in cf_to_delete:
			frappe.delete_doc('Custom Field',f)
		for sb in sb_to_delete:
			frappe.delete_doc('Custom Field',sb)
		for f in cf_to_add:
			fl = [f.fieldname for f in frappe.get_doc('DocType',f.dt).fields]
			frappe.get_doc({
				'doctype':'Custom Field',
				'dt':f.dt,
				'fieldtype':'Section Break',
				'module':'Document Manager',
				'label':'Related Documents',
				'insert_after':f.insert_after if f.insert_after in fl else None,
				'fieldname':'related_documents_section'
			}).insert(ignore_permissions=True)
			frappe.get_doc({
				'doctype':'Custom Field',
				'dt':f.dt,
				'fieldtype':'Table',
				'options':'Document',
				'module':'Document Manager',
				'label':'Related Documents',
				'insert_after':'related_documents_section'
			}).insert(ignore_permissions=True)
		for f in setting_fields:
			doc = frappe.db.get_list('Custom Field',{'doctype':f.dt})
	pass
