op_list = list("()+-/*^")


def to_postfix(in_expr, debug=False):
    # -(A = (-1)*(A, (-(A = ((-1)*(A, +(A, (-(A 처리
    expr = in_expr.replace("(-(", "((-1)*(").replace("(+(", "((")
    if expr[0] in ["+", "-"]:
        expr = f"({expr[0]}1)*{expr[1:]}"
    if debug:
        print(f"input: {in_expr}\nprocessed: {expr}")
    operator = []
    out = []
    num = ""
    for pos, ch in enumerate(expr):
        if ch not in op_list:
            # 연산자가 아닌 경우
            num += ch
            if pos == len(expr) - 1:
                # 마지막인 경우 num을 out에 넣어줌
                out.append(float(num))
        else:
            # 연산자인 경우
            if len(num) > 0:
                # num에 숫자가 들어있을 경우, out에 숫자를 넣어주고, num=""로 초기화
                out.append(float(num))
                num = ""
            if ch == "(":
                # 괄호 (는 무조건 추가
                operator.append(ch)
            elif pos > 0 and ch in ["+", "-"] and expr[pos - 1] == "(":
                # (+ 와 (-를 처리: (-3/2) 이나 (+3/2) 등
                num += ch
            elif ch == ")":
                # 괄호 )를 만나면 (가 나올때까지 팝하여 out에 넣기
                while 1:
                    op = operator.pop()
                    if op == "(":
                        break
                    out.append(op)
            else:
                while 1:
                    if len(operator) == 0 or op_list.index(ch) > op_list.index(
                        operator[-1]
                    ):
                        # 연산자 스택에 아무것도 없으면 연산자 추가
                        # ch가 스택의 연산자보다 우선순위가 높으면 스택에 연산자 추가
                        operator.append(ch)
                        break
                    else:
                        # 그렇지 않으면
                        out.append(operator.pop())
        if debug:
            print(f"{pos}: {ch} => {out} , {operator}")
    while len(operator) > 0:
        # 연산자 스택에 남아있으면 모두 pop해서 out에 추가
        out.append(operator.pop())
    return out


def eval_postfix(postfix_list, debug=False):
    out = []
    for pos, ch in enumerate(postfix_list):
        if ch not in op_list:
            out.append(ch)
        else:
            y = out.pop()
            x = out.pop()
            if ch == "+":
                out.append(x + y)
            elif ch == "-":
                out.append(x - y)
            elif ch == "*":
                out.append(x * y)
            elif ch == "/":
                out.append(x / y)
            elif ch == "^":
                out.append(x**y)
        if debug:
            print(f"{pos}: {out}")
    return out[0]


infix = "(2*(-1-90/2)+2)/4+3"
infix = "-(+(1-2/2)+2)/4+3-5*2/(-3)"
postfix = to_postfix(infix, debug=True)
print(f"infix: {infix}\npostfix: {postfix}")
print(f"eval: {eval(infix.replace('^', '**'))}")
print(f"eval: {eval_postfix(postfix)}")
