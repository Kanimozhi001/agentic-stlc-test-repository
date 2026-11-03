"""Demo-only web application used to execute the repository's QA tests."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 3000
TOKEN = "demo-token"
PRODUCTS = [
    {"id": "P-101", "name": "Laptop Pro 14"},
    {"id": "P-102", "name": "Laptop Air 13"},
    {"id": "P-201", "name": "Phone Max"},
    {"id": "P-202", "name": "Phone Mini"},
    {"id": "P-301", "name": "Tablet Plus"},
]

PAGE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>QA demo application</title></head>
<body>
<main id="app"></main>
<script>
const TOKEN = "demo-token";
const app = document.querySelector("#app");
const path = window.location.pathname;
const formPage = (title, fields, button, script) => {
  app.innerHTML = `<h1>${title}</h1><form>${fields}<button type="submit">${button}</button></form>
    <p role="alert" hidden></p><p id="success" hidden></p>`;
  const form = app.querySelector("form");
  form.addEventListener("submit", async event => {
    event.preventDefault();
    await script(new FormData(form));
  });
};
const post = async (url, data) => fetch(url, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify(data)
});
const showError = message => {
  const alert = app.querySelector('[role="alert"]');
  alert.textContent = message;
  alert.hidden = false;
};
if (path === "/login") {
  formPage("Login", `
    <label>Username<input name="username" required></label>
    <label>Password<input name="password" type="password" required></label>`,
    "Login", async form => {
      const response = await post("/api/auth/login", {
        username: form.get("username"), password: form.get("password")
      });
      if (response.ok) window.location.href = "/home";
      else showError("Invalid username or password");
    });
} else if (path === "/register") {
  formPage("Register", `
    <label>Username<input name="username" required></label>
    <label>Email<input name="email" type="email" required></label>
    <label>Password<input name="password" type="password" required></label>`,
    "Register", async form => {
      const response = await post("/api/auth/register", {
        username: form.get("username"), email: form.get("email"),
        password: form.get("password")
      });
      if (response.ok) {
        const success = app.querySelector("#success");
        success.textContent = "Registration successful";
        success.hidden = false;
      } else showError("Registration failed");
    });
} else if (path === "/forgot-password") {
  formPage("Forgot password", `
    <label>Email<input name="email" required></label>`,
    "Send reset instructions", async form => {
      const response = await post("/api/auth/password-reset", {
        email: form.get("email")
      });
      const data = await response.json();
      if (response.ok) {
        const success = app.querySelector("#success");
        success.textContent = data.message;
        success.hidden = false;
      } else showError(data.error);
    });
} else if (path === "/profile") {
  app.innerHTML = `<h1>My Profile</h1>
    <label>Display name<input name="displayName" value="Demo User"></label>
    <button type="button">Save</button><p id="success" hidden></p>`;
  app.querySelector("button").addEventListener("click", async () => {
    const response = await fetch("/api/users/me", {
      method: "PATCH",
      headers: {"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN},
      body: JSON.stringify({displayName: app.querySelector("[name='displayName']").value})
    });
    if (response.ok) {
      const success = app.querySelector("#success");
      success.textContent = "Profile updated";
      success.hidden = false;
    }
  });
} else if (path === "/home") {
  app.innerHTML = `<h1>Home</h1><button type="button">Logout</button>`;
  app.querySelector("button").addEventListener("click", async () => {
    await fetch("/api/auth/logout", {
      method: "POST", headers: {"Authorization": "Bearer " + TOKEN}
    });
    window.location.href = "/login";
  });
} else if (path === "/") {
  app.innerHTML = `<h1>Product Search (Demo)</h1>
    <form id="searchForm">
      <label for="search">Product name</label>
      <input id="search" name="search" autocomplete="off">
      <button id="searchBtn" type="submit">Search</button>
    </form>
    <p class="search-validation" role="alert" hidden>Please enter a product name</p>
    <p class="no-results" hidden>No products found</p>
    <div class="search-results" aria-live="polite"></div>`;
  const form = app.querySelector("#searchForm");
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const query = app.querySelector("[name='search']").value.trim();
    const validation = app.querySelector(".search-validation");
    const noResults = app.querySelector(".no-results");
    const results = app.querySelector(".search-results");
    validation.hidden = true;
    noResults.hidden = true;
    results.replaceChildren();
    if (!query) {
      validation.hidden = false;
      return;
    }
    const response = await fetch(`/api/products/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    if (Array.isArray(data) && data.length) {
      for (const product of data) {
        const item = document.createElement("div");
        item.className = "product-item";
        item.textContent = product.name;
        results.appendChild(item);
      }
    } else {
      noResults.hidden = false;
    }
  });
} else {
  app.innerHTML = "<h1>QA demo application</h1>";
}
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return None

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        if path == "/api/users/me":
            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                self._send_json(401, {"error": "Unauthorized"})
            else:
                self._send_json(200, {"username": "demo_user", "displayName": "Demo User"})
            return
        if path == "/api/products/search":
            query = parse_qs(parsed.query).get("q", [""])[0].strip()
            if not query:
                self._send_json(400, {"error": "Search term is required"})
                return
            matches = [
                product for product in PRODUCTS
                if query.casefold() in product["name"].casefold()
            ]
            self._send_json(200, matches or {"message": "No products found"})
            return
        if path == "/" or path in {
            "/login", "/register", "/forgot-password", "/profile", "/home"
        }:
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        data = self._read_json()
        if data is None:
            self._send_json(400, {"error": "Invalid JSON"})
            return
        if path == "/api/auth/login":
            if data.get("username") == "demo_user" and data.get("password") == "DemoPass123!":
                self._send_json(200, {"token": TOKEN})
            else:
                self._send_json(401, {"error": "Invalid username or password"})
        elif path == "/api/auth/register":
            if data.get("email") == "existing@example.test":
                self._send_json(409, {"error": "Email already registered"})
            elif all(data.get(key) for key in ("username", "email", "password")):
                self._send_json(201, {"message": "Registration successful"})
            else:
                self._send_json(400, {"error": "Missing required fields"})
        elif path == "/api/auth/logout":
            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                self._send_json(401, {"error": "Unauthorized"})
            else:
                self._send_json(200, {"message": "Logged out"})
        elif path == "/api/auth/password-reset":
            email = data.get("email", "")
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                self._send_json(400, {"error": "Invalid email address"})
            else:
                self._send_json(
                    202,
                    {"message": "If the account exists, reset instructions will be sent"},
                )
        else:
            self._send_json(404, {"error": "Not found"})

    def do_PATCH(self):
        if urlparse(self.path).path != "/api/users/me":
            self._send_json(404, {"error": "Not found"})
            return
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self._send_json(401, {"error": "Unauthorized"})
            return
        data = self._read_json()
        if data is None:
            self._send_json(400, {"error": "Invalid JSON"})
        else:
            self._send_json(200, {"username": "demo_user", **data})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"QA demo app listening at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
