import os

sizes = ["1KB", "4KB", "1MB", "10MB", "100MB"]

stats = {
    "get": {
        "1KB": [],
        "4KB": [],
        "1MB": [],
        "10MB": [],
        "100MB": []
    },
    "set": {
        "1KB": [],
        "4KB": [],
        "1MB": [],
        "10MB": [],
        "100MB": []
    }
}

if __name__ == '__main__':
    for op in ["get", "set"]:
        for size in sizes:
            filename = "results/{}_{}".format(op, size)
            with open(filename, "r") as f:
                for line in f:
                    stats[op][size].append(float(line.strip()))

    with open("results/summary", "w") as f:
        for get_1KB, get_4KB, get_1MB, get_10MB, get_100MB, set_1KB, set_4KB, set_1MB, set_10MB, set_100MB in zip(
                stats["get"]["1KB"], stats["get"]["4KB"], stats["get"]["1MB"], stats["get"]["10MB"],
                stats["get"]["100MB"],
                stats["set"]["1KB"], stats["set"]["4KB"], stats["set"]["1MB"], stats["set"]["10MB"],
                stats["set"]["100MB"]):
            f.write("{},{},{},{},{}, , ,{},{},{},{},{}\n".format(get_1KB, get_4KB, get_1MB, get_10MB, get_100MB,
                                                                 set_1KB, set_4KB, set_1MB, set_10MB, set_100MB))
