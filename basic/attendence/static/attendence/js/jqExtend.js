$.fn.V = function(value) {
    if (!value && value != '') {
        return false
    };

    if ($(this).is(":text") || $(this).is("textarea")) {
        $(this).val(value);
        $(this).blur();
        return;
    }

    if ($(this).is("select")) {
        $(this).val(value);
        $(this).change();
        return;
    }

    if ($(this).is(":radio") || $(this).is(":checkbox")) {
        if (($(this).val() == "1" || $(this).val() == "0") && (value == "True" || value == "False")) {
            value = value == "True" ? 1 : 0;
        }
        if ($(this).val() == value) {
            $(this).attr("checked", true);
        } else {
            $(this).removeAttr("checked");
        }
        $(this).change();
    }
    return this;
};

$.fn.param = function(obj) {
    if (obj) {
        if (typeof obj == "string")
            obj = jsonParse(obj)[0];
        for (var prop in obj) {
            $('[name=' + prop + ']', this).each(function() {
                $(this).V(obj[prop]);
            });
        }

    } else {
        var param = "";
        this.find("input[type=text]").each(function() {
            if (!$(this).is(":visible") || !$(this).closest("div").is(":visible")) return true;
            param = param + "&" + this.id + '=' + encodeURIComponent($(this).val());
        });

        this.find("textarea").each(function() {
            if (!$(this).is(":visible") || !$(this).closest("div").is(":visible")) return true;
            param = param + "&" + this.id + '=' + encodeURIComponent($(this).val());
        });

        this.find("select").each(function() {
            if (!$(this).is(":visible") || !$(this).closest("div").is(":visible")) return true;
            param = param + "&" + this.id + '=' + encodeURIComponent($(this).val());
        });

        this.find("input[type=checkbox]").each(function() {
            if (!$(this).is(":visible") || !$(this).closest("div").is(":visible")) return true;
            param = param + "&" + this.id + '=' + ($(this).is(":checked") ? 1 : 0);
        });

        this.find("input[type=radio]:checked").each(function() {
            if (!$(this).is(":visible") || !$(this).closest("div").is(":visible")) return true;
            param = param + "&" + $(this).attr("name") + '=' + $(this).val();
        });

        $.each(this.data(), function(key, value) {
            if (!/^jqx.+/.test(key)) {
                param = param + "&" + key + '=' + value;
            }
        })

        if (param != "") {
            param = param.substring(1);
        }
        return param;
    }
}

$.fn.clear = function() {
    var targetObj = this;
    $("textarea,:text", targetObj).each(function() {
        $(this).val("");
    });
    $("select", targetObj).each(function() {
        $(this).val("-1");
        $(this).change();
    });
    $(":radio,:checkbox", targetObj).each(function() {
        $(this).attr("checked", false);
        $(this).change();
    });
    $.each(targetObj.data(), function(key, value) {
        if (!/^jqx.+$/.test(key)) {
            targetObj.removeData(key);
        }
    })
}
