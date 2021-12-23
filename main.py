import sys
import os
from azure.storage.blob import BlobServiceClient, BlobProperties
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
from datetime import datetime, date, timedelta
import cv2
import numpy as np
import os
from timelapse_photo import TimelapsePhoto

def daterange(startDate: date, endDate: date):
    for n in range(int ((endDate - startDate).days)+1):
        yield startDate + timedelta(n)

def main() -> None:
    account_url = "https://{}.blob.core.windows.net".format(
        os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    )
    shared_access_key = os.getenv('AZURE_STORAGE_SHARED_ACCESS_KEY')
    container = os.getenv('AZURE_STORAGE_CONTAINER')

    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=shared_access_key)
    container_client = blob_service_client.get_container_client(container)

    blobs = []

    grow_start_date = date(2021, 12, 11)

    end_dt = date.today()
    # end_dt = date(2021, 12, 11) + timedelta(days=7)
    # end_dt = date(2021, 12, 13) + timedelta(days=3)
    # start_dt = end_dt - timedelta(days=7)
    start_dt = grow_start_date
    # start_dt = end_dt - timedelta(days=3)

    skip_from_hour = 22
    skip_to_hour = 7

    for dt in daterange(start_dt, end_dt):
        dayPrefix = dt.strftime("%Y-%m-%d")
        print("Prefix: ", dayPrefix)

        try:
            for blob in container_client.list_blobs(name_starts_with=dayPrefix):
                print("Found blob: ", blob.name)
                if blob.name is None:
                    continue

                blobs.append(TimelapsePhoto(blob.name))
        except ResourceNotFoundError:
            print("Container not found.")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # fourcc = cv2.VideoWriter_fourcc(*'h264')
    out = cv2.VideoWriter("output.mp4", fourcc, 23.0, (1920, 1439))
    
    blobs.sort(key=lambda x: x.datetime, reverse=False)

    for blob in blobs:

        if blob.datetime.hour > skip_from_hour or blob.datetime.hour < skip_to_hour:
            print("Skip blob in hour ", blob.datetime.hour)
            continue

        print("Downloading ", blob.name)
        blob_client = container_client.get_blob_client(blob.name)
        download_stream = blob_client.download_blob()

        # Save image to disk
        # filepath = f"./files/{blob.name}"
        # os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # with open(filepath, 'wb') as fp:
        #     fp.write(download_stream.content_as_bytes())

        print("Adding to frame...")

        image = np.asarray(bytearray(download_stream.content_as_bytes()))
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
        resized = cv2.resize(frame, (1920, 1439))

        BLACK = (255,255,255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1.1
        font_color = BLACK
        font_thickness = 2
        text = f"Tag {str((blob.datetime.date() - grow_start_date).days).rjust(4)} ({blob.datetime.strftime('%H:%M:%S: %d.%m.%Y')})"
        x,y = 1250,1400
        frame_with_text = cv2.putText(resized, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

        print("Write frame...")

        out.write(frame_with_text) # Write out frame to video

    # Release everything if job is finished
    out.release()

if __name__ == '__main__':
    sys.exit(main())
