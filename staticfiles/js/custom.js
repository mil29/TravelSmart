$(document).ready(function() {

    // Function to remove flash messages from screen  after 2 seconds 
    setTimeout(function () {
        if ($("#msg").length > 0) {
            $("#msg").remove();
        }
        }, 2000);

    //  for longer messages timeout longer 
    setTimeout(function () {
        if ($("#msg-info").length > 0) {
            $("#msg-info").remove();
        }
        }, 5000);


    // Function to remove form error messages from screen  after 2 seconds 
    setTimeout(function () {
        if ($("#form-msg").length > 0) {
            $("#form-msg").remove();
        }
        }, 2000);



    // function to confirm profile pic delete on profile page
    $(document).on('click', '.trash_pic_button', function(){
        return confirm('Are you sure you want to delete profile pic?');
    })


    // function for travel-currency.html for select2 live search using option select and placing text from selected into innerhtml

    function formatState (state) {
        if (!state.id) {
            return state.text;
        }
        var baseUrl = "/static/img/flags";
        var $state = $(
            '<span><img src="' + baseUrl + '/' + state.element.value.toLowerCase() + '.png" id="img-flag" /> ' + state.text + '</span>'
        );
        return $state;
    };



    let currency1 = document.getElementById('curr1');
    let currency2 = document.getElementById('curr2');
    let currencySymbol = document.getElementById('currency-sym');
    let imgFlag = document.getElementById('countryFlag');
    let imgFlag2 = document.getElementById('countryFlag2');


    $('.currency-selector').select2({
        templateResult: formatState
    }).change(function(){
        let selectCurrency = $('.currency-selector').val();
        // adding currency symbol next to currency amount input 
        currency1.innerHTML = selectCurrency;
        currencySymbol.innerHTML = selectCurrency;
        let countryFlag = document.getElementById('img-flag').src.slice(0, -7);
        imgFlag.innerHTML = `<img src='${countryFlag}${selectCurrency.toLowerCase()}.png'>`;
    });

    $('.currency-selector2').select2({
        templateResult: formatState
    }).change(function(){
        let selectCurrency2 = $('.currency-selector2').val();
        currency2.innerHTML = selectCurrency2;
        let countryFlag2 = document.getElementById('img-flag').src.slice(0, -7);
        imgFlag2.innerHTML = `<img src='${countryFlag2}${selectCurrency2.toLowerCase()}.png'>`;
    });
    




    // this function below is needed in order for the search box to be in focus when selecting dropdown as there was an issue with jquery 3.6.0
    $(document).on('select2:open', () => {
    document.querySelector('.select2-search__field').focus();
    });    


    // ajax function subitted on currency form submit button to get api data from currency api and update results on page without refresh

    // Submit post on submit
    $('#currency-form').on('submit', function(event){
        event.preventDefault();
        convert_currency();
    });



    // AJAX for posting
    function convert_currency() {
        // let currvalue = $(".currency-selector").select2('data')[0].text;
        // console.log(currvalue);
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url  : $('#currency-form').attr("data-currency-form-url"), // endpoint
            type : "POST", // http method
            data : {
                curr1: $('.currency-selector').val(),
                curr2: $('.currency-selector2').val(),
                amount: $('.currency-amount-input').val(),
                'csrfmiddlewaretoken': csrftoken,
            },
            // handle a successful response
            success : function(json) {
                $('.currency-amount-input').val('');  // remove the value from the input
                if (json.hasOwnProperty('result')) {
                    add_loading_icon();
                    setTimeout(add_conversion, 3000, json);
                };
            },
            error : function(xhr, errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    function add_conversion(json) {
        let convert_result = document.getElementById('convert-result');
        convert_result.style.opacity = 0;
        setTimeout(function(){
            const results = `
                            <div class="lower-bottom">
                                <h2>
                                    ${json['amount']} ${json['from']} = ${json['to']} ${json['result']}
                                </h2>
                                  <h5>
                                    1 ${json['from']} = ${json['rate']} ${json['to']}
                                </h5>
                                <br>
                                <br>
                            </div>
                            `;
            convert_result.innerHTML = results;
            convert_result.style.opacity = 1;
        },500)
    }

    function add_loading_icon(){
        let convert_result = document.getElementById('convert-result');
        const loader = `
                        <div class="pre-loading-icon">
                        </div>
                        `;
        convert_result.innerHTML = loader;
    }



});
