var followUser = function () {
    $('.btn-follow').on('click', function () {
        var user_id = $(this).data('uid')
        var current_node = $(this)
        var follows_node = current_node.parents('.dashed').next()
        var followed_count = parseInt(follows_node.find('a.followed_count').text())
        var response = function (r) {
            if (r.success) {
                if (r.follow) {
                    current_node.find('span.follow-text').text('取关')
                    follows_node.find('a.followed_count').text(followed_count + 1)
                }
                if (r.unfollow) {
                    current_node.find('span.follow-text').text('关注')
                    follows_node.find('a.followed_count').text(followed_count - 1)
                }
            } else {
                alert(r.message)
            }
        }
        api.followUser(user_id, response);
    })
};

var bindEvents = function () {
    followUser()
}

$(document).ready(function () {
    bindEvents()
})
