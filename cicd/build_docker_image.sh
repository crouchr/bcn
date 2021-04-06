cd ..
docker build --no-cache -t cicd:bcnd .
docker tag cicd:bcnd registry:5000/bcnd:$VERSION
docker push registry:5000/bcnd:$VERSION
docker rmi cicd:bcnd
