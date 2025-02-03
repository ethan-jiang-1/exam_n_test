from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

YOUR_API_KEY = "iqDFvfPGRnlgSTVydbH9z8WRLIGH46"
YOUR_API_URL = "https://bowheadtechnologyl-ce8sccag.api.unstructuredapp.io"

def create_client():
    client = UnstructuredClient(
        api_key_auth=YOUR_API_KEY,
        server_url=YOUR_API_URL,
    )
    return client

def construct_req(filename):
    with open(filename, "rb") as f:
        files=shared.Files(
            content=f.read(),
            file_name=filename,
        )

    req = shared.PartitionParameters(files=files, languages=["chi_sim"])
    return req

def pickup_table(resp):
    table_in_html = None
    header_texts = []
    title_texts = []
    if resp is not  None:
        print(resp.elements)

        for el in resp.elements:
            # first table only
            el_type = el["type"]    
            if el_type == "Table":
                metadata = el["metadata"]  
                table_in_html = metadata["text_as_html"]
            elif el_type== "Header":
                header_texts.append(el["text"])
            elif el_type == "Title":
                title_texts.append(el["text"])

    return table_in_html, header_texts, title_texts

def parse_table_from_image(client, filename):

    req = construct_req(filename)

    try:
        resp = client.general.partition(req)
    except SDKError as e:
        print("Exception Occured" + str(e))

    return pickup_table(resp)

if __name__ == "__main__":
    filename = "_data/unstruct_stock0.jpg"
    client = create_client()
 
    table_in_html, header_texts, title_texts = parse_table_from_image(client, filename)
    print()
    print(table_in_html)
    print(header_texts)
    print(title_texts)
