#!/usr/bin/env python3
"""
Test script to verify the services module import works
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from services.search_engine_service.serper_dev_service import SerperDevService
    print("✅ Successfully imported SerperDevService")
except ImportError as e:
    print(f"❌ Failed to import SerperDevService: {e}")

try:
    from services.stocks_service.finhub_service import FinHubService
    print("✅ Successfully imported FinHubService")
except ImportError as e:
    print(f"❌ Failed to import FinHubService: {e}")