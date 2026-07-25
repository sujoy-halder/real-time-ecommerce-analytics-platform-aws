from __future__ import annotations

import unittest
from unittest.mock import patch

from app.config import ProducerConfig


class ProducerConfigTests(unittest.TestCase):
    def test_reads_local_stream_creation_settings(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "KINESIS_STREAM_NAME": "test-stream",
                "AWS_ENDPOINT_URL": "",
                "AUTO_CREATE_STREAM": "true",
                "KINESIS_SHARD_COUNT": "3",
            },
        ):
            config = ProducerConfig.from_env()

        self.assertEqual(config.stream_name, "test-stream")
        self.assertIsNone(config.aws_endpoint_url)
        self.assertTrue(config.auto_create_stream)
        self.assertEqual(config.stream_shard_count, 3)


if __name__ == "__main__":
    unittest.main()
