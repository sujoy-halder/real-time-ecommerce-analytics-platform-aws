from __future__ import annotations

import json
import time

from app.config import ProducerConfig
from app.generator import generate_batch
from app.kinesis_client import KinesisPublisher


def run() -> None:
    config = ProducerConfig.from_env()
    publisher = KinesisPublisher(config)

    while True:
        events = generate_batch(config.batch_size)
        response = publisher.publish_batch(events)
        failed = response.get("FailedRecordCount", 0)
        print(
            json.dumps(
                {
                    "message": "published_batch",
                    "stream": config.stream_name,
                    "records": len(events),
                    "failed_records": failed,
                }
            ),
            flush=True,
        )

        if config.mode == "once":
            break
        time.sleep(config.interval_seconds)


if __name__ == "__main__":
    run()

