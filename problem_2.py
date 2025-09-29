import random
import math

def exponential(mean):
    """Generate an exponentially distributed random variable."""
    return -mean * math.log(1 - random.random())

def simulate_servers(years=20, mtbf=500, restore_time=50):
    total_hours = years * 365 * 24
    events = {"server1": [], "server2": []}
    times = [0, 0]  # Current time for each server

    for server in range(2):
        t = 0
        while t < total_hours:
            uptime = exponential(mtbf)
            fail_time = t + uptime
            restore_end = fail_time + restore_time
            if fail_time < total_hours:
                events[f"server{server+1}"].append((round(fail_time, 2), "fail"))
            t = restore_end
        
    return events

def simulate_system_lifetime(mtbf=500, restore_time=10):
    t1 = exponential(mtbf)
    t2 = exponential(mtbf)
    current_time = 0
    while True:
        if t1 < t2:
            fail_time = t1
            if t2 <= fail_time + restore_time:
                return t2
            else:
                current_time = fail_time + restore_time
                t1 = current_time + exponential(mtbf)
        else:
            fail_time = t2
            if t1 <= fail_time + restore_time:
                return t1
            else:
                current_time = fail_time + restore_time
                t2 = current_time + exponential(mtbf)


def system_failure_times(trials=50, mtbf=500,restore_time=10):
    #fail_times = []
    results = []
    for _ in range(trials):
        #t1, t2 = 0, 0
        #while True:
            # uptime1 = exponential(mtbf); uptime2 = exponential(mtbf)
            # t1 += uptime1; t2 += uptime2
            # if(abs(t1-t2)) < restore_time:
            #     fail_times.append(min(t1,t2))
            #     break
            # t1 += restore_time; t2 += restore_time
        lifetime = simulate_system_lifetime(mtbf, restore_time)
        results.append(lifetime)
    #return sum(fail_times)/len(fail_times)
    return sum(results)/len(results)

if __name__ == "__main__":
    random.seed(42)

    events = simulate_servers()
    print("Server1 failures:", events["server1"][:5], "...")
    print("Server2 failures:", events["server2"][:5], "...")

    avg_failure_time = system_failure_times()
    print("\nExpected system failure time:", round(avg_failure_time, 2), "hours")
    print("In years:", round(avg_failure_time/(24*365), 2), "years")
    