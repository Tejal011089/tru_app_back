# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from test.doctype import assign_notify,verfy_bottle_number,update_test_log
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#self.assign_pour_point()
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)
		self.create_result_record('Running')

	def add_equipment(self,equipment):
		#webnotes.errprint(equipment)
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	


	def on_submit(self):
		self.create_result_record('Confirm')

	def create_result_record(self,status):

		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Pour Point", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by,'status':status}
		#diffrence={'Sediment & Precipitable Sludge':self.doc.diffrence}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			parent=create_test_results(test_detail)
			#for val in voltage:
			create_child_testresult(parent,self.doc.temperature_ir,test_detail,'Pour Point')

		