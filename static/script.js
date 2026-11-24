function verifyAge() {

    let dob = document.getElementById("dob").value;

    let birth = new Date(dob);

    let today = new Date();

    let age = today.getFullYear() -

    birth.getFullYear();

    if(age >= 18){

        document.getElementById(

            "agePopup"

        ).style.display = "none";

    }

    else{

        document.getElementById(

            "msg"

        ).innerHTML = "Access Denied";

    }
}


function recommendVehicle() {

    let env = document.getElementById(

        "environment"

    ).value;

    let budget = document.getElementById(

        "budget"

    ).value;

    let passengers = document.getElementById(

        "passengers"

    ).value;

    let cars = document.getElementById("cars");

    cars.innerHTML = "";


    let vehicleList = [];


    if(env == "city") {

        vehicleList.push({

            name: "Maruti Swift",

            image: "/static/images/swift.jpg",

            price: "₹2500/day"

        });
    }


    if(env == "hill") {

        vehicleList.push({

            name: "Mahindra Thar",

            image: "/static/images/thar.jpeg",

            price: "₹5000/day"

        });
    }


    if(env == "highway") {

        vehicleList.push({

            name: "Honda City",

            image: "/static/images/city.jpeg",

            price: "₹4000/day"

        });
    }


    if(env == "eco") {

        vehicleList.push({

            name: "Nexon EV",

            image: "/static/images/nexon.jpeg",

            price: "₹4500/day"

        });
    }


    if(passengers >= 6){

        vehicleList.push({

            name: "Toyota Innova",

            image: "/static/images/innova.jpeg",

            price: "₹6000/day"

        });
    }


    vehicleList.forEach(vehicle => {

        cars.innerHTML += `

        <div class="card">

            <img src="${vehicle.image}">

            <div class="card-content">

                <h3>${vehicle.name}</h3>

                <p>${vehicle.price}</p>

                <a href="/booking/${vehicle.name}">

                    <button class="btn">

                    Book Now

                    </button>

                </a>

            </div>

        </div>

        `;
    });
}