import schedule
import time


def job():
  print('Ngoding time...')


schedule.every(10).seconds.do(job)