import json
from parsing import parser
from parsing import pdf


def make_report(vin, clinlibase_data="", with_gibdd=False):
    info = {}
    # with open("info_example.json", "w") as file:
    #     json.dump(info, file)
    # with open(r"parsing/info_example.json", "r") as file:
    #     info = json.load(file)
    info["clinlibase_data"] = clinlibase_data
    if with_gibdd:
        info["osago"] = parser.parse_rsa(vin)
        if len(vin) != 17:
            vin = info["osago"]["vin"]
        info.update(parser.parse_gibdd(vin))
        pdf.make_pdf_report_with_gibdd(info)
        return
    pdf.make_pdf_report_without_gibdd(info)


# chinlibase_data = [1231, "Rio", 2012, "30000", "Описание "*30]
# make_report(1231, chinlibase_data)
