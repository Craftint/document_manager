// Copyright (c) 2023, Dx and contributors
// For license information, please see license.txt

frappe.ui.form.on('Document Assignment', {
	dt: function (frm) {
		frappe.db.get_doc('DocType', frm.doc.dt, 'fields').then(r => {

			let field_list = r.fields.map(f => f.fieldname).join('\n')

			frm.set_df_property('insert_after', 'options', field_list)

			let contact_fields = r.fields.filter(f => {
				return f.fieldtype == 'Link' && ['Contact', 'User'].includes(f.options) || f.fieldtype == 'Data' && ['Email', 'Phone'].includes(f.options)

			}).map(f => f.fieldname).join('\n')

			frm.fields_dict.recipients.grid.update_docfield_property('df', 'options', contact_fields)
		})
	},
	refresh: function (frm) {
		if (frm.doc.dt){
			frappe.db.get_doc('DocType', frm.doc.dt, 'fields').then(r => {

				let field_list = r.fields.map(f => f.fieldname).join('\n')

				frm.set_df_property('insert_after', 'options', field_list)

				let contact_fields = r.fields.filter(f => {
					return f.fieldtype == 'Link' && ['Contact', 'User'].includes(f.options) || f.fieldtype == 'Data' && ['Email', 'Phone'].includes(f.options)

				}).map(f => f.fieldname).join('\n')

				frm.fields_dict.recipients.grid.update_docfield_property('df', 'options', contact_fields)
			})
		}
	}
});