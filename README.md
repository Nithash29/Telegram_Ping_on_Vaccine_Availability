# CoWIN vaccination slot availability and send automated ping to Telgram channel/group using Python
Script to check the available slots for Covid-19 Vaccination Centers for age group 18-44 from CoWIN API (https://apisetu.gov.in/public/marketplace/api/cowin) in India. Slots of both Dose 1 and Dose 2 are checked for a duration of 4 days and then a text message is sent to a telegram channel/group.

## Contents of the repository
- Clone the repository or download the zip file. If you have downloaded the zip file, extract it.
- `CoWIN_Vaccine_Avail_Telegram.ipynb` - main python script to generate the districtwise vaccine slot availability and send a telegram message.
- `requirements.txt` - librabries required to run the python file.
- `state_id_mapping_generation.ipynb` - python script to generate the state id and its corresponding state name list.
- `State_ID_Mapping.csv` - state to id mapping excel generated after running `state_id_mapping_generation.ipynb`.
- `Update_Overview` - output of the main script.

## Recommended Method: Anaconda
The Anaconda is an easily-installable bundle of Python and many of the libraries used throughout this class.
The script is written in python notebook (.ipynb). So, we recommend Anaconda's Jupyter Notebook for the run. If you wish to use any other software, feel free to do so.

### Anaconda Installation
1. Download the Anaconda from (https://www.anaconda.com/products/individual)
2. Follow the instructions on the above page to run the installer.
3. Check for python version: Start the `Anaconda Prompt` terminal, which you can find in the Start menu. On the Terminal type `python --version`, which outputs the version number. Kindly check python version is above 3.8.0.
4. Check whether Jupyter notebook is opening: Start the `Anaconda Prompt` terminal. Type `jupyter notebook`. A new browser window should open. 

## How to run the code
- Open the `Anaconda Prompt` terminal.
- Enter the command `cd !!location of the dowloaded/cloned file!!`. 
  As an example the command should look like this- `cd C:\Users\user_name\Downloads\Telegram_message_on_vaccine_availability`
- Install all the dependencies - `pip install -r requirements.txt`
- Make changes into the main pyhton script before running. Check "Code Change Info" section for the same.
- Run the main script - `python CoWIN_Vaccine_Avail_Telegram.py`

## Code Change Info
- For sections where there is such link 'https://api.telegram.org/your_generated_bot_token/sendMessage?chat_id=your_chat_id&text="Your Message"' (basically line no. 236 and 240) check this link `https://www.youtube.com/watch?v=ps1yeWwd6iA&t=256s` to learn how to generate the `bot_token` and `chat_id`.

## Additional info
- You can automate this task through `Task Scheduler`(available in Windows) to run after fixed intervals. However, this process is subject to your host system to be up and connected to internet. 
