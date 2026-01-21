#!/usr/bin/env python3

import random
import re
import time

history = list()

def colorize_symbols(symbols: str) -> str:
    result = ""
    for ch in symbols:
        if ch == '!': result += "\033[32m!\033[0m"   # зелёный
        elif ch == '*': result += "\033[92m*\033[0m" # светло-зелёный
        elif ch == '?': result += "\033[31m?\033[0m" # красный
        elif ch == '/': result += "\033[91m/\033[0m" # светло-красный
        else: result += ch
    return result

def colorize_throw_str(s: str) -> str:
    if not s.strip():
        return s

    sign = s[0] if s[0] in '+-' else ''
    rest = s[1:] if sign else s

    symbols = ''.join(reversed(re.search(r'[!*?/]*$', rest).group()))
    clean_rest = rest[:-len(symbols)] if symbols else rest

    if 'd' in clean_rest:
        num_dice_str, die_type_str = clean_rest.split('d', 1)
        num_dice_str = num_dice_str or '1'
        colored_num = f"\033[36m{num_dice_str}\033[0m"
        colored_die = f"\033[34md{die_type_str}\033[0m"
    else:
        colored_num = f"\033[36m{clean_rest}\033[0m"
        colored_die = ""

    return sign + colored_num + colored_die + colorize_symbols(symbols)

def colorize_full_line(s: str) -> str:
    parts = re.split(r'(?=[+-])', s)
    return ''.join(colorize_throw_str(p) for p in parts if p)

def handle_line(s: str) -> tuple[float, float, float]:
    throws = re.split(r'(?=[+-])', s)
    res, mn, mx = 0.0, 0.0, 0.0
    for t in throws:
        if not t: continue
        r, _mn, _mx = handle_throw(t)
        colored_t = colorize_throw_str(t)
        print(f"{colored_t}[\033[94m{r}\033[0m]", end=" ")
        res += r
        mn += _mn
        mx += _mx
    return res, mn, mx

def handle_throw(s: str) -> tuple[float, float, float]:
    random.seed(time.time())

    mn, mx = 0, 0

    sign = 1
    if s and s[0] in "+-":
        sign = 1 if s[0] == "+" else -1
        s = s[1:]

    if not s:
        return 0.0, 0.0, 0.0

    if s.startswith('d'):
        s = "1" + s

    best = s.count('!')
    worst = s.count('?')
    modifier = 2 if s.count("*")>s.count("/") else (0.5 if s.count("*")<s.count("/") else 1)

    clean_s = re.sub(r'[!*?/]', '', s)

    if 'd' in clean_s:
        n_str, d_str = clean_s.split('d', 1)
        n, d = int(n_str or 1), int(d_str)
    else:
        n, d = int(clean_s), 1

    mn = n  # все броски единица
    mx = n*d  # все броски максимум
    if sign == -1:
        mn = -n*d
        mx = -n

    rolls = [sum(random.randint(1, d) for _ in range(n)) for _ in range(1 + bool(best or worst))]

    if best > worst:
        return max(rolls) * sign * modifier, mn, mx
    elif worst > best:
        return min(rolls) * sign * modifier, mn, mx
    return rolls[0] * sign * modifier, mn, mx

def main():
    global history
    while True:
        if history:
            print("\033[2mИстория бросков:\033[0m")
            for i, h in enumerate(history):
                print(f"[\033[33m{i}\033[0m: {colorize_full_line(h)}] ", end="")
            print("\n")

        try:
            command = input("\033[35m>\033[0m ").strip()
        except EOFError:
            break

        if not command and history:
            line = history[0]
        elif command.isdigit() and int(command) < len(history):
            line = history[int(command)]
        else:
            line = command.replace(' ', '').lower().replace("к", "d")

        if not line:
            continue

        res, mn, mx = handle_line(line)

        color_code = "\033[31m"  # красный по умолчанию
        if mx > mn:
            range_span = mx - mn
            lower_bound = mn + range_span / 3
            upper_bound = mn + 2 * range_span / 3

            if res > upper_bound:
                color_code = "\033[32m"  # зелёный (верхняя треть)
            elif res > lower_bound:
                color_code = "\033[33m"  # жёлтый (средняя треть)

        result_str = f"\n\033[1;33m=\033[0m {color_code}{res}\033[0m \033[34m[{mn} ... {mx}]\033[0m\n"
        print(result_str)

        if line in history:
            history.remove(line)
        history.insert(0, line)
        history = history[:10]

if __name__ == "__main__":
    main()
