import sys

RD = "\033[31m" #red
BK = "\033[0m" #black

def input_int(message:str, values:tuple = None, no_negative:bool = False, no_zero:bool = False, minimum:int = None, maximum:int = None)->int:
    ans = None
    repeat = ""
    while True:
        try:
            ans = input(repeat + message).strip()
            ans = int(ans)
        except ValueError:
            repeat = f"{RD}Must be an integer.{BK}\n"
            continue
        except EOFError:
            sys.exit("Exiting...")
        else:
            if values and ans not in values:
                repeat = f"{RD}Invalid input. Expected: {" or ".join(map(repr, values))}{BK}\n"
                continue
            elif no_zero and no_negative and ans <= 0:
                repeat = f"{RD}Must be a positive number.{BK}\n"
                continue
            elif no_negative and ans < 0:
                repeat = f"{RD}Can't be a negative number.{BK}\n"
                continue
            elif no_zero and ans == 0:
                repeat = f"{RD}Can't be zero.{BK}\n"
                continue
            if minimum is not None  and ans < minimum:
                repeat = f"{RD}Must be {minimum} or more.{BK}\n"
                continue
            if maximum is not None and ans > maximum:
                repeat = f"{RD}Must be {maximum} or less.{BK}\n"
                continue
            break
    return ans

def input_float(message:str, values:tuple = None, no_negative:bool = False, no_zero:bool = False, minimum:float = None, maximum:float = None)->float:
    ans = None
    repeat = ""
    while True:
        try:
            ans = input(repeat + message).strip()
            ans = float(ans)
        except ValueError:
            repeat = f"{RD}Must be a decimal number.{BK}\n"
            continue
        except EOFError:
            sys.exit("Exiting...")
        else:
            if values and ans not in tuple(map(float, values)):
                repeat = f"{RD}Invalid input. Expected: {" or ".join(map(repr, values))}{BK}\n"
                continue
            elif no_zero and no_negative and ans <= 0:
                repeat = f"{RD}Must be a positive number.{BK}\n"
                continue
            elif no_negative and ans < 0:
                repeat = f"{RD}Can't be a negative number.{BK}\n"
                continue
            elif no_zero and ans == 0:
                repeat = f"{RD}Can't be zero.{BK}\n"
                continue
            if minimum is not None and ans < minimum:
                repeat = f"{RD}Must be {minimum} or more.{BK}\n"
                continue
            if maximum is not None and ans > maximum:
                repeat = f"{RD}Must be {maximum} or less.{BK}\n"
                continue
            break
    return ans


def input_choice(message:str, values:tuple = ("Yes", "No"), first_letter= False, case_sensitive=False, numeric=False)->str:
    ans = None
    repeat = ""
    repeat_err=f"{RD}Invalid input. Expected: {" or ".join(map(repr, values))}{BK}\n"
    fixed_values=tuple(map(str, values))
    match numeric:
        case False:
            message = f"{message}({"/".join(map(str, fixed_values))}): "
            if not case_sensitive:
                fixed_values = tuple(map(lambda s: s.lower(), fixed_values))
            while True:
                try:
                    ans = input(repeat + message).strip()
                except EOFError:
                    sys.exit("Exiting...")
                else:
                    if not case_sensitive:
                        ans = ans.lower()
                    if first_letter and len(ans) == 1:
                        first_letters=tuple(map(lambda x: x[0], fixed_values))
                        if not ans in first_letters:
                            repeat = repeat_err
                            continue
                        index_ans=first_letters.index(ans)
                        return values[index_ans]
                    elif ans not in fixed_values:
                        repeat = repeat_err
                        continue
                    else:
                        index_ans=fixed_values.index(ans)
                        return values[index_ans]
        case True:
            for i in range(len(values)):
                message+="\n"+str(i+1)+") "+values[i]
            message += "\n"
            int_ans = input_int(message, tuple(i+1 for i in range(len(values))))
            ans = values[int_ans-1]
    return ans

