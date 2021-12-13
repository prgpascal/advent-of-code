import time


def clock(print_input=False, print_output=False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = function(*args)
            elapsed = time.time() - t0
            function_name = function.__name__
            s_builder = f"[{format(elapsed, '0.8f')} sec] {function_name}"
            if print_input:
                arg_str = ", ".join(repr(arg) for arg in args)
                s_builder += f"({arg_str})"
            if print_output:
                s_builder += f" => {str(result)}"
            print(s_builder)
            return result

        return wrapper

    return decorator
