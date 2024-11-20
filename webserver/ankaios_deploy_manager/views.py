from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import mqtt_handler

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def index(request):
    ankaios_data = [
        {
            "cluster_id": 1,
            "agents": [
                {
                    "agent_id": 1,
                    "agent_name": "HPC1",
                    "active_workloads": [
                        {
                            "workload_name": "myapp1",
                            "workload_version": "1.44.4",
                        },
                        {
                            "workload_name": "ankaios_deployment_manager_connector",
                            "workload_version": "1.02.4",
                        },
                    ]
                },
                {
                    "agent_id": 2,
                    "agent_name": "HPC1",
                    "active_workloads": [
                        {
                            "workload_name": "myapp2",
                            "workload_version": "1.44.4",
                        }
                    ]
                },
            ]
        }
    ]

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            file.seek(0)
            yaml_content = file.read()
            mqtt_handler.deploy_yaml(yaml_content)
            return HttpResponseRedirect("/")
    else:
        form = UploadFileForm()

    context = {
        "ankaios_list": ankaios_data,
        "file_upload_form" : form
    }
    return render(request, "ankaios_deploy_manager/index.html", context)

def update_connector(id):
    #TODO Implement new connector registration over MQTT
    pass

def delete_connector(id):
    #TODO Implement connector removal over MQTT
    pass