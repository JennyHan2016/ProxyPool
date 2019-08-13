from proxypool.scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    try:
        s = Scheduler() # 调度器
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
