# Use a Debian-based Node image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package files first to optimize caching
COPY package*.json ./

# Install dependencies with no cache to prevent issues
RUN npm install --no-cache

# Install Playwright dependencies
RUN apt update && apt install -y libnss3 libatk1.0-0 libx11-xcb1 libdrm2
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
# Install Playwright Chrome binary
RUN npx playwright install chrome

# Copy the rest of the MCP code into the container
COPY . .

# Expose the MCP port inside the container
EXPOSE 8931

# Run the MCP server in headless mode
CMD ["npx", "@playwright/mcp@latest", "--port", "8931", "--headless"]