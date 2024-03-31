import { env } from '$env/dynamic/public';
// Function to fetch data from the API
export async function GET<T>(url: string): Promise<T> {
  try {
    const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching:', error);
    throw error;
  }
}

// Function to post data to the API
export async function POST<T, T1>(url: string, body: T): Promise<T1> {
  try {
    const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error posting:', error);
    throw error;
  }
}

// Function to post delete to the API
export async function DELETE(url: string): Promise<void> {
  try {
    const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
      method: 'DELETE'
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error posting:', error);
    throw error;
  }
}

// Function to post patch to the API
export async function PATCH<T>(url: string, body: T): Promise<void> {
  try {
    const response = await fetch(`${env.PUBLIC_BASE_URL}${url}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }
  } catch (error) {
    console.error('Error posting:', error);
    throw error;
  }
}