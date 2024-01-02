import time


def s_to_size(size_s: str):
    if size_s == "4KB":
        return 4 * 1024
    elif size_s == "1MB":
        return 1024 * 1024
    elif size_s == "10MB":
        return 10 * 1024 * 1024
    elif size_s == "100MB":
        return 100 * 1024 * 1024
    else:
        return 1024


def set_date(client, data: bytes, size_s: str):
    start_time = time.time()
    client.set("data_%s" % size_s, data)
    set_use_time = (time.time() - start_time) * 1000
    print("Set {} data use time: {:.3f} ms".format(size_s, set_use_time))
    with open(f"results/set_{size_s}", "a") as f:
        f.write("{:.3f}\n".format(set_use_time))


def get_date(client, size_s: str):
    start_time = time.time()
    result = client.get("data_%s" % size_s)
    get_use_time = (time.time() - start_time) * 1000
    print("Get {} data use time: {:.3f} ms".format(size_s, get_use_time))
    with open(f"results/get_{size_s}", "a") as f:
        f.write("{:.3f}\n".format(get_use_time))
    return result
