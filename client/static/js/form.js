import {
  getPlace,
  getQueue,
  createPlace,
  updatePlace,
  createQueue,
  updateQueue
} from './api.js';

const params = new URLSearchParams(window.location.search);

const type = params.get('type'); 
// "place" or "queue"

const placeName = params.get('place');
const queueType = params.get('queue');
const isEdit = !!params.get('edit'); // ?edit=true

// Form elements
const form = document.getElementById('form');
const nameInput = document.getElementById('name');
const extraInput = document.getElementById('extra'); 
// e.g. queue size or description

// --- Prefill for edit ---
async function prefill() {
  if (!isEdit) return;

  try {
    if (type === 'place') {
      const place = await getPlace(placeName);
      nameInput.value = place.name;
    }

    if (type === 'queue') {
      const queue = await getQueue(placeName, queueType);
      nameInput.value = queue.name;
      extraInput.value = queue.size || '';
    }

  } catch (err) {
    console.error("Prefill failed:", err);
  }
}

// --- Submit handler ---
async function handleSubmit(e) {
  e.preventDefault();

  const data = {
    name: nameInput.value
  };

  if (type === 'queue') {
    data.size = extraInput.value;
  }

  try {
    if (type === 'place') {
      if (isEdit) {
        await updatePlace(placeName, data);
      } else {
        await createPlace(data);
      }
    }

    if (type === 'queue') {
      if (isEdit) {
        await updateQueue(placeName, queueType, data);
      } else {
        await createQueue(placeName, data);
      }
    }

    // Redirect after success
    window.location.href = 'home.html';

  } catch (err) {
    alert("Error: " + err.message);
  }
}

form.addEventListener('submit', handleSubmit);

prefill();