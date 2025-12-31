import itertools

def print_s(s):
    spaces = "            "
    print(spaces + s)
def print_header():
    print_s("")
    print_s(f"#[allow(unused_variables)]")
    print_s(f"#[allow(missing_docs)]")

def has_duplicates(iterable):
    return len(set(iterable)) != len(iterable)

def generate():
    fields = ['x', 'y', 'z', 'w']
    
    for dim in [2, 3, 4]:
        src_fields = fields[:dim]
        header = f"[{', '.join(src_fields)}]"
        
        # unique swizzles
        print_header()
        print_s(f"impl<T> Vec{dim}<T> {{")
        
        print_s(f"    swizzle!(read, {header},")
        for length in range(1, dim + 1):
            for p in itertools.product(src_fields, repeat=length):
                # only unique components. Otherwise we need Copy/Clone
                if not has_duplicates(p):
                    print_s(f"        {''.join(p)} = {', '.join(p)};")
        print_s("    );")

        print_s(f"    swizzle!(write, {header},")
        for length in range(1, dim + 1):
            # permutations for unique components only (cannot assign to same field twice)
            for p in itertools.permutations(src_fields, length):
                print_s(f"        with_{''.join(p)} = {', '.join(p)};")
        print_s("    );")
        print_s("}")

        # repeated swizzles
        print_header()
        print_s(f"impl<T> Vec{dim}<T> where T: Copy {{")
        
        print_s(f"    swizzle!(read, {header},")
        for length in range(1, dim + 1):
            # product for all combinations (repeats like xxx)
            for p in itertools.product(src_fields, repeat=length):
                if has_duplicates(p):
                    print_s(f"        {''.join(p)} = {', '.join(p)};")
        print_s("    );")
        print_s("}")

if __name__ == "__main__":
    generate()