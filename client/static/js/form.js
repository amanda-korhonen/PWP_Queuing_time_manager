import {
  getPlace,
  getQueue,
  createPlace,
  updatePlace,
  createQueue,
  updateQueue
} from "./api.js";

const params = new URLSearchParams(window.location.search);

const type = params.get("type"); // "place" | "queue"
const placeName = params.get("place");
const queueType = params.get("queue");

const isEdit = window.location.pathname.includes("edit");

console.log("TYPE:", type);
console.log("PLACE:", placeName);
console.log("QUEUE:", queueType);
console.log("EDIT:", isEdit);

/* ---------------- DOM ---------------- */

const placeFields = document.getElementById("place-fields");
const queueFields = document.getElementById("queue-fields");

/* ---------------- UI TOGGLE ---------------- */

if (type === "queue") {
  placeFields.style.display = "none";
  queueFields.style.display = "block";
} else {
  placeFields.style.display = "block";
  queueFields.style.display = "none";
}

/* ---------------- PREFILL ---------------- */

async function prefill() {
  if (!isEdit) return;

  if (type === "queue" && !queueType) {
    alert("Missing queue type in URL");
    return;
  }

  try {
    if (type === "place") {
        const place = await getPlace(placeName);
        console.log("PLACE DATA:", place);
        console.log("place-name element:", document.getElementById("place-name"));
        console.log("capacity element:", document.getElementById("capacity"));
        console.log("place-people-count element:", document.getElementById("place-people-count"));

        document.getElementById("place-name").value = place.name;
        document.getElementById("capacity").value = place.capacity;
        document.getElementById("place-people-count").value = place.people_count;
        document.getElementById("place-type").value = place.place_type;
        document.getElementById("location").value = place.location;
      }

    if (type === "queue") {
      const queue = await getQueue(placeName, queueType);
      console.log("QUEUE DATA:", queue);
      console.log("queue-type element:", document.getElementById("queue-type"));
      console.log("queue-people-count element:", document.getElementById("queue-people-count"));

      document.getElementById("queue-type").value = queue.queue_type;
      document.getElementById("queue-people-count").value = queue.people_count || "";
    }
  } catch (err) {
    console.error(err);
    alert("Failed to load data");
  }
}

/* ---------------- SUBMIT ---------------- */

document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  try {
    if (type === "place") {
      const data = {
        name: document.getElementById("place-name").value,
        capacity: Number(document.getElementById("capacity").value),
        people_count: Number(document.getElementById("place-people-count").value),
        place_type: document.getElementById("place-type").value,
        location: document.getElementById("location").value
      };

      if (isEdit) {
        await updatePlace(placeName, data);
      } else {
        await createPlace(data);
      }
    }

    if (type === "queue") {
      const data = {
        queue_type: document.getElementById("queue-type").value,
        people_count: Number(document.getElementById("queue-people-count").value)
      };

      if (isEdit) {
        await updateQueue(placeName, queueType, data);
      } else {
        await createQueue(placeName, data);
      }
    }

    window.location.href = "../templates/home.html";
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
});

prefill();