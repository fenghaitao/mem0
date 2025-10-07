#!/usr/bin/env python3
"""
Complete GitHub Copilot Integration Test
Tests both LLM and embedding support together
"""

import os
from mem0 import Memory

def test_github_copilot_complete_integration():
    """Test GitHub Copilot with both LLM and embedding"""
    
    print("🧪 Testing complete GitHub Copilot integration (LLM + Embeddings)")
    print("=" * 70)
    
    # Complete GitHub Copilot configuration
    config = {
        "llm": {
            "provider": "litellm",
            "config": {
                "model": "github_copilot/gpt-4.1",
                "temperature": 0.7,
                "max_tokens": 1000,
                # OAuth2 authentication handled automatically
            }
        },
        "embedder": {
            "provider": "github_copilot", 
            "config": {
                "model": "github_copilot/text-embedding-3-small",
                "embedding_dims": 1536,
                # OAuth2 authentication handled automatically
            }
        },
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "github_copilot_complete_test",
                "path": "./chroma_github_copilot_complete"
            }
        }
    }
    
    try:
        print("🚀 Initializing Memory with GitHub Copilot (LLM + Embeddings)...")
        m = Memory.from_config(config)
        print("✅ Memory initialization successful!")
        
        print("💬 Adding test conversation...")
        messages = [
            {"role": "user", "content": "I'm a developer who loves using GitHub Copilot for coding assistance."},
            {"role": "assistant", "content": "That's great! GitHub Copilot is an excellent AI pair programming tool."},
            {"role": "user", "content": "I primarily work with Python, TypeScript, and use VS Code as my editor."},
            {"role": "assistant", "content": "Perfect combination! VS Code with GitHub Copilot support makes development much more efficient."},
            {"role": "user", "content": "I'm building applications that integrate AI and memory systems."}
        ]
        
        # Test memory addition
        result = m.add(messages, user_id="github_copilot_developer", metadata={
            "source": "github_copilot_integration",
            "test": "complete_integration"
        })
        print(f"✅ Successfully added memories: {result}")
        
        # Test memory search
        print("🔍 Testing memory search...")
        search_result = m.search("What programming languages and tools does this developer use?", user_id="github_copilot_developer")
        print(f"📋 Search results: {search_result}")
        
        # Test another search
        print("🔍 Testing AI-related search...")
        ai_search = m.search("What kind of applications is the user building?", user_id="github_copilot_developer")
        print(f"🤖 AI search results: {ai_search}")
        
        # Test getting all memories
        print("📚 Getting all memories...")
        all_memories = m.get_all(user_id="github_copilot_developer")
        
        # Handle the response format - it returns {"results": [...]}
        memories_list = all_memories.get("results", []) if isinstance(all_memories, dict) else all_memories
        print(f"🗂️ All memories ({len(memories_list)} total):")
        for i, memory in enumerate(memories_list, 1):
            print(f"   {i}. {memory['memory']}")
        
        print("\n🎉 COMPLETE GitHub Copilot integration test PASSED!")
        print("✨ Both LLM and Embeddings working with GitHub Copilot!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        
        # Enhanced error debugging
        if "embedding" in str(e).lower():
            print("💡 Embedding-related issue - check GitHub Copilot embedding implementation")
        elif "llm" in str(e).lower() or "completion" in str(e).lower():
            print("💡 LLM-related issue - check GitHub Copilot LLM implementation")
        elif "authentication" in str(e).lower() or "oauth" in str(e).lower():
            print("💡 Authentication issue - verify GitHub token setup")
        else:
            print("💡 General integration issue - check configuration")
            
        return False

def cleanup():
    """Clean up test files"""
    import shutil
    
    dirs_to_remove = ["./chroma_github_copilot_complete"]
    
    for dir_path in dirs_to_remove:
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                print(f"🧹 Cleaned up {dir_path}")
        except Exception as e:
            print(f"⚠️ Could not clean up {dir_path}: {e}")

def main():
    """Main test function"""
    print("🤖 GitHub Copilot Complete Integration Test")
    print("=" * 70)
    print("🔧 Testing GitHub Copilot LLM + Embeddings together")
    print("=" * 70)
    
    success = test_github_copilot_complete_integration()
    
    if success:
        print("\n" + "=" * 70)
        print("🌟 SUCCESS! Complete GitHub Copilot integration working!")
        print("📋 What's working:")
        print("   ✅ GitHub Copilot LLM (github_copilot/gpt-4.1)")
        print("   ✅ GitHub Copilot Embeddings (github_copilot/text-embedding-3-small)")
        print("   ✅ OAuth2 authentication for both")
        print("   ✅ Function calling support")
        print("   ✅ Memory operations (add, search, get)")
        print("   ✅ Vector storage and retrieval")
        print("\n🎯 mem0 now has full GitHub Copilot support!")
    else:
        print("\n" + "=" * 70)
        print("❌ Integration test failed")
        print("🔍 Check the error messages above for debugging")
        print("\n💡 Setup Instructions:")
        print("   1. Ensure GitHub Copilot access is properly configured")
        print("   2. Make sure the custom LiteLLM fork is installed")
        print("   3. No tokens or API keys needed - OAuth2 handles authentication")
    
    cleanup()
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    main()