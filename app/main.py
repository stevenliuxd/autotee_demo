import uvicorn
import util
import time
import re
import datetime
import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException as noelem
from selenium.common.exceptions import ElementNotInteractableException as elemnotinter
from typing import Optional
from fastapi import FastAPI, BackgroundTasks
from exceptions import InvalidDateException, DateTooFarException, UnknownException, TeeTimeException, CourseException

app = FastAPI()

def job_executor(request_info):

    try:
        tee_url = 'https:samplegolftee.com'
        
        # Load metadata
        date = request_info["Date"]
        teetime = request_info["Time"]
        course_num = request_info["Course"]
        players = request_info["Players"]
        holes = request_info["Holes"]
        taskid = request_info["TaskID"]
        requestor = request_info["User"]

        print(f'Begin job execution for Task: {taskid}.')

        # Load user name and password
        with open('users.json', 'r') as f:
            userdata = json.load(f)
        requestor = requestor.lower()
        email_temp = ''
        pswd = ''
        user_found = False
        name_list = userdata["data"]
        for user in name_list:
            if user["name"] == requestor:
                email_temp = user["username"]
                pswd = user["password"]
                user_found = True
        if user_found is False:
            print('User not found in db. Task will be terminated.')
            return ('Failed to execute job due to invalid user.')

        # Calculate countdown
        ttw = util.timedelta(date)
        print(f'Program sleeping for {ttw[0]} seconds. Request will begin login at {ttw[1]}.')
        if ttw[0] > 0:
            time.sleep(ttw[0])
        else:
            pass

        # Open browser instance
        web = util.dockerparam()
        web.get(tee_url)
        print('url obtained.')
        time.sleep(10)

        # Implement login feature
        web.find_element(By.XPATH, '//*[@id="SignInNavbarLarge"]/li[3]/a').click()
        print('Clicked sign in button.')
        time.sleep(5)

        web.find_element(By.XPATH, '//*[@id="Email"]').send_keys(f'{email_temp}')
        print('Entered email.')
        time.sleep(2)
        web.find_element(By.XPATH, '//*[@id="Password"]').send_keys(f'{pswd}')
        print('Entered password.')
        time.sleep(2)

        # Time check
        time_after_login = datetime.datetime.now()
        print(f'Login params finished at: {time_after_login.strftime("%H")}:{time_after_login.strftime("%M")}:{time_after_login.strftime("%S")}  ||  TaskID: {taskid}')

        # Wait until 6 am
        execute_form = util.timefinetune(date)
        if execute_form > 0:
            print(f'Now waiting until exactly 6:00:01 am to execute task. TaskID: {taskid}  ||  Time left (s): {execute_form}')
            time.sleep(execute_form)
        else:
            print(f'Time already surpassed 6am. Executing script now. TaskID: {taskid}  ||  Time passed (s): {execute_form}')

        web.find_element(By.XPATH, '//*[@id="frmLogOn"]/div/div[6]/div/a').click()
        time.sleep(1)

        # Time select
        try:
            web.find_element(By.XPATH, f"//*[@id='StartTimeDropDown']/option[text()='{teetime}']").click()
        except Exception as e:
            print('Login not succesful. Terminating...')
            error_time = datetime.datetime.now()
            error_msg = f'Error occured on month/day hr:min:sec: {error_time.strftime("%m")}/{error_time.strftime("%d")} {error_time.strftime("%H")}:{error_time.strftime("%M")}:{error_time.strftime("%S")}\nPossibly invalid user credentials!\n{e}\n'
            with open('crash_report.txt', 'a') as f:
                f.write(error_msg)
            with open('log.txt', 'a') as f:
                f.write(f'Job failed for task ID: {taskid}. Please consult crash logs.\n\n')
            return error_msg

        # Calendar select
        web.find_element(By.XPATH, '//*[@id="inpFromDate"]/span').click()
        all_dates = web.find_elements(By.XPATH, '//*[@id="inpFromDate"]/div/div[1]/table/tbody')
        date_element = all_dates[0]
        date_list = re.split(' |\n', date_element.text)
        x = 0
        y = 1
        for day in date_list:
            x += 1
            if x == 8:
                x = 1
                y += 1
            if int(day) == int(date[1]):
                try:
                    web.find_element(By.XPATH, f'//*[@id="inpFromDate"]/div/div[1]/table/tbody/tr[{y}]/td[{x}]').click()
                except noelem:
                    pass
        
        # Course Select
        web.find_element(By.XPATH, f'//*[@id="ddlCourse"]/option[{course_num}]').click()

        # Player Select
        p_num = 0
        if players == "Any":
            p_num = 5
        elif players == "1":
            p_num = 1
        elif players == "2":
            p_num = 2
        elif players == "3":
            p_num = 3
        elif players == "4":
            p_num = 4
        else:
            print("Defaulting to any players.")
            p_num = 5 
        web.find_element(By.XPATH, f'//*[@id="playerNumberGroup"]/button[{p_num}]').click()

        # Hole Select
        h_num = 0
        if holes == "9":
            h_num = 1
        elif holes == "18":
            h_num = 2
        else:
            h_num = 3
        web.find_element(By.XPATH, f'//*[@id="holeNumberGroup"]/button[{h_num}]').click()

        # Submission Time Check
        time_find_date = datetime.datetime.now()
        print(f'Time finder submitted at: {time_find_date.strftime("%H")}:{time_find_date.strftime("%M")}:{time_find_date.strftime("%S")}  ||  TaskID: {taskid}')

        # Submit to Website
        web.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
        time.sleep(1)
        print('Data submitted for tee times.')

        # Find the appropriate time
        time_found = False
        time_index = 6
        print('Begin time finder.')
        while time_found is False:
            try:
                print('Begin time finder 1.')
                web.find_element(By.XPATH, f'//*[@id="bodyContent"]/div[1]/div[{time_index}]/div/a/div/div/div[1]/h3').click()
                print('Begin time finde 2.')
                time_found = True
                time.sleep(6)
                web.find_element(By.XPATH, '//*[@id="divSelectPlayersAndHole"]/div[3]/button[2]').click()
                print('Begin time finder 3')
                time.sleep(2)
                web.find_element(By.XPATH, '//*[@id="term"]/div[3]/label').click()
                print('Begin time finder 4')
                time.sleep(1)
                web.find_element(By.XPATH, '//*[@id="btnBook"]').click()
                print('Begin time finder 5')
                time.sleep(1)
            except noelem or elemnotinter:
                print(f'Error selecting time... Trying the next one...')
                try:
                    web.find_element(By.CSS_SELECTOR, 'body > div.bootbox.modal.fade.in > div > div > div.modal-footer > button').click()
                    print('Time taken already.. skipping to next available time.')
                except noelem or elemnotinter:
                    pass
                time_found = False
                time_index = time_index - 1
                time.sleep(1)
                if time_index <= 0:
                    print(f'Background task for ID: {taskid} has failed due to no times being available.')
                    time.sleep(10)
                    web.close()

        success_msg = f'Succesfully Booked Task: {taskid} at {datetime.datetime.now().strftime("%m%d%H%M%S")}.\nRequestor: {requestor}\nDesired Timeframe: {date[0]}/{date[1]} at {teetime}'
        print(success_msg)

        with open('log.txt', 'a') as f:
            f.write(success_msg + '\n\n')

        time.sleep(20)
        web.close()

    except Exception as e:
        error_time = datetime.datetime.now()
        error_msg = f'Error occured on month/day hr:min:sec: {error_time.strftime("%m")}/{error_time.strftime("%d")} {error_time.strftime("%H")}:{error_time.strftime("%M")}:{error_time.strftime("%S")}\n{e}\n'
        with open('crash_report.txt', 'a') as f:
            f.write(error_msg)
        with open('log.txt', 'a') as f:
            f.write(f'Job failed for task ID: {taskid}. Please consult crash logs.\n\n')


