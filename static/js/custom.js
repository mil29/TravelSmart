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

    // function to confirm country recent searches delete on profile page
    $(document).on('click', '.delete-btn', function(){
        return confirm('Are you sure you want to delete item?');
    })


    // changes colour of navbar mnu item when it has been selected 
    $(function(){
        $('a').each(function(){
            if ($(this).prop('href') == window.location.href) {
                $(this).addClass('active'); $(this).parents('li').addClass('active');
            }
        });
    });


    // function for travel-currency.html for select2 live search using option select and placing text from selected into innerhtml

    function formatState (state) {
        if (!state.id) {
            return state.text;
        }
        var baseUrl = "/static/img/flags";
        var $state = $(
            '<span><img src="{% static '+'"/\\img/\\flags/\\' + state.element.value.slice(0,3).toLowerCase() + '.png" %}" id="img-flag" /> ' + state.text + '</span>'
        );
        return $state;
    };



    let currency1 = document.getElementById('curr1');
    let currency2 = document.getElementById('curr2');
    let currencySymbol = document.getElementById('currency-sym');
    let imgFlag = document.getElementById('countryFlag');
    let imgFlag2 = document.getElementById('countryFlag2');
    let currencyInput = document.getElementById('currency-amount-input');

    // sets elements innerhtml to empty only if object is not null
    if (currency1 || currency2 !== null){
        currency1.innerHTML = '';
        currency2.innerHTML = '';
    };


    $('.currency-selector').select2({
        templateResult: formatState
    }).change(function(){
        //  getting the 3 letter currency abbreviation
        let selectCurrency = $('.currency-selector').val().slice(0,3);
        //  getting currency monetary symbol 
        let currency_sym = $('.currency-selector').val().slice(4);
        // add currency three letter symbol above select dropdown
        currency1.innerHTML = selectCurrency;
        // adding currency symbol next to currency amount input 
        currencySymbol.innerHTML = currency_sym;
        let countryFlag = document.getElementById('img-flag').src.slice(0, -7);
        imgFlag.innerHTML = `<img src='${countryFlag}${selectCurrency.toLowerCase()}.png'>`;
    });

    $('.currency-selector2').select2({
        templateResult: formatState
    }).change(function(){
        let selectCurrency2 = $('.currency-selector2').val().slice(0,3);
        // add currency three letter symbol above select dropdown
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
                curr1: $('.currency-selector').val().slice(0,3),
                curr2: $('.currency-selector2').val().slice(0,3),
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
                                <h2 class="result-text">
                                    ${json['amount']} <span class="result_highlight">${json['from']}</span> 
                                    <span class="result_equals_highlight">=</span> 
                                    <span class="result_highlight">${json['to']}</span> ${json['result']}
                                </h2>
                                  <h5 class="result-text">
                                    1 <span class="result_highlight">${json['from']}</span> 
                                    <span class="result_equals_highlight">=</span>  
                                    ${json['rate']} <span class="result_highlight">${json['to']}</span>  
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
                        <div class="lds-ripple"><div></div><div></div></div>
                        `;
        convert_result.innerHTML = loader;
    };

   

    // functions for places category options 
    // AJAX for getting new category options from buttons
    $(document).on('click', ".category_btn", function(e) {
        e.preventDefault();
        // toggles class checked onto only one button and switches off previously pressed button
        $('button').removeClass('checked');
        $(this).addClass('checked');

        //  gets the 2nd clas name from category_btn class which is the column number of the pressed button
        btn_column_number = $(this).attr('class').split(' ')[1];
        // console.log(btn_column_number);

        // console.log(catSelected);
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type : "POST", // http method
            url  : $('#category-form').attr("data-category-url"), // endpoint 'get-category' view
            data : {
                category_data: $(this).val(),
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success : function(json) {
                // console.log(json);
                add_category_options(json, btn_column_number);
            },
        });
    })

    //  4 results divs for each category of option buttons to be added dynamically
    let cat_result1 = document.getElementById('category_result1');
    let cat_result2 = document.getElementById('category_result2');
    let cat_result3 = document.getElementById('category_result3');
    let cat_result4 = document.getElementById('category_result4');
    // submit button which is hidden until final option button is pressed 
    let submit = document.getElementById('submit_category');
    let sub2_btns = document.querySelector('#sub2_category');

    function add_category_options(json, btn_column_number){
        console.log(json);
        // convert btn_column_number into INT
        let btn_number = parseInt(btn_column_number);

        if (json.hasOwnProperty('result')){

            submit.innerHTML = "";
            remove_buttons(btn_number);
            // loop to add buttons to page
            $.each(json['result'], function(index, value){
            let category_results = `
                <button type="submit" name="category_options" class="category_btn ${json['column_number']}" value="${value}" id="sub${btn_number+1}_category">${value}</button>
            `;
            if (json['top_cat_id'] != null){
                const submit_btn = `
                <button type="submit" name="get_cat_id" id="category-submit" class="form-submit" value="${json['top_cat_id']}-${json['category']}">Get Info</button>
                `;
                submit.innerHTML = submit_btn;
            };
            // add new options to correct results div based on btn number
            if (btn_number == 0){
                cat_result1.innerHTML += category_results;
            }
            if (btn_number == 1){
                cat_result2.innerHTML += category_results;
            }
            if (btn_number == 2){
                cat_result3.innerHTML += category_results;
            }
            if (btn_number == 3){
                cat_result4.innerHTML += category_results;
            }
            // always scroll to bottom of page as many options appear
        });
        window.scrollTo({top: document.body.scrollHeight, behaviour: 'smooth'});
            
        } else {
            remove_buttons(btn_number);
            const submit_btn = `
            <button type="submit" name="get_cat_id" id="category-submit" class="form-submit" value="${json['id']}-${json['category']}">Get Info</button>
            `;
            submit.innerHTML = submit_btn;
            window.scrollTo({ top: document.body.scrollHeight, behaviour: 'smooth'});
        }
    };

    // gets rid of any buttons after the selected button
    function remove_buttons(btn_number){
        if (btn_number == 0 && cat_result1.hasChildNodes()){
            cat_result1.innerHTML = "";
            cat_result2.innerHTML = "";
            cat_result3.innerHTML = "";
            cat_result4.innerHTML = "";
        }
        else if (btn_number == 1 && cat_result2.hasChildNodes()){
            cat_result2.innerHTML = "";
            cat_result3.innerHTML = "";
            cat_result4.innerHTML = "";
        }
        else if (btn_number == 2 && cat_result3.hasChildNodes()){
            cat_result3.innerHTML = "";
            cat_result4.innerHTML = "";
        }
        else if (btn_number == 3 && cat_result4.hasChildNodes()){
            cat_result4.innerHTML = "";
        }
    };


    // ajax to send category save button info to django views to save in db Places model 
    $(document).on('click', ".places-save", function(e) {
        e.preventDefault();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        // change button text and color after pressed
        $(this).text('saved');
        $(this).css('color', 'white')
        $(this).css('background-color', 'green').attr('disabled', true);
        // ajax call to save-place-result view sending form button value
        $.ajax({
            type : "POST", // http method
            url  : $('#places-save-form').attr("places-save-form-url"), // endpoint goes to "save_place_result" view in place_api.py
            data : {
                placeSave: $(this).val(),
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success : function(response) {
                if (response.result == 'already_saved'){
                    window.alert('Already saved in your Profile!')
                }
            },
        });
    })
  
});


