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

import { getAllPlaces } from "./api.js";

const placesList = document.getElementById("places-list");

async function loadPlaces() {
  try {
    const places = await getAllPlaces();

    // Clear list just in case
    placesList.innerHTML = "";

    places.forEach(place => {
      const li = document.createElement("li");

      // Adjust depending on your API response shape
      const placeName = place.name;

      li.textContent = placeName;
      li.classList.add("place-item");

      li.addEventListener("click", () => {
        // Navigate to establishment page
        window.location.href = `establishment.html?place=${encodeURIComponent(placeName)}`;
      });

      placesList.appendChild(li);
    });

  } catch (error) {
    console.error("Failed to load places:", error);
    placesList.innerHTML = "<li>Error loading places</li>";
  }
}

// Run on page load
loadPlaces();