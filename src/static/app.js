document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  
  // Auth elements
  const loginButton = document.getElementById("login-button");
  const logoutButton = document.getElementById("logout-button");
  const userInfoSpan = document.getElementById("user-info");
  const loginModal = document.getElementById("login-modal");
  const closeModal = document.querySelector(".close");
  const loginForm = document.getElementById("login-form");
  const loginMessageDiv = document.getElementById("login-message");
  
  // Calculator elements
  const calculatorContainer = document.getElementById("calculator-container");
  const calculatorForm = document.getElementById("calculator-form");
  const calculatorResult = document.getElementById("calculator-result");
  const resultValue = document.getElementById("result-value");
  
  // Auth state
  let authToken = localStorage.getItem("auth_token");
  let currentUser = null;
  
  // Auth functions
  const updateAuthUI = () => {
    if (authToken) {
      loginButton.classList.add("hidden");
      logoutButton.classList.remove("hidden");
      calculatorContainer.classList.remove("hidden");
      
      // Get and display user info
      if (currentUser) {
        userInfoSpan.textContent = `Logged in as ${currentUser.username}`;
      } else {
        fetchUserInfo();
      }
    } else {
      loginButton.classList.remove("hidden");
      logoutButton.classList.add("hidden");
      calculatorContainer.classList.add("hidden");
      userInfoSpan.textContent = "Not logged in";
    }
  };
  
  const fetchUserInfo = async () => {
    if (!authToken) return;
    
    try {
      const response = await fetch("/users/me", {
        headers: {
          "Authorization": `Bearer ${authToken}`
        }
      });
      
      if (response.ok) {
        currentUser = await response.json();
        userInfoSpan.textContent = `Logged in as ${currentUser.username}`;
      } else {
        // Token might be invalid
        localStorage.removeItem("auth_token");
        authToken = null;
        updateAuthUI();
      }
    } catch (error) {
      console.error("Error fetching user info:", error);
    }
  };
  
  // Open login modal
  loginButton.addEventListener("click", () => {
    loginModal.classList.remove("hidden");
  });
  
  // Close login modal
  closeModal.addEventListener("click", () => {
    loginModal.classList.add("hidden");
  });
  
  // Close modal when clicking outside
  window.addEventListener("click", (event) => {
    if (event.target === loginModal) {
      loginModal.classList.add("hidden");
    }
  });
  
  // Handle login
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    try {
      const response = await fetch("/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
      });
      
      const result = await response.json();
      
      if (response.ok) {
        // Store token and update UI
        authToken = result.access_token;
        localStorage.setItem("auth_token", authToken);
        
        loginMessageDiv.textContent = "Login successful!";
        loginMessageDiv.className = "success";
        loginMessageDiv.classList.remove("hidden");
        
        setTimeout(() => {
          loginModal.classList.add("hidden");
          loginForm.reset();
          loginMessageDiv.classList.add("hidden");
        }, 1500);
        
        fetchUserInfo();
        updateAuthUI();
      } else {
        loginMessageDiv.textContent = result.detail || "Login failed. Please try again.";
        loginMessageDiv.className = "error";
        loginMessageDiv.classList.remove("hidden");
      }
    } catch (error) {
      loginMessageDiv.textContent = "Login failed. Please try again.";
      loginMessageDiv.className = "error";
      loginMessageDiv.classList.remove("hidden");
      console.error("Error during login:", error);
    }
  });
  
  // Handle logout
  logoutButton.addEventListener("click", () => {
    localStorage.removeItem("auth_token");
    authToken = null;
    currentUser = null;
    updateAuthUI();
  });
  
  // Handle calculator
  calculatorForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const expression = document.getElementById("expression").value;
    
    try {
      const response = await fetch(`/calculate?expression=${encodeURIComponent(expression)}`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${authToken}`
        }
      });
      
      const result = await response.json();
      
      if (response.ok) {
        resultValue.textContent = result.result;
        calculatorResult.classList.remove("hidden");
      } else {
        resultValue.textContent = `Error: ${result.detail}`;
        calculatorResult.classList.remove("hidden");
      }
    } catch (error) {
      resultValue.textContent = "Error calculating expression";
      calculatorResult.classList.remove("hidden");
      console.error("Error using calculator:", error);
    }
  });

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle activity signup form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
  updateAuthUI();
});
