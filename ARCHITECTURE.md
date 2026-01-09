# Architecture Documentation

## Overview

Convertify 2.0 implements **Clean Architecture** (also known as Hexagonal Architecture or Ports and Adapters), which provides a clear separation of concerns and makes the codebase highly maintainable and testable.

## Layers

### 1. Domain Layer (`src/domain/`)

The innermost layer containing business entities and interfaces. This layer has **no dependencies** on external frameworks or libraries.

#### Entities (`entities.py`)

- `VideoFile`: Represents a video file with metadata
- `ConversionResult`: Represents the outcome of a conversion
- `ConversionConfig`: Configuration for video conversion
- `VideoFormat`: Enum for supported formats
- `ConversionStatus`: Enum for conversion states

#### Interfaces (`interfaces.py`)

- `IVideoConverter`: Contract for video conversion
- `IFileRepository`: Contract for file operations
- `ILogger`: Contract for logging

#### Exceptions (`exceptions.py`)

- Custom exception hierarchy for domain errors

### 2. Infrastructure Layer (`src/infrastructure/`)

Implements the interfaces defined in the domain layer using external libraries and frameworks.

#### Implementations

- `MoviePyVideoConverter`: Video conversion using MoviePy
- `FileSystemRepository`: File operations using pathlib and Windows API
- `LoguruLogger`: Logging using Loguru library

### 3. Application Layer (`src/application/`)

Contains business logic and use cases that orchestrate the domain and infrastructure layers.

#### Services

- `VideoConversionService`: Orchestrates video conversion with retry logic
- `FileDiscoveryService`: Discovers video files in directories

#### Use Cases

- `ConvertVideosUseCase`: Main use case for batch video conversion

### 4. Presentation Layer (`main.py`)

The CLI interface built with Typer and Rich.

## Dependency Flow

```
Presentation → Application → Domain ← Infrastructure
```

- **Presentation** depends on Application
- **Application** depends on Domain
- **Infrastructure** depends on Domain
- **Domain** depends on nothing

This ensures that business logic is independent of external frameworks.

## Dependency Injection

The `Container` class (`src/container.py`) manages all dependencies:

```python
container = Container(settings)
use_case = container.convert_videos_use_case
```

Benefits:

- Easy to swap implementations
- Simplified testing with mocks
- Clear dependency graph

## Configuration Management

Uses `pydantic-settings` for type-safe configuration:

1. Define settings in `Settings` class
2. Load from `.env` file
3. Validate on startup
4. Access via container

## Testing Strategy

### Unit Tests

- Test each layer independently
- Mock dependencies using fixtures
- Focus on business logic

### Integration Tests

- Test interaction between layers
- Use real implementations where possible
- Verify end-to-end workflows

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_entities.py         # Domain tests
├── test_file_repository.py  # Infrastructure tests
├── test_video_service.py    # Application tests
└── test_config.py           # Configuration tests
```

## Design Patterns Used

1. **Repository Pattern**: Abstract file operations
2. **Dependency Injection**: Manage dependencies
3. **Strategy Pattern**: Pluggable converters
4. **Factory Pattern**: Create entities
5. **Protocol Pattern**: Define interfaces

## Benefits of This Architecture

1. **Testability**: Easy to mock and test each component
2. **Maintainability**: Clear separation of concerns
3. **Scalability**: Easy to add new features
4. **Flexibility**: Swap implementations without changing business logic
5. **Independence**: Business logic independent of frameworks

## Future Enhancements

Potential improvements enabled by this architecture:

1. **Multiple Output Formats**: Add WebM, AV1, etc.
2. **Cloud Storage**: Add S3, Azure Blob support
3. **Database Tracking**: Store conversion history
4. **Web Interface**: Add FastAPI frontend
5. **Parallel Processing**: True multiprocessing support
6. **Plugin System**: Allow custom converters
