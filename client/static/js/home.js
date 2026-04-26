/*
A homepage for the QueuingHub, java script creates the logic of UI
Code generated with ChatGPT and reviewed to fit our purpose. 

Prompt used:
//First I gave api.js and snippets of readme where the examples 
of URL's that connect to resources are//

I need to do a home.js and home.html files, that acts as a homepage. 
It has the QueuingHub-app's name as a big title, and has a list of all users. 
When user (for example bar1) is clicked, another page is opened that is hadled by 
establishment.js implemented by another teammate.
*/
import { getLocations, getPlacesByLocation } from "./api.js";

async function loadLocations() {
  const container = document.getElementById("locations-container");

  try {
    const locations = await getLocations(); // e.g. ["City1", "City2"]

    container.innerHTML = "";

    for (const city of locations) {
      const places = await getPlacesByLocation(city);

      const cityDiv = document.createElement("div");
      cityDiv.className = "city";

      const title = document.createElement("h2");
      title.textContent = city;

      const placesList = document.createElement("ul");

      places.forEach(placeName => {
        const li = document.createElement("li");
        li.textContent = placeName;

        li.addEventListener("click", () => {
          window.location.href = `establishment.html?place=${encodeURIComponent(placeName)}`;
        });

        placesList.appendChild(li);
      });

      cityDiv.appendChild(title);
      cityDiv.appendChild(placesList);
      container.appendChild(cityDiv);
    }

  } catch (err) {
    container.innerHTML = "Error loading locations";
    console.error(err);
  }
}

loadLocations();