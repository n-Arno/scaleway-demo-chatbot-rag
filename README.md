scaleway-demo-chatbot-rag
=========================

Simple demo of a Chatbot based on Kapsule + L40s + Ollama (LLM and embedding).

RAG is done leveraging a Scaleway Managed PostgreSQL database with pgvector extension.

Setup
-----

1) **Deploy infrastructure using terraform**


```
terraform init && terraform apply -auto-approve
```

Needed environment variables:

```
SCW_ACCESS_KEY
SCW_SECRET_KEY
SCW_DEFAULT_ORGANIZATION_ID
SCW_DEFAULT_PROJECT_ID
```

NB: the infrastructure will be deployed on FR-PAR/FR-PAR-2

Sample output:

```
Outputs:

lb_ip             = "X.X.X.X"
database_ip       = "Y.Y.Y.Y"
database_password = "ZZZZZZZ"
```

2) **Collect resulting IP address for LB and create a DNS entry**

Example using Scaleway CLI and a Scaleway Managed DNS:

```
scw dns record add my-domain.fr type=A name=chatbot data=X.X.X.X ttl=60
```

3) **Add LB IP and DNS entry in deployment**

Edit `deploy.yaml` and insert the value for the LB IP and DNS entry:

```
(...)
        command:
        - caddy
        args:
        - reverse-proxy
        - -f
        - <your-dns-entry>:443
        - -t
        - chatbot:8080
(...)
  - name: https
    port: 443
    protocol: TCP
    targetPort: 443
  loadBalancerIP: <your-lb-ip>
  selector:
    app: caddy
(...)
```

4) **Create an Object Storage bucket and upload documents for RAG**

Create an Object Storage bucket, upload documents at the root of the bucket (no prefix) and create the associated API Key.

The type of document readable is found [here](https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/#supported-file-types).

5) **Add credentials in the deployment**

Edit `deploy.yaml` and insert DB internal IP and password, together with the Object Storage access information:

```
(...)
apiVersion: v1
kind: Secret
metadata:
  labels:
    app: chatbot
  name: chatbot
stringData:
  S3_ACCESS_KEY: "<scw api access key>"
  S3_SECRET_KEY: "<scw api secret key>"
  S3_ENDPOINT: "https://s3.fr-par.scw.cloud"
  S3_REGION: "fr-par"
  S3_BUCKET: "<bucket-name>"
  DB_CFG: "postgres://vector:<db password>@<db internal ip>:5432/vector"
(...)
```

6) **Deploy the chatbot in Kapsule**

We will use the created `kubeconfig.yaml` file to access the cluster, but you can also use the console to generate this file. 

On linux or Mac OSX
```
export KUBECONFIG=kubeconfig.yaml
```

On windows
```
set KUBECONFIG=kubeconfig.yaml
```

Deploy Ollama instance:

```
kubectl apply -f ollama.yaml
```

Deploy the chat bot:

```
kubectl apply -f deploy.yaml
```

Ingestion of new documents
--------------------------

To trigger re-ingestion, navigate to `https://<your-dns-entry>:443/api/docs` and trigger `/ingest`

Credits
-------

The initial code is built via [create-llama](https://www.npmjs.com/package/create-llama). The frontend part is available in the folder `frontend` but has been compiled as a static JS+HTML and integrated in the FastAPI chatbot via root mount.
