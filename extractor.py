import fitz
import os
import json
import subprocess
import re

#Extract desired json value
def extract_adt1_from_dict(form_data):
    def clean(value):
        return value.replace("\r", "").strip() if isinstance(value, str) else ""

    return {
        "company_name": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CompanyName_C[0]", "")),
        "cin": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CIN_C[0]", "")),
        "registered_office": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CompanyAdd_C[0]", "")),
        "appointment_date": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DateReceipt_D[0]", "")),         "auditor_name": clean(form_data.get("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].NameAuditorFirm_C[0]", "")),
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

#Summarize the extracted json value from the ADT-1 PDF
def ai_style_summay(data):

    # Convert JSON to flat text for summarization
    formatted = "\n".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in data.items())

    #Create the prompt for summarization
    prompt = f"Summarize the following structured company data into a professional human-readable paragraph:\n\n{formatted}"

    #Run the Ollama model (tinyllama or mistral)
    result = subprocess.run(
        ["ollama", "run", "mistral"],  # Change to "tinyllama" if needed
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )

    # return the summary
    summary=result.stdout.decode("utf-8")
    return summary   

# Extract embedded pdf file attachments 
def sanitize_filename(filename):
    # Replace problematic characters with underscores
    return re.sub(r'[^\w\-_\. ()]', '_', filename)

def extract_attachments(doc, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    total = doc.embfile_count()
    print(f"Total embedded attachments found is the given pdf: {total}")

    attachment_count = 0

    for i in range(total):
        try:
            # Try to get file info
            file_info = doc.embfile_info(i)
            file_name = file_info.get("filename", None)

            if not file_name:
                print(f" Failed attachment {i}: No filename found.")
                continue

            safe_name = sanitize_filename(file_name)

            # Try to get file data
            file_data = doc.embfile_get(i)
            if not file_data:
                print(f" Failed attachment {i}: No file data found.")
                continue

            # Save only if everything is valid
            output_path = os.path.join(output_folder, safe_name)
            with open(output_path, "wb") as f:
                f.write(file_data)

            print(f"Extracted: {safe_name}")
            attachment_count += 1

        except Exception as e:
            print(f"Failed attachment {i} due to error: {e}")

    print(f"Extracted {attachment_count} of {total} attachment(s) to '{output_folder}'")

#Summarize Attachments folder's files
def summarize_attachments(folder):
    # Extract all text from the pdfs of the attachments folder.
    all_text=[]
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder, filename)
            doc = fitz.open(filepath)
            text = "\n".join([page.get_text() for page in doc])
            all_text.append(f"{filename}:\n{text.strip()}\n")
    combined = "\n".join(all_text)
    prompt = f"""
Summarize the following document and return a two sentenced passage:{combined}
"""
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
    )

    return result.stdout.decode("utf-8")


#Create a dictionary by field and value of the ADT-1 form using widgets
doc=fitz.open("Form ADT-1-29092023_signed.pdf")
form_data={}
for page_number in range(doc.page_count):
    page=doc[page_number]
    for widget in page.widgets():
        field_name=widget.field_name
        field_value=widget.field_value
        form_data[field_name]=field_value


#Hash-map/Dictionary of the form value
dict_data=extract_adt1_from_dict(form_data)

#Convert to the Json
json_data=json.dumps(dict_data, indent=2)
print(json_data)

#Save the json file as output.json
with open("output.json","w") as json_file:
    json_file.write(json_data)


#Generate summary from the json data using LLM Model and save the summary as summary.txt
json_summary=ai_style_summay(dict_data)


#Extract attached files from the ADT-1 pdf and save thoose files in a folder 
extract_attachments(doc,"attachments")


#Summarize the total files embedded in the pdf
folder="attachments"
attachments_summary=summarize_attachments(folder)


#Summary combined with attachments pdf and Json_Data extracted from the pdf
summary=" ".join((json_summary+attachments_summary).split())
print(summary)

# Save the final summary
output_file="summary.txt"
with open(output_file,"w", encoding="utf-8") as f :
    f.write(summary)



