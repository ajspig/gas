const form = document.getElementById("submit_form")
const predictions_div = document.getElementById("predictions")

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const formData = new FormData(form);
    console.log(formData.get("location"))

    const response = await fetch("https://rs1yn1si37.execute-api.us-west-1.amazonaws.com/prod/get-data", {
        method: "POST",
        body: JSON.stringify({"location": "New York City"})
    })
    let json = await response.json()
    console.log(json.body)
    
    table = "\
    <table>                             \
        <thead>                         \
            <th>Date</th>               \
            <th>Price</th>              \
        </thead>                        \
        <tbody>"

    for (let item of json.body) {
        console.log(item)
        table += "\
            <tr>                                        \
                <td>" + item.date + "</td>        \
                <td>" + item.price + "</td>  \
            </tr>"
    }
    table += "  \
        </tbody>\
    </table>"

    predictions_div.innerHTML = table
})

