export const sendCommand = async (type: string, params: object = {}) => {
  try {
    const response = await fetch("/api/control", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ...params, type: type }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error("Failed to send command:", error);
      return;
    }
  } catch (error) {
    console.error("Error sending command:", error);
  } finally {
  }
};
