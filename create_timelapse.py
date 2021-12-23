# import sys
# import os
# from azure.storage import blob
# from azure.storage.blob import BlobServiceClient, BlobProperties
# from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
# from datetime import datetime, date, timedelta
# import cv2
# import numpy as np
# import os
# from timelapse_photo import TimelapsePhoto

# def main():
#     grow_start_date = date(2021, 12, 11)
#     blobs = []

#     for photo in os.listdir("./files"):
#         blobs.append(TimelapsePhoto(photo))

#     blobs.sort(key=lambda x: x.datetime, reverse=False)

#     # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     fourcc = cv2.VideoWriter_fourcc(*'H264')
#     # fourcc = cv2.VideoWriter_fourcc(*'HEVC')
#     out = cv2.VideoWriter("output_test.mp4", fourcc, 23.0, (1920, 1439))

#     for blob in blobs:
#         # print("Adding to frame...")

#         frame = cv2.imread(f"./files/{blob.name}")
#         resized = cv2.resize(frame, (1920, 1439))

#         BLACK = (255,255,255)
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         font_size = 1.1
#         font_color = BLACK
#         font_thickness = 2
#         text = f"Tag {str((blob.datetime.date() - grow_start_date).days).rjust(4)} ({blob.datetime.strftime('%H:%M:%S: %d.%m.%Y')})"
#         x,y = 1250,1400
#         frame_with_text = cv2.putText(resized, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

#         # print("Write frame...")

#         out.write(frame_with_text) # Write out frame to video

#     # Release everything if job is finished
#     out.release()
#     print("Done!")


# if __name__ == '__main__':
#     sys.exit(main())