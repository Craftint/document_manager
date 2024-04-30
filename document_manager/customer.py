import frappe
from datetime import datetime
from dateutil.relativedelta import relativedelta

@frappe.whitelist()
def expiry_doc_creation():
    customers = frappe.get_all('Customer')

    for customer in customers:
        doc = frappe.get_doc('Customer', customer.name)

        for i in doc.related_documents_table:
            if float(i.default_expiry) == 0.0:
                continue

            date_of_expiry = i.date_of_expiry

            creation_deadline = date_of_expiry - relativedelta(months=int(float(i.default_expiry)))

            if datetime.now().date() >= creation_deadline:
                existing_doc_expiry = frappe.db.exists('Document Expiry', {'document_name': i.document_name, 'name1': doc.name})

                if existing_doc_expiry:
                    doc_expiry = frappe.get_doc('Document Expiry', existing_doc_expiry)
                else:
                    doc_expiry = frappe.new_doc('Document Expiry')

                doc_expiry.document_name = i.document_name
                doc_expiry.document_type = doc.doctype
                doc_expiry.date_of_expiry = i.date_of_expiry
                doc_expiry.default_expiry_in_months = i.default_expiry
                doc_expiry.notification_date = creation_deadline
                doc_expiry.name1 = doc.name

                doc_assignment = frappe.get_doc('Document Assignment', "Customer")

                doc_expiry.recipient = []

                if doc_assignment.dt == 'Customer':
                    for j in doc_assignment.recipients:
                        custom_recipient = doc_expiry.append('recipient', {})
                        custom_recipient.email = j.email
                        custom_recipient.whatsapp = j.whatsapp
                        custom_recipient.role = j.role
                        custom_recipient.user = j.user
                        custom_recipient.df = j.df

                doc_expiry.save()
                create_notification(doc_expiry)
                whatsapp_notification(doc_expiry)


def create_notification(doc_expiry):
    existing_notification = frappe.db.exists('Notification', {'name': doc_expiry.name})

    if existing_notification:
        notification = frappe.get_doc('Notification', existing_notification)
    else:
        notification = frappe.new_doc('Notification')

    notification.subject = f"Action Required: Your Document is Approaching its Expiry Date"
    notification.document_type = 'Document Expiry'
    notification.name = doc_expiry.name
    notification.event = 'Days Before'
    notification.date_changed = 'notification_date'
    notification.days_in_advance = 1
    notification.channel = 'Email'
    notification.enabled = 1
    notification.send_system_notification = 1
    notification.message = f"Your Document <b>{{doc.document_name}}</b> expires on <b>{{doc.get_formatted('date_of_expiry')}}</b>. Please renew it soon."

    notification.recipients = []

    for recipient in doc_expiry.recipient:
        if recipient.email == 1 :
            notification_recipient = notification.append('recipients', {})
            notification_recipient.receiver_by_document_field = "user,recipient"
            notification_recipient.receiver_by_role = recipient.role

    notification.save()

def whatsapp_notification(doc_expiry):
    existing_notification = frappe.db.exists('Notification', {'name': doc_expiry.name + " " + "WhatsApp"})

    if existing_notification:
        notification = frappe.get_doc('Notification', existing_notification)
    else:
        notification = frappe.new_doc('Notification')

    notification.document_type = 'Document Expiry'
    notification.name = doc_expiry.name + " " + "WhatsApp"
    notification.event = 'Days Before'
    notification.date_changed = 'notification_date'
    notification.days_in_advance = 1
    notification.channel = 'WhatsApp'
    notification.enabled = 1
    notification.twilio_number = 'Twilio Number'

    notification.message = f"Your Document <b>{{doc.document_name}}</b> expires on <b>{{doc.get_formatted('date_of_expiry')}}</b>. Please renew it soon."

    notification.recipients = []

    for recipient in doc_expiry.recipient:
        if recipient.whatsapp == 1 :
            notification_recipient = notification.append('recipients', {})
            notification_recipient.receiver_by_document_field = "whatsapp_number"
            notification_recipient.receiver_by_role = recipient.role

    notification.save()