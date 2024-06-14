# Build front
FROM node:lts-slim as build
WORKDIR /app
COPY front /app
RUN npm ci
RUN npm run build

# Run the runtime image
FROM python:3.8-slim as runtime
WORKDIR /app/back
# Use a non-root user
RUN adduser --disabled-password --gecos '' app
USER app
# Install dependencies
COPY back/requirements.txt .
ENV PATH=/home/app/.local/bin:$PATH
RUN pip install -r requirements.txt
# Copy the back
COPY back .
# Copy the built front
COPY --from=build /app/dist /app/front/dist
# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000