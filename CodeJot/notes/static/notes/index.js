document.addEventListener('DOMContentLoaded', function() 
    {
        const formele = document.querySelector("form");
        formele.onsubmit = () =>
        {
            const data = document.querySelector("#data").value; 
            console.log(data)

            let liele = document.createElement('li');
            liele.textContent = data;
            document.querySelector("ul").appendChild(liele);

            fetch('/addNote', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            document.querySelector("#data").value = "";

            return false;

        }

    });
