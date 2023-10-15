// Copyright (c) 2023, Ecosoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('EA Journal Entry', {

	refresh: function (frm) {
		if (frm.doc.docstatus === 0 && !frm.is_new()) {
			// frm.page.clear_primary_action();
			frm.add_custom_button(__("Get ETax Account Entries"),
				function() {
					frm.events.get_etax_account_entries(frm);
				}
			).toggleClass("btn-primary", !(frm.doc.accounts || []).length);
		}
	},

	get_etax_account_entries: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'fill_etax_account_entries',
		}).then(r => {

			console.log(	)

			if (r.docs && r.docs[0].accounts) {
				frm.accounts = r.docs[0].accounts;
				frm.dirty();
				frm.save();
				frm.refresh();
				frm.scroll_to_field("accounts");
			}
		});
	},



});
