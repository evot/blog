var log = function () {
    console.log(arguments);
};

// form
var formFromIdPrefix = function (keys, prefix) {
    var form = {};
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var idTag = prefix + key;

        var value = $('#' + idTag).val();

        form[key] = value;
    }
    return form;
};

var formFromDataAttr = function (keys, selector) {
    var form = {};
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var value = selector.data(key);
        form[key] = value;
    }
    return form;
};

var api = {};


api.ajax = function (url, method, form, callback) {
    // 生成一个请求
    var request = {
        url: url,
        type: method,
        data: JSON.stringify(form),
        contentType: 'application/json',
        success: function (responseData) {
            // var r = JSON.parse(responseData)
            var r = responseData;
            callback(r)
        },
        error: function (XHR, textStatus, errorThrown) {
            var r = {
                'success': false,
                'message': textStatus
            };
            callback(r)
        }
    };
    $.ajax(request)
};

///////////////////////////////////////////////

api.get = function (url, response) {
    api.ajax(url, 'get', {}, response)
};

api.post = function (url, form, response) {
    // response 是一个回调函数
    api.ajax(url, 'post', form, response)
};

///////////////////////////////////////////////


// auth api
api.register = function (form, response) {
    var url = '/api/register';
    this.post(url, form, response);
};

api.login = function (form, response) {
    var url = '/api/login';
    this.post(url, form, response);
};

api.visitor = function (form, response) {
    var url = '/api/visitor';
    this.post(url, form, response);
};

// comment api
api.addComment = function (form, response) {
    var url = '/api/comment/add';
    this.post(url, form, response);
};

api.upvoteComment = function (comment_id, response) {
    var url = '/api/comment/' + comment_id + '/upvote'
    this.get(url, response);
};

api.deleteComment = function (comment_id, response) {
    var url = '/api/comment/' + comment_id + '/delete'
    this.get(url, response);
};

// user api
api.followUser = function (user_id, response) {
    var url = '/api/user/' + user_id + '/follow'
    this.get(url, response);
};

// reply api
api.addReply = function (form, response) {
    var url = '/api/reply/add';
    this.post(url, form, response);
};

api.upvoteReply = function (reply_id, response) {
    var url = '/api/reply/' + reply_id + '/upvote'
    this.get(url, response);
};

api.deleteReply = function (reply_id, response) {
    var url = '/api/reply/' + reply_id + '/delete'
    this.get(url, response);
};