@app.get("/autotee/register",
    tags=["Autotee"],
    summary="Request for specific tee times",
)
async def request_tee_time(
    User: str,
    Date: str,
    Time: Optional[str] = 'Afternoon',
    Course: Optional[str] = 'Lakeview',
    Players: Optional[str] = 'Any',
    Holes: Optional[str] = 'Any',
    background_tasks: BackgroundTasks = None,
):
    print('Autotee release v1.0.6')

    try:
        date = util.date(Date)
        teetime = util.teetime(Time)
        course =  util.course(Course)
    except InvalidDateException:
        return InvalidDateException(message="please verify that the date is entered correctly.")
    except DateTooFarException:
        return DateTooFarException(message="please verify the desired date is within 7 days from today.")
    except TeeTimeException:
        return TeeTimeException(message="Please double check the desired tee time.")
    except CourseException:
        return CourseException(message="Please enter a valid Public YYC course.")
    except Exception:
        return UnknownException(message="Unknown error.")

    gen_task_id = datetime.datetime.now().strftime("%m%d%H%M%S")
    request_info = {"Date": date, "Time": teetime, "Course": course, "Players": Players, "Holes": Holes, "TaskID": gen_task_id, "User": User}
    background_tasks.add_task(job_executor, request_info)

    return_resp = {
        "Task ID": gen_task_id,
        "Task Details": f"Request for {date[0]}-{date[1]}-{date[2]} @{teetime} at course #{course} with {Players} players and {Holes} holes."
    }

    with open('log.txt', 'a') as f:
            f.write(f'Created task ID: {gen_task_id}\n\n')

    return return_resp

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")