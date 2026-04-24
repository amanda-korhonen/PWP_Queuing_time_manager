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

async function apiFetch(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);

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
