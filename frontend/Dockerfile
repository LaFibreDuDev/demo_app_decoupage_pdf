FROM node:22-alpine

WORKDIR /app

# Installer les dépendances dans l'image (avant le montage du volume source)
COPY package.json package-lock.json* ./
RUN npm install

# Le code source est monté en volume (dev).
# node_modules est protégé par un volume anonyme dans docker-compose.
CMD ["npm", "run", "dev", "--", "--host"]
