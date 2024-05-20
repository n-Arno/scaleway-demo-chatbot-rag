import os, warnings
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from app.settings import get_storage_context, get_boto3_client

def do_ingest():
    # Avoid deprecation warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    storage_context = get_storage_context()
    b3_client = get_boto3_client()
    bucket = os.getenv("S3_BUCKET")

    # Get root prefixes as contexts
    contexts = [p["Prefix"] for p in b3_client.list_objects_v2(Bucket=bucket, Prefix="", Delimiter="/")["CommonPrefixes"]]

    print(f"I found those prefixes: {contexts}")

    # for each root prefixes
    for prefix in contexts:
        print(f"Handling context {prefix}")
        # create folder
        try:
            os.mkdir(f"./{prefix}")
        except FileExistsError:
            pass

        # download files
        keys = [k["Key"] for k in b3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, StartAfter=prefix)["Contents"]]
        for key in keys:
            print(f"Downloading {key}")
            b3_client.download_file(Bucket=cfg.bucket, Key=key, Filename=f"./{key}")

        # ingest folder
        print(f"Reading all documents from ./{prefix[:-1]}")
        documents = SimpleDirectoryReader(f"./{prefix[:-1]}").load_data()

        print(f"Indexing...")
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )
