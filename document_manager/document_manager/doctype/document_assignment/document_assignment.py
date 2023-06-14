# Copyright (c) 2023, Dx and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DocumentAssignment(Document):
	def on_update(self):
		if not self.field_id:
			existing = frappe.db.get_all('Custom Field',{'options':'Related Document','dt':self.dt})
			if len(existing)>0:
				for f in existing:
					frappe.delete_doc('Custom Field',f.name)
			section_breaks = frappe.db.get_all('Custom Field',{'fieldname':'related_documents_section_break','dt':self.dt})
			if len(section_breaks) > 0:
				for b in section_breaks:
					frappe.delete_doc('Custom Field',b.name)
			
			section_break = frappe.get_doc({
				"doctype":"Custom Field",
				"dt":self.dt,
				"module":"Document Manager",
				'label':'Related Documents',
				"fieldtype":"Section Break",
				"fieldname":"related_documents_section_break",
				"insert_after":self.insert_after if self.insert_after else None
			}).insert()

			self.sn_bk = section_break.name

			field = frappe.get_doc({
				"doctype":"Custom Field",
				"dt":self.dt,
				"module":"Document Manager",
				"fieldname":"related_documents_table",
				"label":"Related Documents",
				"options":"Related Document",
				"fieldtype":"Table",
				"insert_after":"Related Documents"
			}).insert()

			self.field_id = field.name

			self.save()

		else:
			sb = frappe.get_doc('Custom Field',self.sn_bk)
			sb.insert_after = self.insert_after
			sb.save()
			cf = frappe.get_doc('Custom Field',self.field_id)
			cf.insert_after = 'related_documents_section_break'
			cf.save()
	def on_trash(self):
		if self.sn_bk:
			frappe.delete_doc('Custom Field',self.sn_bk)
		if self.field_id:
			frappe.delete_doc('Custom Field',self.field_id)
	
	def get_email_recipients(self):
		rec_list = self.recipients

		return

def send_alerts():

	pass


def get_email_recipients():
	rec_data = frappe.db.sql("""
	select exr.user,exr.role,exr.df,exr.email,exr.whatsapp,das.dt,das.subject,das.message,das.wa_msg_template from `tabExpiry Alert Recipient` exr inner join `tabDocument Assignment` das
	""",as_dict=True)

	


