GCP Backend
===========

Using Coiled's GCP account
--------------------------

You can have Coiled launch computations on Google Cloud Platform (GCP). Your
computations will run inside Coiled's Google Cloud account by default, this makes it easy
for you to get started quickly, without needing to set up any additional
infrastructure.

.. figure:: images/backend-coiled-gcp-vm.png

.. note::

   GCP support is currently experimental with new features under active
   development.

.. tip::

    In addition to the usual cluster logs, our current GCP backend support also
    includes system-level logs. This provides rich insight into any potential
    issues while GCP support is still experimental.


Switching Coiled backend to GCP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use Coiled on GCP, log in to your Coiled account 
and access your dashboard. Click on `Account` on the left navigation bar, then click 
the `Edit` button to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

On the Select Your Cloud Provider step, select the GCP option, then click the 
Next button:

.. figure:: images/cloud-backend-provider-gcp.png
   :width: 100%

Proceed by selecting "Launch in Coiled's GCP Account".  Select Next, then the registry 
you wish to use and Submit. 


Using your own GCP Account
--------------------------

Alternatively, you can configure Coiled to create Dask clusters and run 
computations entirely within your own GCP account (within a project of your 
choosing). This allows you to make use of security/data access controls, 
compliance standards, and promotional credits that you already have in place 
within your GCP account.

.. figure:: images/backend-external-gcp-vm.png

Note that when running Coiled on your GCP account, Coiled Cloud is only 
responsible for provisioning cloud resources for Dask clusters that you create. 
Once a Dask cluster is created, all computations, data transfer, and Dask 
client-to-scheduler communication occurs entirely within your GCP account.

.. note::

   GCP support is currently experimental with new features under active
   development.  GCP customer-hosted operation is currenlty in alpha
   deployment and available only to early-adopter users. Interested users 
   should contact `coiled support <https://docs.coiled.io/user_guide/support.html>`_.

Step 1: Obtain GCP credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled provisions resources on your GCP account by using a key tied to a 
Service Account, Role, and Project within your organization's GCP account.
You can use an existing service account (with appropriate permissions, see below) 
or create a service account and generate a key. To do that, please consult the 
corresponding GCP docs:

- `Creating & Managing Service Accounts <https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating>`_
- `Creating & Managing Service Account Keys <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating_service_account_keys>`_

The service account credentials will be saved with a file name like, `gcp-project-name-d9e9114d534e.json`, 
with content like this:

.. code-block:: json

    {
      "type": "service_account",
      "project_id": "gcp-ch-01",
      "private_key_id": "##################################",
      "private_key": "-----BEGIN PRIVATE KEY-----\################################################",
      "client_email": "service-account-name@project-name.iam.gserviceaccount.com",
      "client_id": "##############################",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account-name%40project-name.iam.gserviceaccount.com"
    }


Step 2: Create a custom IAM Role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled requires a limited set of IAM permissions to be able to provision
infrastructure and compute resources in your GCP account.

You'll need to create a new IAM role and assign the appropriate set of
permissions to it. Specify an IAM role name such as `Coiled` that will make it
easy to locate in the next step.
For information on creating an IAM role, see the `GCP custom role creation 
documentation <https://cloud.google.com/iam/docs/creating-custom-roles#creating_a_custom_role>`_.

Due to the amount of permissions that you will have to add, we recommend that you use
the ``gcloud`` command to create your role from the following yaml file.

