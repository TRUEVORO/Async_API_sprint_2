#!/bin/sh

echo "Waiting for Elasticsearch to start..."
until curl -s "${ELASTICSEARCH_DSN}/_cat/health?h=status" | grep -E -q "(yellow|green)"; do
  sleep 2
done

echo "Elasticsearch started."

cd src || exit

gunicorn -c gunicorn/gunicorn.py main:app
