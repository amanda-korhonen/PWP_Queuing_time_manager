/*
Single connection layer between client and QueuingHub API
 * This module exposes helper functions for interacting with the backend API.
 * All public functions return Promises.

Code generated with Copilot generative AI and reviewed to fit our purpose. 

Prompt used:
// cut some information about our code structure//  
how to handle the api.js that would connect client to our API so it would have every helper function to connect to api

This instruction video was used as reference when coding: https://www.youtube.com/watch?v=lTpa6r-JBhk&t=338s
*/

// Central API configuration
const API_BASE_URL = "http://127.0.0.1:5000/api";


/**
 * Performs a fetch request to the backend API with common configuration.
 *
 * @param {string} endpoint - API endpoint path (e.g. "/places/").
 * @param {Object} [options={}] - Optional fetch configuration (method, headers, body, etc.).
 *
 * @returns {Promise<Object|null>} Parsed JSON response or null if response is empty.
 *
 * @throws {Error}
 * Thrown when the HTTP response status is not OK (status outside 200–299).
 * The error message includes the HTTP status code and server error text.
 *
 * @failure_handling
 * This error should be caught by the calling function using try/catch or .catch().
 */


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


/* =========================
   Locations
   ========================= */

/**
 * Fetches all available locations.
 *
 * @returns {Promise<Array>} List of locations.
 *
 * @throws {Error}
 * Propagated from apiFetch when the API call fails.
 */

export function getLocations() {
  return apiFetch("/locations/");
}

/**
 * Fetches all places for a specific location.
 *
 * @param {string} locationName - Name of the location.
 *
 * @returns {Promise<Array>} List of places within the location.
 *
 * @throws {Error}
 * Thrown when the location does not exist or the API is unreachable.
 */

export function getPlacesByLocation(locationName) {
  return apiFetch(`/locations/${encodeURIComponent(locationName)}/`);
}


/* =========================
   Places
   ========================= */

/**
 * Fetches all places from the system.
 *
 * @returns {Promise<Array>} List of all places.
 *
 * @throws {Error}
 * Thrown if the API request fails.
 */

export function getAllPlaces() {
  return apiFetch("/places/");
}

/**
 * Fetches a single place by name.
 *
 * @param {string} placeName - Name of the place.
 *
 * @returns {Promise<Object>} Place data object.
 *
 * @throws {Error}
 * Thrown if the place does not exist or the API call fails.
 */

export function getPlace(placeName) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/`);
}


/* =========================
   Queues
   ========================= */

/**
 * Fetches all queues for a given place.
 *
 * @param {string} placeName - Name of the place.
 *
 * @returns {Promise<Array>} List of queues for the place.
 *
 * @throws {Error}
 * Thrown if the place is invalid or the API call fails.
 */

export function getQueues(placeName) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/queues/`);
}

/**
 * Fetches a specific queue by type for a place.
 *
 * @param {string} placeName - Name of the place.
 * @param {string} queueType - Type of the queue.
 *
 * @returns {Promise<Object>} Queue data object.
 *
 * @throws {Error}
 * Thrown if the queue does not exist or the API request fails.
 */

export function getQueue(placeName, queueType) {
  return apiFetch(
    `/places/${encodeURIComponent(placeName)}/queues/${encodeURIComponent(queueType)}/`
  );
}

//Leons vibe code if it works it works

/* =========================
   Create / Update
   ========================= */

/**
 * Creates a new place.
 *
 * @param {Object} data - Place data (name, capacity, type, etc.).
 *
 * @returns {Promise<Object>} Created place data.
 *
 * @throws {Error}
 * Thrown if validation fails or the API rejects the request.
 */

export function createPlace(data) {
  return apiFetch("/places/", {
    method: "POST",
    body: JSON.stringify(data)
  });
}


/**
 * Updates an existing place.
 *
 * @param {string} place - Name of the place to update.
 * @param {Object} data - Updated place data.
 *
 * @returns {Promise<Object>} Updated place object.
 *
 * @throws {Error}
 * Thrown if the place does not exist or the update fails.
 */

export function updatePlace(place, data) {
  return apiFetch(`/places/${encodeURIComponent(place)}/`, {
    method: "PUT",
    body: JSON.stringify(data)
  });
}


/**
 * Creates a new queue for a place.
 *
 * @param {string} place - Name of the place.
 * @param {Object} data - Queue data (type, limits, etc.).
 *
 * @returns {Promise<Object>} Created queue data.
 *
 * @throws {Error}
 * Thrown if the queue data is invalid or request fails.
 */

export function createQueue(place, data) {
  return apiFetch(`/places/${encodeURIComponent(place)}/queues/`, {
    method: "POST",
    body: JSON.stringify(data)
  });
}


/**
 * Updates an existing queue.
 *
 * @param {string} place - Name of the place.
 * @param {string} queueType - Type of the queue to update.
 * @param {Object} data - Updated queue data.
 *
 * @returns {Promise<Object>} Updated queue data.
 *
 * @throws {Error}
 * Thrown if queue does not exist or update fails.
 */

export function updateQueue(place, queueType, data) {
  return apiFetch(
    `/places/${encodeURIComponent(place)}/queues/${encodeURIComponent(queueType)}/`,
    {
      method: "PUT",
      body: JSON.stringify(data)
    }
  );
}


/* =========================
   Delete
   ========================= */

/**
 * Deletes a place.
 *
 * @param {string} placeName - Name of the place to delete.
 *
 * @returns {Promise<void>} Resolves when deletion is successful.
 *
 * @throws {Error}
 * Thrown if place does not exist or deletion fails.
 */

export function deletePlace(placeName) {
  return apiFetch(`/places/${encodeURIComponent(placeName)}/`, {
    method: "DELETE"
  });
}

/**
 * Deletes a queue from a place.
 *
 * @param {string} placeName - Name of the place.
 * @param {string} queueType - Type of the queue to delete.
 *
 * @returns {Promise<void>} Resolves when deletion is successful.
 *
 * @throws {Error}
 * Thrown if the queue does not exist or deletion fails.
 */

export function deleteQueue(placeName, queueType) {
  return apiFetch(
    `/places/${encodeURIComponent(placeName)}/queues/${encodeURIComponent(queueType)}/`,
    {
      method: "DELETE"
    }
  );
}