import pyexcel as pe
recoders = pe.iget_records(file_name='new.xlsx')
for i in recoders:
    print(i["name"],i["age"])

