from model_mommy import mommy
from unittest.mock import patch, Mock

from django.test import TestCase

from src.core import tasks
from src.core.models import AnalysedImage
from proj_utils.redis import RedisAsyncClient


class AnalysedImageModelTests(TestCase):

    def setUp(self):
        self.analysed_image = mommy.make(
            AnalysedImage,
            recokgnition_result={'fake': 'data'},
            ibm_watson_result={'fake': 'data'},
        )

    @patch.object(RedisAsyncClient, 'enqueue_default', Mock(id=42))
    def test_do_not_enqueue_if_data(self):
        client = RedisAsyncClient()

        self.analysed_image.enqueue_analysis()

        assert client.enqueue_default.called is False

    @patch.object(RedisAsyncClient, 'enqueue_default', Mock(id=42))
    def test_enqueue_aws_analysis(self):
        self.analysed_image.recokgnition_result = {}
        self.analysed_image.save()
        client = RedisAsyncClient()

        self.analysed_image.enqueue_analysis()
        self.analysed_image.refresh_from_db()

        client.enqueue_default.assert_called_once_with(
            tasks.aws_analyse_image_task, self.analysed_image.id
        )
        self.analysed_image.recokgnition_job_id = '42'

    @patch.object(RedisAsyncClient, 'enqueue_default', Mock(id=42))
    def test_enqueue_ibm_analysis(self):
        self.analysed_image.ibm_watson_result = {}
        self.analysed_image.save()
        client = RedisAsyncClient()

        self.analysed_image.enqueue_analysis()
        self.analysed_image.refresh_from_db()

        client.enqueue_default.assert_called_once_with(
            tasks.ibm_analyse_image_task, self.analysed_image.id
        )
        self.analysed_image.ibm_watson_job_id = '42'
