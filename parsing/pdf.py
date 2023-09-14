import fpdf

translated_names = {"Natural": "ФизЛицо",
                    "AccidentDateTime": "Дата",
                    "VehicleDamageState": "Состояние ТС",
                    "AccidentType": "Тип аварии",
                    "Collision": "Столкновение",
                    "Damaged": "Нанесенный урон",
                    "DamageDestription": "Описание",
                    "VehicleMark": "Марка машины",
                    "VehicleAmount": "Количество",
                    "VehicleYear": "Год",
                    "AccidentPlace": "Место",
                    "VehicleSort": "Вид ТС",
                    "VehicleModel": "Модель машины",
                    "OwnerOkopf": "Владелец",
                    "PhizLiza": "ФизЛица",
                    "numberID": "Номер ID",
                    "seria": "Серия",
                    "nomer": "Номер",
                    "orgosago": "Организация",
                    "status": "Статус",
                    "term": "Срок действия",
                    "regnum": "Регномер",
                    "kuzovNumber": "Номер кузова",
                    "maxMassa": "Максимальная масса",
                    "sledToRegorTo": "Идет до регистрации",
                    "trailer": "Прицеп",
                    "cel": "Цель использования",
                    "ogran": "Ограничения",
                    "insured": "Страхователь",
                    "owner": "Собственник",
                    "kbm": "КБМ",
                    "region": "Регион",
                    "strahsum": "Сумма страховки",
                    "dateactual": "Действие страховки",
                    "engineVolume": "Мощность двигателя",
                    "color": "Цвет",
                    "bodyNumber": "Номер кузова",
                    "year": "Год",
                    "engineNumber": "Номер двигателя",
                    "vin": "ВИН",
                    "model": "Модель",
                    "category": "Категория",
                    "type": "Тип",
                    "powerHp": "Мощность",
                    "powerKwt": "Мощность в Квт",
                    "regname": "Регион",
                    "gid": "ГИД",
                    "codDL": "Код ДЛ",
                    "dateogr": "Дата",
                    "ogrkod": "Код организации",
                    "tsmodel": "Модель ТС",
                    "codeTo": "Код",
                    "dateadd": "Дата добавления",
                    "phone": "Телефон",
                    "regid": "Код региона"}


