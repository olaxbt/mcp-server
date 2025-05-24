# MCP Server: Modern SDK Collection & Integration Platform

## Overview

MCP Server is a sophisticated Flask-based platform designed to bootstrap and consolidate multiple SDKs within a single server environment. It provides a unified interface for integrating various services and technologies through a collection of modular, extensible components organized as blueprints.

## Features

- **Modular Blueprint Architecture**: Easily integrate new SDKs with a structured, maintainable approach
- **Pre-configured SDK Integrations**:
  - WalletConnect integration for blockchain wallet interactions
  - Authentication system with JWT token support
  - File attachment handling with secure storage
- **Interactive API Documentation**: Auto-generated Swagger documentation for all endpoints
- **Cross-Origin Resource Sharing (CORS)**: Built-in support for cross-domain requests
- **Secure Authentication**: JWT-based authentication system
- **Developer-Friendly**: Clear organization makes extending functionality straightforward

## Tech Stack

- **Framework**: Flask
- **Documentation**: Flasgger (Swagger UI)
- **Authentication**: Flask-JWT-Extended
- **Logging**: Loguru
- **Security**: CORS support

## Project Structure

```
mcp-server/
├── app/
│   ├── routes/
│   │   ├── auth_routes/           # JWT authentication endpoints
│   │   ├── attachment_routes/     # File upload/download functionality  
│   │   ├── main_routes/           # Core application routes
│   │   ├── swagger_routes/        # API documentation
│   │   └── walletconnect_routes/  # Blockchain wallet integration
│   ├── static/                    # Static assets
│   └── templates/                 # HTML templates
├── config.ini                     # Configuration settings
├── requirements.txt               # Project dependencies
└── run.py                         # Application entry point
```

## Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/olaxbt/mcp-server.git
   cd mcp-server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   ```bash
   # Ensure config.ini has your JWT secret key configured
   ```

4. Run the server:
   ```bash
   python run.py
   ```

5. Access the Swagger UI documentation:
   ```
   http://localhost:5000/apidocs/
   ```

## Extending MCP Server

The blueprint-based architecture makes it easy to add new SDKs or services:

1. Create a new directory in `app/routes/` for your service
2. Define your SDK wrapper class to encapsulate the SDK functionality
3. Create a blueprint with your routes
4. Register your blueprint in `app/__init__.py`

## Use Cases

- **Blockchain Applications**: Leverage the WalletConnect integration for decentralized applications
- **Multi-API Gateway**: Create a unified interface for multiple third-party services
- **Microservice Aggregator**: Combine several microservices under a single API
- **Developer Tools**: Build and test against multiple SDKs in a controlled environment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to [https://github.com/olaxbt/mcp-server](https://github.com/olaxbt/mcp-server).

## License

Copyright (c) 2025 olaxbt

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by olaxbt 