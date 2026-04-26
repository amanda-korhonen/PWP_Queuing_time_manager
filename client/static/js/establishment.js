import { getPlace, getQueues } from "./api.js";

function getPlaceFromURL() {
  var params = new URLSearchParams(window.location.search);
  return params.get("place");
}

function render(data) {
  var list = document.getElementById("places-list");
  var i;
  var q;
  var li;

  list.innerHTML = "";

  if (data.queues && data.queues.length > 0) {
    for (i = 0; i < data.queues.length; i += 1) {
      q = data.queues[i];

      li = document.createElement("li");
      li.textContent = q.queue_type + " (" + (q.people_count || 0) + ")";
      list.appendChild(li);
    }
  } else {
    li = document.createElement("li");
    li.textContent = "No queues available";
    list.appendChild(li);
  }
}

async function init() {
  var placeName;
  var results;
  var place;
  var queues;
  var title;
  var description;
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
    title.textContent = place.name;

    description = document.getElementById("app-description");
    description.textContent = `Queues for: ${place.name || "unknown"}`;

    createBtn = document.getElementById("createQueueButton");
    if (createBtn && placeName) {
      createBtn.href = "../templates/create.html?type=queue&place=" +
        encodeURIComponent(placeName);
    }

    render({
      name: place.name,
      queues: queues
    });

  } catch (err) {
    console.error("Failed to load establishment:", err);
  }
}

init();
