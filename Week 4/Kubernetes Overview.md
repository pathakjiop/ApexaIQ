# Kubernetes Overview

## What is Kubernetes?
Kubernetes (K8s) is an open-source container orchestration platform originally developed by Google and now maintained by the Cloud Native Computing Foundation (CNCF). It provides a platform for automating deployment, scaling, and operations of application containers across clusters of hosts.

## Core Concepts

### 1. **Cluster Architecture**
A Kubernetes cluster consists of two main parts:
- **Control Plane (Master)**: The brain of the cluster that makes global decisions
- **Worker Nodes**: Machines that run the actual containerized applications

### 2. **Pods**
- Smallest and simplest Kubernetes object
- A logical host for one or more containers
- Containers in a Pod share:
  - Network namespace (same IP address and port space)
  - Storage volumes
  - Linux namespaces, cgroups, and other isolation aspects
- Ephemeral lifecycle - can be created, destroyed, and recreated

### 3. **Controllers**
Higher-level abstractions that manage Pods:
- **Deployment**: Manages stateless applications, provides rolling updates
- **StatefulSet**: Manages stateful applications, maintains sticky identity
- **DaemonSet**: Ensures all nodes run a copy of a Pod
- **Job**: Creates Pods that run to completion
- **CronJob**: Runs Jobs on a time-based schedule

## Detailed Component Breakdown

### Control Plane Components

#### **kube-apiserver**
- Front-end to the control plane
- Exposes the Kubernetes API
- Processes REST operations, validates and configures data
- Scales horizontally

#### **etcd**
- Consistent and highly-available key-value store
- Stores all cluster data
- Backbone of Kubernetes cluster state
- Implements raft consensus algorithm

#### **kube-scheduler**
- Watches for newly created Pods with no assigned node
- Selects a node for Pods to run on based on:
  - Resource requirements
  - Hardware/software constraints
  - Affinity/anti-affinity specifications
  - Data locality
  - Deadlines

#### **kube-controller-manager**
- Runs controller processes including:
  - Node Controller: Manages node status
  - Replication Controller: Maintains correct number of Pods
  - Endpoints Controller: Populates Endpoints objects
  - Service Account & Token Controllers: Create default accounts and API access tokens

#### **cloud-controller-manager**
- Embeds cloud-specific control logic
- Allows cloud providers to integrate with Kubernetes
- Runs controllers for Node, Route, and Service handling

### Node Components

#### **kubelet**
- Primary node agent that runs on each node
- Ensures containers are running in a Pod
- Takes Pod specifications and ensures described containers are running
- Reports node and Pod status to control plane

#### **kube-proxy**
- Network proxy running on each node
- Maintains network rules on the node
- Implements Kubernetes Service concept
- Uses operating system packet filtering or forwards traffic

#### **Container Runtime**
- Software responsible for running containers
- Supports Docker, containerd, CRI-O, and any implementation of Kubernetes CRI

## Key Objects and Resources

### **Services**
- Abstract way to expose an application running on a set of Pods
- Types:
  - **ClusterIP**: Exposes the service on a cluster-internal IP
  - **NodePort**: Exposes the service on each Node's IP at a static port
  - **LoadBalancer**: Exposes the service externally using cloud provider's load balancer
  - **ExternalName**: Maps the service to the contents of the externalName field

### **Volumes and Storage**
- **PersistentVolume (PV)**: Cluster resource for storage
- **PersistentVolumeClaim (PVC)**: User's request for storage
- **StorageClass**: Describes different types of storage available
- **ConfigMap & Secret**: Manage configuration data and sensitive information

### **Networking**
- **Container Network Interface (CNI)**: Plugin-based networking
- **Network Policies**: Firewall rules for Pods
- **Ingress**: Manages external access to services
- **DNS**: Built-in service discovery via DNS

## Advanced Features

### **Auto-scaling**
- **Horizontal Pod Autoscaler (HPA)**: Automatically scales number of Pods
- **Vertical Pod Autoscaler (VPA)**: Automatically adjusts Pod resource requests
- **Cluster Autoscaler**: Automatically adjusts cluster size

### **Resource Management**
- **Requests**: Minimum resources guaranteed to a container
- **Limits**: Maximum resources a container can use
- **Quality of Service (QoS) Classes**:
  - Guaranteed: Both limits and requests set
  - Burstable: Requests set but limits optional
  - BestEffort: Neither requests nor limits set

### **Security**
- **RBAC (Role-Based Access Control)**: Authorization mechanism
- **Security Context**: Pod and container-level security settings
- **Network Policies**: Control Pod-to-Pod communication
- **Pod Security Standards**: Security policies for Pods

## Workload Management

### **Deployment Strategies**
- **Rolling Update**: Gradually update Pods instances
- **Blue-Green**: Two identical environments, switch traffic between them
- **Canary**: Roll out changes to a small subset of users
- **Recreate**: Terminate all Pods then create new ones

### **Configuration Management**
- **ConfigMaps**: Store non-confidential data in key-value pairs
- **Secrets**: Store sensitive information like passwords, OAuth tokens
- **Environment Variables**: Inject configuration into containers
- **Volume Mounts**: Mount configuration files directly

## Monitoring and Observability

### **Health Checks**
- **Liveness Probes**: Determine if container is running properly
- **Readiness Probes**: Determine if container is ready to serve traffic
- **Startup Probes**: Determine if container application has started

### **Logging and Monitoring**
- **Container Logs**: Standard output and error streams
- **Metrics Server**: Cluster-wide resource usage data
- **Prometheus Integration**: Popular monitoring solution
- **Dashboard**: Web-based Kubernetes user interface

## Ecosystem and Tools

### **Package Management**
- **Helm**: The package manager for Kubernetes
- **Kustomize**: Template-free configuration customization
- **Operators**: Kubernetes-aware applications

### **CI/CD Integration**
- **GitOps**: Using Git as single source of truth
- **ArgoCD**: Declarative GitOps tool
- **Jenkins X**: Cloud-native CI/CD solution
- **Tekton**: Cloud-native CI/CD framework

### **Service Mesh**
- **Istio**: Comprehensive service mesh solution
- **Linkerd**: Lightweight service mesh
- **Consul Connect**: Service mesh with service discovery

## Best Practices

### **Application Design**
- Design for statelessness where possible
- Implement proper health checks
- Use microservices architecture appropriately
- Implement circuit breakers and retry logic

### **Cluster Management**
- Use namespaces for resource isolation
- Implement resource quotas and limits
- Use network policies for security
- Regular cluster upgrades and maintenance

### **Security**
- Follow principle of least privilege
- Regularly rotate secrets and certificates
- Scan container images for vulnerabilities
- Implement pod security standards

## Common Patterns

### **Sidecar Pattern**
- Helper containers that extend and enhance main container
- Used for logging, monitoring, or proxy services

### **Ambassador Pattern**
- Proxy network requests for main container
- Handles connection pooling, TLS, etc.

### **Adapter Pattern**
- Standardizes and normalizes application output
- Useful for monitoring and logging consistency

## Production Considerations

### **High Availability**
- Multi-master configurations
- etcd cluster with odd number of members
- Distributed worker nodes across availability zones
- Backup and disaster recovery strategies

### **Performance**
- Proper resource requests and limits
- Efficient container images
- Optimized network policies
- Appropriate storage classes

### **Cost Optimization**
- Right-sizing resource requests
- Cluster autoscaling
- Spot instance utilization
- Efficient storage management

