# Copyright (c) 2023, Ecosoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class EAJournalEntry(Document):

	def validate(self):
		self.set_total_debit_credit()

	@frappe.whitelist()
	def fill_etax_account_entries(self):
		self.set("accounts", [])
		entries = self.get_etax_account_entries()
		if not entries:
			error_msg = _(
				"No summarized entries found for criterias:<br>Company: {0}<br> Currency: {1}<br>Payroll Payable Account: {2}"
			).format(
				frappe.bold(self.company),
				frappe.bold("X"),
				frappe.bold("Y"),
			)
			# if self.branch:
			# 	error_msg += "<br>" + _("Branch: {0}").format(frappe.bold(self.branch))
			frappe.throw(error_msg, title=_("No journal entries found"))

		for d in entries:
			self.append("accounts", d)
		return

		# self.number_of_employees = len(self.employees)
		# return self.get_employees_with_unmarked_attendance()

	def get_etax_account_entries(self):
		"""
		Return summarized entries from ETax Documents based on selected criteria.
		"""
		self.check_mandatory()
		filters = self.make_filters()
		etax_list = get_etax_entries(filters)
		return get_summarize_entries(etax_list)

	def check_mandatory(self):
		pass
		# for fieldname in ["company", "start_date", "end_date"]:
		# 	if not self.get(fieldname):
		# 		frappe.throw(_("Please set {0}").format(self.meta.get_label(fieldname)))

	def make_filters(self):
		filters = frappe._dict()
		# filters["company"] = self.company
		# filters["branch"] = self.branch
		# filters["department"] = self.department
		# filters["designation"] = self.designation

		return filters
	
	def set_total_debit_credit(self):
		self.total_debit, self.total_credit = 0, 0
		for d in self.get("accounts"):
			if d.debit and d.credit:
				frappe.throw(_("You cannot credit and debit same account at the same time"))

			self.total_debit = flt(self.total_debit) + flt(d.debit, d.precision("debit"))
			self.total_credit = flt(self.total_credit) + flt(d.credit, d.precision("credit"))

		if self.total_debit != self.total_credit:
				frappe.throw(_("Debit is not equal to Credit"))


def get_etax_entries(filters):
	"""
	Return filtered data from INET ETax Document
	"""
	return frappe.db.get_all(
		"INET ETax Document",
		fields=[
			"f46_tax_basis_total_amount",
			"f48_tax_total_amount",
			"f50_grand_total_amount",
		],
		filters=filters,
	)

def get_summarize_entries(etax_list):
	"""
	Summarize data into Dr/Cr entreis
	"""
	account_entries = []
	base = sum([x["f46_tax_basis_total_amount"] for x in etax_list])
	tax = sum([x["f48_tax_total_amount"] for x in etax_list])
	total = sum([x["f50_grand_total_amount"] for x in etax_list])
	# Dr Receivable,  Cr Income,  Cr Tax
	account_entries.append({"debit": total, "credit": 0, "account": "Accounts Receivable - F"})
	account_entries.append({"debit": 0, "credit": base, "account": "Income - F"})
	account_entries.append({"debit": 0, "credit": tax, "account": "Income - F"})
	return account_entries



# Server Script to auto create EA Journal Entry
# doc = frappe.new_doc(
#     "EA Journal Entry",
# )
# doc.posting_date = frappe.utils.today()
# doc.insert()
# doc.fill_etax_account_entries()
# doc.save()
