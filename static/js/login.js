var loginForm = function () {
    var keys = [
        'username',
        'password',
        'csrf_token',
    ];
    var idPrefix = 'id-input-login-';
    var form = formFromIdPrefix(keys, idPrefix);
    return form;
};

var registerForm = function () {
    var keys = [
        'username',
        'password',
        'csrf_token',
    ];
    var idPrefix = 'id-input-';
    var form = formFromIdPrefix(keys, idPrefix);
    return form;
};

var visitorForm = function () {
    var keys = [
        'csrf_token',
    ];
    var idPrefix = 'id-input-visitor';
    var form = formFromIdPrefix(keys, idPrefix);
    return form;
};

// var registerNameForm = function () {
//     var keys = [
//         'username',
//         'csrf_token',
//     ];
//     var idPrefix = 'id-input-';
//     var form = formFromIdPrefix(keys, idPrefix);
//     return form;
// };
//
// var registerPwdForm = function () {
//     var keys = [
//         'password',
//         'csrf_token',
//     ];
//     var idPrefix = 'id-input-';
//     var form = formFromIdPrefix(keys, idPrefix);
//     return form;
// };

// actions
var registerCheckName = function () {
    var form = registerForm();
    var checkLabel = $('#id-register-username-check');
    var response = function (r) {
        if (!(r.name_info.is_length_ok)) {
            checkLabel.removeClass();
            checkLabel.addClass('error');
            checkLabel.text('长度不合格!');
        } else if (r.name_info.is_not_exists) {
            checkLabel.removeClass();
            checkLabel.addClass('info');
            checkLabel.text('用户名可以使用!');
        } else {
            checkLabel.removeClass();
            checkLabel.addClass('error');
            checkLabel.text('用户名已存在!');
        }

    };
    api.register(form, response);
};

var loginCheckName = function () {
    var form = loginForm();
    var checkLabel = $('#id-login-username-check');
    var response = function (r) {
        if (r.name_info.is_not_exists) {
            checkLabel.removeClass();
            checkLabel.addClass('error');
            checkLabel.text('用户名不存在！');
        } else {
            checkLabel.text('');
        }
    };
    api.login(form, response);
};

var register = function () {
    var form = registerForm();
    var response = function (r) {
        if (r.success) {
            window.location.href = r.next;
        } else {
            alertify.error(r.message);
        }
    };
    api.register(form, response);
};

var login = function () {
    var form = loginForm();
    var response = function (r) {
        if (r.success) {
            window.location.href = r.next;
        } else {
            alertify.error(r.message)
            // alert(r.message)
        }
    };
    api.login(form, response);
};

var visitor = function () {
    var form = registerForm();
    var response = function (r) {
        if (r.success) {
            window.location.href = r.next;
        } else {
            alertify.error(r.message);
            // alert('服务器提出了一个问题, 请稍后再试!');

        }
    };
    api.visitor(form, response);
};

var bindActions = function () {
    $('#id-input-username').blur(function () {
        registerCheckName();
    });

    $('#id-input-login-username').blur(function () {
        loginCheckName();
    });

    $('#id-button-register').on('click', function () {
        register();
    });

    $('#id-button-login').on('click', function () {
        login();
    });

    $('#id-button-visitor').on('click', function () {
        visitor();
    });
};

// setup
var setup = function () {
    // tab click
    $('.tao-tab > a').on('click', function () {
        var self = $(this);
        $('.active').removeClass('active');
        self.addClass('active');
    });
    // tab action
    var tabAction = function (position, showLogin) {
        $(".tao-block").animate({
            "left": position
        }, "fast");
        $('#id-div-login').toggle(showLogin);
        $('#id-div-signup').toggle(!showLogin);
    };

    $('#id-a-signup').on('click', function () {
        var position = '80px';
        var showLogin = false;
        tabAction(position, showLogin);
    });
    $('#id-a-login').on('click', function () {
        var position = '135px';
        var showLogin = true;
        tabAction(position, showLogin);
    });
};

var __main = function () {
    setup();
    bindActions();
    // initial -- select signup
    $('#id-a-signup').click();
};

$(document).ready(function () {
    __main();
});
