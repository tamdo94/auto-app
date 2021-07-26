# auto-app

<h4>1. create docker-resources/env.list file for aws credentials</h4>

<p>env.list</p>
<p>AWS_ACCESS_KEY={YOUR AWS ACCESS KEY}</p>
<p>AWS_PRIVATE_KEY={YOUR AWS SECRET KEY}</p>
<p>AWS_REGION={YOUR AWS REGION}</p>

<h4>2. docker build</h4>
<p>docker build -t tamaws2/heapdump .</p>

<h4>3. docker run</h4>
<p>docker run -d -p 8080:8080 -m 1024m --env-file docker-resources/env.list --name heapdump tamaws2/heapdump</p>
