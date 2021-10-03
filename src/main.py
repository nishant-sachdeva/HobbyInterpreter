from basic import run_command

while True:

    command = input("[command] > ")
    
    if command == "exit":
        break

    result, error = run_command('<stdin>', command)

    if error:
        print(error.as_string())
    elif result:
        print(result)

