from airflow import DAG
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import psycopg2

def check_new_images():
    # Postgres
    conn = psycopg2.connect(
        dbname="airflow",
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor()

    # Lấy số ảnh hiện tại trong bảng
    cursor.execute("SELECT COUNT(*) FROM images")
    current_count = cursor.fetchone()[0]
    conn.close()

    # Đọc số lượng ảnh cũ từ file
    try:
        with open('/opt/airflow/last_image_count.txt', 'r') as f:
            last_count = int(f.read())
    except FileNotFoundError:
        last_count = 0

    # Ghi log ra UI
    print(f"Last count: {last_count}, Current count: {current_count}")

    # So sánh
    if current_count > last_count:
        with open('/opt/airflow/last_image_count.txt', 'w') as f:
            f.write(str(current_count))
        return True
    return False

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='retrain_yolo_on_new_images',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    check_images = ShortCircuitOperator(
        task_id='check_new_images',
        python_callable=check_new_images,
    )

    retrain_model = BashOperator(
        task_id='retrain_model_task',
        bash_command='bash /opt/airflow/scripts/retrain_model.sh',
    )

    check_images >> retrain_model
