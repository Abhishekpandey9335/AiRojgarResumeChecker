import { API_URL } from "./config";

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_URL}/api${path}`, options);
  } catch {
    throw new Error("Cannot reach the server. Please check that the backend is running and try again.");
  }
  let data = null;
  try {
    data = await response.json();
  } catch {
    /* no JSON body */
  }
  if (!response.ok) {
    const message = (data && (data.detail || data.error)) || `Request failed (${response.status}). Please try again.`;
    throw new Error(message);
  }
  return data;
}

export const getBranches = () => request("/branches/");
export const getRoles = (branch) => request(`/roles/?branch=${encodeURIComponent(branch)}`);
export const getRole = (id) => request(`/roles/${id}/`);
export const getAnalysis = (id) => request(`/analyses/${id}/`);

export function analyzeResume({ file, roleId, branch }) {
  const form = new FormData();
  form.append("resume", file);
  form.append("role_id", roleId);
  form.append("branch", branch);
  return request("/analyze/", { method: "POST", body: form });
}
