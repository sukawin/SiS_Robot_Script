import os
import time
from datetime import datetime
from datetime import timedelta
#from azure.storage.blob import BlobServiceClient
from robot import run
import zipfile

download_path = r"C:\Users\sukawin\Downloads"
sale_des_path = r"C:\Users\sukawin\SIS DISTRIBUTION (THAILAND) PUBLIC COMPANY LIMITED\OFM Project - Documents\General\HomePro_Sales\Automate"
stock_des_path = r"C:\Users\sukawin\SIS DISTRIBUTION (THAILAND) PUBLIC COMPANY LIMITED\OFM Project - Documents\General\HomePro_Stock\Automate"
stockpivot_des_path = r"C:\Users\sukawin\SIS DISTRIBUTION (THAILAND) PUBLIC COMPANY LIMITED\OFM Project - Documents\General\HomePro_Stock\Automate\pivot"
robot_script = r"C:\Users\sukawin\OneDrive - SIS DISTRIBUTION (THAILAND) PUBLIC COMPANY LIMITED\Documents\GitHub\SiS_Robot_Script\hp_robot_script.robot"

def execute_robot_script(robot_script):
    run(robot_script)

def extract_zip(zip_file_path, extract_to_path):
  try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
      zip_ref.extractall(extract_to_path)
    print(f"Successfully extracted '{zip_file_path}' to '{extract_to_path}'")
  except FileNotFoundError:
    print(f"Error: ZIP file not found at '{zip_file_path}'")
  except zipfile.BadZipFile:
    print(f"Error: Invalid ZIP file at '{zip_file_path}'")
  except Exception as e:
    print(f"An error occurred during extraction: {e}")

def main():
    today = datetime.today()
    suffix = (today  - timedelta(days=1)).strftime('%Y%m%d')

    execute_robot_script(robot_script)

    files_list = os.listdir(download_path)

    HP_dailyfile_list = [file for file in files_list if "VRM" in file]

    stock_originalName = "VRM_0000003096_InventoryData_"+suffix+".csv"

    for file in HP_dailyfile_list:
        file_path = os.path.join(download_path,file)
        if 'Sale' in file:
            os.rename(file_path,os.path.join(sale_des_path,"HomePro_Sale_"+suffix+".csv"))
        elif 'InventoryData' and '(1)'in file:
            extract_zip(file_path,stockpivot_des_path)
            os.rename(os.path.join(stockpivot_des_path,stock_originalName),os.path.join(stockpivot_des_path,"HomePro_Sale_"+suffix+"_pivot.csv"))
            os.remove(file_path)
        elif 'InventoryData' in file:
            extract_zip(file_path,stock_des_path)
            os.rename(os.path.join(stock_des_path,stock_originalName),os.path.join(stock_des_path,"HomePro_Sale_"+suffix+".csv"))
            os.remove(file_path)
def is_target_daytime():
    target_day = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    if datetime.today().strftime("%A") in target_day:
        if 8 <= datetime.today().hour <= 18:
            return 1
        else:
            return 0
    else:
        return 0
    
def seconds_till_next_9am():
    bangkok_tz = pytz.timezone('Asia/Bangkok')
    now_local = datetime.now(bangkok_tz)
    today_9am = now_local.replace(hour=9, minute=0, second=0, microsecond=0)

    if now_local < today_9am:
        target_time = today_9am
    else:
        next_day = now_local + timedelta(days=1)
        target_time = next_day.replace(hour=9, minute=0, second=0, microsecond=0)

    seconds_left = ((target_time - now_local).total_seconds())
    print(f"Hours left until the next 9:00 AM (Bangkok time): {(seconds_left/3600):.0f}")
    return int(seconds_left)

if __name__ == "__main__":
    while True:
        if is_target_daytime():
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Current date and time: {current_datetime}')
            main()
            print('Waiting till next day 9AM...')
            time.sleep(seconds_till_next_9am())
        else:
            time.sleep (60)