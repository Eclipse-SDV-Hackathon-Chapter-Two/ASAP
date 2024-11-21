from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from ankaios_deploy_manager.mqtt.mqtt_handler import MqttHandler

class UploadFileForm(forms.Form):
    file = forms.FileField()
    target_vin = forms.CharField(label="Target VIN")

def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        print("Request")
        print(request)
        if form.is_valid():
            print("Valid")
            file = request.FILES["file"]
            file.seek(0)
            target_vin = form.cleaned_data['target_vin']
            print(target_vin)
            yaml_content = file.read()
            MqttHandler.deploy_yaml(yaml_content, [target_vin])
            return HttpResponseRedirect("/")
    else:
        form = UploadFileForm()
    print("Active Vehicle Dynamics")
    print(MqttHandler.active_vehicle_dynamics)
    context = {
        "active_vehicle_dynamics": MqttHandler.active_vehicle_dynamics,
        "file_upload_form" : form
    }
    return render(request, "ankaios_deploy_manager/index.html", context)

def update_connector(id):
    #TODO Implement new connector registration over MQTT
    pass

def delete_connector(id):
    #TODO Implement connector removal over MQTT
    pass