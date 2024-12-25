def is_increasing_errors(report:list[int]) -> int:
    errors = 0
    for i in range(1, len(report)):
        if report[i-1] >= report[i]:
            errors += 1
    return errors

def is_decreasing_errors(report:list[int]) -> int:
    errors = 0
    for i in range(1, len(report)):
        if report[i-1] <= report[i]:
            errors += 1
    return errors

def values_in_range_errors(report:list[int]) -> int:
    errors = 0
    for i in range(1, len(report)):
        difference = abs(report[i-1] - report[i])
        if difference > 3 or difference == 0:
            errors += 1
    return errors

def new_increasing(report:list[int]) -> list[list[int]]:
    new_report = []
    for i in range(len(report)-1):
        if report[i] < report[i+1]:
            new_report.append(report[i])
        else:
            r1 = new_report + [report[i]] + report[i+2:]
            r2 = new_report + report[i+1:]
            return [r for r in [r1, r2] if is_increasing_errors(r) == 0]

    return [r for r in [new_report, new_report + [report[-1]]] if is_increasing_errors(r) == 0]

def new_decreasing(report:list[int]) -> list[list[int]]:
    new_report = []
    for i in range(len(report)-1):
        if report[i] > report[i+1]:
            new_report.append(report[i])
        else:
            r1 = new_report + [report[i]] + report[i+2:]
            r2 = new_report + report[i+1:]
            return [r for r in [r1, r2] if is_decreasing_errors(r) == 0]

    return [r for r in [new_report, new_report + [report[-1]]] if is_decreasing_errors(r) == 0]

def new_values_in_range(report:list[int]) -> list[list[int]]:
    new_report = []
    for i in range(len(report)-1):
        difference = abs(report[i+1] - report[i])
        if difference >= 1 and difference <= 3:
            new_report.append(report[i])
        else:
            r1 = new_report + [report[i]] + report[i+2:]
            r2 = new_report + report[i+1:]
            return [r for r in [r1, r2] if values_in_range_errors(r) == 0]

    return [r for r in [new_report, new_report + [report[-1]]] if values_in_range_errors(r) == 0]

def is_safe(report:list[int]) -> bool:
    increasing_errors = is_increasing_errors(report)
    decreasing_errors = is_decreasing_errors(report)
    range_errors = values_in_range_errors(report)
    safe = (increasing_errors == 0 or decreasing_errors == 0) and range_errors == 0
    if safe:
        return True

    new_reports = []
    if (increasing_errors != 0 and decreasing_errors != 0):
        min_errors = min(increasing_errors, decreasing_errors)
        if min_errors == increasing_errors:
            new_reports = new_increasing(report)
        else:
            new_reports = new_decreasing(report)
    else:
        new_reports = new_values_in_range(report)
    for r in new_reports:
        if values_in_range_errors(r) == 0:
            return True
    return False

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
