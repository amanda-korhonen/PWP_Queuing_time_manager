/*
Single connection layer between client and QueuingHub API
Code generated with Copilot generative AI and reviewed to fit our purpose. 

Prompt used:
// cut some information about our code structure//  
how to handle the api.js that would connect client to our API so it would have every helper function to connect to api

This instruction video was used as reference when coding: https://www.youtube.com/watch?v=lTpa6r-JBhk&t=338s
*/

// Central API configuration
// NOTE: this might need to change??
const API_BASE_URL = "http://127.0.0.1:5000/api";

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

  const text = await response.text();
  return text ? JSON.parse(text) : null;
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
export function updatePlace(place, data) {
  return apiFetch(`/places/${encodeURIComponent(place)}/`, {
    method: "PUT",
    body: JSON.stringify(data)
  });
}

// Create queue
export function createQueue(place, data) {
  return apiFetch(`/places/${encodeURIComponent(place)}/queues/`, {
    method: "POST",
    body: JSON.stringify(data)
  });
}

// Update queue
export function updateQueue(place, queueType, data) {
  return apiFetch(
    `/places/${encodeURIComponent(place)}/queues/${encodeURIComponent(queueType)}/`,
    {
      method: "PUT",
      body: JSON.stringify(data)
    }
  );
}