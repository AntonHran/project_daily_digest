import threading
import time
import schedule


class DailyDigestScheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        self.__stop_running = threading.Event()

    # Schedule a task to repeat at the same time every day
    @staticmethod
    def schedule_daily(hour, minute, second, job):
        schedule.clear()
        schedule.every().day.at(f'{hour:02}:{minute:02}:{second:02}').do(job)

    # start a scheduler as a background thread
    def run(self):
        self.__stop_running.clear()
        while not self.__stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    # stop the scheduler thread
    def stop(self):
        self.__stop_running.set()


if __name__ == '__main__':

    '''import dd_email
    email_ = dd_email.DailyDigestEmail()

    scheduler = DailyDigestScheduler()
    scheduler.start()

    h = time.localtime().tm_hour
    # print(h, type(h))
    m = time.localtime().tm_min + 1
    s = 0
    print(f'Scheduling test email for {h:02}:{m:02}:{s:02}')
    scheduler.schedule_daily(h, m, s, email_.handle_email_type)

    time.sleep(60)
    scheduler.stop()'''
