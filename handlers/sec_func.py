

async def write_info(variable):
    input_file = open("inputfile.txt", "w")
    input_file.write(variable["photo"])
    input_file.close

    input_text = open("inputtext.txt", "w")
    input_text.write(variable["invite"])
    input_text.close()