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

const backLink = document.getElementById("back-link");
const titleEl = document.getElementById("title");
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
  titleEl.textContent = isEdit
    ? "Edit Queue " + queueType + " of " + placeName
    : "Create New Queue for " + placeName;

    // NAVIGATION
  backLink.textContent = `Back to ${placeName}`;
  backLink.href = `../templates/establishment.html?place=${placeName}`;
} else {
  placeFields.style.display = "block";
  queueFields.style.display = "none";
  titleEl.textContent = isEdit
    ? "Edit Place " + placeName
    : "Create New Place";

    // NAVIGATION
  if (isEdit) {
    backLink.textContent = `Back to ${placeName}`;
    backLink.href = `../templates/establishment.html?place=${placeName}`;
  } else {
    backLink.style.display = "none";
  }
}

/* ---------------- HELPER FUNCTIONS: INPUT VALIDATION ---------------- */

function validateString(value, maxLength, fieldName) {
  if (!value || value.trim() === "") {
    throw new Error(`${fieldName} is required`);
  }
  if (value.length > maxLength) {
    throw new Error(`${fieldName} must be at most ${maxLength} characters`);
  }
  return value.trim();
}

function validateNumber(value, fieldName) {
  const num = Number(value);

  if (!Number.isInteger(num)) {
    throw new Error(`${fieldName} must be an integer`);
  }

  if (num < 0) {
    throw new Error(`${fieldName} must be positive`);
  }

  if (num > 10000) {
    throw new Error(`${fieldName} must be ≤ 10000`);
  }

  return num;
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
        name: validateString(document.getElementById("place-name").value, 20, "Name"),
        capacity: validateNumber(document.getElementById("capacity").value, "Capacity"),
        people_count: validateNumber(document.getElementById("place-people-count").value, "People count"),
        place_type: validateString(document.getElementById("place-type").value, 120, "Place type"),
        location: validateString(document.getElementById("location").value, 60, "Location")
      };

      if (isEdit) {
        await updatePlace(placeName, data);
      } else {
        await createPlace(data);
      }
    }

    if (type === "queue") {
      const data = {
        queue_type: validateString(document.getElementById("queue-type").value, 20, "Queue type"),
        people_count: validateNumber(document.getElementById("queue-people-count").value, "People count")
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