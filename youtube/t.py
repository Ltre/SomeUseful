import sys,time
import tracemalloc
tracemalloc.start()
while 1:
    with open('youtube_names.txt','a+') as f:
        f.seek(0)
        sys.stdout.write('%d ' % len(f.read().splitlines()))
    sys.stdout.flush()
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("\n[ Top 10 ]")
    for stat in top_stats[:10]:
            print(stat)
    time.sleep(1)
