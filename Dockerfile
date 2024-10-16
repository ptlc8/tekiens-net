# Build front
FROM node:lts-slim AS build
WORKDIR /app

# Install dependencies
COPY front/package*.json ./
RUN npm ci

# Copy the code
COPY front .

# Build
RUN npm run build


# Run the runtime image
FROM python:3.12-slim AS runtime
WORKDIR /app/back

# Install dependencies
COPY back/requirements.txt ./
ENV PATH=/home/app/.local/bin:$PATH
RUN pip install --no-cache-dir -r requirements.txt

# Copy the back
COPY back/app ./app
COPY back/templates ./templates
COPY back/app.wsgi ./

# Copy sample data
#COPY back/data.sample ./data

# Copy the built front
COPY --from=build /app/dist /app/front/dist

# Use a non-root user
RUN adduser --disabled-password --gecos '' app

# Set ownership of the data folder to app user
RUN mkdir -p data
RUN chown -R app:app data

# Run the app
USER app
CMD ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
