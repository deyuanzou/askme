function bindEmailCaptchaClick() {
    $('#captcha-btn').click(function (e) {
        e.preventDefault();

        let $this = $(this)

        let email = $("input[name='email']").val();
        $.ajax({
            url: '/auth/captcha/email?email=' + email,
            method: 'GET',
            success: function (data) {
                switch (data.code) {
                    case 200:
                        $this.off('click')
                        let countdown = 20
                        let timer = setInterval(function() {
                            $this.text(''+countdown+'s')
                            countdown -= 1
                            if (countdown <= 0) {
                                clearInterval(timer)
                                $this.text('获取验证码')
                                bindEmailCaptchaClick()
                            }
                        },1000)
                        alert('验证码发送成功')
                    default:
                        break
                }
            },
            fail: function (error) {
              console.log(error);
            }
        })


    })
}

$(function () {
    bindEmailCaptchaClick()
})