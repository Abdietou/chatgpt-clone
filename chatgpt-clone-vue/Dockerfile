# Base image
FROM node:16.17.0

# Set working directory
WORKDIR /app

# Copy the source code into the container
COPY . .

# Install dependencies
RUN npm install

EXPOSE 8080

# Start the Vue app
CMD ["npm", "run", "serve"]