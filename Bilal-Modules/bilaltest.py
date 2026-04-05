import time, traceback
GR = "\033[32m" #green
RD = "\033[31m" #red
BK = "\033[0m" #black
BL = "\033[34m" #blue
YL = "\033[33m" #yellow
NL = "\n"

FAILURE = "FAILURE"
SUCCESS = "SUCCESS"
counter = 0
counting = False
indent = f"{'':^8}|{'':^8}| "
def header(numbers=True)->tuple:
    global counting, indent
    counting = numbers
    no_head = f"{'No.':>4}| " if counting else ""
    head = f"{BL}{no_head}{'STATE':^8}|{'TIME':^8}|{'DETAILS':^10}{BL}"
    no_indent = "    | "
    if counting: indent = no_indent + indent
    print(head)
    return None, head

def log_shaper(state:bool, seconds:float, *details, prnt=True, time_limit=0.00005)->str:
    global counter, counting
    no_str = ""
    if counting:
        counter += 1
        no_str = f"{counter:>3} | "
    color = GR if state else RD
    time_color = YL if (state and seconds<time_limit) else RD
    output = color + no_str + (SUCCESS if state else FAILURE)
    if seconds < 0.001:
        time_str = f"{round(seconds * 1000000, 1)}μs"
    elif seconds < 1:
        time_str = f"{round(seconds * 1000, 1)}ms"
    elif seconds < 60:
        time_str = f"{round(seconds, 2)}s"
    elif seconds < 3600:
        time_str = f"{round(seconds / 60, 2)}m"
    else:
        time_str = f"{round(seconds / 3600, 2)}h"

    output += f" |{time_color}{time_str:^8}{color}| "
    if details:
        output += details[0]
        if len(details) > 1:
            for i in range(1, len(details)):
                output += "\n" + indent + str(details[i])
    output += BK
    if prnt: print(output)
    return output

def test_value(returned, func,  *args, msg="") -> tuple:
    ans = None
    args_str = ", ".join(map(repr, args))
    if not msg:
        msg = repr(returned) + " is not returned from " + func.__name__ + "(" + args_str +")"

    start = time.perf_counter()

    try:
        ans = func(*args)
        assert ans == returned
    except AssertionError:
        output = log_shaper(False, time.perf_counter() - start, msg, f"Instead, {repr(ans)} is returned.")

        return False, output
    except Exception as e:
        output = log_shaper(False, time.perf_counter() - start,msg,
                            *trace(e))
        return False, output
    else:
        output = log_shaper(True, time.perf_counter() - start, msg.replace(" not", ""))
        return True, output

def test_type(returned_type, func,  *args, msg="") -> tuple:
    ans = None
    args_str = ", ".join(map(repr, args))
    if not msg:
        msg = "<" + returned_type.__name__ + "> is not returned from " + func.__name__ + "(" + args_str + ")"
    start = time.perf_counter()

    try:
        ans = func(*args)
        assert isinstance(ans, returned_type)
    except AssertionError:
        output = log_shaper(False, time.perf_counter() - start, msg, f"Instead, <{type(ans).__name__}> is returned.")
        return False, output
    except Exception as e:
        output = log_shaper(False, time.perf_counter() - start, msg,
                            *trace(e))
        return False, output
    else:
        output = log_shaper(True, time.perf_counter() - start, msg.replace(" not", ""))
        return True, output

def test_in(contained, func,  *args, msg="") -> tuple:
    ans = None
    args_str = ", ".join(map(repr, args))
    if not msg:
        msg = repr(contained) + " is not a substring in <str> returned from " + func.__name__ + "(" + args_str + ")"
    start = time.perf_counter()

    try:
        ans = func(*args)
        if not isinstance(ans, (str, dict, list, set, tuple)): raise TypeError
        if isinstance(ans, (dict, list, set, tuple)):
            msg = msg.replace("a substring", "an item").replace("str", type(ans).__name__)
        if isinstance(ans, dict):
            msg = msg.replace("an item", "a key")

        assert contained in ans

    except TypeError:
        output = log_shaper(False, time.perf_counter() - start,
                            msg.replace("a substring in <str> returned from", "found in return of"),
                            f"Instead, <{type(ans).__name__}> is returned.")
        return False, output

    except AssertionError:
        output = log_shaper(False, time.perf_counter() - start, msg, f"Instead, {repr(ans)} is returned.")
        return False, output
    except Exception as e:
        output = log_shaper(False, time.perf_counter() - start, msg,
                            *trace(e))
        return False, output
    else:
        output = log_shaper(True, time.perf_counter() - start, msg.replace(" not", ""))
        return True, output

def summary(tests, windows = False):
    width = 40
    results = [x[0] for x in tests]
    outputs = [x[1] for x in tests]
    success = results.count(True)
    fail = results.count(False)
    total = success + fail
    if total < 1:
        output = f"{YL}WARNING: 0 tests are performed{BK}"
        print(output)
        outputs.append(output)
    success_percent = round(success/total*100, 1)
    fail_percent = round(fail/total*100, 1)

    lines = [f"{BL}{'!@#---TESTS RESULTS SUMMARY---#@!'.center(width)}{BK}",
             f"{BL}Total tests!: {total}{BK}",
             f"{GR}Passed tests: {success}{BK}",
             f"{RD}Failed tests: {fail}{BK}"
             ]

    success_count = round(success_percent/100 * width)
    success_bar = "#" * success_count
    fail_bar = "_" * (width - success_count)

    if success_percent == 100:
        lines.append(f"{GR}{f'{success_percent:.1f}%'.center(width)}{BK}")
    elif fail_percent == 100:
        lines.append(f"{RD}{f'{fail_percent:.1f}%'.center(width)}{BK}")
    else:
        lines.append(f"{GR}{success_percent:.1f}%{' ' * (width - 10)}{RD}{fail_percent:.1f}%{BK}")
    lines.append(f"{GR}{success_bar}{RD}{fail_bar}{BK}")
    for l in lines:
        print(l)
    if windows:
        import bilalwindow as bw
        # بنضيف فاصل شيك وبعده الـ Summary اللي لسه مجهزينها
        final_logs = outputs + ["\n" + "=" * width + "\n"] + lines
        bw.render(final_logs, success_percent)

def trace(e):
    lines = []
    tb = traceback.extract_tb(e.__traceback__)
    filename, line, func, text = tb[-1]
    lines.append(f"Instead, Error: {type(e).__name__}")
    lines.append(f"Detail: {str(e)}")
    lines.append(f"File: {filename.split('\\')[-1]}, Line: {line}, Func: {func}")
    lines.append("Code: " + (f"-->> {text} <<--" if text else "Unknow code"))
    return lines
