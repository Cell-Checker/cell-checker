def metroui_table(data):
    # for column_name in enumerate(data.columns):
    #     column_meta = {"name":f"${column_name}","title":f"${column_name.title()}","sortable":"true","size":200}
    #     print('**')
    #     print (column_meta.__class__)
    rows = data.values.tolist()
    print(rows)
