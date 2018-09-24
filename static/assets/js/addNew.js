console.log('okay seen')
$('#form').submit(function (e) {
    var form_data = {
        name: $('#name')[0].value,
        email: $('#email')[0].value,
        hours: $('#hours')[0].value,
        space: $('#space')[0].value,
        date: $('#date')[0].value,
        time: $('#time')[0].value,
    }

    for (i = 0; i < Object.keys(form_data).length; i++) {        
        if (form_data[i] === '') {
            console.log(form_data[i], 'false')
        }
        console.log(form_data[i])
    }
    return false

    var time = form_data.time;
    if (time.length > 5) {
        alert('time not that long')
        alert('ohh and please right click and click on inspect element.')
        console.log('fuck you!!!!!!')

        return false
    }

    for (var i = 0; i < time.length; i++) {
        if ((isNaN(time[i]) === true) && (time[i] !== ':')) {
            alert('Enter valid time!!')
            alert('ohh and please right click and click on inspect element.')
            console.log('fuck you!!!!!!')
            return false
        }
    }
    return true
})
var timepicker = new TimePicker('time', {
    lang: 'en',
    theme: 'dark'
});
timepicker.on('change', function (evt) {
    var value = (evt.hour || '00') + ':' + (evt.minute || '00');
    evt.element.value = value;
})
