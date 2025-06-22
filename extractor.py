import fitz
import json
doc=fitz.open("Form ADT-1-29092023_signed.pdf")
form_data={}
for page_number in range(doc.page_count):
    page=doc[page_number]
    for widget in page.widgets():
        field_name=widget.field_name
        field_value=widget.field_value
        form_data[field_name]=field_value

def extract_adt1_from_dict(form_data):
    def clean(value):
        return value.replace("\r", "").strip() if isinstance(value, str) else ""

    return {
        "company_name": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CompanyName_C[0]", "")),
        "cin": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CIN_C[0]", "")),
        "registered_office": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CompanyAdd_C[0]", "")),
        "appointment_date": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DateOfAppSect_D[0]", "")),
        "auditor_name": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].NameAuditorFirm_C[0]", "")),
        "auditor_address": ", ".join(filter(None, [
            clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].permaddress2a_C[0]", "")),
            clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].permaddress2b_C[0]", "")),
            clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].City_C[0]", "")),
            clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].State_P[0]", "")),
            clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].Pin_C[0]", ""))
        ])),
        "auditor_frn_or_membership": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].MemberShNum[0]", "")),
        "appointment_type": "Appointment/Re-appointment in AGM" if clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform2[0].DropDownList1[0]")) == "ARGM"
        else clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform2[0].DropDownList1[0]", ""))
    }
adt1_data = extract_adt1_from_dict(form_data)
print(json.dumps(adt1_data, indent=2))
