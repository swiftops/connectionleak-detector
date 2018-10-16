#Replace <Port No.> with port which your service is going to deploy.
bind = "0.0.0.0:5004"

#Workers means no. of nodes connected with master node. The no. you defined here, that no. of process will get triggered
# formula for setting worker nodes : (2 Workers * CPU Cores) + 1
# In above if machines have 2 CPU Cores the (2*2)+1 i.e 5 workers should be set.
workers = 5

#no of threads should get started on each worker node.
threads = 2
