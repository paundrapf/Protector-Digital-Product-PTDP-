#!/bin/bash
# Cross-platform build script for PTDP executables

echo "╔════════════════════════════════════════════════╗"
echo "║  PTDP Multi-Platform Build Script            ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Detect platform
PLATFORM=$(uname -s)

echo "🔍 Detected platform: $PLATFORM"
echo ""

if [ "$PLATFORM" == "Linux" ]; then
    echo "🐧 Building for Linux..."
    
    # Build Linux versions
    pyinstaller --clean build_viewer_modern.spec
    pyinstaller --clean build_creator.spec
    
    # Rename with platform suffix
    mv dist/PTDP-Viewer dist/PTDP-Viewer-Linux 2>/dev/null || true
    mv dist/PTDP-Creator dist/PTDP-Creator-Linux 2>/dev/null || true
    
    echo "✅ Linux builds complete!"
    echo "   - PTDP-Viewer-Linux"
    echo "   - PTDP-Creator-Linux"
    
elif [ "$PLATFORM" == "Darwin" ]; then
    echo "🍎 Building for macOS..."
    
    # Build macOS versions
    pyinstaller --clean build_viewer_modern.spec
    pyinstaller --clean build_creator.spec
    
    # Rename with platform suffix
    mv dist/PTDP-Viewer dist/PTDP-Viewer-macOS 2>/dev/null || true
    mv dist/PTDP-Creator dist/PTDP-Creator-macOS 2>/dev/null || true
    
    echo "✅ macOS builds complete!"
    
else
    echo "❌ Unsupported platform: $PLATFORM"
    exit 1
fi

echo ""
echo "📦 Copying to website downloads..."
cp -v dist/PTDP-*-* website/downloads/ 2>/dev/null || true

echo ""
echo "✅ Build complete!"
ls -lh dist/

# Note about Windows builds
echo ""
echo "📝 Note: For Windows .exe builds, use Windows machine or:"
echo "   - Use Wine with PyInstaller"
echo "   - Use GitHub Actions for cross-platform builds"
echo "   - Use Docker with Windows base image"
