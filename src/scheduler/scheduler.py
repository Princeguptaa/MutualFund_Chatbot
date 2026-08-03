import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from src.scheduler.jobs.audit_sample_gen import generate_audit_sample
from src.scheduler.jobs.url_health_check import check_url_health
from src.scheduler.jobs.stale_data_sweep import sweep_stale_data
from src.scheduler.jobs.analytics_aggregate import aggregate_analytics
from src.scheduler.jobs.corpus_reingestion import reingest_corpus
import atexit

def start_scheduler():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, "data", "scheduler_jobs.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    jobstores = {
        'default': SQLAlchemyJobStore(url=f'sqlite:///{db_path}')
    }
    executors = {
        'default': ThreadPoolExecutor(3)
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 3600
    }
    
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    
    # Register jobs
    # 1. URL Health check (Weekly - Sun 02:00)
    scheduler.add_job(check_url_health, 'cron', day_of_week='sun', hour=2, id='health_check', replace_existing=True)
    # 2. Corpus Reingestion (Weekly - Mon 03:00)
    scheduler.add_job(reingest_corpus, 'cron', day_of_week='mon', hour=3, id='reingestion', replace_existing=True)
    # 3. Audit Sample Gen (Weekly - Mon 06:00)
    scheduler.add_job(generate_audit_sample, 'cron', day_of_week='mon', hour=6, id='audit_gen', replace_existing=True)
    # 4. Stale Data Sweep (Daily - 01:00)
    scheduler.add_job(sweep_stale_data, 'cron', hour=1, id='stale_sweep', replace_existing=True)
    # 5. Analytics Aggregate (Daily - 00:30)
    scheduler.add_job(aggregate_analytics, 'cron', hour=0, minute=30, id='analytics_agg', replace_existing=True)
    
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown(wait=False))
    return scheduler
