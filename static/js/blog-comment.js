var commentTemplate = function (comment) {
    var c = comment
    var t = `                    
            <div class="ud-pd-md dashed blog-comment-cell">
                <div class="blue ud-pd-sm">
                    <span class="right-pd-sm px16">
                    <a href="${ c.sender_profile}">${ c.sender_name }</a>
                    </span>
                    回复
                    <span class="left-pd-sm px16">
                    <a href="${ c.receiver_profile }">${ c.receiver_name }</a>
                    </span>
                </div>
                <div>
                    <p>${ c.content }</p>
                </div>
    
                <div class="bm-pd-md grey">
                    <span class="small">${ c.formatted_time }</span>
                    <a class="nounderline" href="javascript:void(0);">
                        <span class="glyphicon glyphicon-thumbs-up comment-glyphicon-thumbs-up left-pd-lg grey" data-cid="${ c.id }"></span>
                        <span class="upvote-count">${ c.upvote_count }</span>
                    </a>
                    
                    <a class="nounderline" href="javascript:void(0);">
                        <span class="glyphicon glyphicon-comment comment-glyphicon-comment grey left-pd-md"></span>
                        <span class="comment-reply-count">${ c.reply_count }</span>
                    </a>
                    
                  
                    <!-- 隐藏的评论回复区 -->
                    <div class="comment-reply-container tao-hide">

                        <div class="comment-reply-form-container">
                            <div class="ud-pd-sm">
                                <textarea class="tao-comment-reply-content" name="content" style="width: 70%"></textarea>
                            </div>
                            <button type="submit" class="btn btn-blue btn-flat shadow comment-reply-add" data-cid='${ c.id }' data-rid='${ c.sender_id }' data-csrf_token="${ c.csrf_token }">提交
                            </button>
                        </div>

                        <!-- 评论所有回复 -->
                        <div class="replies-container left-bd-solid">
                        </div>
                        
                    </div>
                    <span class="pull-right">
                    <a class="nounderline" href="javascript:void(0);">
                    <span class="glyphicon glyphicon-trash  comment-glyphicon-trash grey left-pd-md small" data-cid="${ c.id }"></span>
                    </a>
                    </span>
                </div>
            </div>
        `
    return t
}

var replyTemplate = function (reply) {
    var r = reply
    var t = `                    
            <div class="ud-pd-md dashed left-mg-sm comment-reply-cell">
                <!-- 回复头 -->
                <div class="blue ud-pd-sm">
                    <span class="right-pd-sm px16">
                      <a href="${r.sender_profile }">${r.sender_name }</a>
                    </span>
                    回复
                    <span class="left-pd-sm px16">
                      <a href="${r.receiver_profile }">${ r.receiver_name }</a>
                    </span>
                </div>
                <!-- end 回复头 -->

                <!-- 回复正文 -->
                <div>
                    <p>${ r.content }</p>
                </div>
                <!-- end 回复正文 -->

                <!-- 回复底部（评论时间, 点赞等）-->
                <div class="bm-pd-md grey">
                    <span class="small">${ r.formatted_time }</span> 
                    <a class="nounderline" href="javascript:void(0);">
                        <span class="glyphicon glyphicon-thumbs-up reply-glyphicon-thumbs-up left-pd-lg grey" data-rid="${ r.id }"></span>
                        <span class="upvote-count">${ r.upvote_count }</span>
                    </a>
                    
                    <span class="pull-right">
<a class="nounderline" href="javascript:void(0);">
    <span class="glyphicon glyphicon-trash reply-glyphicon-trash grey left-pd-md small"
          data-rid="${ r.id }"></span>
                    </a>
                    </span>
                   
                </div>
                <!-- end 回复底部（评论时间, 点赞等）-->
            </div>
        `
    return t
}

var addCommentForm = function () {
    var content = editor.getData();
    var idForm = {
        content: content
    };

    var dataKeys = [
        'bid',
        'sid',
        'rid',
        'csrf_token',
    ];
    var selector = $('#id-button-blog-comment-add');
    var dataForm = formFromDataAttr(dataKeys, selector)
    var form = $.extend({}, idForm, dataForm)
    return form
}

var addReplyForm = function (selector) {
    var content = selector.parent().find('.tao-comment-reply-content').val()
    var idForm = {content: content}
    var dataKeys = [
        'cid',
        'rid',
        'csrf_token',
    ];
    var dataForm = formFromDataAttr(dataKeys, selector)
    var form = $.extend({}, idForm, dataForm)
    return form
}

var toggleComment = function () {
    $('#id-button-comment').on('click', function () {
        $(this).parent().next().slideToggle()
    })
};

