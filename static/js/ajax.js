function format_numbers(numbers){
    let entry = {
        elements : []
    };

    for (let i =0; i < numbers.length; i++){
        entry['elements'].push(
            {
                id : numbers[i].id,
                value  : numbers[i].value ? numbers[i].value : 0
            });
    }
    let msg_log = "FETCH: " + entry;

    fetch(format_numbers_url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function (response){
        if (response.status !== 200){
            console.log('Response status was not 200:', msg_log);
            return;
        }
        response.json().then(function (data){

            for (let i =0; i < numbers.length; i++){
                let element = document.getElementById(data[i].id);
                element.value = data[i].value;
            }

        });
    });
}
