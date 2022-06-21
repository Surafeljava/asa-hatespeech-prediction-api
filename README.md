# Amharic Sentiment Analysis - Hate Speech Detection Using Machine Learning

The scope of this project is limited to the presence or absence of hate 
speech on Amharic language Twitter posts. In this context, the term 'hate speech' 
refers to abusive or threatening statements or phrases that describe prejudice against 
a particular group in Ethiopia.


## Advisor

- Elefelious Getachew (Ph.D.)


## Members

- [Surafel Kindu](https://github.com/Surafeljava) - ATR/9237/10 - Section-1
- [Samia Abdella](https://github.com/Surafeljava) - ATR/3142/10 - Section-1
- [Daniel Tefera](https://github.com/Surafeljava) - ATR/1145/10 - Section-1
- [Eyob Maru](https://github.com/Surafeljava) - ATR/0121/10 - Section-1
- [Ahlam Muhdin](https://github.com/Surafeljava) - ATR/2923/10 - Section-3

## How to run the project locally

To deploy this project first begin by cloning the [This Repository](https://github.com/Surafeljava/asa-hatespeech-prediction-api)

### Requirements on users machine before running the project

The project is made with flask which a python framework therefore you need python before running the project:

* Download and install python locally on your computer: [Python Download Link](https://www.python.org/downloads/)

After installing python you can go a head and run the following command inside the "project folder directory"

* Install All Packages (from requirements.txt file with in the project folder)

```bash
  pip install -r requirements.txt
```

* Run the project

```bash
  python ./app.py
```

This will run a flask server locally on you machine with http://localhost:5000 

### Run Deployed Project

The project is currently launched on an Ubuntu server on Lenode with the link below:

https://178.79.135.192/

## This project can be used by

This REST-API server is used by our front-end platform to predict texts and tweets using the model trained

## References and Documentations used while developing this project

* [How to Deploy Flask App on Lenode Server](https://www.youtube.com/watch?v=BpcK5jON6Cg)
* [How to save and load models using tensorflow](https://www.tensorflow.org/tutorials/keras/save_and_load)
* [Making series of async requests with python](https://stackoverflow.com/questions/58758081/asyncio-aiohttp-how-to-make-series-of-async-but-dependent-requests)
