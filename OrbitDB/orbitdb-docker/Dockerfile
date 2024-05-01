# Use an official Node runtime as a parent image
FROM node:21

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pwd

RUN echo "pr1inted!"

# Install any needed packages specified in package.json
# RUN npm i helia @orbitdb/core
# RUN npm i blockstore-level
RUN npm i
RUN npm install helia
RUN npm list helia

# Make ports available to the world outside this container
EXPOSE 4001 4002 4003

# Define environment variable
ENV NODE_ENV production

# Run the specified script when the container launches
CMD ["node", "mainPeer.js"] # Default command, can be overridden
