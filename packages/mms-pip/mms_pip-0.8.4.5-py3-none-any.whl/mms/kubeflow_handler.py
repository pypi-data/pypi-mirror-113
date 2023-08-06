from kfp.v2 import components

from google.cloud import storage


class KubeFlowHandler(object):

    def __init__(self):
        self.storage_client = storage.Client()

    def load_kfp_component(self, filename: str, bucket_id: str = 'tadd-kubeflow-components') -> components:

        bucket = self.storage_client.get_bucket(bucket_id)

        blob = bucket.blob(filename)
        blob = blob.download_as_string()
        blob = blob.decode('utf-8')

        blob_string = str(blob)

        return components.load_component_from_text("""{}""".format(blob_string))


if __name__ == '__main__':


    kf = KubeFlowHandler()


    component = kf.load_kfp_component('tadd-kubeflow-components', 'test/component.yaml')


    print("test")











