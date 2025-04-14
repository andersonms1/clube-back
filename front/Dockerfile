# Build Stage 1

FROM node:22-alpine AS build

WORKDIR /app

# Enable pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

# Copy package.json and your lockfile, here we add pnpm-lock.yaml for illustration
# COPY package.json package-lock.json ./
# COPY package.json ./
COPY ./package.json /app/
COPY ./pnpm-lock.yaml /app/

# Install dependencies
RUN pnpm install --shamefully-hoist

# Copy the entire project
COPY . ./

# Build the project
# RUN npm run build
RUN pnpm run build


# Build Stage 2

FROM node:22-alpine
WORKDIR /app

# Only `.output` folder is needed from the build stage
COPY --from=build /app/.output/ ./

# Change the port and host
ENV PORT=80
ENV HOST=0.0.0.0

EXPOSE 80

CMD ["node", "/app/server/index.mjs"]
