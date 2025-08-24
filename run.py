#!/usr/bin/env python3
import asyncio
import uvicorn
from app.mcp.server import MCPServer

async def main():
    server = MCPServer()
    await server.start()

if __name__ == "__main__":
    uvicorn.run(
        "app.mcp.server:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
