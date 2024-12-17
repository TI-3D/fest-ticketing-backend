from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.config import Logger
import datetime
from app.dependencies.database import get_db
from app.models import Event, EventStatus
from sqlalchemy.future import select

# Initialize the scheduler
scheduler = AsyncIOScheduler()

# Initialize the logger
logger = Logger(__name__).get_logger()

# Contoh task yang akan dijalankan setiap waktu tertentu
async def my_cron_job():
    logger.info(f"Running cron job at {datetime.datetime.now()}")
    async for session in get_db():  # Use async for to get the session
        try:
            logger.info("Attempting to retrieve all events with status 'PENDING'")
            # Menggunakan ORM untuk mengambil event dengan status 'PENDING'
            query = select(Event).where(Event.status == EventStatus.PENDING).order_by(Event.updated_at.desc())
            result = await session.execute(query)
            events = result.scalars().all()
            
            # update status event yang sudah lewat waktu
            for event in events:
                if event.updated_at < datetime.datetime.now() - datetime.timedelta(minutes=30):
                    event.status = EventStatus.CANCELLED
                    await session.commit()
                    logger.info(f"Event {event.event_id} has been cancelled")
                else:
                    logger.info(f"Event {event.event_id} is still pending")
                    
        except Exception as e:
            logger.error(f"Error retrieving events: {str(e)}")

# Fungsi untuk mengatur dan memulai scheduler
def start_scheduler():
    # Cron trigger: Menjalankan setiap 10 detik
    logger.info("Starting scheduler...")
    scheduler.add_job(my_cron_job, CronTrigger(minute="*/1"))
    scheduler.start()

# Fungsi untuk menghentikan scheduler saat aplikasi shutdown
def shutdown_scheduler():
    logger.info("Shutting down scheduler...")
    scheduler.shutdown()