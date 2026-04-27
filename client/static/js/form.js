/*
This file contains the logic for the create/edit form used for both places and queues.
 * It supports both creation and editing based on URL parameters.

ChatGPT was used to generate the base code which was then modified to fit our purpose.

Prompt used:
we have an api and want to do a separate html client that a user can use to view edit
and create content. We want a javascript file for the form page that would handle both
creating and editing of places and queues.

This instruction video was used as reference when coding: https://www.youtube.com/watch?v=lTpa6r-JBhk&t=338s
*/
import {
  getPlace,
  getQueue,
  createPlace,
  updatePlace,
  createQueue,
  updateQueue,
  deletePlace,
  deleteQueue
} from "./api.js";

/* =========================
   URL PARAMETERS
   ========================= */

const params = new URLSearchParams(window.location.search);

const type = params.get("type"); // "place" | "queue"
const placeName = params.get("place");
const queueType = params.get("queue");

/* =========================
   DOM REFERENCES
   ========================= */

const backLink = document.getElementById("back-link");
const titleEl = document.getElementById("title");
const isEdit = window.location.pathname.includes("edit");


const deleteBtn = document.getElementById("delete-btn");

console.log("TYPE:", type);
console.log("PLACE:", placeName);
console.log("QUEUE:", queueType);
console.log("EDIT:", isEdit);


/* ---------------- DOM ---------------- */

const placeFields = document.getElementById("place-fields");
const queueFields = document.getElementById("queue-fields");

/* ---------------- UI TOGGLE ---------------- */

/**
 * Shows or hides form sections and configures navigation
 * depending on whether the user edits/creates a place or queue.
 *
 * @failure_handling
 * Assumes required DOM elements exist.
 */

if (type === "queue") {
  placeFields.style.display = "none";
  queueFields.style.display = "block";

  titleEl.textContent = isEdit
    ? "Edit Queue " + queueType + " of " + placeName
    : "Create New Queue for " + placeName;

  // NAVIGATION
  backLink.style.display = "inline";
  backLink.textContent = `Back to ${placeName}`;
  backLink.href = `../templates/establishment.html?place=${placeName}`;

} else {
  placeFields.style.display = "block";
  queueFields.style.display = "none";

  titleEl.textContent = isEdit
    ? "Edit " + placeName
    : "Create New Place";

  // NAVIGATION
  if (isEdit) {
    backLink.style.display = "inline";
    backLink.textContent = `Back to ${placeName}`;
    backLink.href = `../templates/establishment.html?place=${placeName}`;
  } else {
    backLink.style.display = "none";
  }
}

/* ---------------- HELPER FUNCTIONS: INPUT VALIDATION ---------------- */

/**
 * Validates a string input field.
 *
 * @param {string} value - The input value.
 * @param {number} maxLength - Maximum allowed length.
 * @param {string} fieldName - Name used in error messages.
 *
 * @returns {string} Trimmed valid string.
 *
 * @throws {Error}
 * Thrown if value is empty or exceeds maxLength.
 */

function validateString(value, maxLength, fieldName) {
  if (!value || value.trim() === "") {
    throw new Error(`${fieldName} is required`);
  }
  if (value.length > maxLength) {
    throw new Error(`${fieldName} must be at most ${maxLength} characters`);
  }
  return value.trim();
}


/**
 * Validates a numeric input field.
 *
 * @param {string} value - Raw input string.
 * @param {string} fieldName - Name used in error messages.
 *
 * @returns {number} Validated integer.
 *
 * @throws {Error}
 * Thrown if value is not a positive integer or exceeds limits.
 */

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

/* ---------------- DELETE ---------------- */

/**
 * Handles deletion of either a place or queue.
 *
 * @returns {Promise<void>}
 *
 * @throws {Error}
 * Thrown if the API delete request fails.
 *
 * @failure_handling
 * User confirmation is required before deletion.
 * Errors are reported via alert and console.
 */

if (deleteBtn) {
  deleteBtn.addEventListener("click", async () => {
    if (!confirm("Delete this " + (type === "queue" ? "queue?" : "place?"))) return;

    try {
      if (type === "queue") {
        await deleteQueue(placeName, queueType);
      } else {
        await deletePlace(placeName);
      }
      window.location.href = "../templates/home.html";
    } catch (err) {
      console.error(err);
      alert("Failed to delete " + (type === "queue" ? "queue" : "place"));
    }
  });
}

/* ---------------- PREFILL ---------------- */

/**
 * Prefills the form fields when editing an existing place or queue.
 *
 * @returns {Promise<void>}
 *
 * @throws {Error}
 * Thrown if API request fails or required URL parameters are missing.
 */

async function prefill() {
  if (!isEdit) return;

  if (type === "queue" && !queueType) {
    alert("Missing queue type in URL");
    return;
  }

  try {
    if (type === "place") {
        const place = await getPlace(placeName);
        document.getElementById("place-name").value = place.name;
        document.getElementById("capacity").value = place.capacity;
        document.getElementById("place-people-count").value = place.people_count;
        document.getElementById("place-type").value = place.place_type;
        document.getElementById("location").value = place.location;
      }

    if (type === "queue") {
      const queue = await getQueue(placeName, queueType);
      document.getElementById("queue-type").value = queue.queue_type;
      document.getElementById("queue-people-count").value = queue.people_count || "";
    }
  } catch (err) {
    console.error(err);
    alert("Failed to load data");
  }
}

/* ---------------- SUBMIT ---------------- */

/**
 * Handles form submission for creating or updating a place or queue.
 *
 * @param {Event} e - Submit event.
 *
 * @throws {Error}
 * Thrown when validation or API operations fail.
 *
 * @failure_handling
 * Error messages are shown to the user via error box.
 */


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
    document.getElementById("error-box").textContent = err.message;
  }
});

prefill();
