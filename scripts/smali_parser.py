def get_smali_lines(file: str) -> list[str]:
    lines = []
    with open(file, "r", encoding="utf-8") as smali:
        lines = smali.readlines()
    return lines

def find_smali_method_start(lines: list[str], index: int) -> int:
    while True:
        index -= 1
        if lines[index].find(".method") >= 0:
            return index

def find_smali_method_end(lines: list[str], index: int) -> int:
    while True:
        index += 1
        if lines[index].find(".end method") >= 0:
            return index

def debug_print_smali_method(lines: list[str], start: int, end: int) -> None:
    while start != (end + 1):
        print(start, lines[start])
        start += 1

def replace_smali_method_body(lines: list[str], start: int, end: int, new_lines: list[str]) -> list[str]:
    new_content = []
    index = 0
    skip = end - start - 1

    while index != (start + 1):
        new_content.append(lines[index])
        index += 1
    
    for line in new_lines:
        new_content.append(line)
    
    index += skip
    while index < len(lines):
        new_content.append(lines[index])
        index += 1

        
    return new_content

# example i guess
# if __name__ == "__main__":
#     lines = get_smali_lines("./decompiled/smali_classes2/com/radiquum/anixart/Prefs.smali")
    
#     for index, line in enumerate(lines):
#         if line.find("IS_SPONSOR") >= 0:
#             method_start = find_smali_method_start(lines, index)
#             method_end = find_smali_method_end(lines, index)
#             new_content = replace_smali_method_body(lines, method_start, method_end, c)
            
#             with open("./help/Prefs_orig.smali", "w", encoding="utf-8") as file:
#                 file.writelines(lines)
#             with open("./help/Prefs_modified.smali", "w", encoding="utf-8") as file:
#                 file.writelines(new_content)
        