# Wildlife Conservation Detection System

This repository contains a Wildlife Conservation Detection System that utilizes machine learning techniques to detect animals, people, and potential intruders in a wildlife sanctuary. The system is designed to enhance the conservation efforts by monitoring wildlife activities and ensuring the safety of both animals and personnel.

## Model Development

The Machine Learning model was developed using the YOLO (You Only Look Once) technique, a popular object detection algorithm. It was trained using datasets from roboflow and Kaggle, which provide diverse and comprehensive data for effective training. To further improve prediction accuracy and overall quality, a multi-model architecture was implemented.

The system consists of three distinct models:

1) **Animal and People Detection Model**: This model is based on YOLOv5 and utilizes Microsoft MegaDetector. It has been trained to detect both animals and people within a given frame. By accurately identifying these entities, the system gains a comprehensive understanding of the wildlife sanctuary's dynamics.

2) **Personal Protective Equipment (PPE) Detection Model**: Built on YOLOv8 using  [Robolow dataset](https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety/dataset/30), this model specializes in identifying PPE kits such as hard hats and vests. It plays a crucial role in ensuring the safety of individuals within the sanctuary. If someone is detected without the required PPE, they are flagged as potential intruders or poachers.

3) **Animal Species Identification Model**: Currently under development, this model focuses on identifying the species of animals captured in the frames. By leveraging a custom labeled dataset and YOLOv8, the system aims to raise an alert when both predator and prey species are detected together. This feature is particularly valuable in identifying situations where endangered prey animals may be under threat from predators.

## System Workflow

The Wildlife Conservation Detection System follows a specific workflow for accurate detection and analysis:

1) Image or frame extraction: Using OpenCV's video or webcam capabilities, frames are extracted from the video stream or live feed.

2) Animal and people detection: Each frame is sent to the first model, which identifies and localizes animals and people. The model provides coordinates for each detection.

3) Separation of coordinates: The coordinates of animals and people are separated into two distinct arrays for further processing.

4) PPE detection: The array containing the coordinates of people is passed to the second model, which determines whether individuals are wearing the necessary PPE, including hard hats and vests. This step helps identify potential intruders or individuals who may pose a risk to wildlife or themselves.

5) Animal species identification: The array containing the coordinates of animals is sent to the third model for species identification. Currently, the model has been trained on a limited set of animal species, including Elephant, Leopard, Chimpanzee, Jaguar, Lion, Panda, and Rhino. Future enhancements aim to expand the model's capabilities to cover a wider range of species.

## Challenges Faced and how they were tackled

During the development of the detection system, the following challenges were encountered and effectively addressed:

1) **Limited training time and resources**: With the constraints of a 36-hour hackathon, there were limitations in terms of training time and available resources. To overcome this challenge, the focus was narrowed down to training the models specifically for a critical set of animal species. This approach ensured optimal utilization of the available time and resources.

2) **Model performance and accuracy**: Ensuring high performance and accuracy of the models is essential for reliable detection. To address this challenge, a multi-model architecture was implemented. Leveraging Microsoft MegaDetector's exceptional accuracy in detecting animals and people, unnecessary information in the image was reduced by extracting only animal coordinates. This significantly improved the accuracy of both the first and third models.

By strategically tackling these challenges and maximizing the available resources, the Wildlife Conservation Detection System was successfully developed within the hackathon's constraints.

## Alert Output
- WebSite Quick Demo:- (https://drive.google.com/file/d/1S8TOoh9hTh7WAUCdIvk-cJzlFV27jHjn/view)
- Alert sent to email
- ![image](https://github.com/Naveenlingala/Wildlife-Conservation-Project/assets/60232407/f3c55d94-10f1-4655-935d-d9a14aaf263c)

