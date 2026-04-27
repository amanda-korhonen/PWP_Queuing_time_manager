import { getPlace, getQueues } from "./api.js";

/**
 * Extracts the "place" parameter from the page URL.
 *
 * @returns {string|null} Place name if present, otherwise null.
 *
 * @failure_case
 * Returns null if the URL parameter is missing.
 * The caller must handle this case.
 */
function getPlaceFromURL() {
  var params = new URLSearchParams(window.location.search);
  return params.get("place");
}


/**
 * Renders place details and queue list into the DOM.
 *
 * @param {Object} data - Combined place and queue data.
 *
 * @throws {Error}
 * Runtime errors may occur if required DOM elements are missing.
 *
 * @failure_handling
 * Ensure required HTML elements exist before calling this function.
 */

function render(data) {
  var placeList = document.getElementById("place-details");
  var list = document.getElementById("places-list");
  var i;
  var q;
  var li;

  placeList.innerHTML = "";
  list.innerHTML = "";

  var placeAttributes = [
    { label: "Type", value: data.place_type },
    { label: "Capacity", value: data.capacity },
    { label: "People count", value: data.people_count },
    { label: "Fullness", value: data.fullness },
  ];

  // List attributes
  placeAttributes.forEach(function(attribute) {
    li = document.createElement("li");
    li.textContent = attribute.label + ": " + (attribute.value || "N/A");
    placeList.appendChild(li);
  });

  // List queues
  if (data.queues && data.queues.length > 0) {
    for (i = 0; i < data.queues.length; i += 1) {
      q = data.queues[i];

      li = document.createElement("li");
      li.textContent = q.queue_type + " (" + (q.people_count || 0) + ")";

      li.addEventListener("click", (function(currentQueue) {
        return function() {
          window.location.href =
            `edit.html?type=queue&place=${encodeURIComponent(data.name)}&queue=${encodeURIComponent(currentQueue.queue_type)}`;
        };
      })(q));  // Immediately invoked function expression to pass the current 'q'

      list.appendChild(li);
    }
  } else {
    li = document.createElement("li");
    li.textContent = "No queues available";
    list.appendChild(li);
  }
}

/**
 * Initializes the page by loading place and queue data.
 *
 * @returns {Promise<void>}
 *
 * @throws {Error}
 * Thrown if API calls fail or required URL parameters are missing.
 *
 * @failure_handling
 * Errors are logged to the console; application remains stable.
 */

async function init() {
  var placeName;
  var results;
  var place;
  var queues;
  var title;
  var description;
  var editBtn;
  var createBtn;

  placeName = getPlaceFromURL();

  if (!placeName) {
    console.error("Missing place in URL");
    return;
  }

  try {
    results = await Promise.all([
      getPlace(placeName),
      getQueues(placeName)
    ]);

    place = results[0];
    queues = results[1];

    title = document.getElementById("app-title");
    title.textContent = placeName;

    description = document.getElementById("app-description");
    description.textContent = `Queues for: ${placeName || "unknown"}`;

    editBtn = document.getElementById("editButton");
    if (editBtn && placeName) {
      editBtn.href = "../templates/edit.html?type=place&place=" +
        encodeURIComponent(placeName);
    }

    createBtn = document.getElementById("createQueueButton");
    if (createBtn && placeName) {
      createBtn.href = "../templates/create.html?type=queue&place=" +
        encodeURIComponent(placeName);
    }


    render({
      name: place.name,
      capacity: place.capacity,
      people_count: place.people_count,
      fullness: place.fullness,
      place_type: place.place_type,
      queues: queues
    });

  } catch (err) {
    console.error("Failed to load establishment:", err);
  }
}

init();