class PDF(fpdf.FPDF, fpdf.HTMLMixin):
    def __init__(self, orientation, unit, format):
        super().__init__(orientation, unit, format)
        self.add_page()
        self.add_font('DejaVuSansCondensed', "", 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font("DejaVuSansCondensed", size=18)


def make_pdf_report_with_gibdd(info):
    title_cell_width, content_cell_width, cell_height = 60, 135, 10
    pdf = PDF(orientation='P', unit='mm', format='A4')

    if info['clinlibase_data']:
        pdf.cell(title_cell_width, cell_height, txt="Описание.")
        pdf.write_html(f"<p>{info['clinlibase_data'][4]}</p>", table_line_separators=True)
        pdf.ln(cell_height)

        pdf.cell(title_cell_width, cell_height, txt="Данные из СlinliBase")
        pdf.write_html(make_table(list(zip(["Марка/модель:", "Год выпуска:", "Пробег:", "Описание:"], info['clinlibase_data'][1:4]))))
        pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="Данные из ГИБДД.")
    owners = info["ownershipPeriods"]
    pdf.cell(title_cell_width, cell_height, txt="Владельцы.")
    pdf.ln(cell_height)
    if owners:
        table_content = [["Владелец", "Период"]]
        for owner in owners:
            table_content.append([translated_names[owner["simplePersonType"]], f"с {owner['from']} по {owner['to']}"])
        pdf.write_html(make_table(table_content), table_line_separators=True)

    else:
        pdf.cell(title_cell_width, cell_height, txt="Нет информации о владельцах.", align="C")

    pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="ДТП.")
    pdf.ln(cell_height)
    accidents = info["dtp"]["Accidents"]
    if accidents:
        exceptions = ["AccidentNumber", "RegionName", "DamagePoints"]
        for i in range(len(accidents)):
            accident = accidents[i]
            pdf.cell(title_cell_width, cell_height, txt=f"{i+1}-e ДТП ", align="C")
            pdf.ln(cell_height)
            table_content = []
            for name, status in accident.items():
                if name not in exceptions:
                    row_content = [translated_names[name] if name in translated_names.keys() else name]
                    if status:
                        row_content.append(translated_names[status] if status in translated_names.keys() else status)
                    else:
                        row_content.append("Нет информации.")
                    table_content.append(row_content)
            pdf.write_html(make_table(table_content))
    else:
        pdf.cell(title_cell_width, cell_height, txt="Нет информации.")

    pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="Розыск.")
    wanted = info["wanted"]
    if wanted:
        pass
    else:
        pdf.cell(title_cell_width, cell_height, txt="Нет информации.")

    pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="Диагностика.")
    diagnostic = info["diagnostic"]
    if diagnostic:
        pass
    else:
        pdf.cell(title_cell_width, cell_height, txt="Нет информации.")

    pdf.ln(cell_height)
    pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="Ограничения.")
    restrict = info["restrict"]
    if restrict:
        table_content = []
        exceptions = ["tsyear", "tsVIN", "tsKuzov", "divtype", "divid"]
        for name, status in restrict.items():
            if name not in exceptions:
                if name != "osnOgr":
                    table_content.append([translated_names[name], status if status else "Нет информации."])
                else:
                    data = [word for word in status.split(",")]
                    data[1] = f"Имя: {data[1]}"
                    table_content.extend(list(info.split(":") for info in data))
        pdf.write_html(make_table(table_content))
    else:
        pdf.cell(title_cell_width, cell_height, txt="Нет информации.")
    pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="Машина.")
    vehicle = info["vehicle"]
    if vehicle:
        pdf.ln(cell_height)
        table_content = []
        for name, status in vehicle.items():
            table_content.append([translated_names[name], status if status else "Нет информации"])
    pdf.write_html(make_table(table_content))

    pdf.cell(title_cell_width, cell_height, txt="Данные из РСА. Информация по осаго.")
    osago = info["osago"]
    if osago:
        table_content = []

        for name, status in osago.items():
            if name != "ogran":
                if name == "term":
                    status = "Договор активен" if "активен" in status.split() else "Договор не активен"
                row_content = [translated_names[name], status if status else "Нет информации."]
            else:
                for word in status.split():
                    if word.isdecimal():
                        row_content = [translated_names[name], "Допущенно " + word + " чел."]
                        break
            table_content.append(row_content)
        pdf.write_html(make_table(table_content))
    else:
        pdf.cell(title_cell_width, cell_height, txt="Нет информации.")
    pdf.ln(cell_height)

    pdf.cell(title_cell_width, cell_height, txt="Изображения ТС.")
    pdf.ln(cell_height)

    i = 1
    while True:
        try:
            pdf.image(fr"C:/Users/Семен/Desktop/photo/{info['clinlibase_data'][0]}_{i}.jpg", h=120)
        except FileNotFoundError:
            break
        pdf.ln(cell_height)
        i += 1
    pdf.ln(cell_height)

    if i == 0:
        pdf.cell(content_cell_width, cell_height, txt="Изображений нет.")
    pdf.ln(cell_height)
    pdf.output(f"{info['vehicle']['vin']}.pdf")


def make_pdf_report_without_gibdd(info):

    title_cell_width, content_cell_width, cell_height = 60, 135, 10
    pdf = PDF(orientation='P', unit='mm', format='A4')

    if info['clinlibase_data']:
        pdf.cell(title_cell_width, cell_height, txt="Описание.")
        pdf.write_html(f"<p>{info['clinlibase_data'][4]}</p>", table_line_separators=True)
        pdf.ln(cell_height)

        pdf.cell(title_cell_width, cell_height, txt="Данные из СlinliBase")
        pdf.write_html(make_table(list(zip(["Марка/модель:", "Год выпуска:", "Пробег:", "Описание:"], info['clinlibase_data'][1:4]))))
        pdf.ln(cell_height)

    i = 1
    while True:
        try:
            pdf.image(fr"C:/Users/Семен/Desktop/photo/{info['clinlibase_data'][0]}_{i}.jpg", h=120)
        except FileNotFoundError:
            break
        pdf.ln(cell_height)
        i += 1
    pdf.ln(cell_height)

    if i == 0:
        pdf.cell(content_cell_width, cell_height, txt="Изображений нет.")
    pdf.ln(cell_height)
    print(info['clinlibase_data'][0])
    pdf.output(f"{info['clinlibase_data'][0]}.pdf")


def make_table(table_content):
    table = "<table width='105%' border='1'>"
    try:
        for title, content in table_content:
            table += f"<tr height='100'><td width='35%'>{str(title).strip()}</td><td width='65%'>{str(content).strip()}</td></tr>"
    except ValueError:
        for content in table_content:
            print(content)
    table += "<tfoot><tr></tr></tfoot></table>"
    return table