.. dropdown:: Coiled Permissions Yaml File
  :title: bg-white

  .. code-block:: yaml

   title: coiled
   description: coiled-externally-hosted
   stage: GA
   includedPermissions:
   - compute.acceleratorTypes.list
   - compute.addresses.list
   - compute.disks.create
   - compute.disks.list
   - compute.disks.useReadOnly
   - compute.firewalls.create
   - compute.firewalls.delete
   - compute.firewalls.get
   - compute.firewalls.list
   - compute.globalOperations.get
   - compute.globalOperations.getIamPolicy
   - compute.images.create
   - compute.images.get
   - compute.images.list
   - compute.images.setLabels
   - compute.images.useReadOnly
   - compute.instances.create
   - compute.instances.delete
   - compute.instances.get
   - compute.instances.list
   - compute.instances.setLabels
   - compute.instances.setMetadata
   - compute.instances.setTags
   - compute.machineTypes.get
   - compute.machineTypes.list
   - compute.networks.create
   - compute.networks.delete
   - compute.networks.get
   - compute.networks.list
   - compute.networks.updatePolicy
   - compute.projects.get
   - compute.projects.setCommonInstanceMetadata
   - compute.regions.get
   - compute.regions.list
   - compute.routers.create
   - compute.routers.delete
   - compute.routers.get
   - compute.routers.list
   - compute.routers.update
   - compute.routes.delete
   - compute.routes.list
   - compute.subnetworks.create
   - compute.subnetworks.delete
   - compute.subnetworks.get
   - compute.subnetworks.getIamPolicy
   - compute.subnetworks.list
   - compute.subnetworks.use
   - compute.subnetworks.useExternalIp
   - compute.zones.list
   - iam.serviceAccounts.actAs
   - logging.buckets.create
   - logging.buckets.get
   - logging.buckets.list
   - logging.sinks.create
   - logging.sinks.get
   - logging.sinks.list
   - storage.buckets.create
   - storage.buckets.get
   - storage.objects.create
   - storage.objects.get
   - storage.objects.list
   - storage.objects.update



Step 3: Connect the Service Account and Role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally, you you will need to grant that Service Account access to that Role.
For information on connecting service accounts to roles, see the corresponding 
`GCP role access granting documentation <https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-console>`_.

Step 4: Configure Coiled cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you're ready to configure the cloud backend in your Coiled Cloud account 
to use your GCP account and GCP credentials. To configure Coiled to use your 
GCP account, log in to your Coiled account and access your dashboard. Click 
on ``Account`` on the left navigation bar, then click the ``Edit`` button to configure 
your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

On the Select Your Cloud Provider step, select the GCP option, then click the 
Next button:

.. figure:: images/cloud-backend-provider-gcp.png
   :width: 100%

On the Configure GCP step, select the GCP region that you want to use by default 
(i.e., when a region is not specified), choose the Launch in my GCP account option, 
and add your service account credentials file, then click the 
``Next`` button.

On the Container Registry step, select where you would like to store your  
software environments, then click the Next button.

Coiled is now configured to use your GCP Account!

Region
------

GCP support is currently only available in the ``us-east1`` region. If you have
data in a different region on Google Cloud, you may be charged transfer fees.

Backend options
---------------

Similar to the AWS backend, the GCP backend uses
`preemptible instances <https://cloud.google.com/compute/docs/instances/preemptible>`_
for the workers by default. Note that GCP automatically terminates these after 24 hours.


.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - ``region``
     - GCP region to create resources in
     - ``us-east1``
   * - ``zone``
     - GCP zone to create resources in
     - ``us-east1-c``
   * - ``spot``
     - Whether or not to use preemptible instances for cluster workers
     - ``True``

Example
^^^^^^^

You can specify backend options directly in Python:

.. code-block::

    import coiled

    cluster = coiled.Cluster(backend_options={"region": "us-west1", "spot": False})

Or save them to your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        region: us-west1

to have them used as the default value for the ``backend_options=`` keyword:

.. code-block::

    import coiled

    cluster = coiled.Cluster()


GPU support
-----------

This backend allows you to run computations with GPU-enabled machines if your
account has access to GPUs. See the :doc:`GPU best practices <gpu>`
documentation for more information on using GPUs with this backend.

Workers currently have access to a single GPU, if you try to create a cluster
with more than one GPU, the cluster will not start, and an error will be
returned to you.
