import time
GR = "\033[32m" #green
RD = "\033[31m" #red
BK = "\033[0m" #black
CY = "\033[36m" #cyan
YL = "\033[33m" #yellow
NL = "\n"

def test_value(returned, func,  *args, msg="") -> bool:
    ans = None
    args_str = ", ".join(map(repr, args))
    if not msg:
        msg = repr(returned) + " is not returned from " + func.__name__ + "(" + args_str +").."
    success_str = msg.replace(" not", "")
    fail_str = msg + '\n    ..Instead, '
    start = time.perf_counter()

    try:
        ans = func(*args)
        assert ans == returned
    except AssertionError:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}{repr(ans)} is returned.{BK}")
        return False
    except Exception as e:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}an Exception occurred:..")
        print("   ..", type(e).__name__+":", e, BK)
        return False
    else:
        timing = f"Success in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{GR}{timing}{success_str}{BK}")
        return True


def test_type(returned_type, func,  *args, msg="") -> bool:
    ans = None
    args_str = ", ".join(map(repr, args))
    if not msg:
        msg = "<" + returned_type.__name__ + "> is not returned from " + func.__name__ + "(" + args_str + ").."
    success_str = msg.replace(" not", "")
    fail_str = msg + '\n    ..Instead, '
    start = time.perf_counter()

    try:
        ans = func(*args)
        assert isinstance(ans, returned_type)
    except AssertionError:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}<{type(ans).__name__}> is returned.{BK}")
        return False
    except Exception as e:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}an Exception occurred:..")
        print("   ..", type(e).__name__+":", e, BK)
        return False
    else:
        timing = f"Success in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{GR}{timing}{success_str}{BK}")
        return True

def test_contain(contained, func,  *args, msg="") -> bool:
    ans = None
    args_str = ", ".join(map(repr, args))
    if not msg:
        msg = repr(contained) + " is not in result of " + func.__name__ + "(" + args_str + ").."
    success_str = msg.replace(" not", "")
    fail_str = msg
    start = time.perf_counter()

    try:
        ans = func(*args)
        if not isinstance(ans, str): raise TypeError
        assert contained in ans
    except TypeError:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}\n    ..Instead, <{type(ans).__name__}> is returned.{BK}")
        return False
    except AssertionError:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}{BK}")
        return False
    except Exception as e:
        timing = f"Failure in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{RD}{timing}{fail_str}an Exception occurred:..")
        print("   ..", type(e).__name__+":", e, BK)
        return False
    else:
        timing = f"Success in: {repr(round((time.perf_counter()-start)*1000, 1))}ms, "
        print(f"{GR}{timing}{success_str}{BK}")
        return True

def summary(tests):
    width = 40
    success = tests.count(True)
    fail = tests.count(False)
    total = success + fail
    if total < 1:
        print(f"{YL}WARNING: 0 tests are performed{BK}")
        return False
    success_percent = round(success/total*100, 2)
    fail_percent = round(fail/total*100, 2)
    print(f"{CY}{'!@#---TESTS RESULTS SUMMARY---#@!'.center(width)}")
    print(f"Total tests!: {total}")
    print(f"{GR}Passed tests: {success}")
    print(f"{RD}Failed tests: {fail}{BK}")
    success_count = round(success_percent/100 * width)
    success_bar = "#" * success_count
    fail_bar = "_" * (width - success_count)

    if success_percent == 100:
        print(f"{GR}{f'{success_percent:.1f}%'.center(width)}{BK}")
    elif fail_percent == 100:
        print(f"{RD}{f'{fail_percent:.1f}%'.center(width)}{BK}")
    else:
        print(f"{GR}{success_percent:.1f}%{' ' * (width - 10)}{RD}{fail_percent:.1f}%{BK}")

    print(f"{GR}{success_bar}{RD}{fail_bar}{BK}")
    return True

