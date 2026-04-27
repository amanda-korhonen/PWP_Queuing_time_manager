/*
A homepage for the QueuingHub, java script creates the logic of UI
Code generated with ChatGPT and reviewed to fit our purpose. 

Prompt used:
//First I gave api.js and snippets of readme where the examples 
of URL's that connect to resources are//

I need to do a home.js and home.html files, that acts as a homepage.
It has the QueuingHub-app's name as a big title, and has a list of locations and the places in that location.
When user (for example bar1) is clicked, another page is opened that is hadled by
establishment.js implemented by another teammate.
*/
import { getLocations } from "./api.js";

async function loadLocations() {
  const container = document.getElementById("locations-container");
  container.innerHTML = "Loading...";

  try {
    let locations = await getLocations();

    console.log("RAW locations:", locations);

    //handle string JSON (if api.js returns text sometimes)
    if (typeof locations === "string") {
      locations = JSON.parse(locations);
    }

    if (!locations || typeof locations !== "object") {
      throw new Error("Invalid API response format");
    }

    container.innerHTML = "";

    for (const [city, places] of Object.entries(locations)) {

      const cityDiv = document.createElement("div");
      cityDiv.className = "city";

      const title = document.createElement("h2");
      title.textContent = city;

      const list = document.createElement("ul");

      places.forEach(place => {
        const li = document.createElement("li");

        // safety fallback in case structure differs
        li.textContent = place.name ?? place;

        li.addEventListener("click", () => {
          const name = place.name ?? place;

          window.location.href =
            `establishment.html?place=${encodeURIComponent(name)}`;
        });

        list.appendChild(li);
      });

      cityDiv.appendChild(title);
      cityDiv.appendChild(list);
      container.appendChild(cityDiv);
    }

  } catch (err) {
    console.error("LOAD ERROR:", err);
    container.innerHTML = "Error loading locations";
  }
}

loadLocations();