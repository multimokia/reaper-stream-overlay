import { io, Socket } from "socket.io-client";

export const socket: Socket = io("http://127.0.0.1:5000");
