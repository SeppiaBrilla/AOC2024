def is_increasing(report:list[int]) -> bool:
    for i in range(1, len(report)):
        if report[i-1] > report[i]:
            return False
    return True

def is_decreasing(report:list[int]) -> bool:
    for i in range(1, len(report)):
        if report[i-1] < report[i]:
            return False
    return True

def values_in_range(report:list[int]) -> bool:
    for i in range(1, len(report)):
        difference = abs(report[i-1] - report[i])
        if difference > 3 or difference == 0:
            return False
    return True

def is_safe(report:list[int]) -> bool:
    return (is_increasing(report) or is_decreasing(report)) and values_in_range(report)

def main():
    f = open("input.txt")
    data = f.read()
    f.close()
    reports = []
    for line in data.splitlines():
        reports.append([int(e) for e in line.split(' ')])

    safe = 0
    for report in reports:
        if is_safe(report):
            safe += 1

    print(safe)



if __name__ == "__main__":
    main()
