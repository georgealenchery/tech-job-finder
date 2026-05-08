from database import init_db, get_all_jobs, update_job_status

if __name__ == "__main__":
    init_db()

    update_job_status(1, "Applied", "Applied via company website")

    jobs = get_all_jobs()
    for job in jobs[:3]:
        print(job)