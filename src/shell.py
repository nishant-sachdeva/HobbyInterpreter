import basic

while True:

    command = input("[command] > ")
    
    if command == "exit":
        break

    result, error = basic.run('<stdin>', command)

    if error:
        print(error.as_string())
    else:
        print(result)

