FROM node:lts-alpine as builder

WORKDIR /opt/yawm/frontend
ADD ./frontend/ ./
RUN npm install
RUN npm run build

# ========= RUN =========
FROM caddy:2.4.6-alpine

COPY --from=builder /opt/yawm/frontend/build /usr/share/caddy/html
