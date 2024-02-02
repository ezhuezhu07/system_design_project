minikube start 
cd auth/manifests
kubectl delete -f ./ 
kubectl apply -f ./ 
cd ../../gateway/manifests
kubectl delete -f ./                                                    
kubectl apply -f ./ 
cd ../../converter/manifests
kubectl delete -f ./
kubectl apply -f ./
cd ../../rabbit/manifests
kubectl delete -f ./ 
kubectl apply -f ./





