from logging import Logger

from ankaios_deploy_manager.mqtt.mqtt_handler import MqttHandler
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

logger = Logger(__name__)


class UploadFileForm(forms.Form):
    file = forms.FileField()
    target_vin = forms.CharField(label="Target VIN")


def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        logger.info("Request")
        logger.info(request)
        if form.is_valid():
            logger.info("Valid")
            file = request.FILES["file"]
            file.seek(0)
            target_vin = form.cleaned_data["target_vin"]
            print(target_vin)
            yaml_content = file.read()
            MqttHandler.deploy_yaml(yaml_content, [target_vin])
            return HttpResponseRedirect("/")
    else:
        form = UploadFileForm()
    logger.info("Active Vehicle Dynamics")
    logger.info(MqttHandler.active_vehicle_dynamics)
    context = {
        "active_vehicle_dynamics": MqttHandler.active_vehicle_dynamics,
        "file_upload_form": form,
    }
    return render(request, "ankaios_deploy_manager/index.html", context)


def update_connector(id):
    # TODO Implement new connector registration over MQTT
    pass


def delete_connector(id):
    # TODO Implement connector removal over MQTT
    pass
