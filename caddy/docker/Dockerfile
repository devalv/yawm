FROM devalv/yawm-frontend:latest as builder

# ========= RUN =========
FROM caddy:2.4.6-alpine

COPY --from=builder /home/app/build /usr/share/caddy/html
