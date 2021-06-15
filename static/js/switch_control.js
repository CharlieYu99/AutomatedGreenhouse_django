function checkbox_light_Onclick(checkbox){
    if ( checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_light_on": "",},
        });
    }else{
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_light_off": "",},
        });
    }
}
function checkbox_fan0_Onclick(checkbox){
    if ( checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_fan0_on": "",},
        });
    }else{
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_fan0_off": "",},
        });
    }
}
function checkbox_fan1_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_fan1_on": "",},
        });
    }else{
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_fan1_off": "",},
        });
    }
}
function checkbox_humidifier_off_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_humidifier_off": "",},
        });
    }
}
function checkbox_humidifier_weak_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_humidifier_on_weak": "",},
        });
    }
}
function checkbox_humidifier_strong_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_humidifier_on_strong": "",},
        });
    }
}
function checkbox_heater_off_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_heater_off": "",},
        });
    }
}
function checkbox_heater_weak_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_heater_on_weak": "",},
        });
    }
}
function checkbox_heater_strong_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_heater_on_strong": "",},
        });
    }
}
function checkbox_waterpump_on_Onclick(checkbox){
    if (checkbox.checked == true){
        $.ajax({
            type: "POST",
            url: "",
            data: {"button_waterpump_on": "",},
        });
        checkbox_waterpump.checked = false;
    }
}