var addComment = function () {
    $('#id-button-blog-comment-add').on('click', function () {

        var form = addCommentForm();
        var response = function (r) {
            if (r.success) {
                var c = r.data
                $('.blog-comment-container').append(commentTemplate(c))
                $('.tips').slideUp()
                alertify.success("添加成功")
            } else {
                alertify.error(r.message)
            }
        }
        api.addComment(form, response)
        editor.setData('')
        $('#id-button-comment').parent().next().slideUp()
    })
};

var toggleCommentReply = function () {
    $('.blog-comment-container').on('click', '.glyphicon-comment', function () {
        $(this).parent().next().slideToggle()
    })
};

var addCommentReply = function () {
    $('.blog-comment-container').on('click', '.comment-reply-add', function () {

        var selector = $(this)
        var form = addReplyForm(selector);
        var currentFormContainer = $(this).parent()
        var currentRepliesContainer = $(this).parent().next();
        var response = function (r) {
            if (r.success) {

                var r = r.data;
                currentRepliesContainer.append(replyTemplate(r))
                currentFormContainer.find('.tao-comment-reply-content').val("")
                var countNode = currentFormContainer.parent().prev().find('span.comment-reply-count')
                var count = parseInt(countNode.text())
                countNode.text(count + 1)

                // alert("评论成功")
            } else {
                alertify.error(r.message)
            }
        }
        api.addReply(form, response)
    })
};

var upvoteComment = function () {
    $('.blog-comment-container').on('click', '.comment-glyphicon-thumbs-up', function () {
        var comment_id = $(this).data('cid')
        var current_node = $(this).parent()
        var response = function (r) {

            if (r.success) {
                if (r.upvote) {
                    current_node.find('span.glyphicon').removeClass('grey')
                    current_node.find('span.glyphicon').addClass('dark-blue')
                    var upvoteCount = parseInt(current_node.find('span.upvote-count').text())
                    current_node.find('span.upvote-count').text(upvoteCount + 1)
                }
                if (r.cancel_upvote) {
                    current_node.find('span.glyphicon').removeClass('dark-blue')
                    current_node.find('span.glyphicon').addClass('grey')
                    var upvoteCount = parseInt(current_node.find('span.upvote-count').text())
                    current_node.find('span.upvote-count').text(upvoteCount - 1)
                }
            } else {
                alertify.error(r.message)
            }
        }
        api.upvoteComment(comment_id, response);
        // return false
    })
};

var upvoteCommentReply = function () {
    $('.blog-comment-container').on('click', '.reply-glyphicon-thumbs-up', function () {
        var reply_id = $(this).data('rid')
        var current_node = $(this).parent()
        var response = function (r) {
            if (r.success) {
                if (r.upvote) {
                    current_node.find('span.glyphicon').removeClass('grey')
                    current_node.find('span.glyphicon').addClass('dark-blue')
                    var upvoteCount = parseInt(current_node.find('span.upvote-count').text())
                    current_node.find('span.upvote-count').text(upvoteCount + 1)
                }
                if (r.cancel_upvote) {
                    current_node.find('span.glyphicon').removeClass('dark-blue')
                    current_node.find('span.glyphicon').addClass('grey')
                    var upvoteCount = parseInt(current_node.find('span.upvote-count').text())
                    current_node.find('span.upvote-count').text(upvoteCount - 1)
                }
            } else {
                alertify.error(r.message)
            }
        }
        api.upvoteReply(reply_id, response);
        // return false
    })
};

var deleteComment = function () {
    $('.blog-comment-container').on('click', '.comment-glyphicon-trash', function () {
        var comment_id = $(this).data('cid')
        var comment_cell = $(this).closest('.blog-comment-cell')
        var response = function (r) {
            if (r.success) {
                comment_cell.slideUp()
            }
        }
        api.deleteComment(comment_id, response);
        return false
    })
};

var deleteCommentReply = function () {
    $('.blog-comment-container').on('click', '.reply-glyphicon-trash', function () {
        var reply_id = $(this).data('rid')
        var reply_cell = $(this).closest('.comment-reply-cell')
        var response = function (r) {
            if (r.success) {
                reply_cell.slideUp()
            }
        }
        api.deleteReply(reply_id, response);
        return false
    })
};

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
                alertify.error(r.message)
            }
        }
        api.followUser(user_id, response);
    })
};

var bindEvents = function () {
    CKEDITOR.disableAutoInline = true;
    editor = CKEDITOR.replace('tao-editor');
    toggleComment()
    addComment()
    followUser()
    // 事件委托
    upvoteComment()
    deleteComment()
    toggleCommentReply()
    addCommentReply()
    upvoteCommentReply()
    deleteCommentReply()

}

$(document).ready(function () {
    bindEvents()
})

