import os, warnings, psycopg2, shutil
from llama_index.core import StorageContext, SimpleDirectoryReader, VectorStoreIndex
from app.settings import get_vector_store, get_boto3_client


def db_init():
    dsn = os.getenv("DB_CFG")

    # Register extension
    with psycopg2.connect(dsn=dsn) as conn:
        try:
            cur = conn.cursor()
            cur.execute("CREATE EXTENSION vector;")
        except psycopg2.errors.DuplicateObject:
            pass

    # Clean data
    with psycopg2.connect(dsn=dsn) as conn:
        try:
            cur = conn.cursor()
            cur.execute("DROP TABLE data_chatbot;")
        except psycopg2.errors.UndefinedTable:
            pass


def do_ingest():
    # Avoid ugly warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    # prepare database
    db_init()

    # get config
    vector_store = get_vector_store()
    b3_client = get_boto3_client()
    bucket = os.getenv("S3_BUCKET")

    # clean target folder
    shutil.rmtree("./data", ignore_errors=True)
    os.mkdir("./data")

    # download files
    keys = [k["Key"] for k in b3_client.list_objects_v2(Bucket=bucket)["Contents"]]
    for key in keys:
        print(f"Downloading {key}")
        b3_client.download_file(Bucket=bucket, Key=key, Filename=f"./data/{key}")

    # ingest folder
    documents = SimpleDirectoryReader("./data").load_data()

    print(f"Indexing...")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
