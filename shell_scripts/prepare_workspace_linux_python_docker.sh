sudo apt-get update
sudo apt-get install libmysqlclient-dev
sudo pip3 install mysqlclient
pip3 install numpy
pip3 install pandas
pip3 install scikit-learn
pip3 install pytest
pip3 install fastapi
pip3 install sqlalchemy==1.4
pip3 install uvicorn
pip3 install asyncio
docker image pull mysql:latest
docker network create --subnet=172.20.0.0/16 customnetwork