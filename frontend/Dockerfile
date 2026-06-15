# Use official Node runtime as a parent image
FROM node:18-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy project
COPY . .

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "run", "dev", "--", "--host"]
