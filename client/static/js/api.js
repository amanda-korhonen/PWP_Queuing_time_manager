/*
Single connection layer between client and QueuingHub API
Code generated with Copilot generative AI and reviewed to fit our purpose. 

Prompt used:
// cut some information about our code structure//  
how to handle the api.js that would connect client to our API so it would have every helper function to connect to api
*/

// Central API configuration
// NOTE: this might need to change??
const API_BASE_URL = "";

async function apiFetch(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${errorText}`);
  }

  return response.json();
}

// Locations
export function getLocations() {
  return apiFetch("/locations/");
}

export function getPlacesByLocation(locationName) {
  return apiFetch(`/locations/${encodeURIComponent(locationName)}/`);
}

// Places
export function getAllPlaces() {
  return apiFetch("/places/");
}

export function getPlace(placeName) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/`);
}

// Queues
export function getQueues(placeName) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/queues/`);
}

export function getQueue(placeName, queueType) {
  return apiFetch(
    `/places/${encodeURIComponent(placeName)}/queues/${encodeURIComponent(queueType)}/`
  );
}


//Leons vibe code if it works it works
// Create place
export function createPlace(data) {
  return apiFetch("/places/", {
    method: "POST",
    body: JSON.stringify(data)
  });
}

// Update place
export function updatePlace(placeName, data) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/`, {
    method: "PUT",
    body: JSON.stringify(data)
  });
}

// Create queue
export function createQueue(placeName, data) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/queues/`, {
    method: "POST",
    body: JSON.stringify(data)
  });
}

// Update queue
export function updateQueue(placeName, queueType, data) {
  return apiFetch(
    `/places/${encodeURIComponent(placeName)}/queues/${encodeURIComponent(queueType)}/`,
    {
      method: "PUT",
      body: JSON.stringify(data)
    }
  );
}