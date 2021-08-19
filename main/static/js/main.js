$(document).ready(function(){
	onLoadImg();
});

function onLoadImg(){
    var $label = $('.img_upload_label');
    var labelVal = $label.html();

    $('#img').on('change', function(element) {

        $('#result').html('');
        $('#preview img').remove();
        $('.bar-loader').removeClass('hide');
        $('section').removeClass('row').addClass('column');

        img = element.target.files[0];
        if(validateFile(img)){
            $('#preview').append('<img src="'+ URL.createObjectURL(img) +'" style="max-width:500px">');
            $('#preview').after(getAlert('Processing...', 'info'));

            if(img.name){
                $label.find('.fa').removeClass('fa-download').addClass('fa-check');
                $label.addClass('has-img').find('.img_name').html(img.name);
            }
            else{
                $label.find('.fa').removeClass('fa-check').addClass('fa-download');
                $label.removeClass('has-img').html(labelVal);
            }
            sendImg(img);
        }
    });
}


function sendImg(img){
    fd = new FormData();
    fd.append('img', img);

    start = new Date().getTime()
    $.ajax({
        url: '/get_img',
        data: fd,
        type: 'POST',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        timeout: 800000,
        success: function(response){
            stop = new Date().getTime()
            load_time = Math.floor(((stop-start) % (1000 * 60)) / 1000);
            response = JSON.parse(response);
            if (response['status'] == 'OK'){
                if(load_time < 3){
                    setTimeout(function(){
                    	loadResponse(response)
                    }, 5000);
                }
                else{
                    loadResponse(response);
                }
            }
        },
        error: function(){
	        alert("Something went wrong. Select another image after reloading the page");
	        window.location.reload();
	     }
    });
};


function getAlert(text, class_suf){
    return '<div class="alert alert-'+ class_suf +' alert-dismissible fade show" role="alert">'+
              text+
              '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
                '<span aria-hidden="true">&times;</span>'+
              '</button>'+
            '</div>'
}


function loadResponse(response){
    $('.close').click();
    $('.bar-loader').addClass('hide');
    $('section').removeClass('column').addClass('row');

    $.each(response['images_name'], function(index, value){
        $('#result').append('<img src="static/images/'+ value +'" style="max-width:100px">');
    })
}


function validateFile(img){
    if(img.size > 30*10**6){
        $('#img_choose').before(getAlert('Image size must be less than 30 MB', 'danger'));
        return false;
    }
    if(!['image/png', 'image/jpeg', 'image/jpg', 'image/svg'].includes(img.type)){
        $('#img_choose').before(getAlert('Image type must be png, jpeg, jpg or svg', 'danger'));
        return false;
    }
    return true;
}