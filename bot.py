"""
This is a echo bot.
It echoes any incoming text messages.
"""
import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher, executor, types
from requests.adapters import Retry, HTTPAdapter

API_TOKEN = '5418879472:AAH1p7D5vJTW7NLTUF0zcOFDXYfipDrxFx4'

ses = requests.Session()
retries = Retry(total=10,
                backoff_factor=0.1)
ses.mount('https://', HTTPAdapter(max_retries=retries))
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',)
logger = logging.getLogger("bot")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

token = "Bearer glpat-T7jMoBNBiVFF8Dg2Wa7x"


def get_merge_request(merge_request_id):
    response = ses.get(f'https://gitlab.litebox.ru/api/v4/projects/53/merge_requests/{merge_request_id}',
                            headers={"Authorization": token})
    return response.json()


def get_pipeline_jobs(pipeline_id):
    response = ses.get(f'https://gitlab.litebox.ru/api/v4/projects/53/pipelines/{pipeline_id}/jobs',
                            headers={"Authorization": token})
    return response.json()


def retry_job(job_id):
    response = ses.post(f'https://gitlab.litebox.ru/api/v4/projects/53/jobs/{job_id}/retry',
                             headers={"Authorization": token})
    return response.json()


def get_job(job_id):
    response = ses.get(f'https://gitlab.litebox.ru/api/v4/projects/53/jobs/{job_id}',
                            headers={"Authorization": token})
    return response.json()


async def check_pipeline(mr_id):
    while True:
        mr = get_merge_request(mr_id)
        pipeline_id = mr.get('head_pipeline').get('id')
        jobs = get_pipeline_jobs(pipeline_id)
        failed_e2e_id = None
        build_e2e_id = None
        e2e_id = None
        for job in jobs:
            if job['status'] == 'failed' and job['name'] == 'test:e2eTestDevelop':
                failed_e2e_id = job['id']
            elif job['name'] == 'build:e2eDevelopTests':
                build_e2e_id = job['id']
        if failed_e2e_id:
            retry_job(build_e2e_id)
            logger.info(f"Restarting the build e2e {build_e2e_id}")
            await asyncio.sleep(7)

            for job in get_pipeline_jobs(pipeline_id):
                if job['name'] == 'build:e2eDevelopTests':
                    build_e2e_id = job['id']
            while get_job(build_e2e_id)['status'] != 'success':
                await asyncio.sleep(30)
            retry_job(failed_e2e_id)
            logger.info(f"Restarting e2e {failed_e2e_id}")

        for job in get_pipeline_jobs(pipeline_id):
            if job['name'] == 'test:e2eTestDevelop':
                e2e_id = job['id']
        await asyncio.sleep(60)
        logger.info(f"Check status e2e {e2e_id}")
        if get_job(e2e_id)['status'] == 'success':
            break


@dp.message_handler(commands=['mr'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    mr_id = int(message.text.split(" ")[1])
    logger.info(f"New MR {mr_id}")
    await message.answer(f"Начал отслеживать МР {mr_id}")
    await check_pipeline(mr_id)
    await message.answer(f"e2e успешно прошли в МРе {mr_id}")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    mr_id = int(message.text)
    logger.info(f"New MR {mr_id}")
    await message.answer(f"Начал отслеживать МР {mr_id}")
    await check_pipeline(mr_id)
    await message.answer(f"e2e успешно прошли в МРе {mr_id}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
